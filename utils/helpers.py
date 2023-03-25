from config import settings


def get_description_file() -> str:
    with open(settings.DESCRIPTION_FILE, "r") as description_file:
        return description_file.read()
