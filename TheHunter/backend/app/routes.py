from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

# ============= AUTH ROUTES =============
@router.post("/api/auth/login")
async def login(credentials: dict):
    """
    Test login endpoint
    Accepts: {"email": "test@agentshome.com", "password": "TestPassword123"}
    """
    email = credentials.get("email")
    password = credentials.get("password")
    
    # Test credentials
    if email == "test@agentshome.com" and password == "TestPassword123":
        return {
            "token": "test-jwt-token-12345",
            "user": {
                "id": "user-1",
                "email": email,
                "name": "Test User",
                "provider": "email"
            }
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/api/auth/signup")
async def signup(credentials: dict):
    """
    Test signup endpoint
    """
    email = credentials.get("email")
    password = credentials.get("password")
    name = credentials.get("name", "New User")
    
    # For now, accept any signup
    return {
        "token": "test-jwt-token-67890",
        "user": {
            "id": "user-new",
            "email": email,
            "name": name,
            "provider": "email"
        }
    }

@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AgentsHome API",
        "version": "1.0.0"
    }
