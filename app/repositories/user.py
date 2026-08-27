from sqlalchemy.orm import Session

from app.models.user import User
from app.models.policy import Policy
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(
        User.uemail == user.uemail
    ).first()

    if existing_user:
        return None

    new_user = User(
        uname=user.uname,
        uemail=user.uemail,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_users(db: Session):

    return db.query(User).all()


def get_user(db: Session, uid: int):

    return db.query(User).filter(
        User.uid == uid
    ).first()


def update_user(db: Session, uid: int, user_data: UserCreate):

    user = get_user(db, uid)

    if user is None:
        return None

    user.uname = user_data.uname
    user.uemail = user_data.uemail

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, uid: int):

    user = get_user(db, uid)

    if user is None:
        return "NOT_FOUND"

    active_policy = db.query(Policy).filter(
        Policy.uid == uid,
        Policy.status == "ACTIVE"
    ).first()

    if active_policy:
        return "HAS_ACTIVE_POLICY"

    db.delete(user)
    db.commit()

    return "DELETED"