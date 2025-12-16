# Phase 1 Quick Reference - Developers

This is your quick reference for common Phase 1 development tasks.

## 🚀 Getting Started (First Time)

```bash
# 1. Clone and navigate
git clone https://github.com/dlai-sd/yashus.git
cd yashus

# 2. Install Python dependencies
cd TheHunter/backend
pip install -r requirements.txt

# 3. Install Node dependencies
cd ../frontend
npm install
cd ../..

# 4. Setup pre-commit hooks
pip install pre-commit
pre-commit install

# 5. Setup local database
psql postgresql://localhost/yashus < TheHunter/backend/migrations/001_init.sql

# 6. Run tests
cd TheHunter/backend
pytest tests/ -v
```

---

## 📝 Writing Tests

Tests use provided fixtures from `conftest.py`. No mocking needed—fixtures handle it.

### Example 1: Test AI Component Scoring

```python
import pytest

@pytest.mark.component
async def test_ai_scoring(ai_component):
    """Test AI component returns valid scores."""
    result = await ai_component.execute({
        "lead_data": {"company": "Test Co", "industry": "dental"}
    })
    
    assert result["status"] == "success"
    assert 0.0 <= result["score"] <= 1.0
```

### Example 2: Test Recipe Response Schema

```python
@pytest.mark.recipe
def test_recipe_response(recipe_success_response):
    """Validate recipe returns correct schema."""
    assert recipe_success_response["status"] == "success"
    assert "metadata" in recipe_success_response
    assert recipe_success_response["metadata"]["credits_consumed"] >= 0
```

### Example 3: Test Multi-tenancy Isolation

```python
@pytest.mark.recipe
async def test_customer_isolation(state_manager):
    """Ensure states are isolated per customer."""
    await state_manager.set_state("cust-001", "pref", {"theme": "dark"})
    await state_manager.set_state("cust-002", "pref", {"theme": "light"})
    
    pref1 = await state_manager.get_state("cust-001", "pref")
    pref2 = await state_manager.get_state("cust-002", "pref")
    
    assert pref1["theme"] == "dark"
    assert pref2["theme"] == "light"
```

### Available Fixtures

```python
# Components
ai_component                # AI scoring (Discovery, Intelligence)
action_component            # Data fetching (Scraping, Enrichment)
correspondence_component    # Message generation (Personalization)
state_manager              # Context storage
audit_logger               # Compliance logging
subscription_component     # Credit management

# Recipe Inputs
discovery_recipe_input()              # Scraping query
intelligence_recipe_input()           # Enrichment targets
personalization_recipe_input()        # Message context
subscription_recipe_input()           # Credit tracking

# Response Schemas
recipe_success_response()             # Valid success response
recipe_failure_response()             # Valid failure response
```

---

## 🧪 Running Tests

```bash
# Run all tests
cd TheHunter/backend
pytest tests/ -v

# Run specific test file
pytest tests/test_recipe_executor.py -v

# Run specific test
pytest tests/test_recipe_executor.py::TestAIComponent::test_ai_component_execute -v

# Run by marker
pytest -m component           # Only component tests
pytest -m recipe             # Only recipe tests
pytest -m audit              # Only audit tests
pytest -m integration        # Only integration tests

# With coverage
pytest tests/ --cov=app --cov-report=html

# Watch mode (rerun on file changes)
pip install pytest-watch
ptw tests/ -- -v
```

---

## 🔧 Code Quality (Pre-commit)

Pre-commit hooks run automatically before commit. Setup once:

```bash
pip install pre-commit
pre-commit install
```

Now all commits are validated:

```bash
git commit -m "..."
# ✅ Hooks run automatically
# If issues found: fix and try again
```

### Manual Hook Runs

```bash
# Check all files
pre-commit run --all-files

# Check specific hook
pre-commit run black --all-files    # Code formatting
pre-commit run mypy --all-files     # Type checking
pre-commit run flake8 --all-files   # Linting
```

### Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `black` says reformat | Stage changes: `git add .` then commit |
| `isort` rearranged imports | Stage changes: `git add .` then commit |
| `pylint` or `flake8` violation | Fix manually, then stage and commit |
| `mypy` type error | Add type hints or fix variable usage |
| `detect-secrets` found API key | **Remove immediately!** Use env vars instead |

---

## 💾 Database

### Schema & Migrations

```bash
# Apply initial schema (one time)
psql postgresql://localhost/yashus < TheHunter/backend/migrations/001_init.sql

# Check tables created
psql postgresql://localhost/yashus
  \dt
  \d customers    # Describe table
  \q             # Quit

# Reset database (development only)
dropdb yashus
createdb yashus
psql postgresql://localhost/yashus < TheHunter/backend/migrations/001_init.sql
```

### Query Examples

```sql
-- View customers
SELECT id, name, email, subscription_tier FROM customers;

-- View subscription plans
SELECT * FROM subscription_plans;

-- Insert test customer
INSERT INTO customers (name, email)
VALUES ('Test Customer', 'test@example.com');

-- View subscription for customer
SELECT s.* FROM subscriptions s
WHERE s.customer_id = 'cust-001';

-- View audit logs (compliance)
SELECT timestamp, action_type, resource_id, result_status
FROM audit_logs
WHERE customer_id = 'cust-001'
ORDER BY timestamp DESC;
```

