from typing import Type

from fastapi import File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session, joinedload

from models import User
from src.s3.service import S3Service


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.s3_service = S3Service()

    def retrieve(self, user_id: str) -> Type[User]:
        instance = (
            self.session.query(User)
            .options(
                joinedload(User.organization)
            )  # Organization relation fetch
            .filter(User.id == user_id)
            .first()
        )
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден.",
            )
        return instance

    def upload_avatar(self, current_user: User, image: UploadFile = File(...)):
        instance = self.retrieve(current_user.id)

        if instance:
            image_url = self.s3_service.upload_user_avatar(
                instance.id, file=image
            )
            instance.avatar = image_url
            self.session.commit()
            self.session.refresh(instance)

        return instance
