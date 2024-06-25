from app.api.database.robotMonitoring import RobotMonitoring
from pydantic import BaseModel, Field
from datetime import datetime


class RobotMonitoringIn(BaseModel):
    robot_monitoring: RobotMonitoring = RobotMonitoring.BLOCKING_PAGE_1_TO_2
    robot_serial_number: str = Field(example="SNXXX")


class RobotMonitoringInDB(RobotMonitoringIn):
    heartbeat_timestamp: datetime


class RobotMonitoringOutDB(RobotMonitoringInDB):
    id: int
