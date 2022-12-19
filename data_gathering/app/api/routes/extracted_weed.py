from app.api.models.extracted_weed import ExtractedWeedIn, ExtractedWeedOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/extracted_weed', response_model=ExtractedWeedOut, status_code=201)
async def create_extracted_weed(payload: ExtractedWeedIn):
    extracted_weed_id = await db_manager.add_extracted_weed(payload)
    response = {
        'id': extracted_weed_id,
        **payload.dict()
    }
    return response


@router.get('/extracted_weeds', response_model=list[ExtractedWeedOut])
async def get_extracted_weeds():
    return await db_manager.get_all_extracted_weeds()
