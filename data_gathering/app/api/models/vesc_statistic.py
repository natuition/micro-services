from pydantic import BaseModel, Field
from datetime import datetime


class VescStatisticIn(BaseModel):
    session_id: int = Field(example=1)
    voltage: float = Field(example=12.5)
    timestamp: datetime


class VescStatisticOut(VescStatisticIn):
    id: int
