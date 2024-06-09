import uuid
from typing import Optional

from fastapi_users import schemas
from fastapi_users.models import ID
from pydantic import EmailStr, constr

from models.user import UserRole


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: ID
    avatar: Optional[str] = None
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    full_name: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
