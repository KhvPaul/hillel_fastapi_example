import http

from fastapi.exceptions import HTTPException


class ObjectAlreadyExistsException(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Object Already Exists",
        )


class SomethingWentWrongException(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Something went wrong",
        )
