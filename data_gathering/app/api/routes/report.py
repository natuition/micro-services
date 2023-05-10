from app.api.models.report import ReportOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.get('/get_report_data', response_model=ReportOut, status_code=200)
async def get_report_data_of_one_session(session_id: int):
    return await db_manager.get_report_data_one_session(session_id)
