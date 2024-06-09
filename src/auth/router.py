from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User, UserRole
from src.auth.auth_backend import (
    auth_backend_bearer_jwt,
    auth_backend_cookie_jwt,
    current_active_user,
    fastapi_users,
)
from src.auth.rbac import rbac
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.auth.service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend_bearer_jwt),
)
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie_jwt), prefix="/cookies"
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
service = UserService


@auth_router.post(
    "/me/avatar",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
@rbac(roles=[UserRole.CUSTOMER, UserRole.OWNER])
def upload_my_avatar(
    image: UploadFile = File(...),
    current_user: User = Depends(current_active_user),
    session: Session = Depends(get_db),
):
    return service(session).upload_avatar(current_user, image)
