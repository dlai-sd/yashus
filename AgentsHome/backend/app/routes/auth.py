from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import (
    LoginRequest, SignupRequest, AuthResponse, UserResponse,
    TokenResponse, SSOCallbackRequest
)
from app.services.auth_service import (
    hash_password, verify_password, create_access_token, 
    create_refresh_token, verify_token
)
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=AuthResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password),
        provider="email"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    
    return AuthResponse(
        token=access_token,
        user=UserResponse.from_orm(user)
    )

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash or ""):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    
    return AuthResponse(
        token=access_token,
        user=UserResponse.from_orm(user)
    )

@router.post("/sso-callback", response_model=AuthResponse)
def sso_callback(request: SSOCallbackRequest, db: Session = Depends(get_db)):
    """
    Handle SSO provider callbacks.
    In production, validate the code with provider and get user info.
    """
    # TODO: Implement provider-specific validation
    # For now, this is a placeholder
    raise HTTPException(status_code=501, detail="SSO not yet implemented")

@router.post("/refresh", response_model=AuthResponse)
def refresh_token(token: str, db: Session = Depends(get_db)):
    """Refresh access token"""
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_access_token = create_access_token(data={"sub": user.id})
    
    return AuthResponse(
        token=new_access_token,
        user=UserResponse.from_orm(user)
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = None, db: Session = Depends(get_db)):
    """Get current user info"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse.from_orm(user)
