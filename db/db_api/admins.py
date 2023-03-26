from db.db_api import base as base_db_api
from db.models import models_base as db_models


class AdminsDBAPI(base_db_api.DBApiBase):
    model = db_models.Admin
