from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Policy(Base):
    __tablename__ = "policies"

    pid = Column(Integer, primary_key=True, index=True)

    uid = Column(
        Integer,
        ForeignKey("users.uid"),
        nullable=False
    )

    pname = Column(String, nullable=False)
    ptype = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")

    user = relationship(
        "User",
        back_populates="policies"
    )
