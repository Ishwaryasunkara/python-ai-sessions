from fastapi import FastAPI

from app.database import Base, engine

from app.models.user import User
from app.models.policy import Policy

from app.routers.user import router as user_router
from app.routers.policy import router as policy_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="User and Policy Management API"
)


app.include_router(user_router)
app.include_router(policy_router)


@app.get("/")
def home():
    return {
        "message": "User and Policy Management API"
    }
