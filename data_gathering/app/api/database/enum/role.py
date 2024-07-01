from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    DISTRIBUTOR = "DISTRIBUTOR"
    USER = "USER"
