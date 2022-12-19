from app.api.models.field_corner import FieldCornerIn, FieldCornerOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/field_corner', response_model=FieldCornerOut, status_code=201)
async def create_field_corner(payload: FieldCornerIn):
    field_corner_id = await db_manager.add_field_corner(payload)
    response = {
        'id': field_corner_id,
        **payload.dict()
    }
    return response


@router.get('/fields_corners', response_model=list[FieldCornerOut])
async def get_fields_corners():
    return await db_manager.get_all_fields_corners()
