from app.api.models.point_of_path import PointOfPathIn, PointOfPathOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/point_of_path', response_model=PointOfPathOut, status_code=201)
async def create_point_of_path(payload: PointOfPathIn):
    try:
        point_of_path_id = await db_manager.add_point_of_path(payload)
        response = {
            'id': point_of_path_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/points_of_paths', response_model=list[PointOfPathOut])
async def get_points_of_paths():
    return await db_manager.get_all_points_of_paths()

@router.get('/points_of_path_of_session', response_model=list[PointOfPathOut])
async def get_points_of_path_of_session(session_id: int):
    return await db_manager.get_all_points_of_path_of_session(session_id)
