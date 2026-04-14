from sqlalchemy.orm import Session
from src.models.payslip import Payslip
from src.schemas.payslip import PayslipCreate
from src.ai.indexing import index_payslip
def upload_payslip_service(data:PayslipCreate,pdf_path:str,db:Session):
    payslip = Payslip(
        user_id=data.user_id,
        month=data.month,
        year=data.year,
        gross_salary=data.gross_salary,
        deduction=data.deduction,
        net_salary=data.net_salary,
        bonuses=data.bonuses,
        pdf_url=pdf_path)
    
    db.add(payslip)
    db.commit()
    db.refresh(payslip)

    metadata = {
        "user_id": data.user_id,
        "type": "payslip",
        "month": data.month,
        "year": str(data.year)
    }

    index_payslip(pdf_path, metadata)

    return payslip