# Agent Development Guide

## Overview

This guide will help you create custom agents for the Yashus Agent Platform. The platform provides a flexible framework for building autonomous AI agents that can perform various marketing automation tasks.

## Agent Architecture

All agents inherit from the `BaseAgent` class which provides:
- Task validation
- Execution lifecycle management
- Error handling
- Status tracking
- Result accumulation

## Creating a New Agent

### Step 1: Define Your Agent Class

```python
from typing import Dict, Any
from datetime import datetime
from app.agents.base_agent import BaseAgent, AgentResult, AgentStatus

class MyMarketingAgent(BaseAgent):
    """
    Description of what your agent does
    """
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, config)
        self.agent_type = "my_marketing_agent"
```

### Step 2: Implement Task Validation

```python
def validate_task(self, task: Dict[str, Any]) -> bool:
    """
    Validate that the task has all required parameters
    
    Args:
        task: Task configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["field1", "field2"]
    
    for field in required_fields:
        if field not in task:
            self.logger.error(f"Missing required field: {field}")
            return False
    
    # Add custom validation logic
    if not self._validate_custom_logic(task):
        return False
    
    return True
```

### Step 3: Implement Task Execution

```python
async def execute(self, task: Dict[str, Any]) -> AgentResult:
    """
    Execute the agent's main task
    
    Args:
        task: Task configuration
        
    Returns:
        AgentResult with execution results
    """
    started_at = datetime.utcnow()
    
    try:
        # Extract task parameters
        param1 = task["field1"]
        param2 = task["field2"]
        
        # Perform the agent's work
        results = await self._do_work(param1, param2)
        
        # Return success result
        return AgentResult(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            status=AgentStatus.COMPLETED,
            data={
                "results": results,
                "summary": f"Processed {len(results)} items"
            },
            started_at=started_at,
            completed_at=datetime.utcnow(),
            metadata={
                "processed_count": len(results)
            }
        )
        
    except Exception as e:
        self.logger.error(f"Execution failed: {str(e)}", exc_info=True)
        raise
```

### Step 4: Add Helper Methods

```python
async def _do_work(self, param1: str, param2: str) -> List[Dict]:
    """
    Private helper method for doing the actual work
    """
    results = []
    
    # Your implementation here
    
    return results
```

## Registering Your Agent

### 1. Add to API Endpoints

Edit `backend/app/api/endpoints/tasks.py`:

```python
async def execute_agent_task(task_id: str, agent_type: str, task_config: Dict[str, Any]):
    """Execute agent task in background"""
    try:
        # Add your agent type
        if agent_type == "sales_hunter":
            agent = SalesHunterAgent(agent_id=task_id)
        elif agent_type == "my_marketing_agent":
            agent = MyMarketingAgent(agent_id=task_id)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # ... rest of the code
```

### 2. Add to Agent Types Endpoint

Edit `backend/app/api/endpoints/agents.py`:

```python
@router.get("/types")
async def get_agent_types():
    """Get available agent types and their configurations"""
    return {
        "agent_types": [
            {
                "type": "sales_hunter",
                "name": "Sales Hunter Agent",
                "description": "Scrapes Google Maps and internet for business leads",
                # ... config ...
            },
            {
                "type": "my_marketing_agent",
                "name": "My Marketing Agent",
                "description": "Description of what your agent does",
                "required_params": [
                    {
                        "name": "field1",
                        "type": "string",
                        "description": "Description of field1"
                    }
                ],
                "optional_params": [
                    {
                        "name": "field2",
                        "type": "integer",
                        "description": "Description of field2",
                        "default": 100
                    }
                ]
            }
        ]
    }
```

### 3. Update Frontend (Optional)

If you want custom UI for your agent, update `frontend/src/app/components/task-create/task-create.component.html` to add agent-specific form fields.

## Testing Your Agent

### Unit Tests

Create tests in `backend/tests/unit/test_my_marketing_agent.py`:

```python
import pytest
from app.agents.my_marketing_agent import MyMarketingAgent

def test_validation_success():
    """Test successful task validation"""
    agent = MyMarketingAgent(agent_id="test-001")
    task = {
        "field1": "value1",
        "field2": "value2"
    }
    
    assert agent.validate_task(task) is True

@pytest.mark.asyncio
async def test_execution():
    """Test agent execution"""
    agent = MyMarketingAgent(agent_id="test-002")
    task = {
        "field1": "value1",
        "field2": "value2"
    }
    
    result = await agent.execute(task)
    
    assert result.status.value == "completed"
    assert "results" in result.data
```

### Integration Tests

