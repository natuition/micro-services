from app.api.models.session import SessionIn, SessionOut, SessionUpdate
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/session', response_model=SessionOut, status_code=201)
async def create_session(payload: SessionIn):
    try:
        session_id = await db_manager.add_session(payload)
        response = {
            'id': session_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/sessions', response_model=list[SessionOut])
async def get_sessions():
    return await db_manager.get_all_sessions()


@router.patch('/session/{id}', status_code=200)
async def update_session(id: int, payload: SessionUpdate):
    try:
        await db_manager.update_session(id, payload)
        updated_session = await db_manager.get_session(id)
        updated_session_out = {
            "id": updated_session[0],
            "start_time": updated_session[1],
            "end_time": updated_session[2],
            "robot_serial_number": updated_session[3],
            "field_id": updated_session[4],
            "previous_sessions_id": updated_session[5],
        }
        return updated_session_out
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})
