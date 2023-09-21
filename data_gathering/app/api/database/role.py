from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    DISTRIBUTOR = "distributor"
    USER = "user"
    ROBOT = "robot"
    EKYLIBRE = "ekylibre"