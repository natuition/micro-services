import time
from app.api.models.customer import CustomerOut
from app.api.database.enum.role import Role

class Token:

    SECONDS_BEFORE_TOKEN_EXPIRATION = 60 * 60 * 24

    def __init__(self, payload = None) -> None:
        if payload is not None:
            self.customer_id: str = payload["customer_id"]
            self.customer_role: Role = Role[payload["customer_role"].upper()]
            self.expires = payload["expires"]

    def generate(self, customer: CustomerOut):
        self.customer_id : str = customer.id,
        self.customer_role : Role = customer.role
        self.expires : str = time.time() + self.SECONDS_BEFORE_TOKEN_EXPIRATION
        return self

    def get_str(self) -> str:
        return {
            "customer_id": self.customer_id,
            "customer_role": self.customer_role,
            "expires": self.expires
        }
    
