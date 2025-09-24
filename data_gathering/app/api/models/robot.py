from pydantic import BaseModel, Field
from app.api.models.robot_of_customer import RobotOfCustomerOut

class RobotIn(BaseModel):
    serial_number: str = Field(example="SNXXX")


class RobotOut(RobotIn):
    pass