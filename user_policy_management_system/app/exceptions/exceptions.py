class UserNotFoundException(Exception):
    def __init__(self, uid: int):
        self.message = f"User with UID {uid} not found"
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.message = f"User with email {email} already exists"
        super().__init__(self.message)


class UserHasPoliciesException(Exception):
    def __init__(self, uid: int):
        self.message = (
            f"User {uid} cannot be deleted because they have active policies"
        )
        super().__init__(self.message)


class PolicyNotFoundException(Exception):
    def __init__(self, pid: int):
        self.message = f"Policy with PID {pid} not found"
        super().__init__(self.message)


class PolicyUserNotFoundException(Exception):
    def __init__(self, uid: int):
        self.message = f"Cannot create policy because user {uid} does not exist"
        super().__init__(self.message)
