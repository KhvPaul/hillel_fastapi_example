from pydantic import BaseModel


class ResponseBaseModel(BaseModel):
    class Config:
        orm_mode = True


class ResponseOk(ResponseBaseModel):
    message: str = "OK"
