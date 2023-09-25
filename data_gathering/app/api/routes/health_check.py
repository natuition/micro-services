from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.api.models.http_error import HTTPErrorOut

router = APIRouter(responses={ 500: {"model": HTTPErrorOut}})

@router.get('/health_check')
async def get_health_check_status() -> None:
    return JSONResponse(status_code=status.HTTP_200_OK, content=True)