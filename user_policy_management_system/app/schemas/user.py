from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    uname: str = Field(..., min_length=2, max_length=100)
    uemail: EmailStr
    uage: int = Field(..., ge=18, le=100)
    uphone: str = Field(..., min_length=10, max_length=15)
    uaddress: str = Field(..., min_length=3, max_length=255)


class UserUpdate(BaseModel):
    uname: str | None = Field(None, min_length=2, max_length=100)
    uemail: EmailStr | None = None
    uage: int | None = Field(None, ge=18, le=100)
    uphone: str | None = Field(None, min_length=10, max_length=15)
    uaddress: str | None = Field(None, min_length=3, max_length=255)


class UserResponse(BaseModel):
    uid: int
    uname: str
    uemail: EmailStr
    uage: int
    uphone: str
    uaddress: str

    model_config = ConfigDict(from_attributes=True)
