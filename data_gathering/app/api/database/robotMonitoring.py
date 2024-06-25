from enum import Enum


class RobotMonitoring(str, Enum):
    BLOCKING_PAGE_1_TO_2 = "BLOCKING_PAGE_1_TO_2"
    BLOCKING_DURING_OPERATION = "BLOCKING_DURING_OPERATION"
