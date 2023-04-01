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


class InvalidUserCredentialsException(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Invalid user credentials",
        )


class ErrorTokenValidation(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            detail="Error token validation",
        )


class ErrorCredentialsValidation(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Could not validate credentials",
        )


class BirthDateInFutureException(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Birth date can't be in future",
        )


class AccessDenied(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="You don't have permission to access callable information",
        )
