from pydantic import BaseModel, Field


class ExtractedWeedIn(BaseModel):
    point_of_path_id: int = Field(example=1)
    weed_type_id: int = Field(example=1)
    session_id: int = Field(example=1)
    number: int = Field(1, example=1)


class ExtractedWeedOut(ExtractedWeedIn):
    id: int
