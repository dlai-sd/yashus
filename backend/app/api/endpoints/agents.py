"""
Agents API endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import uuid

from app.agents.base_agent import AgentStatus
from app.schemas.agent import (
    AgentInfo,
    AgentStatusResponse,
    AgentListResponse
)

router = APIRouter()

# In-memory storage for demo (use database in production)
active_agents: Dict[str, Any] = {}


@router.get("/", response_model=AgentListResponse)
async def list_agents():
    """List all available agent types"""
    agents = [
        AgentInfo(
            agent_type="sales_hunter",
            name="Sales Hunter Agent",
            description="Scrapes Google Maps and web for business leads",
            version="1.0.0",
            capabilities=[
                "Google Maps search",
                "Web scraping",
                "Lead deduplication",
                "Lead enrichment",
                "Geographic filtering"
            ]
        )
    ]
    return AgentListResponse(agents=agents, total=len(agents))


@router.get("/{agent_id}/status", response_model=AgentStatusResponse)
async def get_agent_status(agent_id: str):
    """Get status of a specific agent instance"""
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = active_agents[agent_id]
    return AgentStatusResponse(
        agent_id=agent_id,
        status=agent.get("status", AgentStatus.IDLE),
        created_at=agent.get("created_at"),
        updated_at=agent.get("updated_at")
    )


@router.get("/types")
async def get_agent_types():
    """Get available agent types and their configurations"""
    return {
        "agent_types": [
            {
                "type": "sales_hunter",
                "name": "Sales Hunter Agent",
                "description": "Scrapes Google Maps and internet for business leads",
                "required_params": [
                    {
                        "name": "search_phrase",
                        "type": "string",
                        "description": "What to search for (e.g., 'restaurants', 'dentists')"
                    },
                    {
                        "name": "location",
                        "type": "string",
                        "description": "Center location (address or coordinates)"
                    }
                ],
                "optional_params": [
                    {
                        "name": "radius",
                        "type": "integer",
                        "description": "Search radius in meters",
                        "default": 5000
                    },
                    {
                        "name": "max_results",
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 20
                    }
                ]
            }
        ]
    }
