import time
from typing import Dict
from app.api.models.customer import CustomerLogin, CustomerOut
from app.api.database import db_manager
from app.auth.token import Token
import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(customer: CustomerOut) -> Dict[str, str]:
    payload = Token().generate(customer).get_str()
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
async def get_customer(data: CustomerLogin) -> CustomerOut:
    customers = await db_manager.get_all_customers()
    for customer in customers:
        if customer.email == data.email and customer.hash_pwd == data.hash_pwd:
            return customer
    return None