# User Policy Management API

A small FastAPI project for the User + Policy rule.

## Quick start

### Windows

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Run tests:

```text
pytest -v
```

## Design

```text
Request
  |
  v
Router
  |
  v
Service
  |
  v
Repository
  |
  v
SQLAlchemy
  |
  v
SQLite
```

Pydantic validates request data before it reaches the service layer.

Authentication and authorization are intentionally not implemented because the task says they are not mandatory.
