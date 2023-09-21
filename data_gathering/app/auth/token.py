import time
from app.api.models.customer import CustomerOut

class Token:
    def __init__(self, payload = None) -> None:
        if payload is not None:
            self.customer_id = payload["customer_id"]
            self.customer_role = payload["customer_role"]
            self.expires = payload["expires"]

    def generate(self, customer: CustomerOut):
        self.customer_id : str = customer.id,
        self.customer_role : str = customer.role
        self.expires : str = time.time() + 6000
        return self

    def get_str(self) -> str:
        return {
            "customer_id": self.customer_id,
            "customer_role": self.customer_role,
            "expires": self.expires
        }
    
