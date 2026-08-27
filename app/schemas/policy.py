from pydantic import BaseModel

class PolicyCreate(BaseModel):
    pname : str
    ptype : str
    uid : int

class PolicyUpdate(BaseModel):
    pid : int
    pname : str
    ptype : str
    status : str

class PolicyResponse(BaseModel):
    pid : int
    pname : str
    ptype : str
    
    class Config:
        from_attributes = True