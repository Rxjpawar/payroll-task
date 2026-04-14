from pydantic import BaseModel
from typing import Optional

class PayslipCreate(BaseModel):
    user_id:str
    month:str
    year:int
    gross_salary:int
    deduction:int
    net_salary:int
    bonuses:Optional[int]=0

class PayslipResponse(BaseModel):
    id:str
    user_id:str
    month:str
    year:int
    gross_salary:int
    deduction:int
    net_salary:int
    bonuses:Optional[int]
    pdf_url:Optional[str]

    class Config:
        from_attributes=True
