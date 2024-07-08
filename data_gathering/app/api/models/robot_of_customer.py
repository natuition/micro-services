from pydantic import BaseModel, Field

class RobotOfCustomer(BaseModel):
    robot_serial_number: str = Field(example="SNXXX")

class RobotOfCustomerIn(RobotOfCustomer):
    customer_id: int 

class RobotOfCustomerOut(RobotOfCustomerIn):
    id: int