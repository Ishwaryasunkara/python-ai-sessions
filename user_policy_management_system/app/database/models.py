from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    uname = Column(String(100), nullable=False)
    uemail = Column(String(255), nullable=False, unique=True, index=True)
    uage = Column(Integer, nullable=False)
    uphone = Column(String(15), nullable=False)
    uaddress = Column(String(255), nullable=False)

    # One user can have many policies.
    policies = relationship(
        "Policy",
        back_populates="user",
        cascade="save-update, merge",
    )


class Policy(Base):
    __tablename__ = "policies"

    pid = Column(Integer, primary_key=True, index=True)

    # Added because a policy must belong to a user.
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False, index=True)

    pname = Column(String(100), nullable=False)
    ptype = Column(String(50), nullable=False)
    ppremium = Column(Float, nullable=False)
    psumassured = Column(Float, nullable=False)

    user = relationship("User", back_populates="policies")
