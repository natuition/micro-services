from pydantic import BaseModel, Field


class FieldCornerIn(BaseModel):
    field_id: int = Field(example=1)
    gps_point_id: int = Field(example=1)


class FieldCornerOut(FieldCornerIn):
    id: int
