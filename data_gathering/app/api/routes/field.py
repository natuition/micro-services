from app.api.models.field import FieldIn, FieldOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/field', response_model=FieldOut, status_code=201)
async def create_field(payload: FieldIn):
    field_id = await db_manager.add_field(payload)
    response = {
        'id': field_id,
        **payload.dict()
    }
    return response


@router.get('/fields', response_model=list[FieldOut])
async def get_fields():
    return await db_manager.get_all_fields()
