from pydantic import BaseModel
from typing import Optional

class PolicyCreate(BaseModel):
  
    name:str
    year:int


class PolicyResponse(BaseModel):
    id:str

    name:str
    year:int
    pdf_url:Optional[str]

    class Config:
        from_attributes=True

