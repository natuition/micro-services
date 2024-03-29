from app.api.models.gps_point import GPSPointIn, GPSPointOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/gps_point', response_model=GPSPointOut, status_code=201)
async def create_gps_point(payload: GPSPointIn):
    try:
        gps_point_id = await db_manager.add_gps_point(payload)
        response = {
            'id': gps_point_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/gps_points', response_model=list[GPSPointOut])
async def get_gps_points():
    return await db_manager.get_all_gps_points()
