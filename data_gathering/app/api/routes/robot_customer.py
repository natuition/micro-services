from app.api.models.robot_of_customer import RobotOfCustomerOut, RobotOfCustomerInForm
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from app.api.database.enum.role import has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/add_robot_of_customer', response_model=RobotOfCustomerOut, status_code=201)
async def add_robot_of_customer(payload: RobotOfCustomerInForm, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    try:
        return await db_manager.add_one_robot_of_one_customer(payload)
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})

@router.get('/get_all_customer_with_robot', response_model=list[RobotOfCustomerOut])
async def get_all_customer_with_robot(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_customer_with_robot()