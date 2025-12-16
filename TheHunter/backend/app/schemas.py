from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CalculationBase(BaseModel):
    operation: str  # "add", "subtract", "multiply", "divide"
    operand1: float
    operand2: float

class CalculationCreate(CalculationBase):
    pass

class CalculationResponse(CalculationBase):
    id: int
    result: float
    created_at: datetime
    
    class Config:
        from_attributes = True
