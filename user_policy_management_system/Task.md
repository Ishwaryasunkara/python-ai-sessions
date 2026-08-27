# Design a FastAPI app to manage users and policy

## Entity: User

- UID PK
- UNAME
- UEMAIL
- UAGE
- UPHONE
- UADDRESS

## Entity: Policy

- PID
- UID (foreign key to User)
- PNAME
- PTYPE
- PPREMIUM
- PSUMASSURED

## Functional Requirements

- Create User
- Read all Users
- Read one User
- Update User
- Delete User
- Create Policy
- Read all Policy
- Read one Policy
- Update Policy
- Delete Policy
- Authentication & Authorization (Not Mandatory)

## Non Functional Requirements

- Dependency Injection
- Structured Folders
- Logging Enabled
- Pytest - Unit Testing
- Validation - Pydantic

## Business Rules

1. One user can have multiple policies.
2. A policy must belong to an existing user.
3. A user cannot be deleted if they have policies.
4. User email must be unique.
5. Premium and sum assured must be greater than zero.
6. User age is validated between 18 and 100 for this assignment.
