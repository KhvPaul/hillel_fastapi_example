from db.db_api import users as users_db_api
from managers.base_manager import BaseModelManager


class SellerModelManager(BaseModelManager):
    _db_api = users_db_api.SellerDBAPI()
