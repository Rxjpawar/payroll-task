from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas.payslip import PayslipResponse, PayslipCreate
from src.services.payslip_service import upload_payslip_service
from src.utils.file_upload import save_pdf
from src.utils.role_checker import require_roles
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os
from src.models.payslip import Payslip
from src.utils.dependencies import get_current_user
from src.models.payslip import Payslip
router = APIRouter(prefix="/payslip", tags=["Payslip"])


@router.post("/upload", response_model=PayslipResponse)
def upload_payslip(
    user_id: str = Form(...),
    month: str = Form(...),
    year: int = Form(...),
    gross_salary: int = Form(...),
    deduction: int = Form(...),
    net_salary: int = Form(...),
    bonuses: int = Form(0),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["hr", "admin"]))
):
    pdf_path = save_pdf(file)

    data = PayslipCreate(
        user_id=user_id,
        month=month,
        year=year,
        gross_salary=gross_salary,
        deduction=deduction,
        net_salary=net_salary,
        bonuses=bonuses
    )

    return upload_payslip_service(data, pdf_path, db)


@router.get("/download/{payslip_id}")
def download_payslip(
    payslip_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # fetch payslip
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()

    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")

    #RBAC
    if current_user.role == "employee":
        if payslip.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this payslip"
            )

    # check file exists
    if not payslip.pdf_url or not os.path.exists(payslip.pdf_url):
        raise HTTPException(status_code=404, detail="File not found")

    # rreturn file
    return FileResponse(
        path=payslip.pdf_url,
        media_type="application/pdf",
        filename=f"payslip_{payslip.month}_{payslip.year}.pdf"
    )