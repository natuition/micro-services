from pydantic import BaseModel, Field

class RobotOfCustomer(BaseModel):
    robot_serial_number: str = Field(example="SNXXX")

class RobotOfCustomerInForm(RobotOfCustomer):
    customer_email: str = Field(example="v.lambert@natuition.com")

class RobotOfCustomerIn(RobotOfCustomer):
    customer_id: int 

class RobotOfCustomerOut(RobotOfCustomerIn):
    id: int