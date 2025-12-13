"""
Agent schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.agents.base_agent import AgentStatus


class AgentInfo(BaseModel):
    """Agent type information"""
    agent_type: str
    name: str
    description: str
    version: str
    capabilities: List[str] = Field(default_factory=list)


class AgentListResponse(BaseModel):
    """List of agents response"""
    agents: List[AgentInfo]
    total: int


class AgentStatusResponse(BaseModel):
    """Agent status response"""
    agent_id: str
    status: AgentStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
