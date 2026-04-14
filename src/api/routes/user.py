from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.dependencies import get_current_user
from src.models.user import User
from src.models.payslip import Payslip
from src.database.db import get_db

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payslips = db.query(Payslip).filter(
        Payslip.user_id == current_user.id
    ).all()

    payslip_data = [
        {
            "id": p.id,
            "month": p.month,
            "year": p.year,
            "net_salary": p.net_salary,
            "download_url": f"/payslip/download/{p.id}"
        }
        for p in payslips
    ]

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "payslips": payslip_data
    }