from fastapi import Depends
from app.repositories.policy_repository import PolicyRepository
from app.repositories.user_repository import UserRepository
from app.services.policy_service import PolicyService
from app.services.user_service import UserService


def get_user_repository():
    return UserRepository()


def get_policy_repository():
    return PolicyRepository()


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
):
    return UserService(repository)


def get_policy_service(
    repository: PolicyRepository = Depends(get_policy_repository),
    user_repository: UserRepository = Depends(get_user_repository),
):
    return PolicyService(repository, user_repository)
