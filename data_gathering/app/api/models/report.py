from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.api.models.session import SessionOut
from app.api.models.field import FieldOut
from app.api.models.extracted_weed import ExtractedWeedOut
from app.api.models.gps_point import GPSPointOut
from app.api.models.weed_type import WeedTypeOut
from app.api.models.field_corner import FieldCornerOut
from app.api.models.point_of_path import PointOfPathOut

class ExtractedWeedWithGPSPointWithWeedTypeOut(BaseModel):
    latitude: float = Field(example=46.157638375739220000)
    longitude: float = Field(example=-1.135048542875101200)
    number: int = Field(1, example=1)
    label: str = Field(example="Daisy")

class ReportOut(BaseModel):
    session: SessionOut
    field: FieldOut
    fields_corners: list[GPSPointOut]
    extracted_weed_with_GPS_point_with_weed_type: list[ExtractedWeedWithGPSPointWithWeedTypeOut]
    points_of_paths: list[GPSPointOut]