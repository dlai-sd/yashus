import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Calculation

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/calculator/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_calculate_add():
    response = client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "add", "operand1": 5, "operand2": 3}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_calculate_subtract():
    response = client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "subtract", "operand1": 10, "operand2": 4}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 6

def test_calculate_multiply():
    response = client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "multiply", "operand1": 3, "operand2": 7}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 21

def test_calculate_divide():
    response = client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "divide", "operand1": 20, "operand2": 4}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_calculate_divide_by_zero():
    response = client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "divide", "operand1": 10, "operand2": 0}
    )
    assert response.status_code == 400

def test_get_history():
    # Add some calculations
    client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "add", "operand1": 1, "operand2": 1}
    )
    client.post(
        "/api/v1/calculator/calculate",
        json={"operation": "multiply", "operand1": 2, "operand2": 3}
    )
    
    response = client.get("/api/v1/calculator/history")
    assert response.status_code == 200
    assert len(response.json()) >= 2
