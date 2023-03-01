from app.api.models.robot import RobotIn, RobotOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/robot', response_model=RobotOut, status_code=201)
async def create_robot(payload: RobotIn):
    try:
        robot_id = await db_manager.add_robot(payload)
        response = {
            'id': robot_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/robots', response_model=list[RobotOut])
async def get_robot():
    return await db_manager.get_all_robots()
