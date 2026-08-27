import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.auth import get_current_user, get_supabase_client
from app.main import app


class FakeUser:
    id = "test-user"


class FakeAuth:
    def get_user(self, token):
        if token == "invalid-token":
            raise ValueError("invalid token")

        return type("UserResponse", (), {"user": FakeUser()})()


class FakeSupabase:
    auth = FakeAuth()


@pytest.fixture
def client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        "app.auth.get_supabase_client",
        lambda: FakeSupabase(),
    )

    with TestClient(
        app,
        headers={"Authorization": "Bearer test-token"},
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()