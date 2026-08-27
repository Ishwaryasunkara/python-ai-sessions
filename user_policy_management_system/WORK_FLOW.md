## 1. What are we building?

We are building a REST API using FastAPI.

There are two main entities:

- User
- Policy

The important relationship is:

```text
One User
   |
   +---- Policy 1
   |
   +---- Policy 2
   |
   +---- Policy 3
```

So this is a **one-to-many relationship**.

One user can own multiple policies.

A policy cannot exist without a user.

according to business rule, a user cannot be deleted while the user has policies.

---

# 2. Folder structure

```text
app/
├── core/
│   ├── config.py
│   └── logging_config.py
│
├── database/
│   ├── database.py
│   └── models.py
│
├── dependencies/
│   └── dependencies.py
│
├── exceptions/
│   └── exceptions.py
│
├── repositories/
│   ├── user_repository.py
│   └── policy_repository.py
│
├── routers/
│   ├── user_router.py
│   └── policy_router.py
│
├── schemas/
│   ├── user.py
│   └── policy.py
│
├── services/
│   ├── user_service.py
│   └── policy_service.py
│
└── main.py

tests/
├── conftest.py
├── test_users.py
└── test_policies.py
```

Each folder has a specific responsibility.

This avoids putting the complete application into one large Python file.

---

# 3. Complete request workflow

Suppose we send:

```http
POST /users/
```

with:

```json
{
  "uname": "Aakash",
  "uemail": "aakash@example.com",
  "uage": 25,
  "uphone": "9876543210",
  "uaddress": "Indore"
}
```

The request follows this path:

```text
Client
  |
  v
FastAPI Router
  |
  v
Pydantic Schema
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
SQLAlchemy
  |
  v
SQLite Database
```

Let's understand each step.

---

# 4. Router layer

Example:

```python
@router.post("/")
def create_user(...):
```

The router receives the HTTP request.

It is responsible mainly for:

- URL
- HTTP method
- request/response handling
- converting application exceptions into HTTP errors

It should not contain all business logic.

---

# 5. Pydantic schema

The request is first validated by Pydantic.

Example:

```python
class UserCreate(BaseModel):
    uname: str
    uemail: EmailStr
    uage: int = Field(..., ge=18, le=100)
```

This means:

- name must be a string
- email must be a valid email
- age must be between 18 and 100

For example:

```json
{
  "uname": "Aakash",
  "uemail": "wrong-email",
  "uage": 15
}
```

will be rejected by FastAPI with HTTP 422.

This is why Pydantic is useful for request validation.

---

# 6. Dependency Injection

FastAPI's `Depends()` is used for dependency injection.

Example:

```python
db: Session = Depends(get_db)
```

FastAPI calls `get_db()` and gives the route a database session.

We also inject services:

```python
service: UserService = Depends(get_user_service)
```

The router does not manually create the service.

This makes the application easier to test and maintain.

---

# 7. Service layer

The service contains business rules.

For example:

```python
if user.policies:
    raise UserHasPoliciesException(uid)
```

This implements the mentor's rule:

> A user cannot be deleted if they have active policies.

Another example:

```python
if not user:
    raise PolicyUserNotFoundException(data.uid)
```

This means we cannot create a policy for a user who does not exist.

The service layer is therefore where the important application/business decisions happen.

---

# 8. Repository layer

The repository talks to the database.

For example:

```python
def get_by_id(self, db, uid):
    return db.query(User).filter(User.uid == uid).first()
```

The service does not need to know the SQLAlchemy query details.

It simply calls:

```python
repository.get_by_id(...)
```

This separation is useful because database-related code stays in one place.

---

# 9. Database models

`models.py` contains SQLAlchemy models.

User:

```text
users
----------------
uid       PK
uname
uemail
uage
uphone
uaddress
```

Policy:

```text
policies
----------------
pid        PK
uid        FK
pname
ptype
ppremium
psumassured
```

The important relationship is:

```text
users.uid
    |
    | 1
    |
    | many
    v
policies.uid
```

This means one user can have many policies.

---

# 10. Why UID is added to Policy

The original task lists:

```text
Policy
PID
PNAME
PTYPE
PPREMIUM
PSUMASSURED
```

But the mentor gave the additional rule:

> One user can have multiple policies.

To represent this relationship in a relational database, Policy needs to know which User owns it.

Therefore:

```text
Policy.uid -> User.uid
```

is added as a foreign key.

This is an important design decision you can explain to the mentor.

---

# 11. Delete User business rule

Suppose:

```text
User 1
 |
 +--- Policy 101
 +--- Policy 102
```

If someone sends:

```http
DELETE /users/1
```

the service checks:

```python
if user.policies:
    raise UserHasPoliciesException(uid)
```

The API returns:

```text
409 Conflict
```

The user is not deleted.

First the policies need to be deleted according to the application's policy lifecycle.

Then the user can be deleted.

---

# 12. Policy creation workflow

Suppose:

```http
POST /policies/
```

contains:

