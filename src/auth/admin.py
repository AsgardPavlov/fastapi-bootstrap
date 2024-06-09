from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from config import AUTH_SECRET
from models import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # user = await fastapi_users.get_user_manager(user)
        if (
            not username == "owl@owltribe.dev"
            or not password == "12OwnerPass34"
        ):
            return False

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


admin_authentication_backend = AdminAuth(secret_key=AUTH_SECRET)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.role,
        User.is_active,
        User.created_at,
    ]
    column_searchable_list = [
        User.first_name,
        User.last_name,
        User.email,
    ]
    column_sortable_list = [
        User.created_at,
    ]
