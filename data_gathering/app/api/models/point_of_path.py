from pydantic import BaseModel, Field


class PointOfPathIn(BaseModel):
    point_number: int = Field(example=1)
    session_id: int = Field(example=1)
    gps_point_id: int = Field(example=1)


class PointOfPathOut(PointOfPathIn):
    id: int
