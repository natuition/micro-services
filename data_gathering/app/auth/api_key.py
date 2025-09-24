from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from decouple import config
import json

api_key_header = APIKeyHeader(name="X-API-Key")

API_KEYS = json.loads(config("api_keys", default=""))

def verify_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if not API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="No API Key on server",
        )
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )