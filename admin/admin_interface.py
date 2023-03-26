from fastapi import FastAPI
from sqladmin import Admin

from admin.auth import AdminAuth
from admin.views import export_views
from db.session import create_async_engine
from config import settings


class AdminApplicationBuilder:
    def __init__(self, app: FastAPI):
        self.admin_app = Admin(app, create_async_engine())

    def __call__(self, *args, **kwargs):
        # add authentication_backend
        self.admin_app.authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)

        # add admin views
        for view in export_views:
            self.admin_app.add_view(view)

        return self.admin_app.app
