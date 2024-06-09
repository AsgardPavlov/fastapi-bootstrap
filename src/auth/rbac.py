from functools import wraps
from typing import Optional

from fastapi import HTTPException, status

from models import User, UserRole


def rbac(
    roles: list[UserRole], error_message: Optional[str] = "Access denied"
):
    def decorator_permission(func):
        @wraps(func)
        def wrapper_permission(*args, **kwargs):
            user: User = kwargs.get("current_user")
            if not user or user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=error_message,
                )

            return func(*args, **kwargs)

        return wrapper_permission

    return decorator_permission
