import copy
import typing as t

from asyncpg import exceptions as ae
from sqlalchemy import delete, desc, exc as sa_exc, future, orm, text, update
from sqlalchemy.ext import asyncio as sa_asyncio

from logger import logger
from utils import exceptions as custom_exc


class BaseDbApiHandler:
    @classmethod
    async def handle_exception(cls, exc):
        exc_name = "Unhandled Exception"
        raised_error = custom_exc.SomethingWentWrongException
        if type(exc) == sa_exc.IntegrityError:
            exc_name = "IntegrityError"
            raised_error = custom_exc.ObjectAlreadyExistsException
        if type(exc) == sa_exc.DBAPIError:
            if hasattr(exc, "orig") and hasattr(exc.orig, "sqlstate"):
                if exc.orig.sqlstate == ae.CharacterNotInRepertoireError.sqlstate:
                    exc_name = "CharacterNotInRepertoireError"
                else:
                    exc_name = exc.orig.args[0]
        logger.error(f"{exc_name}: {repr(exc)}")
        raise raised_error()

    @classmethod
    async def _execute(cls, session: sa_asyncio.AsyncSession, stmt, kwargs=None):
        kwargs = {} if not kwargs else kwargs
        try:
            res = await session.execute(stmt, kwargs)
        except Exception as exc:
            await session.rollback()
            await cls.handle_exception(exc)
        else:
            return res

    @classmethod
    async def execute(cls, session: sa_asyncio.AsyncSession, stmt, kwargs=None):
        await cls._execute(session, stmt, kwargs)

    @classmethod
    async def _commit(cls, session: sa_asyncio.AsyncSession):
        try:
            await session.commit()
        except Exception as exc:
            await session.rollback()
            await cls.handle_exception(exc)

    @classmethod
    async def commit(cls, session: sa_asyncio.AsyncSession):
        await cls._commit(session)

    @classmethod
    async def ping(cls, session_cls: sa_asyncio.AsyncSession):
        async with session_cls() as session:
            await cls._execute(session, text("SELECT 1"))


class DBApiBase(BaseDbApiHandler):
    model = None
    pk_filed = ""

    @classmethod
    async def retrieve(
        cls, session_cls: sa_asyncio.AsyncSession, condition: list, all_: bool = False, order_by=None
    ) -> t.Union[model, list[model]]:
        async with session_cls() as session:
            stmt = future.select(cls.model).where(*condition)
            if order_by:
                stmt = stmt.order_by(order_by)
            res = await cls._execute(session, stmt)
            return res.scalars().all() if all_ else res.scalar()

    @classmethod
    async def retrieve_with_related_models(
        cls,
        session_cls: sa_asyncio.AsyncSession,
        condition: list,
        selectinload: t.Iterable,
        all_: bool = False,
        order_by=None,
        order_desc: bool = False,
        limit: int = 0,
    ) -> t.Union[model, list[model]]:
        async with session_cls() as session:
            stmt = future.select(cls.model).options(*[orm.subqueryload(el) for el in selectinload]).filter(*condition)
            if order_by:
                stmt = stmt.order_by(order_by) if not order_desc else stmt.order_by(desc(order_by))
            if limit:
                stmt.limit(limit)
            res = await cls._execute(session, stmt)
            return res.scalars().all() if all_ or limit else res.scalar()

    @classmethod
    async def create(
        cls,
        session_cls: sa_asyncio.AsyncSession,
        data: dict,
        return_: bool = False,
    ) -> t.Optional[model]:
        async with session_cls() as session:
            res = None
            obj = cls.model(**data)
            session.add(obj)
            if return_:
                try:
                    await session.flush()
                except Exception as exc:
                    await cls.handle_exception(exc)
                res = copy.deepcopy(obj)
            await cls._commit(session)
            return res

    @classmethod
    async def update(cls, session_cls: sa_asyncio.AsyncSession, data: dict, condition: list):
        async with session_cls() as session:
            stmt = update(cls.model).where(*condition).values(data)
            await cls._execute(session, stmt)
            await cls._commit(session)

    @classmethod
    async def delete(
        cls, session_cls: sa_asyncio.AsyncSession, condition: list, return_: bool = False
    ) -> t.Optional[list[dict]]:
        async with session_cls() as session:
            stmt = delete(cls.model).where(*condition)
            if return_:
                stmt = stmt.returning(cls.model)
            res = await cls._execute(session, stmt)
            result = [dict(el) for el in list(res.mappings())] if return_ else None
            await session.commit()
            return result
