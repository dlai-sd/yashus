"""
Unit tests for BaseAgent
"""
import pytest
import asyncio
from datetime import datetime
from app.agents.base_agent import BaseAgent, AgentResult, AgentStatus


class MockAgent(BaseAgent):
    """Mock agent for testing"""
    
    async def execute(self, task):
        """Mock execute method"""
        return AgentResult(
            agent_id=self.agent_id,
            agent_type="mock",
            status=AgentStatus.COMPLETED,
            data={"result": "success"},
            started_at=datetime.utcnow()
        )
    
    def validate_task(self, task):
        """Mock validate method"""
        return "required_field" in task


@pytest.mark.asyncio
async def test_agent_run_success():
    """Test successful agent execution"""
    agent = MockAgent(agent_id="test-001")
    task = {"required_field": "value"}
    
    result = await agent.run(task)
    
    assert result.status == AgentStatus.COMPLETED
    assert result.agent_id == "test-001"
    assert result.data["result"] == "success"


@pytest.mark.asyncio
async def test_agent_validation_failure():
    """Test agent validation failure"""
    agent = MockAgent(agent_id="test-002")
    task = {}  # Missing required field
    
    result = await agent.run(task)
    
    assert result.status == AgentStatus.FAILED
    assert "Invalid task configuration" in result.error


def test_agent_get_status():
    """Test agent status retrieval"""
    agent = MockAgent(agent_id="test-003")
    
    assert agent.get_status() == AgentStatus.IDLE


def test_agent_add_result():
    """Test adding results to agent"""
    agent = MockAgent(agent_id="test-004")
    
    agent.add_result({"data": "test"})
    results = agent.get_results()
    
    assert len(results) == 1
    assert results[0]["data"] == "test"
