from pydantic import BaseModel, Field


class WeedTypeIn(BaseModel):
    label: str = Field(example="Daisy")


class WeedTypeOut(WeedTypeIn):
    id: int
