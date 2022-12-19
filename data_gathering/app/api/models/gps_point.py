from pydantic import BaseModel, Field


class GPSPointIn(BaseModel):
    quality: int = Field(example=4)
    latitude: float = Field(example=46.157638375739220000)
    longitude: float = Field(example=-1.135048542875101200)


class GPSPointOut(GPSPointIn):
    id: int
