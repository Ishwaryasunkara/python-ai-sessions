from pydantic import BaseModel

class UserCreate(BaseModel):
    uname : str
    uemail : str

class UserResponse(BaseModel):
    uid : int
    uname : str
    uemail : str

    class Config:
        from_attributes = True