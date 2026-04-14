from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.user import User
from src.schemas.user import UserCreate
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token

def register_user_service(user:UserCreate,db:Session):

    #check if email alredy exissts
    existing_user= db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise  HTTPException(status_code=400, detail="Email is alredy registered")
    
    #hash password
    hashed_password = hash_password(user.password)

    new_user=User(
        name= user.name,
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user


# login service
def login_user_service(email: str, password: str, db: Session):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}