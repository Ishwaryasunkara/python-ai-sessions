from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.dependencies import get_policy_service
from app.exceptions.exceptions import (
    PolicyNotFoundException,
    PolicyUserNotFoundException,
)
from app.schemas.policy import PolicyCreate, PolicyResponse, PolicyUpdate
from app.services.policy_service import PolicyService


router = APIRouter(prefix="/policies", tags=["Policies"])


@router.post("/", response_model=PolicyResponse, status_code=201)
def create_policy(
    data: PolicyCreate,
    db: Session = Depends(get_db),
    service: PolicyService = Depends(get_policy_service),
):
    try:
        return service.create_policy(db, data)
    except PolicyUserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.get("/", response_model=list[PolicyResponse])
def get_all_policies(
    db: Session = Depends(get_db),
    service: PolicyService = Depends(get_policy_service),
):
    return service.get_all_policies(db)


@router.get("/{pid}", response_model=PolicyResponse)
def get_policy(
    pid: int,
    db: Session = Depends(get_db),
    service: PolicyService = Depends(get_policy_service),
):
    try:
        return service.get_policy(db, pid)
    except PolicyNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.put("/{pid}", response_model=PolicyResponse)
def update_policy(
    pid: int,
    data: PolicyUpdate,
    db: Session = Depends(get_db),
    service: PolicyService = Depends(get_policy_service),
):
    try:
        return service.update_policy(db, pid, data)
    except PolicyNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/{pid}", status_code=204)
def delete_policy(
    pid: int,
    db: Session = Depends(get_db),
    service: PolicyService = Depends(get_policy_service),
):
    try:
        service.delete_policy(db, pid)
    except PolicyNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)
