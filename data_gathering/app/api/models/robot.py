from pydantic import BaseModel, Field


class RobotIn(BaseModel):
    serial_number: str = Field(example="SNXXX")


class RobotOut(RobotIn):
    pass
