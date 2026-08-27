import logging

from sqlalchemy.orm import Session

from app.database.models import User
from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserHasPoliciesException,
    UserNotFoundException,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, db: Session, data: UserCreate):
        existing_user = self.repository.get_by_email(db, data.uemail)

        if existing_user:
            raise UserAlreadyExistsException(data.uemail)

        user = User(**data.model_dump())
        created_user = self.repository.create(db, user)

        logger.info("User created: UID=%s", created_user.uid)
        return created_user

    def get_all_users(self, db: Session):
        return self.repository.get_all(db)

    def get_user(self, db: Session, uid: int):
        user = self.repository.get_by_id(db, uid)

        if not user:
            raise UserNotFoundException(uid)

        return user

    def update_user(self, db: Session, uid: int, data: UserUpdate):
        user = self.get_user(db, uid)
        update_data = data.model_dump(exclude_unset=True)

        if "uemail" in update_data:
            existing_user = self.repository.get_by_email(
                db, update_data["uemail"]
            )

            if existing_user and existing_user.uid != uid:
                raise UserAlreadyExistsException(update_data["uemail"])

        for field, value in update_data.items():
            setattr(user, field, value)

        return self.repository.update(db, user)

    def delete_user(self, db: Session, uid: int):
        user = self.get_user(db, uid)

        #a user with policies cannot be deleted.
        if user.policies:
            raise UserHasPoliciesException(uid)

        self.repository.delete(db, user)
        logger.info("User deleted: UID=%s", uid)
