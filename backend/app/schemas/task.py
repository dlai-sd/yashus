"""
Task schemas
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Create task request"""
    agent_type: str = Field(..., description="Type of agent to run")
    config: Dict[str, Any] = Field(..., description="Task configuration")


class TaskResponse(BaseModel):
    """Task response"""
    task_id: str
    agent_type: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    error: Optional[str] = None


class TaskResultResponse(BaseModel):
    """Task result response"""
    task_id: str
    agent_type: str
    status: str
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
