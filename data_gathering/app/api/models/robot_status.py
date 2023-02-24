from app.api.database.robotSynthesis import RobotSynthesis
from pydantic import BaseModel, Field
from datetime import datetime


class RobotStatusIn(BaseModel):
    robot_synthesis: RobotSynthesis = RobotSynthesis.OP
    robot_serial_number: str = Field(example="SNXXX")


class RobotStatusInDB(RobotStatusIn):
    heartbeat_timestamp: datetime


class RobotStatusOutDB(RobotStatusInDB):
    id: int
