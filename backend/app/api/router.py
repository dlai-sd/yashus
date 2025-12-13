"""
Main API Router
"""
from fastapi import APIRouter

from app.api.endpoints import agents, tasks

api_router = APIRouter()

# Include sub-routers
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
