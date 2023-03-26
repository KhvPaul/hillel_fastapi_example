import datetime

from pydantic import BaseModel, EmailStr, Field, constr, root_validator

from pydentic_models import common, enums, validators


class UserProfileBase(BaseModel):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    birthday: datetime.date
    gender: enums.Genders
    phone_number: str = Field(..., min_length=10, max_length=10, description="User's phone number")

    _valid_birthday = root_validator(pre=False, skip_on_failure=True, allow_reuse=True)(validators.birthday_validator)
    _valid_phone_number = root_validator(pre=False, skip_on_failure=True, allow_reuse=True)(validators.phone_validator)


class UserProfileRequest(UserProfileBase):
    pass


class UserProfileResponse(UserProfileBase, common.ResponseBaseModel):
    email: EmailStr
