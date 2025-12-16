from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Subscription
from app.schemas import SubscriptionResponse, SubscriptionCreate
from app.services.auth_service import verify_token
from typing import List
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

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

@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions(
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """List all subscriptions for current user"""
    user = get_current_user(authorization, db)
    
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == user.id
    ).all()
    
    return subscriptions

@router.get("/{agent_id}", response_model=SubscriptionResponse)
def get_subscription(
    agent_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get subscription for specific agent"""
    user = get_current_user(authorization, db)
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.agent_id == agent_id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return subscription

@router.post("/", response_model=SubscriptionResponse)
def create_subscription(
    request: SubscriptionCreate,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Create new subscription"""
    user = get_current_user(authorization, db)
    
    # Check if already subscribed
    existing = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.agent_id == request.agent_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed to this agent")
    
    subscription = Subscription(
        id=str(uuid.uuid4()),
        user_id=user.id,
        agent_id=request.agent_id,
        plan_tier=request.plan_tier,
        renewal_date=datetime.utcnow() + timedelta(days=30)
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: str,
    request: SubscriptionCreate,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Update subscription (e.g., upgrade plan)"""
    user = get_current_user(authorization, db)
    
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user.id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.plan_tier = request.plan_tier
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.delete("/{subscription_id}", status_code=204)
def cancel_subscription(
    subscription_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Cancel subscription"""
    user = get_current_user(authorization, db)
    
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user.id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.status = "cancelled"
    db.commit()
    
    return None