---

## 🚢 Deployment

### Local Testing

```bash
# Start backend
cd TheHunter/backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd TheHunter/frontend
npm start

# Test endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:4200    # Frontend
```

### Deploy to Azure (GitHub Actions)

```bash
# Push to develop (auto-deploys to staging)
git push origin develop

# Deploy to production (manual)
# 1. Go to GitHub → Actions → build-push-deploy
# 2. Click "Run workflow"
# 3. Select environment: "production"
# 4. Watch deployment progress

# Verify deployment
bash scripts/smoke-tests.sh
  API_BASE_URL=https://hunter-api-prod.azurewebsites.net \
  FRONTEND_URL=https://hunter-prod.azurewebsites.net \
  bash scripts/smoke-tests.sh
```

---

## 📊 Monitoring

### Check CI/CD Pipeline

```bash
# View workflow runs
# https://github.com/dlai-sd/yashus/actions

# View specific run logs
# Click run → build-push-deploy → expand jobs
```

### Run Smoke Tests

```bash
# Locally (against local backend)
bash scripts/smoke-tests.sh

# Against staging
API_BASE_URL=https://hunter-api-staging.azurewebsites.net \
FRONTEND_URL=https://hunter-staging.azurewebsites.net \
bash scripts/smoke-tests.sh

# Expected output
✓ PASS: API health endpoint (HTTP 200)
✓ PASS: Database connection verified
✓ PASS: API response time: 245ms (acceptable)
...
✅ All smoke tests passed - Deployment is healthy!
```

---

## 🔐 Secrets Management

### Never Commit Secrets!

```python
# ❌ WRONG
DATABASE_URL = "postgresql://user:password@host/db"
API_KEY = "sk-abc123xyz"

# ✅ RIGHT
import os
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("GROQ_API_KEY")
```

### Add GitHub Secrets

1. Go to GitHub repo Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `SECRET_NAME`, Value: `value`
4. Use in code: `${{ secrets.SECRET_NAME }}`

### Required Secrets for Phase 1

```
ACR_USERNAME              # Azure Container Registry user
ACR_PASSWORD              # Azure Container Registry password
AZURE_CREDENTIALS         # Azure service principal JSON
AZURE_RESOURCE_GROUP      # Resource group name
DATABASE_URL              # PostgreSQL connection string
SECRET_KEY                # FastAPI secret key
```

---

## 📚 Documentation Links

| Document | Purpose |
|----------|---------|
| [AGENT_DESIGN.md](../docs/AGENT_DESIGN.md) | Architecture & design specs |
| [SECRETS_SETUP.md](../.github/SECRETS_SETUP.md) | GitHub secrets guide |
| [PRE_COMMIT_SETUP.md](../docs/PRE_COMMIT_SETUP.md) | Pre-commit hooks guide |
| [PHASE1_SETUP_COMPLETE.md](../docs/PHASE1_SETUP_COMPLETE.md) | Full setup overview |

---

## 🆘 Common Issues

### Tests Fail: "fixture 'ai_component' not found"

```bash
# Check conftest.py exists
ls TheHunter/backend/tests/conftest.py

# Check pytest finds it
cd TheHunter/backend
pytest --fixtures | grep ai_component
```

### Pre-commit Hook Fails

```bash
# View what hook failed
pre-commit run --all-files --verbose

# Run only that hook
pre-commit run black --all-files

# Temporarily skip (emergency)
git commit --no-verify
```

### Database Connection Error

```bash
# Check PostgreSQL is running
psql postgresql://localhost/yashus -c "SELECT 1"

# Check schema exists
psql postgresql://localhost/yashus \dt

# Reinitialize
dropdb yashus
createdb yashus
psql postgresql://localhost/yashus < TheHunter/backend/migrations/001_init.sql
```

### Deployment Fails

```bash
# Check GitHub Actions logs
# https://github.com/dlai-sd/yashus/actions

# Verify secrets are set
# GitHub → Settings → Secrets and variables → Actions

# Check required environment variables
env | grep DATABASE_URL
env | grep GROQ_API_KEY
```

---

## ⚡ Productivity Tips

### 1. Fast Test Loop

```bash
# Terminal 1: Watch mode (reruns tests on file save)
cd TheHunter/backend
ptw tests/ -- -v

# Terminal 2: Make code changes
# Tests auto-run as you save
```

### 2. Check Before Committing

```bash
# Run all checks locally before pushing
pre-commit run --all-files
pytest tests/ -v
```

### 3. Stash Changes Temporarily

```bash
git stash
# ... switch branches, run experiments
git stash pop
```

### 4. View Recent Changes

```bash
git log --oneline -5
git diff                      # Unstaged changes
git diff --cached             # Staged changes
```

---

## 🎯 Next Phase Work

**After Phase 1 Framework is done:**
- Phase 2: The Hunter recipes (Discovery, Intelligence, Personalization, Outreach)
- Phase 3: Subscription & alerts
- Phase 4: Admin dashboard & forensics

Start Phase 1 here: [AGENT_DESIGN.md](../docs/AGENT_DESIGN.md)
