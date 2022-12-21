from app.api.models.extracted_weed import ExtractedWeedIn, ExtractedWeedOut
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/extracted_weed', response_model=ExtractedWeedOut, status_code=201)
async def create_extracted_weed(payload: ExtractedWeedIn):
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
async def get_extracted_weeds():
    return await db_manager.get_all_extracted_weeds()
