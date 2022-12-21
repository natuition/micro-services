from app.api.models.field_corner import FieldCornerIn, FieldCornerOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/field_corner', response_model=FieldCornerOut, status_code=201)
async def create_field_corner(payload: FieldCornerIn):
    try:
        field_corner_id = await db_manager.add_field_corner(payload)
        response = {
            'id': field_corner_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/fields_corners', response_model=list[FieldCornerOut])
async def get_fields_corners():
    return await db_manager.get_all_fields_corners()
