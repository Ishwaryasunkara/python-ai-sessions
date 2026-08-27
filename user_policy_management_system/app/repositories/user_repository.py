from sqlalchemy.orm import Session

from app.database.models import User


class UserRepository:
    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all(self, db: Session):
        return db.query(User).all()

    def get_by_id(self, db: Session, uid: int):
        return db.query(User).filter(User.uid == uid).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.uemail == email).first()

    def update(self, db: Session, user: User):
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User):
        db.delete(user)
        db.commit()
