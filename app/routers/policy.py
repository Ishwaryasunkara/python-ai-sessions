from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse
)
from app.repositories import policy as policy_repository


router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)


@router.post("/", response_model=PolicyResponse)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db)
):

    result = policy_repository.create_policy(
        db,
        policy
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result


@router.get("/", response_model=list[PolicyResponse])
def get_all_policies(
    db: Session = Depends(get_db)
):

    return policy_repository.get_policies(db)


@router.get("/{pid}", response_model=PolicyResponse)
def get_policy(
    pid: int,
    db: Session = Depends(get_db)
):

    policy = policy_repository.get_policy(db, pid)

    if policy is None:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    return policy


@router.put("/{pid}", response_model=PolicyResponse)
def update_policy(
    pid: int,
    policy: PolicyUpdate,
    db: Session = Depends(get_db)
):

    result = policy_repository.update_policy(
        db,
        pid,
        policy
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    return result


@router.delete("/{pid}")
def delete_policy(
    pid: int,
    db: Session = Depends(get_db)
):

    result = policy_repository.delete_policy(
        db,
        pid
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    return {"message": "Policy deleted successfully"}
