from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.delete('/delete_all_data', status_code=202)
async def delete_all_data():
    await db_manager.execute_query("SET foreign_key_checks = 0")
    truncates = await db_manager.get_all_truncate()
    for truncate in truncates:
        await db_manager.execute_query(truncate[0])
    await db_manager.execute_query("SET foreign_key_checks = 1")
