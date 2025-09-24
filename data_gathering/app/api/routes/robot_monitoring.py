from app.api.models.robot_monitoring import RobotMonitoringIn, RobotMonitoringInDB, RobotMonitoringOutDB
from datetime import datetime
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from app.api.database.role import has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql
import pytz
from typing import Union

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/robot_monitoring', response_model=RobotMonitoringOutDB, status_code=201)
async def create_robot_monitoring(payload: RobotMonitoringIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    heartbeat_timestamp = datetime.now(pytz.timezone('Europe/Berlin'))
    try:
        args = payload.dict()
        args["heartbeat_timestamp"] = heartbeat_timestamp
        robot_monitoring_in_db = RobotMonitoringInDB(**args)
        robot_monitoring_out_DB_id = await db_manager.add_robot_monitoring(robot_monitoring_in_db)
        return{
            'id': robot_monitoring_out_DB_id,
            **robot_monitoring_in_db.dict()
        }
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/last_robot_monitoring', response_model=Union[RobotMonitoringOutDB, None])
async def get_last_robot_monitoring(serial_number: str, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_robot_monitoring(serial_number)
