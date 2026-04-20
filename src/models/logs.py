from sqlalchemy import Column, String, Float, Text
from src.database.db import Base
import uuid


class Log(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    endpoint = Column(String)
    response_time = Column(Float)

    ai_response = Column(Text, nullable=True)
    request_query = Column(Text, nullable=True)  # optional upgrade