# Phase 1 Framework - Complete Documentation Index

This is your master reference for Phase 1 setup and development.

## 📖 Documentation Files (Read First)

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [PHASE1_QUICK_REFERENCE.md](PHASE1_QUICK_REFERENCE.md) | **START HERE** - Quick commands for common tasks | 5 min |
| [PHASE1_SETUP_COMPLETE.md](PHASE1_SETUP_COMPLETE.md) | Complete infrastructure overview and next steps | 10 min |
| [AGENT_DESIGN.md](AGENT_DESIGN.md) | Architecture & design specifications (frozen) | 30 min |
| [PRE_COMMIT_SETUP.md](PRE_COMMIT_SETUP.md) | Pre-commit hooks setup and usage guide | 5 min |
| [../ARCHITECTURE.md](ARCHITECTURE.md) | High-level system architecture | 10 min |

---

## 🔧 Setup Files (Configure Once)

| File | Purpose | Action |
|------|---------|--------|
| [../.github/SECRETS_SETUP.md](../.github/SECRETS_SETUP.md) | GitHub secrets configuration | **Add secrets to GitHub** |
| [../TheHunter/backend/tests/conftest.py](../TheHunter/backend/tests/conftest.py) | pytest fixtures (auto-loaded) | ✅ Ready to use |
| [../TheHunter/backend/migrations/001_init.sql](../TheHunter/backend/migrations/001_init.sql) | Database schema | ✅ Auto-runs in CI/CD |
| [../.pre-commit-config.yaml](../.pre-commit-config.yaml) | Pre-commit hooks | `pip install pre-commit && pre-commit install` |

---

## 🧪 Test Files (Development Reference)

| File | Purpose | Run Command |
|------|---------|------------|
| [../TheHunter/backend/tests/test_recipe_executor.py](../TheHunter/backend/tests/test_recipe_executor.py) | 20+ unit tests | `pytest tests/ -v` |

Available Fixtures:
- `ai_component` - AI scoring (Discovery, Intelligence)
- `action_component` - Data fetching (Scraping)
- `correspondence_component` - Message generation (Personalization)
- `state_manager` - Context storage
- `audit_logger` - Compliance logging
- `subscription_component` - Credit management

