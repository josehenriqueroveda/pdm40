from pydantic import BaseModel


class PDMRequest(BaseModel):
    description: str
