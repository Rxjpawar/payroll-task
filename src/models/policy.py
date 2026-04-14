from sqlalchemy import Column,String , Integer , ForeignKey
from src.database.db import Base
import uuid


class Policy(Base):
    __tablename__="policy"
    id=Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    name=Column(String,nullable=False)
    year=Column(Integer,nullable=False)
    pdf_url=Column(String,nullable=False)