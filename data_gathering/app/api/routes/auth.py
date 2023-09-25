from fastapi import APIRouter, status
from app.api.models.customer import CustomerLogin, CustomerToken
from app.auth.auth_handler import signJWT, get_customer
from app.api.models.http_error import HTTPErrorOut
from fastapi.responses import JSONResponse

router = APIRouter(responses={401: {"model": HTTPErrorOut}})

@router.post("/auth/login", response_model=CustomerToken)
async def login(customer: CustomerLogin):
    cutomer_out = await get_customer(customer)
    if cutomer_out is not None:
        return signJWT(cutomer_out)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Wrong login details !"})