from sqlalchemy import Column,String,Integer,ForeignKey
from src.database.db import Base
import uuid


class Payslip(Base):
    __tablename__="payslips"
    id = Column(String,primary_key=True,default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    month = Column(String, nullable=False)
    year = Column(Integer,nullable=False)
    gross_salary = Column(Integer,nullable=False)
    deduction = Column(Integer,nullable= False)
    net_salary=Column(Integer,nullable=False)
    bonuses=Column(Integer,nullable=False)
    pdf_url=Column(String,nullable=False)
