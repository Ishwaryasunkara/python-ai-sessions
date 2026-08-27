from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    uname = Column(String, nullable=False)
    uemail = Column(String, unique=True, nullable=False)

    policies = relationship(
        "Policy",
        back_populates="user"
    )