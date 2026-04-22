from sqlalchemy.orm import Session
from src.models.payslip import Payslip
from src.schemas.payslip import PayslipCreate
from src.ai.indexing import index_payslip
from src.models.payslip import Payslip
from src.ai.vector_store import payslip_qdrant_store
from src.utils.cache import invalidate_user_cache
from fastapi import HTTPException
from qdrant_client.models import Filter, FieldCondition, MatchValue
from src.core.redis_client import redis_client

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
    keys = redis_client.keys("paysip:*")
    if keys:
        redis_client.delete(*keys)
    return payslip


def delete_payslip_service(payslip_id: str, current_user, db: Session):
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()

    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")

    # role check idhr
    if current_user.role == "employee":
        if payslip.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to delete this payslip"
            )

    vector_store =payslip_qdrant_store()

    vector_store.client.delete(
        collection_name="payslip_vectors",
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=payslip.user_id),
                ),
                FieldCondition(
                    key="metadata.month",
                    match=MatchValue(value=payslip.month),
                ),
                FieldCondition(
                    key="metadata.year",
                    match=MatchValue(value=str(payslip.year)),
                ),
            ]
        )
    )

    db.delete(payslip)
    db.commit()

    invalidate_user_cache(payslip.user_id)

    return {"message": "Payslip deleted successfully"}