from sqlalchemy.orm import Session
from src.models.policy import Policy
from src.schemas.policy import PolicyCreate
from src.ai.indexing import index_policy

def upload_policy_service(data:PolicyCreate,pdf_path:str,db:Session):
    policy=Policy(
        name=data.name,
        year=data.year,
        pdf_url=pdf_path
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)

    metadata={
        "type":'policy',
        "name":data.name,
        "year":str(data.year)
    }

    index_policy(pdf_path,metadata)

    return policy