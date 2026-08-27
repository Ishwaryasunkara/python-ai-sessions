import logging
from sqlalchemy.orm import Session
from app.database.models import Policy
from app.exceptions.exceptions import (PolicyNotFoundException, PolicyUserNotFoundException,
)
from app.repositories.policy_repository import PolicyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.policy import PolicyCreate, PolicyUpdate


logger = logging.getLogger(__name__)


class PolicyService:
    def __init__(
        self,
        repository: PolicyRepository,
        user_repository: UserRepository,
    ):
        self.repository = repository
        self.user_repository = user_repository

    def create_policy(self, db: Session, data: PolicyCreate):
        #policy owner must already exist.
        user = self.user_repository.get_by_id(db, data.uid)

        if not user:
            raise PolicyUserNotFoundException(data.uid)

        policy = Policy(**data.model_dump())
        created_policy = self.repository.create(db, policy)

        logger.info("Policy created: PID=%s", created_policy.pid)
        return created_policy

    def get_all_policies(self, db: Session):
        return self.repository.get_all(db)

    def get_policy(self, db: Session, pid: int):
        policy = self.repository.get_by_id(db, pid)

        if not policy:
            raise PolicyNotFoundException(pid)

        return policy

    def update_policy(self, db: Session, pid: int, data: PolicyUpdate):
        policy = self.get_policy(db, pid)
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(policy, field, value)

        return self.repository.update(db, policy)

    def delete_policy(self, db: Session, pid: int):
        policy = self.get_policy(db, pid)
        self.repository.delete(db, policy)

        logger.info("Policy deleted: PID=%s", pid)
