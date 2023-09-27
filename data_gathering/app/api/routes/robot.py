from app.api.database.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.robot import RobotIn, RobotOut
from app.api.models.robot_of_customer import RobotOfCustomer
from app.api.models.customer import CustomerOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/robot', response_model=RobotOut, status_code=201)
async def create_robot(payload: RobotIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT])
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
async def get_robot(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_robots()

@router.get('/robots_of_connected_customer', response_model=list[RobotOfCustomer])
async def get_robot_of_connected_customer(token: str = Depends(JWTBearer())):
    customer: CustomerOut = await db_manager.get_customer(Token(token).customer_id)
    return await db_manager.get_all_robots_of_customer(customer)
