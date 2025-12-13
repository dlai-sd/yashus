# Contributing to Yashus Agent Platform

Thank you for your interest in contributing to the Yashus Agent Platform! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Agent Development](#agent-development)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a feature branch
5. Make your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose
- Git

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start

# Run tests
npm test
```

## Making Changes

### Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Refactoring: `refactor/description`

Example: `feature/add-email-marketing-agent`

### Commit Messages

Follow the conventional commits specification:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(agents): add email marketing agent

Add new agent for automated email campaigns with template support
and A/B testing capabilities.

Closes #123
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_base_agent.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --code-coverage

# Run specific test
npm test -- --include='**/agent-list.component.spec.ts'
```

### Writing Tests

#### Backend Test Example

```python
import pytest
from app.agents.my_agent import MyAgent

def test_agent_validation():
    """Test agent validates inputs correctly"""
    agent = MyAgent(agent_id="test-001")
    
    # Valid task
    assert agent.validate_task({"required_field": "value"}) is True
    
    # Invalid task
    assert agent.validate_task({}) is False

@pytest.mark.asyncio
async def test_agent_execution():
    """Test agent executes successfully"""
    agent = MyAgent(agent_id="test-002")
    result = await agent.execute({"required_field": "value"})
    
    assert result.status.value == "completed"
    assert "data" in result.data
```

#### Frontend Test Example

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MyComponent } from './my.component';

describe('MyComponent', () => {
  let component: MyComponent;
  let fixture: ComponentFixture<MyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(MyComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load data on init', () => {
    component.ngOnInit();
    expect(component.data).toBeDefined();
  });
});
```

## Submitting Changes

### Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests locally**
   ```bash
   # Backend
   cd backend && pytest tests/ -v
   
   # Frontend
   cd frontend && npm test
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/my-feature
   ```

4. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Documentation updated

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #123
```

## Coding Standards

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Docstrings for all public functions/classes

```python
from typing import Dict, Any, Optional

async def process_data(
    data: Dict[str, Any],
    options: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Process data according to specified options.
    
    Args:
        data: Input data dictionary
        options: Optional processing options
        
    Returns:
        Processed data dictionary
        
    Raises:
        ValueError: If data is invalid
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Processing logic here
    return processed_data
```

### TypeScript (Frontend)

- Follow Angular style guide
- Use strict TypeScript mode
- Maximum line length: 120 characters
- Document complex functions

```typescript
/**
 * Fetches agent data from the API
 * @param agentId - The unique identifier for the agent
 * @returns Observable of agent data
 */
getAgent(agentId: string): Observable<Agent> {
  return this.http.get<Agent>(`${this.apiUrl}/agents/${agentId}`);
}
```

### Code Formatting

We use automatic formatters:

**Backend (Python)**
```bash
# Install
pip install black isort

# Format
black backend/
isort backend/
```

**Frontend (TypeScript)**
```bash
# Format
npm run format
```

## Agent Development

When adding a new agent:

1. **Create agent class**
   - Inherit from `BaseAgent`
   - Implement `validate_task()` and `execute()`
   
2. **Add tests**
   - Unit tests for validation
   - Unit tests for execution
   - Integration tests for API

3. **Register agent**
   - Add to `tasks.py` endpoint
   - Add to `agents.py` types list

4. **Update documentation**
   - Add to README
   - Create agent-specific docs
   - Update API documentation

5. **Add UI support (optional)**
   - Create form in `task-create` component
   - Add result visualization

See [AGENT_DEVELOPMENT.md](./AGENT_DEVELOPMENT.md) for detailed guide.

## Documentation

### Update README

- Keep README up-to-date with new features
- Add examples for new functionality
- Update configuration sections

### API Documentation

- FastAPI auto-generates OpenAPI docs
- Add descriptive docstrings to endpoints
- Include request/response examples

```python
@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """
    Create a new agent task.
    
    Example request:
    ```json
    {
      "agent_type": "sales_hunter",
      "config": {
        "search_phrase": "restaurants",
        "location": "San Francisco, CA"
      }
    }
    ```
    
    Returns the created task with a unique ID.
    """
    # Implementation
```

## Review Process

### What Reviewers Look For

1. **Code Quality**
   - Clean, readable code
   - Follows style guidelines
   - Proper error handling

2. **Testing**
   - Adequate test coverage
   - Tests pass
   - Edge cases covered

3. **Documentation**
   - Code is documented
   - README updated
   - API docs complete

4. **Performance**
   - No obvious performance issues
   - Efficient algorithms
   - Proper resource management

### Response Time

- Initial review: Within 3 business days
- Follow-up reviews: Within 2 business days
- Urgent fixes: Within 1 business day

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Email**: support@yashus.in

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in significant feature announcements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Yashus Agent Platform! 🎉
