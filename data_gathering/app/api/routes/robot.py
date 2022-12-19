from app.api.models.robot import RobotIn, RobotOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/robot', response_model=RobotOut, status_code=201)
async def create_robot(payload: RobotIn):
    robot_id = await db_manager.add_robot(payload)
    response = {
        'id': robot_id,
        **payload.dict()
    }
    return response


@router.get('/robots', response_model=list[RobotOut])
async def get_robot():
    return await db_manager.get_all_robots()
