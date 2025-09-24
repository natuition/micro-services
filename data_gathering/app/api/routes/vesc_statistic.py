from app.api.database.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.vesc_statistic import VescStatisticIn, VescStatisticOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/vesc_statistic', response_model=VescStatisticOut, status_code=201)
async def create_vesc_statistic(payload: VescStatisticIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT])
    try:
        vesc_statistic_id = await db_manager.add_vesc_statistic(payload)
        response = {
            'id': vesc_statistic_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/vesc_statistics', response_model=list[VescStatisticOut])
async def get_vesc_statistics(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_vesc_statistics()

@router.get('/last_vesc_statistic_of_session', response_model=VescStatisticOut)
async def get_last_vesc_statistic_of_session(session_id: int, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.USER])
    return await db_manager.get_last_vesc_statistic_of_session(session_id)