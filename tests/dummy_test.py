import pytest


async def some_async_func(a: int, b: int):
    return a + b


@pytest.mark.asyncio
async def test_some_asyncio_code():
    res = await some_async_func(3, 7)
    assert 10 == res