See [PHASE1_QUICK_REFERENCE.md](PHASE1_QUICK_REFERENCE.md#-writing-tests) for test examples.

---

## 🚀 Getting Started (Step by Step)

### First Time Setup (5 minutes)

```bash
# 1. Install dependencies
cd TheHunter/backend
pip install -r requirements.txt

# 2. Install pre-commit hooks
pip install pre-commit
cd /workspaces/yashus
pre-commit install

# 3. Setup local database
createdb yashus
psql postgresql://localhost/yashus < TheHunter/backend/migrations/001_init.sql

# 4. Run tests to verify setup
cd TheHunter/backend
pytest tests/ -v
```

Expected: All tests pass ✅

### Daily Development Workflow

```bash
# 1. Make code changes
vim app/main.py

# 2. Run pre-commit hooks (automatic on commit)
git add .
git commit -m "Add feature X"

# 3. Push to GitHub (triggers CI/CD)
git push origin develop

# 4. Monitor deployment
# Go to GitHub Actions and watch pipeline run
```

---

## 📋 Key Components

### Phase 1 Framework Structure

```
TheHunter/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app (to be built)
│   │   ├── models.py            # Database models (to be built)
│   │   ├── routes.py            # API routes (to be built)
│   │   └── services.py          # Business logic (to be built)
│   ├── tests/
│   │   ├── conftest.py          # ✅ Pytest fixtures (ready)
│   │   └── test_recipe_executor.py  # ✅ Unit tests (ready)
│   └── migrations/
│       └── 001_init.sql         # ✅ Database schema (ready)
└── frontend/
    └── src/
        └── app/                 # Angular app (to be built)
```

### Database Tables

| Table | Purpose | Status |
|-------|---------|--------|
| `customers` | Multi-tenancy foundation | ✅ Schema ready |
| `agents` | The Hunter, Enricher, Messenger | ✅ Schema ready |
| `recipes` | Discovery, Intelligence, Personalization, etc. | ✅ Schema ready |
| `executions` | Execution history & debugging | ✅ Schema ready |
| `audit_logs` | Immutable compliance trail | ✅ Schema ready |
| `subscriptions` | Customer subscription state | ✅ Schema ready |
| `credit_transactions` | Billing audit trail | ✅ Schema ready |

---

## 🔍 CI/CD Pipeline

### Automatic Pipeline (on push to develop)

```
1. detect-changes    (identify changed services)
2. test-backend      (pytest)
3. test-frontend     (npm test)
4. build-push        (Docker build & push)
5. deploy            (Azure Container Instances)
6. migrate-database  (Run 001_init.sql) ✅ NEW
7. smoke-tests       (Post-deployment validation) ✅ NEW
```

View logs: https://github.com/dlai-sd/yashus/actions

### Local Testing Before Push

```bash
# Run tests locally
cd TheHunter/backend
pytest tests/ -v

# Check code quality
pre-commit run --all-files

# Test database migration
createdb test_yashus
psql postgresql://localhost/test_yashus < migrations/001_init.sql
dropdb test_yashus
```

---

## 📊 Testing Strategy

### Component Tests

Test individual components in isolation using fixtures:

```python
@pytest.mark.component
async def test_ai_component_scoring(ai_component):
    result = await ai_component.execute({"lead_data": {...}})
    assert 0.0 <= result["score"] <= 1.0
```

### Recipe Tests

Test recipe execution and response schemas:

```python
@pytest.mark.recipe
def test_recipe_response_schema(recipe_success_response):
    assert recipe_success_response["status"] == "success"
    assert "metadata" in recipe_success_response
```

### Integration Tests

Test multi-component interactions (Phase 2+):

```python
@pytest.mark.integration
async def test_full_hunter_workflow():
    # Discovery → Intelligence → Personalization
    pass
```

### Multi-tenancy Tests

Verify customer data isolation:

```python
@pytest.mark.recipe
async def test_customer_isolation(state_manager):
    await state_manager.set_state("cust-001", "pref", {"theme": "dark"})
    await state_manager.set_state("cust-002", "pref", {"theme": "light"})
    pref1 = await state_manager.get_state("cust-001", "pref")
    assert pref1["theme"] == "dark"
```

---

## 🔐 Security Checklist

- [ ] GitHub Secrets configured (6 minimum)
- [ ] SECRET_KEY is strong (50+ random chars)
- [ ] JWT_SECRET_KEY set (can reuse SECRET_KEY)
- [ ] No hardcoded API keys in code
- [ ] Pre-commit hooks installed (catches secrets)
- [ ] Database password in secrets, not code
- [ ] HTTPS enforced in production
- [ ] CORS properly configured

See [../.github/SECRETS_SETUP.md](../.github/SECRETS_SETUP.md) for full security guide.

---

## 🆘 Troubleshooting

### Tests Fail: "fixture not found"

```bash
cd TheHunter/backend
python -m pytest tests/conftest.py --collect-only
# Should show conftest fixtures
```

### Pre-commit Fails

```bash
# See what failed
pre-commit run --all-files --verbose

# Fix and retry
git add .
git commit -m "Fix linting issues"
```

### Database Connection Error

```bash
# Check PostgreSQL running
psql postgresql://localhost/yashus -c "SELECT 1"

# Reinitialize if corrupted
dropdb yashus
createdb yashus
psql postgresql://localhost/yashus < migrations/001_init.sql
```

### Deployment Fails

1. Check GitHub Actions logs: https://github.com/dlai-sd/yashus/actions
2. Verify GitHub Secrets set: GitHub → Settings → Secrets
3. Check Azure credentials valid: `az account show`

---

## 📚 Reference Links

### Official Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Angular Documentation](https://angular.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Azure Documentation](https://learn.microsoft.com/azure/)

### Internal Documentation
- [AGENT_DESIGN.md](AGENT_DESIGN.md) - Architecture specifications
- [ARCHITECTURE.md](ARCHITECTURE.md) - System overview
- [../.github/SECRETS_SETUP.md](../.github/SECRETS_SETUP.md) - Secrets guide

---

## 🎯 What's Next

### Now (Phase 1)
- ✅ Infrastructure setup complete
- ✅ Database schema ready
- ✅ Test fixtures available
- ⏳ Build core framework (Recipe executor, Components)

### Phase 2
- [ ] The Hunter recipes (Discovery, Intelligence, Personalization)
- [ ] AI integration (Groq, OpenAI)
- [ ] Subscription & credits

### Phase 3
- [ ] Admin dashboard
- [ ] Advanced alerts
- [ ] Customer dashboard

---

## 💬 Questions?

Refer to:
1. **Quick answers:** [PHASE1_QUICK_REFERENCE.md](PHASE1_QUICK_REFERENCE.md)
2. **Setup help:** [PHASE1_SETUP_COMPLETE.md](PHASE1_SETUP_COMPLETE.md)
3. **Design questions:** [AGENT_DESIGN.md](AGENT_DESIGN.md)
4. **Pre-commit help:** [PRE_COMMIT_SETUP.md](PRE_COMMIT_SETUP.md)

---

**Start here:** [PHASE1_QUICK_REFERENCE.md](PHASE1_QUICK_REFERENCE.md)
