from sqlalchemy.orm import Session
from src.models.policy import Policy
from src.schemas.policy import PolicyCreate
from src.ai.indexing import index_policy
from src.core.redis_client import redis_client
from fastapi import HTTPException
from src.ai.vector_store import policy_qdrant_store
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
    keys = redis_client.keys("policy:*")
    if keys:
        redis_client.delete(*keys)

    return policy

# def delete_policy_service(policy_id,current_user,db:Session):
#     policy  = db.query(Policy).filter(Policy.id==policy_id).first()

#     if not policy:
#         raise HTTPException(status_code=404,detail='Policy not found')

#     if current_user.role =="employee":
#         raise HTTPException(
#             status_code = 403,
#             detail="Not authorized to delete this"
#         )
    
#     vector_store = policy_qdrant_store()

