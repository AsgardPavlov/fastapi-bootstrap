import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import (
    BaseUserManager,
    UUIDIDMixin,
    exceptions,
    models,
    schemas,
)

from config import AUTH_SECRET, BASE_CLIENT_URL
from src.auth.schemas import UserCreate, UserRead
from src.sendgrid.service import SendgridService


class UserManager(UUIDIDMixin, BaseUserManager[UserCreate, uuid.UUID]):
    reset_password_token_secret = AUTH_SECRET
    verification_token_secret = AUTH_SECRET

    sendgrid_service = SendgridService()

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(
        self,
        user: UserRead,
        request: Optional[Request] = None,
    ):
        # TODO put your post registration logic here
        return

    async def on_after_forgot_password(
        self,
        user,
        token: str,
        request: Optional[Request] = None,
    ):
        if user and token:
            reset_password_link_url = (
                f"{BASE_CLIENT_URL}/reset-password?token={token}"
            )
            user_full_name = f"{user.first_name} {user.last_name}"

            self.sendgrid_service.send_reset_password_email(
                to_email=user.email,
                url=reset_password_link_url,
                full_name=user_full_name,
            )
