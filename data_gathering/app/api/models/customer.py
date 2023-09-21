from app.api.database.role import Role
from pydantic import BaseModel, Field

class CustomerWithoutHash(BaseModel):
    name: str = Field(example="Natuition")
    email: str = Field(example="v.lambert@natuition.com")
    phone: str = Field(example="+330102030405")
    role: Role = Role.USER

class CustomerIn(CustomerWithoutHash):
    hash_pwd: str = Field()
    hash_rt: str = Field(None)

class CustomerOut(CustomerIn):
    id: int

class CustomerLogin(BaseModel):
    email: str = Field(example="v.lambert@natuition.com")
    hash_pwd: str

class CustomerToken(BaseModel):
    access_token: str