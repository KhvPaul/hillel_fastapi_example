import datetime

from pydantic import BaseModel, EmailStr, Field, constr, root_validator

from pydentic_models import common, enums, validators


class UserBase(BaseModel):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    birthday: datetime.date
    gender: enums.Genders
    phone_number: str = Field(..., min_length=10, max_length=10, description="User's phone number")

    _valid_birthday = root_validator(pre=False, skip_on_failure=True, allow_reuse=True)(validators.birthday_validator)
    _valid_phone_number = root_validator(pre=False, skip_on_failure=True, allow_reuse=True)(validators.phone_validator)


class UserSignUpRequest(common.SignUpRequest, UserBase):
    class Config:
        schema_extra = {
            "example": {
                "email": "email@noreply.com",
                "password": "QWE!@#qwe123",
                "first_name": "Guido",
                "last_name": "van Rossum",
                "birthday": datetime.date.today(),
                "gender": enums.Genders.Male,
                "phone_number": "0677511111",
            }
        }


class UserResponse(UserBase, common.ResponseBaseModel):
    email: EmailStr
