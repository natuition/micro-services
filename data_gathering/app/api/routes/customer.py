from app.api.models.customer import CustomerIn, CustomerOut, CustomerWithoutHash
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/customer', response_model=CustomerOut, status_code=201)
async def create_customer(payload: CustomerIn):
    try:
        customer_id = await db_manager.add_customer(payload)
        customer_id = 0
        response = {
            'id': customer_id,
            **payload.dict()
        }
        return response
    except pymysql.err.IntegrityError as error:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": error.args[1]})
    except Exception as error:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": error})


@router.get('/customers', response_model=list[CustomerOut])
async def get_customers():
    return await db_manager.get_all_customers()


@router.get("/customer/get_info", response_model=CustomerWithoutHash)
async def customer_get_info(token: str = Depends(JWTBearer())):
    customer: CustomerWithoutHash = await db_manager.get_customer(Token(token).customer_id)
    return customer