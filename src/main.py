from fastapi import FastAPI
from src.database.db import Base, engine

#idhr apne database models hai
from src.models import user # imp forrregister models
from src.models import payslip # same 
from src.models import policy #same

#my routes
from src.api.routes import auth,user as user_routes
from src.api.routes import payslip
from src.api.routes import policy
from src.api.routes import ai

#creating app
app = FastAPI(title="Payroll Query and Management System")


#Base.metadata.drop_all(bind=engine)   # drops all tables
Base.metadata.create_all(bind=engine) # create tables

app.include_router(auth.router)
app.include_router(user_routes.router)
app.include_router(payslip.router)
app.include_router(policy.router)
app.include_router(ai.router)

# @app.get("/")
# def root():
#     return {"message": "Payroll system running "}