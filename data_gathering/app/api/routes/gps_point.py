from app.api.models.gps_point import GPSPointIn, GPSPointOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/gps_point', response_model=GPSPointOut, status_code=201)
async def create_gps_point(payload: GPSPointIn):
    gps_point_id = await db_manager.add_gps_point(payload)
    response = {
        'id': gps_point_id,
        **payload.dict()
    }
    return response


@router.get('/gps_points', response_model=list[GPSPointOut])
async def get_gps_points():
    return await db_manager.get_all_gps_points()
