from app.api.database.enum.role import Role
from pydantic import BaseModel, Field
from datetime import datetime


class RobotSubscriberIn(BaseModel):
    role: Role = Role.USER
    robot_serial_number: str = Field(example="SNXXX")
    subscriber_username: str = Field(example="VLnatuition")


class RobotSubscriberOut(RobotSubscriberIn):
    id: int
