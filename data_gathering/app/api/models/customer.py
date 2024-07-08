from app.api.database.enum.role import Role
from pydantic import BaseModel, Field

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