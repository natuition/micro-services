from app.api.models.session import SessionIn, SessionOut
from app.api.database import db_manager
from fastapi import APIRouter

router = APIRouter()


@router.post('/session', response_model=SessionOut, status_code=201)
async def create_session(payload: SessionIn):
    session_id = await db_manager.add_session(payload)
    response = {
        'id': session_id,
        **payload.dict()
    }
    return response


@router.get('/sessions', response_model=list[SessionOut])
async def get_sessions():
    return await db_manager.get_all_sessions()
