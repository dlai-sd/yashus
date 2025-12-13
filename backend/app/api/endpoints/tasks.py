"""
Tasks API endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid
from datetime import datetime

from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskResultResponse
)
from app.agents.sales_hunter_agent import SalesHunterAgent

router = APIRouter()

# In-memory storage for demo (use database in production)
# WARNING: Data will be lost on restart and does not scale across multiple instances
# For production, implement database-backed storage (PostgreSQL, MongoDB, etc.)
tasks: Dict[str, Dict[str, Any]] = {}


async def execute_agent_task(task_id: str, agent_type: str, task_config: Dict[str, Any]):
    """Execute agent task in background"""
    try:
        # Create agent instance
        if agent_type == "sales_hunter":
            agent = SalesHunterAgent(agent_id=task_id)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # Update task status
        tasks[task_id]["status"] = "running"
        tasks[task_id]["updated_at"] = datetime.utcnow()
        
        # Run agent
        result = await agent.run(task_config)
        
        # Store result
        tasks[task_id]["status"] = result.status.value
        tasks[task_id]["result"] = result.dict()
        tasks[task_id]["updated_at"] = datetime.utcnow()
        
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        tasks[task_id]["updated_at"] = datetime.utcnow()


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, background_tasks: BackgroundTasks):
    """Create and execute a new agent task"""
    task_id = str(uuid.uuid4())
    
    # Validate agent type
    valid_types = ["sales_hunter"]
    if task.agent_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid agent type. Must be one of: {valid_types}"
        )
    
    # Store task
    tasks[task_id] = {
        "task_id": task_id,
        "agent_type": task.agent_type,
        "config": task.config,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "result": None,
        "error": None
    }
    
    # Execute task in background
    background_tasks.add_task(
        execute_agent_task,
        task_id,
        task.agent_type,
        task.config
    )
    
    return TaskResponse(
        task_id=task_id,
        agent_type=task.agent_type,
        status="pending",
        created_at=tasks[task_id]["created_at"]
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """Get task status"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = tasks[task_id]
    return TaskResponse(
        task_id=task_id,
        agent_type=task_data["agent_type"],
        status=task_data["status"],
        created_at=task_data["created_at"],
        updated_at=task_data.get("updated_at"),
        error=task_data.get("error")
    )


@router.get("/{task_id}/result", response_model=TaskResultResponse)
async def get_task_result(task_id: str):
    """Get task result"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = tasks[task_id]
    
    if task_data["status"] == "pending" or task_data["status"] == "running":
        raise HTTPException(
            status_code=202,
            detail="Task is still running. Please check status."
        )
    
    if task_data["status"] == "failed":
        raise HTTPException(
            status_code=500,
            detail=f"Task failed: {task_data.get('error', 'Unknown error')}"
        )
    
    return TaskResultResponse(
        task_id=task_id,
        agent_type=task_data["agent_type"],
        status=task_data["status"],
        result=task_data.get("result"),
        created_at=task_data["created_at"],
        completed_at=task_data.get("updated_at")
    )


@router.get("/")
async def list_tasks():
    """List all tasks"""
    return {
        "tasks": [
            {
                "task_id": task_id,
                "agent_type": task_data["agent_type"],
                "status": task_data["status"],
                "created_at": task_data["created_at"],
                "updated_at": task_data.get("updated_at")
            }
            for task_id, task_data in tasks.items()
        ],
        "total": len(tasks)
    }
