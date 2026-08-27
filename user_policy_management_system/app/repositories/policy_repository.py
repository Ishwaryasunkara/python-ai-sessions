from sqlalchemy.orm import Session

from app.database.models import Policy


class PolicyRepository:
    def create(self, db: Session, policy: Policy):
        db.add(policy)
        db.commit()
        db.refresh(policy)
        return policy

    def get_all(self, db: Session):
        return db.query(Policy).all()

    def get_by_id(self, db: Session, pid: int):
        return db.query(Policy).filter(Policy.pid == pid).first()

    def update(self, db: Session, policy: Policy):
        db.commit()
        db.refresh(policy)
        return policy

    def delete(self, db: Session, policy: Policy):
        db.delete(policy)
        db.commit()
