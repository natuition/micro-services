from pydantic import BaseModel, Field
from app.api.models.gps_point import GPSPointOut
from app.api.models.session import SessionOut

class FieldIn(BaseModel):
    label: str = Field(example="Field 1")
    robot_serial_number: str = Field(example="SNXXX")


class FieldOut(FieldIn):
    id: int

class FieldWithGPSPoints(BaseModel):
    field: FieldOut
    fields_corners: list[GPSPointOut]
    session: SessionOut