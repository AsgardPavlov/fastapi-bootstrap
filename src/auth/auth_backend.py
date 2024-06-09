import uuid
from typing import Literal

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from config import AUTH_SECRET, ENVIRONMENT
from models import User
from src.auth.utils import get_user_manager

cookie_samesite: Literal["lax", "none"] = (
    "none" if ENVIRONMENT == "production" else "lax"
)

cookie_transport = CookieTransport(
    cookie_max_age=60 * 60 * 60 * 24,
    cookie_name="asgardfastapiboostrap",
    cookie_samesite=cookie_samesite,
    cookie_secure=True,
)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    # lifetime_seconds is 12 hours
    return JWTStrategy(secret=AUTH_SECRET, lifetime_seconds=60 * 60 * 12)


auth_backend_bearer_jwt = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
auth_backend_cookie_jwt = AuthenticationBackend(
    name="jwt-cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend_bearer_jwt, auth_backend_cookie_jwt],
)
current_active_user = fastapi_users.current_user(active=True)
optional_current_active_user = fastapi_users.current_user(
    active=True,
    optional=True,
)
