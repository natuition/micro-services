from app.api.database.enum.role import Role
from pydantic import BaseModel, Field
from typing import Optional

class CustomerWithoutHash(BaseModel):
    name: str = Field(example="Natuition")
    email: str = Field(example="v.lambert@natuition.com")
    phone: str = Field(example="+330102030405")
    role: Role = Role.USER

class CustomerCreation(BaseModel):
    name: str = Field(example="Natuition")
    email: str = Field(example="v.lambert@natuition.com")
    phone: str = Field(example="+330102030405")
    password: str = Field(example= ".bq_4E2W")

class CustomerIn(CustomerWithoutHash):
    hash_pwd: str = Field()
    hash_rt: str = Field(None)

class CustomerOut(CustomerIn):
    id: int

class CustomerCreationUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Natuition", )
    email: Optional[str] = Field(None, example="v.lambert@natuition.com")
    phone: Optional[str] = Field(None, example="+330102030405")
    password: Optional[str] = Field(None, example= ".bq_4E2W")

class CustomerWithoutHashUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Natuition")
    email: Optional[str] = Field(None, example="v.lambert@natuition.com")
    phone: Optional[str] = Field(None, example="+330102030405")
    role: Optional[Role] = Field(None, example=Role.USER)

class CustomerUpdate(CustomerWithoutHashUpdate):
    hash_pwd: Optional[str] = Field(None)
    hash_rt: Optional[str] = Field(None)
    
class CustomerLogin(BaseModel):
    email: str = Field(example="v.lambert@natuition.com")
    hash_pwd: str

class CustomerToken(BaseModel):
    access_token: str
    token_type: str = "bearer"