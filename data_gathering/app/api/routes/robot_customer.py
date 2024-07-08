from app.api.models.robot_of_customer import RobotOfCustomerIn, RobotOfCustomerOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/add_robot_of_customer', response_model=RobotOfCustomerOut, status_code=201)
async def add_robot_of_customer(payload: RobotOfCustomerIn):
    try:
        robot_of_customer = await db_manager.add_one_robot_of_one_customer(payload)
        response = {
            'id': robot_of_customer,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})

@router.get('/get_all_customer_with_robot', response_model=list[RobotOfCustomerOut])
async def get_all_customer_with_robot():
    return await db_manager.get_all_customer_with_robot()