from app.api.database import db_manager
from fastapi import APIRouter, status

router = APIRouter()


@router.delete('/clean_database', status_code=200)
async def deletion_of_all_data_from_the_database():
    await db_manager.deletion_of_all_data_from_the_database()
    return
