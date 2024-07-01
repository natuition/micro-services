from app.api.models.robot_subscriber import RobotSubscriberIn, RobotSubscriberOut
from app.api.models.robot import RobotOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/add_subscriber_of_robot', response_model=RobotSubscriberOut, status_code=201)
async def add_subscriber_of_robot(payload: RobotSubscriberIn):
    print(payload)
    try:
        subscriber_id = await db_manager.add_subscriber_of_robot(payload)
        response = {
            'id': subscriber_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/get_all_subscriber_with_robot', response_model=list[RobotSubscriberOut])
async def get_all_subscriber_with_robot():
    return await db_manager.get_all_subscriber_with_robot()

@router.get('/get_all_robot_of_one_subscriber', response_model=list[RobotOut])
async def get_all_robot_of_one_subscriber(subscriber_username: str):
    return await db_manager.get_all_robot_of_one_subscriber(subscriber_username)

@router.delete('/remove_one_robot_of_one_subscriber', status_code=200)
async def remove_one_robot_of_one_subscriber(subscriber_username: str, robot_serial_number: str):
    return await db_manager.remove_one_robot_of_one_subscriber(subscriber_username, robot_serial_number)
