import datetime

from utils import exceptions as custom_exc


def birthday_validator(cls, values):  # noqa
    if values["birthday"] > datetime.date.today():
        raise custom_exc.BirthDateInFutureException()
    return values


def phone_validator(cls, values):  # noqa !must be cls not self
    if not values["phone_number"].isdigit() or len(values["phone_number"]) != 10:
        raise ValueError("phone_number must include 10 digits")
    return values
