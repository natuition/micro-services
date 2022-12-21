from pydantic import BaseModel, Field


class FieldIn(BaseModel):
    label: str = Field(example="Field 1")
    robot_serial_number: str = Field(example="SNXXX")


class FieldOut(FieldIn):
    id: int
