from app.api.models.vesc_statistic import VescStatisticIn, VescStatisticOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/vesc_statistic', response_model=VescStatisticOut, status_code=201)
async def create_vesc_statistic(payload: VescStatisticIn):
    vesc_statistic_id = await db_manager.add_vesc_statistic(payload)
    response = {
        'id': vesc_statistic_id,
        **payload.dict()
    }
    return response


@router.get('/vesc_statistics', response_model=list[VescStatisticOut])
async def get_vesc_statistics():
    return await db_manager.get_all_vesc_statistics()
