from sqladmin import ModelView

from db.models.models_base import User, UserProfile


class UserAdmin(ModelView, model=User):
    column_list = [User.sub, User.email]


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name, UserProfile.birthday, UserProfile.phone_number]


export_views = (UserAdmin, UserProfileAdmin)
