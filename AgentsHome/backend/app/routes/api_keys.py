from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, APIKey
from app.schemas import APIKeyResponse, APIKeyCreate, APIKeyCreateResponse
from app.services.auth_service import (
    verify_token, generate_api_key, hash_api_key
)
from typing import List
import uuid

router = APIRouter(prefix="/api/api-keys", tags=["api-keys"])

def get_current_user(authorization: str = None, db: Session = Depends(get_db)):
    """Extract and verify user from auth token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/", response_model=List[APIKeyResponse])
def list_api_keys(
    agent_id: str = None,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """List API keys for current user"""
    user = get_current_user(authorization, db)
    
    query = db.query(APIKey).filter(APIKey.user_id == user.id)
    if agent_id:
        query = query.filter(APIKey.agent_id == agent_id)
    
    keys = query.all()
    return keys

@router.post("/", response_model=APIKeyCreateResponse)
def create_api_key(
    request: APIKeyCreate,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Create new API key"""
    user = get_current_user(authorization, db)
    
    # Generate key
    plain_key = generate_api_key()
    hashed_key = hash_api_key(plain_key)
    
    api_key = APIKey(
        id=str(uuid.uuid4()),
        user_id=user.id,
        agent_id=request.agent_id,
        key_hash=hashed_key,
        name=request.name
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    return APIKeyCreateResponse(
        id=api_key.id,
        agent_id=api_key.agent_id,
        name=api_key.name,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
        key=plain_key  # Only return on creation
    )

@router.get("/{key_id}", response_model=APIKeyResponse)
def get_api_key(
    key_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get API key details"""
    user = get_current_user(authorization, db)
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return api_key

@router.put("/{key_id}/revoke", status_code=204)
def revoke_api_key(
    key_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Revoke API key"""
    user = get_current_user(authorization, db)
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    api_key.is_active = False
    db.commit()
    
    return None

@router.delete("/{key_id}", status_code=204)
def delete_api_key(
    key_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Delete API key"""
    user = get_current_user(authorization, db)
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    db.delete(api_key)
    db.commit()
    
    return None
