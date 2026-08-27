from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.models.user import User
from app.schemas.policy import PolicyCreate, PolicyUpdate


def create_policy(db: Session, policy_data: PolicyCreate):

    user = db.query(User).filter(
        User.uid == policy_data.uid
    ).first()

    if user is None:
        return None

    policy = Policy(
        pname=policy_data.pname,
        ptype=policy_data.ptype,
        uid=policy_data.uid
    )

    db.add(policy)
    db.commit()
    db.refresh(policy)

    return policy


def get_policies(db: Session):

    return db.query(Policy).all()


def get_policy(db: Session, pid: int):

    return db.query(Policy).filter(
        Policy.pid == pid
    ).first()


def update_policy(
    db: Session,
    pid: int,
    policy_data: PolicyUpdate
):

    policy = get_policy(db, pid)

    if policy is None:
        return None

    policy.pname = policy_data.pname
    policy.ptype = policy_data.ptype
    policy.status = policy_data.status

    db.commit()
    db.refresh(policy)

    return policy


def delete_policy(db: Session, pid: int):

    policy = get_policy(db, pid)

    if policy is None:
        return False

    db.delete(policy)
    db.commit()

    return True