from app.api.models.point_of_path import PointOfPathIn, PointOfPathOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/point_of_path', response_model=PointOfPathOut, status_code=201)
async def create_point_of_path(payload: PointOfPathIn):
    point_of_path_id = await db_manager.add_point_of_path(payload)
    response = {
        'id': point_of_path_id,
        **payload.dict()
    }
    return response


@router.get('/points_of_paths', response_model=list[PointOfPathOut])
async def get_points_of_paths():
    return await db_manager.get_all_points_of_paths()
