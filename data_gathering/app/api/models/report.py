from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.api.models.session import SessionOut
from app.api.models.field import FieldOut
from app.api.models.extracted_weed import ExtractedWeedOut
from app.api.models.gps_point import GPSPointOut
from app.api.models.field_corner import FieldCornerOut
from app.api.models.point_of_path import PointOfPathOut

class ReportOut(BaseModel):
    session: SessionOut
    field: FieldOut
    fields_corners: list[GPSPointOut]
    extracted_weeds: list[ExtractedWeedOut]
    points_of_paths: list[GPSPointOut]