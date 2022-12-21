from app.api.models.field import FieldIn, FieldOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/field', response_model=FieldOut, status_code=201)
async def create_field(payload: FieldIn):
    try:
        field_id = await db_manager.add_field(payload)
        response = {
            'id': field_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        if "fields.UC_Fields" in error.args[1]:
            return await db_manager.get_field(payload)
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"message": error.args[1]})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/fields', response_model=list[FieldOut])
async def get_fields():
    return await db_manager.get_all_fields()
