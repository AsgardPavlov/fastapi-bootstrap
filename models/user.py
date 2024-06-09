import enum
import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import UUID_ID
from pydantic import computed_field
from sqlalchemy import UUID, Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserRole(enum.Enum):
    CUSTOMER = "Customer"
    OWNER = "Owner"
    ADMIN = "Admin"


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    id: Mapped[UUID_ID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    role = mapped_column(Enum(UserRole, name="user_role_enum"), nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
