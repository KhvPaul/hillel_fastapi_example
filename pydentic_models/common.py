from pydantic import BaseModel, EmailStr


class ResponseBaseModel(BaseModel):
    class Config:
        orm_mode = True


class ResponseOk(ResponseBaseModel):
    message: str = "OK"


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpResp(ResponseBaseModel):
    access_token: str
    token_type: str
