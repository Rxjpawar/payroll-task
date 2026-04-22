from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.utils.dependencies import get_current_user
from src.models.user import User
from src.ai.payslip_rag_pipeline import run_rag_pipeline
from src.ai.policy_rag_pieline import run_policy_rag_pipeline
router = APIRouter(prefix="/ai", tags=["AI"])


class QueryRequest(BaseModel):
    query: str


@router.post("/payslip/ask")
def ask_ai(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    response = run_rag_pipeline(
        query=request.query,
        user_id=current_user.id
    )

    return {"response": response}



@router.post("/policy/ask")
def ask_ai(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    response = run_policy_rag_pipeline(
        query=request.query,
    )

    return {"response": response}