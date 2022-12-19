from app.api.models.weed_type import WeedTypeIn, WeedTypeOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/weed_type', response_model=WeedTypeOut, status_code=201)
async def create_weed_type(payload: WeedTypeIn):
    weed_type_id = await db_manager.add_weed_type(payload)
    response = {
        'id': weed_type_id,
        **payload.dict()
    }
    return response


@router.get('/weeds_types', response_model=list[WeedTypeOut])
async def get_weeds_types():
    return await db_manager.get_all_weed_types()
