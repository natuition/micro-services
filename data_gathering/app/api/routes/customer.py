from app.api.database.enum.role import Role
from app.api.models.customer import CustomerIn, CustomerOut, CustomerWithoutHash, CustomerCreation
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/create_customer', response_model=CustomerWithoutHash, status_code=201)
async def create_customer(payload: CustomerCreation):
    try:
        final_customer: CustomerIn = {
            "name" : playload.name,
            "email" : playload.email,
            "phone" : playload.phone,
            "role" : playload.role,
            "hash_pwd": "",
            "hash_rt" : ""
        }
        customer_id = await db_manager.add_customer(final_customer)
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