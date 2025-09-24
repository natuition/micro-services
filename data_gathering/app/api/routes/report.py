from app.api.database.enum.role import Role, has_right_role
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from app.api.models.report import ReportOut
from app.api.database import db_manager
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get('/get_report_data', response_model=ReportOut, status_code=200)
async def get_report_data_of_one_session(session_id: int, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role, role_list=[Role.USER])
    return await db_manager.get_report_data_one_session(session_id)
