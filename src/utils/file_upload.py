import os
from fastapi import UploadFile ,HTTPException,status
from uuid import uuid4

UPLOAD_DIR = "src/uploads/payslips"
UPLOAD_DIR2 = "src/uploads/policies"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_pdf(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    if file_ext =="pdf":
        file_name = f"{uuid4()}.{file_ext}"

        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return file_path
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only pdfs are accepted")
    


os.makedirs(UPLOAD_DIR2, exist_ok=True)

def save_policy_pdf(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    if file_ext =="pdf":
        file_name = f"{uuid4()}.{file_ext}"

        file_path = os.path.join(UPLOAD_DIR2, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return file_path
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only pdfs are accepted")