```json
{
  "uid": 1,
  "pname": "Health Secure",
  "ptype": "Health",
  "ppremium": 15000,
  "psumassured": 500000
}
```

The service first checks:

```python
user = user_repository.get_by_id(db, data.uid)
```

If the user does not exist:

```text
404 Not Found
```

Otherwise the policy is created.

This prevents an orphan policy.

---

# 13. Logging

Logging is configured in:

```text
app/core/logging_config.py
```

Logs are written to:

```text
logs/app.log
```

and also displayed in the terminal.

For example:

```text
2026-08-26 21:00:00 | INFO | ... | User created: UID=1
```

Logging helps us understand what the application is doing without using `print()` everywhere.

---

# 14. Exception handling

Custom exceptions are defined in:

```text
app/exceptions/exceptions.py
```

Examples:

```text
UserNotFoundException
UserAlreadyExistsException
UserHasPoliciesException
PolicyNotFoundException
PolicyUserNotFoundException
```

The service raises meaningful application exceptions.

The router converts them to HTTP responses.

Example:

```text
UserNotFoundException
        |
        v
HTTPException
        |
        v
404 Not Found
```

This keeps business logic cleaner.

---

# 15. Pytest

Tests are located in:

```text
tests/
```

Run:

```text
pytest -v
```

The tests cover:

- User create
- User read
- User update
- User delete
- Duplicate email
- Pydantic validation
- User deletion business rule
- Policy create
- Policy read
- Policy update
- Policy delete
- Invalid policy data
- Policy with non-existing user

The tests use a separate in-memory SQLite database so the real development database is not damaged.

---

# 16. API endpoints

## Users

```text
POST   /users/
GET    /users/
GET    /users/{uid}
PUT    /users/{uid}
DELETE /users/{uid}
```

## Policies

```text
POST   /policies/
GET    /policies/
GET    /policies/{pid}
PUT    /policies/{pid}
DELETE /policies/{pid}
```

## Health

```text
GET /health
```

---

# 17. Swagger

After starting the application:

```text
uvicorn app.main:app --reload
```

open:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates Swagger documentation.

You can test every API from the browser.

---

# 18. Example testing sequence

A good way to demonstrate the project is:

### Step 1 - Create User

```http
POST /users/
```

Create:

```text
Aakash
aakash@example.com
25
9876543210
Indore
```

Suppose UID is:

```text
1
```

### Step 2 - Create Policy

Use:

```http
POST /policies/
```

with:

```json
{
  "uid": 1,
  "pname": "Health Secure",
  "ptype": "Health",
  "ppremium": 15000,
  "psumassured": 500000
}
```

### Step 3 - Create another Policy

Use the same:

```text
uid = 1
```

Now:

```text
User 1
 |
 +--- Policy 1
 |
 +--- Policy 2
```

This proves one user can have multiple policies.

### Step 4 - Try deleting User

```http
DELETE /users/1
```

The API returns:

```text
409 Conflict
```

because the user still has policies.

### Step 5 - Delete policies

Delete both policies.

### Step 6 - Delete user

Now:

```http
DELETE /users/1
```

returns:

```text
204 No Content
```

This demonstrates the business rule.

---

# 19. What to explain if mentor asks "Why this architecture?"

A simple answer:

> "I separated the application into router, service, repository and database layers. The router handles HTTP requests, Pydantic handles validation, the service contains business rules, and the repository handles database operations. I used FastAPI dependency injection to provide the database and services. This keeps the code easier to test and maintain."

---

# 20. What to explain about Pydantic

A simple answer:

> "I used Pydantic models for request and response validation. For example, EmailStr validates email format and Field lets me define constraints such as minimum and maximum age. FastAPI automatically returns a 422 validation response when invalid data is received."

---

# 21. What to explain about Dependency Injection

A simple answer:

> "FastAPI provides dependencies through Depends. Instead of creating the database session or service manually inside every endpoint, FastAPI injects them into the endpoint. It also makes testing easier because dependencies can be overridden in pytest."

---

# 22. Why authentication is not implemented

The task says:

```text
Authentication & Authorization (Not Mandatory)
```

Therefore this project intentionally does not add JWT authentication.

If asked:

> "I considered authentication and authorization, but since they were explicitly marked as not mandatory, I focused on completing all mandatory functional and non-functional requirements first."

---

# 23. Final architecture

```text
                    CLIENT
                      |
                      v
               FASTAPI ROUTER
                      |
                      v
              PYDANTIC SCHEMA
                      |
                      v
               SERVICE LAYER
              /             \
             /               \
            v                 v
      BUSINESS RULES     REPOSITORY
                              |
                              v
                         SQLALCHEMY
                              |
                              v
                           SQLITE
```

Cross-cutting support:

```text
Dependency Injection -> FastAPI Depends
Logging              -> logging module
Validation            -> Pydantic
Testing               -> Pytest
Configuration         -> .env + Settings
Exceptions            -> custom exceptions
```

This is the main workflow you should understand before presenting the project.
