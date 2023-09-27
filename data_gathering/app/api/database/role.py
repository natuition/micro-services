from enum import Enum
from fastapi import HTTPException

class Role(str, Enum):
    ADMIN = "admin"
    DISTRIBUTOR = "distributor"
    USER = "user"
    ROBOT = "robot"

def has_right_role(role: Role, role_list: list[Role] = []):
    if Role.ADMIN not in role_list:
        role_list.append(Role.ADMIN)
    if not role in role_list:
        raise HTTPException(status_code=403, detail=f"Invalid role to make this action, you need one of this role : '{role_list}', but you have : '{repr(role)}'.")
    return True