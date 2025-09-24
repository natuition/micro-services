from app.api.database.enum.role import Role, has_right_role
from app.api.models.customer import CustomerIn, CustomerOut, CustomerWithoutHash, CustomerCreation, CustomerCreationUpdate, CustomerUpdate, CustomerWithoutHashUpdate
from app.api.database import db_manager
from app.api.models.http_error import HTTPErrorOut
from app.auth.auth_bearer import JWTBearer
from app.auth.token import Token
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import pymysql
import bcrypt

router = APIRouter(
    responses={400: {"model": HTTPErrorOut}, 500: {"model": HTTPErrorOut}})


@router.post('/create_customer', response_model=CustomerWithoutHash, status_code=201)
async def create_customer(payload: CustomerCreation, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    try:
        hashed_pwd = bcrypt.hashpw(str.encode(payload.password), bcrypt.gensalt(rounds=10))
        final_customer: CustomerIn = CustomerIn(name=payload.name, email=payload.email, phone=payload.phone, role=Role.USER, hash_pwd=hashed_pwd.decode())
        customer_id = await db_manager.add_customer(final_customer)
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

@router.post('/update_customer_by_email', response_model=CustomerWithoutHashUpdate, status_code=201)
async def update_customer_by_email(payload: CustomerCreationUpdate, email: str, token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    try:
        if payload.password is not None:
            hashed_pwd = bcrypt.hashpw(str.encode(payload.password), bcrypt.gensalt(rounds=10))
            hashed_pwd = hashed_pwd.decode()
        else:
            hashed_pwd = None
        final_customer: CustomerUpdate = CustomerUpdate(name=payload.name, email=payload.email, phone=payload.phone, role=Role.USER, hash_pwd=hashed_pwd)
        customer_id = await db_manager.update_customer(final_customer, email)
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
async def get_customers(token: str = Depends(JWTBearer())):
    has_right_role(Token(token).customer_role)
    return await db_manager.get_all_customers()


@router.get("/customer/get_info", response_model=CustomerWithoutHash)
async def customer_get_info(token: str = Depends(JWTBearer())):
    customer: CustomerWithoutHash = await db_manager.get_customer(Token(token).customer_id)
    return customer