from app.api.models.robot_status import RobotStatusIn, RobotStatusInDB, RobotStatusOutDB
from datetime import datetime
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql
import pytz
from typing import Union

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/robot_status', response_model=list[RobotStatusOutDB], status_code=201)
async def create_robot_status(payload: list[RobotStatusIn]):
    heartbeat_timestamp = datetime.now(pytz.timezone('Europe/Berlin'))
    robots_status_out_DB = list()
    try:
        for robot_status_in in payload:
            args = robot_status_in.dict()
            args["heartbeat_timestamp"] = heartbeat_timestamp
            robot_status_in_db = RobotStatusInDB(**args)
            robot_status_out_DB_id = await db_manager.add_robot_synthesis(robot_status_in_db)
            robots_status_out_DB.append({
                'id': robot_status_out_DB_id,
                **robot_status_in_db.dict()
            })
        return robots_status_out_DB
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/last_robots_status', response_model=Union[RobotStatusOutDB, None])
async def get_last_robots_status(serial_number: str):
    return await db_manager.get_robot_synthesis(serial_number)
