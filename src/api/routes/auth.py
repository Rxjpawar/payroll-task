from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas.user import UserCreate, UserResponse
from src.services.auth_service import register_user_service,login_user_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

#create the user
@router.post('/register', response_model=UserResponse)
def register_user(user:UserCreate,db:Session= Depends(get_db)):
    return register_user_service(user, db)

#login the user
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    return login_user_service(
        email=form_data.username,
        password=form_data.password,
        db=db
    )