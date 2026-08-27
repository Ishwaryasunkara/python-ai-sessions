from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.repositories import user as user_repository


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    result = user_repository.create_user(db, user)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return result


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
):

    return user_repository.get_users(db)


@router.get("/{uid}", response_model=UserResponse)
def get_user(
    uid: int,
    db: Session = Depends(get_db)
):

    user = user_repository.get_user(db, uid)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{uid}", response_model=UserResponse)
def update_user(
    uid: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):

    result = user_repository.update_user(
        db,
        uid,
        user
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result


@router.delete("/{uid}")
def delete_user(
    uid: int,
    db: Session = Depends(get_db)
):

    result = user_repository.delete_user(db, uid)

    if result == "NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if result == "HAS_ACTIVE_POLICY":
        raise HTTPException(
            status_code=400,
            detail="User cannot be deleted because active policies exist"
        )

    return {"message": "User deleted successfully"}