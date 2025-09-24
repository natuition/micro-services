from app.api.database.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.field import FieldIn, FieldOut, FieldWithGPSPoints
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/field', response_model=FieldOut, status_code=201, responses={200: {"model": FieldOut}})
async def create_field(payload: FieldIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT])
    try:
        field_id = await db_manager.add_field(payload)
        response = {
            'id': field_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        if "UC_Fields" in error.args[1]:
            response = await db_manager.get_field(payload)
            field_out = {
                "id": response[0],
                "label": response[1],
                "robot_serial_number": response[2]
            }
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=field_out)
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/fields', response_model=list[FieldOut])
async def get_fields(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_fields()

@router.get('/field_of_session', response_model=FieldWithGPSPoints)
async def get_field_of_session(session_id: int, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.USER])
    return await db_manager.get_field_of_session(session_id)