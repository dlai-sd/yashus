from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)  # Null if SSO user
    provider = Column(String, default="email")  # 'email', 'google', 'github', 'microsoft', 'linkedin', 'apple'
    provider_id = Column(String, nullable=True)  # External provider ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    agent_id = Column(String, nullable=False)  # 'hunter', 'agent2', etc
    plan_tier = Column(String, default="free")  # 'free', 'pro', 'enterprise'
    status = Column(String, default="active")  # 'active', 'suspended', 'cancelled'
    api_quota = Column(Integer, default=1000)  # Monthly API calls limit
    api_used = Column(Integer, default=0)  # API calls used this month
    renewal_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    agent_id = Column(String, nullable=False)  # Which agent this key is for
    key_hash = Column(String, nullable=False)  # Hashed key
    name = Column(String, default="API Key")
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="api_keys")
