from fastapi import APIRouter, Depends, UploadFile,File,Form
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas.policy import PolicyCreate , PolicyResponse
from src.services.policy_service import upload_policy_service
from src.utils.file_upload import save_policy_pdf
from src.utils.role_checker import require_roles
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os
from src.models.policy import Policy
from src.utils.dependencies import get_current_user
from src.models.policy import Policy

router = APIRouter(prefix="/policy",tags=["Policy"])

@router.post("/upload",response_model=PolicyResponse)
def upload_policy(

    name:str=Form(...),
    year:int=Form(...),
    file:UploadFile=File(...),
    db:Session=Depends(get_db),
    current_user=Depends(require_roles(["hr",'admin']))
):
    pdf_path=save_policy_pdf(file)

    data=PolicyCreate(

        name=name,
        year=year
    )
    return upload_policy_service(data,pdf_path,db)

@router.get('/download/{policy_id}')
def download_policy(
    policy_id:str,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):
    #fetch policy
    policy = db.query(Policy).filter(Policy.id==policy_id).first()

    if not policy:
        raise HTTPException(status_code=404,detail="Policy not found")
    
    #role access

    if current_user.role =="employee":
        if policy.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You not authorized to access this policy"
            )
        
    #check file exists
    if not policy.pdf_url or not os.path.exists(policy.pdf_url):
        raise HTTPException(status_code=404,detail="File not found")
    

    #return the file

    return FileResponse(
        path=policy.pdf_url,
        media_type="application/pdf",
        filename=f"policy{policy.year}.pdf"
    )
    