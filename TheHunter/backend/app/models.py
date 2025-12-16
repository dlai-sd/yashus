from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class Calculation(Base):
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    operand1 = Column(Float)
    operand2 = Column(Float)
    result = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
