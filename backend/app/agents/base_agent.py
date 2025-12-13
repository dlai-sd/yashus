"""
Base Agent Class - Foundation for all AI agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import logging
import asyncio
from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


class AgentStatus(str, Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentResult(BaseModel):
    """Standard agent result format"""
    agent_id: str
    agent_type: str
    status: AgentStatus
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all agents in the platform.
    Provides common functionality and interface.
    """
    
    def __init__(
        self,
        agent_id: str,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(f"{self.__class__.__name__}:{agent_id}")
        self._results: List[Dict[str, Any]] = []
        self._errors: List[str] = []
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's main task.
        Must be implemented by subclasses.
        
        Args:
            task: Task configuration and parameters
            
        Returns:
            AgentResult with execution results
        """
        pass
    
    @abstractmethod
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """
        Validate task parameters before execution.
        
        Args:
            task: Task configuration to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    async def run(self, task: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with error handling and status management.
        
        Args:
            task: Task configuration
            
        Returns:
            AgentResult with execution results
        """
        started_at = datetime.utcnow()
        
        try:
            # Validate task
            if not self.validate_task(task):
                raise ValueError("Invalid task configuration")
            
            # Update status
            self.status = AgentStatus.RUNNING
            self.logger.info(f"Starting agent execution: {self.agent_id}")
            
            # Execute task
            result = await self.execute(task)
            
            # Mark as completed
            self.status = AgentStatus.COMPLETED
            result.status = AgentStatus.COMPLETED
            result.completed_at = datetime.utcnow()
            
            self.logger.info(f"Agent execution completed: {self.agent_id}")
            return result
            
        except asyncio.CancelledError:
            self.status = AgentStatus.CANCELLED
            self.logger.warning(f"Agent execution cancelled: {self.agent_id}")
            return AgentResult(
                agent_id=self.agent_id,
                agent_type=self.__class__.__name__,
                status=AgentStatus.CANCELLED,
                error="Execution cancelled",
                started_at=started_at,
                completed_at=datetime.utcnow()
            )
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            error_msg = f"Agent execution failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return AgentResult(
                agent_id=self.agent_id,
                agent_type=self.__class__.__name__,
                status=AgentStatus.FAILED,
                error=error_msg,
                started_at=started_at,
                completed_at=datetime.utcnow()
            )
    
    def get_status(self) -> AgentStatus:
        """Get current agent status"""
        return self.status
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get accumulated results"""
        return self._results
    
    def add_result(self, result: Dict[str, Any]):
        """Add a result to the accumulated results"""
        self._results.append(result)
