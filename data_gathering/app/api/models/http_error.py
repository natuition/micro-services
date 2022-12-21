from pydantic import BaseModel, Field


class HTTPErrorOut(BaseModel):
    message: str = Field(example="Error message.")
