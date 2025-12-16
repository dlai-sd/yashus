from sqlalchemy.orm import Session
from app import models, schemas

class CalculationService:
    @staticmethod
    def calculate(operand1: float, operand2: float, operation: str) -> float:
        """Core calculation logic"""
        if operation == "add":
            return operand1 + operand2
        elif operation == "subtract":
            return operand1 - operand2
        elif operation == "multiply":
            return operand1 * operand2
        elif operation == "divide":
            if operand2 == 0:
                raise ValueError("Division by zero")
            return operand1 / operand2
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    @staticmethod
    def create_calculation(db: Session, calculation: schemas.CalculationCreate) -> models.Calculation:
        """Create and save calculation to database"""
        result = CalculationService.calculate(
            calculation.operand1,
            calculation.operand2,
            calculation.operation
        )
        
        db_calculation = models.Calculation(
            operation=calculation.operation,
            operand1=calculation.operand1,
            operand2=calculation.operand2,
            result=result
        )
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        return db_calculation
    
    @staticmethod
    def get_calculations(db: Session, skip: int = 0, limit: int = 100):
        """Get calculation history"""
        return db.query(models.Calculation).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_calculation(db: Session, calculation_id: int):
        """Get single calculation"""
        return db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
