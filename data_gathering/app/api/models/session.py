from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SessionIn(BaseModel):
    start_time: datetime
    end_time: datetime
    robot_serial_number: str = Field(example="SNXXX")
    field_id: int = Field(example=1)
    previous_sessions_id: int = Field(None, example=1)


class SessionOut(SessionIn):
    id: int


class SessionUpdate(SessionIn):
    __annotations__ = {k: Optional[v]
                       for k, v in SessionIn.__annotations__.items()}
