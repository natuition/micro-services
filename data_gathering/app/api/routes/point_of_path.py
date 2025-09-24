from app.api.database.enum.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.point_of_path import PointOfPathIn, PointOfPathOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/point_of_path', response_model=PointOfPathOut, status_code=201)
async def create_point_of_path(payload: PointOfPathIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT])
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
async def get_points_of_paths(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_points_of_paths()

@router.get('/points_of_path_of_session', response_model=list[PointOfPathOut])
async def get_points_of_path_of_session(session_id: int, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.USER])
    return await db_manager.get_all_points_of_path_of_session(session_id)