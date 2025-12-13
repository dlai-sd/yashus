"""
Unit tests for SalesHunterAgent
"""
import pytest
from app.agents.sales_hunter_agent import SalesHunterAgent


def test_sales_hunter_validation_success():
    """Test successful task validation"""
    agent = SalesHunterAgent(agent_id="test-sh-001")
    task = {
        "search_phrase": "restaurants",
        "location": "San Francisco, CA"
    }
    
    assert agent.validate_task(task) is True


def test_sales_hunter_validation_missing_phrase():
    """Test validation with missing search phrase"""
    agent = SalesHunterAgent(agent_id="test-sh-002")
    task = {
        "location": "San Francisco, CA"
    }
    
    assert agent.validate_task(task) is False


def test_sales_hunter_validation_missing_location():
    """Test validation with missing location"""
    agent = SalesHunterAgent(agent_id="test-sh-003")
    task = {
        "search_phrase": "restaurants"
    }
    
    assert agent.validate_task(task) is False


def test_sales_hunter_validation_empty_phrase():
    """Test validation with empty search phrase"""
    agent = SalesHunterAgent(agent_id="test-sh-004")
    task = {
        "search_phrase": "   ",
        "location": "San Francisco, CA"
    }
    
    assert agent.validate_task(task) is False


@pytest.mark.asyncio
async def test_sales_hunter_execute():
    """Test sales hunter execution"""
    agent = SalesHunterAgent(agent_id="test-sh-005")
    task = {
        "search_phrase": "restaurants",
        "location": "San Francisco, CA",
        "radius": 5000,
        "max_results": 10
    }
    
    result = await agent.execute(task)
    
    assert result.status.value == "completed"
    assert "leads" in result.data
    assert result.data["total_found"] >= 0
