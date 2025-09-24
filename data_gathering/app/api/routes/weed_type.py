from app.api.database.enum.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.weed_type import WeedTypeIn, WeedTypeOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/weed_type', response_model=WeedTypeOut, status_code=201)
async def create_weed_type(payload: WeedTypeIn, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT])
    try:
        weed_type_id = await db_manager.add_weed_type(payload)
        response = {
            'id': weed_type_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        if "UC_Weed_types" in error.args[1]:
            response = await db_manager.get_weed_type(payload)
            weed_type_out = {
                "id": response[0],
                "label": response[1]
            }
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=weed_type_out)
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/weeds_types', response_model=list[WeedTypeOut])
async def get_weeds_types(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.ROBOT, Role.USER])
    return await db_manager.get_all_weed_types()
