from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.dependencies import get_user_service
from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserHasPoliciesException,
    UserNotFoundException,
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    try:
        return service.create_user(db, data)
    except UserAlreadyExistsException as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.get_all_users(db)


@router.get("/{uid}", response_model=UserResponse)
def get_user(
    uid: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    try:
        return service.get_user(db, uid)
    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.put("/{uid}", response_model=UserResponse)
def update_user(
    uid: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    try:
        return service.update_user(db, uid, data)
    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)
    except UserAlreadyExistsException as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@router.delete("/{uid}", status_code=204)
def delete_user(
    uid: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    try:
        service.delete_user(db, uid)
    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)
    except UserHasPoliciesException as exc:
        raise HTTPException(status_code=409, detail=exc.message)
