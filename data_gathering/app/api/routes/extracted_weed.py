from app.api.database.enum.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.extracted_weed import ExtractedWeedIn, ExtractedWeedOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/extracted_weed', response_model=ExtractedWeedOut, status_code=201)
async def create_extracted_weed(payload: ExtractedWeedIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT])
    try:
        extracted_weed_id = await db_manager.add_extracted_weed(payload)
        response = {
            'id': extracted_weed_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/extracted_weeds', response_model=list[ExtractedWeedOut])
async def get_extracted_weeds(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_extracted_weeds()

@router.get('/number_of_extraction_of_last_session_of_robot', response_model=int)
async def get_number_of_extraction_of_last_session_of_robot(robot_serial_number: str, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.USER])
    res = await db_manager.get_number_of_extraction_of_last_session_of_robot(robot_serial_number)
    if res:
        return int(res[1])
    return 0

@router.get('/extracted_weeds_of_session', response_model=list[ExtractedWeedOut])
async def get_extracted_weeds_of_session(session_id: int, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.USER])
    return await db_manager.get_all_extracted_weeds_of_session(session_id)