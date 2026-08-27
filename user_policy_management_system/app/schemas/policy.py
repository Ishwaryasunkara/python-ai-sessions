from pydantic import BaseModel, ConfigDict, Field


class PolicyCreate(BaseModel):
    # A policy cannot exist without an owner.
    uid: int = Field(..., gt=0)
    pname: str = Field(..., min_length=2, max_length=100)
    ptype: str = Field(..., min_length=2, max_length=50)
    ppremium: float = Field(..., gt=0)
    psumassured: float = Field(..., gt=0)


class PolicyUpdate(BaseModel):
    pname: str | None = Field(None, min_length=2, max_length=100)
    ptype: str | None = Field(None, min_length=2, max_length=50)
    ppremium: float | None = Field(None, gt=0)
    psumassured: float | None = Field(None, gt=0)


class PolicyResponse(BaseModel):
    pid: int
    uid: int
    pname: str
    ptype: str
    ppremium: float
    psumassured: float

    model_config = ConfigDict(from_attributes=True)
