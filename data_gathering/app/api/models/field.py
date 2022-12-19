from pydantic import BaseModel, Field


class FieldIn(BaseModel):
    label: str = Field(example="Field 1")


class FieldOut(FieldIn):
    id: int