Test the full API flow in `backend/tests/integration/test_my_agent_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_my_agent_task():
    """Test creating a task via API"""
    response = client.post(
        "/api/v1/tasks/",
        json={
            "agent_type": "my_marketing_agent",
            "config": {
                "field1": "value1",
                "field2": "value2"
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
```

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```python
try:
    result = await self._process_data(data)
except ValueError as e:
    self.logger.error(f"Validation error: {str(e)}")
    raise
except Exception as e:
    self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    raise
```

### 2. Logging

Use structured logging:

```python
self.logger.info(
    f"Processing {count} items",
    extra={
        "agent_id": self.agent_id,
        "item_count": count
    }
)
```

### 3. Rate Limiting

Respect API rate limits:

```python
import asyncio

async def _fetch_with_rate_limit(self, items: List[str]):
    """Fetch items with rate limiting"""
    results = []
    
    for item in items:
        result = await self._fetch_item(item)
        results.append(result)
        await asyncio.sleep(1)  # Rate limit: 1 request per second
    
    return results
```

### 4. Progress Tracking

Track progress for long-running tasks:

```python
async def execute(self, task: Dict[str, Any]) -> AgentResult:
    items = task["items"]
    total = len(items)
    
    for i, item in enumerate(items):
        result = await self._process_item(item)
        self.add_result(result)
        
        # Log progress
        self.logger.info(f"Progress: {i+1}/{total} items processed")
```

### 5. Resource Cleanup

Clean up resources properly:

```python
async def execute(self, task: Dict[str, Any]) -> AgentResult:
    browser = None
    try:
        browser = await launch_browser()
        results = await self._scrape_with_browser(browser, task)
        return results
    finally:
        if browser:
            await browser.close()
```

## Common Patterns

### Web Scraping Agent

```python
from playwright.async_api import async_playwright

class WebScraperAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> AgentResult:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            url = task["url"]
            await page.goto(url)
            
            # Extract data
            data = await page.evaluate("""
                () => {
                    // Your scraping logic
                    return document.querySelectorAll('.item');
                }
            """)
            
            await browser.close()
            
            return AgentResult(...)
```

### API Integration Agent

```python
import httpx

class APIIntegrationAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> AgentResult:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                task["api_url"],
                headers={"Authorization": f"Bearer {task['api_key']}"}
            )
            
            data = response.json()
            processed_data = self._process_response(data)
            
            return AgentResult(...)
```

### Data Processing Agent

```python
import pandas as pd

class DataProcessingAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> AgentResult:
        # Load data
        df = pd.read_csv(task["input_file"])
        
        # Process data
        processed_df = self._transform_data(df)
        
        # Save results
        output_file = f"/tmp/{self.agent_id}_results.csv"
        processed_df.to_csv(output_file, index=False)
        
        return AgentResult(
            data={
                "output_file": output_file,
                "rows_processed": len(processed_df)
            },
            ...
        )
```

## Advanced Topics

### Streaming Results

For long-running agents, you can stream results:

```python
async def execute(self, task: Dict[str, Any]) -> AgentResult:
    items = task["items"]
    
    for item in items:
        result = await self._process_item(item)
        
        # Add to results immediately
        self.add_result(result)
        
        # Could also publish to Redis/pub-sub for real-time updates
        await self._publish_progress(result)
    
    return AgentResult(
        data={"results": self.get_results()},
        ...
    )
```

### Multi-step Agents

Break complex tasks into steps:

```python
async def execute(self, task: Dict[str, Any]) -> AgentResult:
    # Step 1: Data collection
    raw_data = await self._collect_data(task)
    
    # Step 2: Data processing
    processed_data = await self._process_data(raw_data)
    
    # Step 3: Data enrichment
    enriched_data = await self._enrich_data(processed_data)
    
    # Step 4: Generate output
    output = await self._generate_output(enriched_data)
    
    return AgentResult(
        data=output,
        metadata={
            "steps_completed": 4,
            "raw_items": len(raw_data),
            "final_items": len(output)
        },
        ...
    )
```

## Troubleshooting

### Common Issues

1. **Task validation fails**: Check that all required fields are present and correctly named
2. **Agent timeout**: Increase `AGENT_TIMEOUT_SECONDS` in config or optimize your agent
3. **Memory issues**: Process data in batches instead of loading everything at once
4. **Rate limiting**: Add delays between API calls

## Next Steps

- Review the Sales Hunter agent implementation for a complete example
- Read the API documentation at http://localhost:8000/docs
- Join the community discussions

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Playwright Documentation](https://playwright.dev/python/)
