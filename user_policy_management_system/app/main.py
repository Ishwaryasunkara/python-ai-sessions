from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.database.database import Base, engine
from app.database import models
from app.routers.policy_router import router as policy_router
from app.routers.user_router import router as user_router


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Simple User and Policy Management API",
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(policy_router)


@app.get("/")
def home():
    return {"message": "User Policy Management API is running"}


@app.get("/health")
def health_check():
    return {"status": "Ok 200"}
