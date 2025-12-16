## Quick Start Guide

**⏱️ Time to running system: 5 minutes**

### What You'll Get

- ✅ AI-powered lead search (using Groq API)
- ✅ Machine learning scoring (predicts conversion probability)
- ✅ Real-time dashboard (Angular frontend)
- ✅ REST API (FastAPI backend)
- ✅ PostgreSQL database
- ✅ Fully containerized with Docker

### Prerequisites

```bash
# Check you have these installed
docker --version      # Docker 24+
docker-compose --version  # Docker Compose 2+
node --version        # Node 18+ (optional, for frontend dev)
python3 --version     # Python 3.11+ (optional, for backend dev)
```

**Don't have Docker?**
- Mac: https://www.docker.com/products/docker-desktop
- Windows: https://www.docker.com/products/docker-desktop
- Linux: `sudo apt-get install docker.io docker-compose`

### Get Groq API Key (2 minutes)

The system uses **Groq LLM** to generate realistic leads from search queries.

1. Go to https://console.groq.com
2. Click "Sign Up" (if new user)
3. Verify email
4. Click "API Keys" in left menu
5. Click "Create New API Key"
6. Copy the key (format: `gsk_xxxxxxxxxxxxxxxx`)

**Save this key - you'll need it next!**

### Setup & Start (3 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/dlai-sd/yashus.git
cd yashus

# 2. Create .env file with your Groq API key
cat > TheHunter/backend/.env << 'EOF'
DATABASE_URL=postgresql://hunter:hunter_password@localhost:5432/hunter_db
GROQ_API_KEY=gsk_your_api_key_here_replace_this
DEBUG=false
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:4200
EOF

# 3. Run setup script (builds images, starts containers)
bash common/scripts/setup-local.sh

# 4. Wait for containers to start (about 30-60 seconds)
# You'll see: "✅ All services healthy!"
```

**That's it! Your system is running!**

### Access The Application

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:4200 | The Hunter dashboard |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **API** | http://localhost:8000 | Backend API |

### Test The System

**Option 1: Use the Web Interface**

1. Open http://localhost:4200 in your browser
2. Go to "Recipe Executor" section
3. Enter search query: `"Dentist doctor in viman nagar Pune India"`
4. Click "Execute"
5. Watch real leads appear with ML predictions:
   - ✅ Rahul Sharma at Smile Care Dental Clinic
   - ✅ Aisha Khan at Dental Hub
   - ✅ 3 more dentists with conversion probability predictions

**Expected Results:**
- Leads show `"source": "ai_search"` (not mock data) ✅
- Each lead has conversion probability (44-48%)
- Confidence scores and risk levels calculated
- Full contact details visible

**Option 2: Use the API**

```bash
# Get your customer ID from database
CUSTOMER_ID=$(docker-compose -f TheHunter/docker-compose.yml exec db \
  psql -U hunter -d hunter_db -t -c "SELECT id FROM customers LIMIT 1")

AGENT_ID=$(docker-compose -f TheHunter/docker-compose.yml exec db \
  psql -U hunter -d hunter_db -t -c "SELECT id FROM agents LIMIT 1")

# Make API call
curl -X POST http://localhost:8000/api/v1/recipes/execute \
  -H "Content-Type: application/json" \
  -d "{
    \"customer_id\": \"$CUSTOMER_ID\",
    \"agent_id\": \"$AGENT_ID\",
    \"recipe_id\": \"discovery\",
    \"input_data\": {
      \"search_query\": \"Dentist doctor in viman nagar Pune India\",
      \"limit\": 5
    }
  }"

# You'll get back 5 dentist leads with ML scores
```

### Common Commands

**View Logs:**
```bash
# All services
docker-compose -f TheHunter/docker-compose.yml logs -f

# Just backend
docker-compose -f TheHunter/docker-compose.yml logs -f backend

# Just frontend
docker-compose -f TheHunter/docker-compose.yml logs -f frontend

# Search for errors
docker-compose logs backend | grep -i "error\|failed"
```

**Access Database:**
```bash
docker-compose -f TheHunter/docker-compose.yml exec db \
  psql -U hunter -d hunter_db

# In psql:
\dt              # List all tables
SELECT * FROM customers;  # View customers
SELECT * FROM lead_feedback;  # View training data
\q               # Exit
```

**Restart Services:**
```bash
# Restart everything
docker-compose -f TheHunter/docker-compose.yml down
docker-compose -f TheHunter/docker-compose.yml up

# Just restart backend (e.g., after code changes)
docker-compose -f TheHunter/docker-compose.yml restart backend
```

**Stop Services:**
```bash
# Stop without deleting data
docker-compose -f TheHunter/docker-compose.yml stop

# Stop and delete everything (keeps data in volumes)
docker-compose -f TheHunter/docker-compose.yml down

# Stop and delete EVERYTHING including data
docker-compose -f TheHunter/docker-compose.yml down -v
```

### Project Structure

```
yashus/
├── TheHunter/                           # Main application
│   ├── backend/                         # FastAPI (Python)
│   │   ├── app/
│   │   │   ├── main.py                 # FastAPI app
│   │   │   ├── components.py           # Recipe components (AI, Actions)
│   │   │   ├── executor.py             # Pipeline executor
│   │   │   ├── routes.py               # API endpoints
│   │   │   ├── database.py             # PostgreSQL setup
│   │   │   ├── models.py               # Data models
│   │   │   └── ml/
│   │   │       ├── trainer.py          # ML model training
│   │   │       └── feature_extractor.py  # Feature engineering
│   │   ├── scripts/
│   │   │   └── mock_leads.py           # Mock data for fallback
│   │   ├── .env                        # Environment variables
│   │   ├── Dockerfile                  # Container definition
│   │   └── requirements.txt            # Python dependencies
│   │
│   ├── frontend/                        # Angular 17 (TypeScript)
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── components/
│   │   │   │   │   └── recipe-executor/  # Search & results
│   │   │   │   ├── services/
│   │   │   │   │   └── calculator.service.ts  # API client
│   │   │   │   └── app.module.ts       # Main module
│   │   │   ├── main.ts
│   │   │   └── index.html
│   │   ├── Dockerfile                  # Container definition
│   │   ├── nginx.conf                  # Web server config
│   │   └── package.json                # Node dependencies
│   │
│   └── docker-compose.yml              # Orchestration
│
├── common/
│   ├── scripts/
│   │   ├── setup-local.sh              # ← RUN THIS!
│   │   ├── setup-from-config.sh        # Alternative setup
│   │   └── run-tests.sh                # Test runner
│   └── .env.example                    # Environment template
│
└── docs/
    ├── QUICKSTART.md                   # ← You are here
    ├── ML_AND_SEARCH_SYSTEM.md         # How AI search & ML scoring works
    ├── ENVIRONMENT_SETUP.md            # Configuration details
    ├── ARCHITECTURE.md                 # Complete system design
    └── ...
```

### File Descriptions

| File | Purpose |
|------|---------|
| `TheHunter/backend/.env` | **Environment variables (API keys, DB URL, etc.)** |
| `TheHunter/backend/app/components.py` | Recipe components: AI search expansion, lead discovery, dedup, ML scoring |
| `TheHunter/backend/app/executor.py` | Runs recipe pipeline (orchestrates 4 components) |
| `TheHunter/backend/app/ml/trainer.py` | Trains RandomForest model on lead_feedback data |
| `TheHunter/backend/scripts/mock_leads.py` | Mock data (used when Groq API fails) |
| `TheHunter/frontend/src/app/components/recipe-executor/` | Search input & results display |

### API Endpoints

**Execute Recipe (Main Endpoint)**
```
POST /api/v1/recipes/execute
Content-Type: application/json

{
  "customer_id": "uuid",
  "agent_id": "uuid",
  "recipe_id": "discovery",
  "input_data": {
    "search_query": "your search here",
    "limit": 5
  }
}

Returns: {
  "recipe_id": "discovery",
  "status": "success",
  "data": {
    "action_result": [
      {
        "name": "Rahul Sharma",
        "email": "rahul@smilecare.in",
        "source": "ai_search",
        "ml_score": {
          "conversion_probability": 0.44,
          "confidence_score": 12,
          "risk_level": "medium"
        }
      },
      ...
    ]
  },
  "metadata": {
    "duration_ms": 1850,
    "components_executed": 4
  }
}
```

**List Recipes**
```
GET /api/v1/recipes
```

**Get Execution History**
```
GET /api/v1/executions?agent_id=<uuid>&limit=10
```

**Interactive API Docs**
```
http://localhost:8000/docs  (Swagger UI)
http://localhost:8000/redoc (ReDoc)
```

### How It Works (Step by Step)

```
User enters: "Dentist doctor in viman nagar Pune India"
                            ↓
                 [Groq AI - Query Expansion]
                 Generates variations for better coverage
                            ↓
              [Groq AI - Lead Generation]
              Generates 5 realistic dentist leads with:
              - Names, emails, companies
              - Industry, location matching search
              - Engagement scores (0-100%)
                            ↓
                [Deduplication Component]
                Removes duplicate leads by email
                            ↓
              [ML Scoring Component]
              Loads RandomForest model, extracts 10 features:
              - Engagement score, industry match, seniority
              - Company size, location match, lead age
              - Quality score, feedback count, conversion rate
              - Recency score
              Predicts for each lead:
              - Conversion probability (44-48%)
              - Confidence score (0-100)
              - Risk level (Low/Medium/High)
                            ↓
          [Frontend Display - Real-time Dashboard]
          Shows all leads with conversion predictions
          ✅ Rahul Sharma (44% conversion, Medium risk)
          ✅ Aisha Khan (44% conversion, Medium risk)
          ✅ ...
```

### When Does It Use Mock Data?

The system **falls back to mock data** (pre-defined SaaS leads) only when:
- ❌ `GROQ_API_KEY` not set in `.env`
- ❌ API key is invalid/expired
- ❌ Network error or API timeout (>30 seconds)
- ❌ JSON parsing fails (bad API response)
- ❌ Rate limited or quota exceeded

**You'll know it's using mock data when:**
- Search results show SaaS companies (Sarah Chen, Marcus Johnson, etc.) instead of your query
- Response field shows `"source": "mock"` instead of `"ai_search"`
- Backend logs show: `[SEARCH] Falling back to mock leads`

**Solution:** Check `.env` for valid Groq API key and restart backend.

See [ML_AND_SEARCH_SYSTEM.md](ML_AND_SEARCH_SYSTEM.md) for detailed fallback logic.

### Troubleshooting

**Getting mock data instead of real leads?**
```bash
# 1. Check API key is set
grep GROQ_API_KEY TheHunter/backend/.env

# 2. Key must start with 'gsk_'
# If blank or 'gsk_xxx', set to your real key

# 3. Restart backend
docker-compose -f TheHunter/docker-compose.yml restart backend

# 4. Check logs
docker-compose logs backend | grep "AI SEARCH"
# Should show: [AI SEARCH] Generated 5 leads
# Not: [SEARCH] Falling back to mock leads
```

**Port already in use?**
```bash
# Find process using port 4200
lsof -i :4200
# Kill it
kill -9 <PID>
# Try again
docker-compose -f TheHunter/docker-compose.yml up
```

**Database connection error?**
```bash
# Restart database
docker-compose -f TheHunter/docker-compose.yml restart db
# Wait 10 seconds
# Restart backend
docker-compose -f TheHunter/docker-compose.yml restart backend
```

**Containers won't start?**
```bash
# Full reset
docker-compose -f TheHunter/docker-compose.yml down -v
# Run setup again
bash common/scripts/setup-local.sh
```

### Next Steps

1. ✅ System is running!
2. 📖 Read [ML_AND_SEARCH_SYSTEM.md](ML_AND_SEARCH_SYSTEM.md) to understand how it works
3. 🔧 Check [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for configuration options
4. 🏗️ Review [ARCHITECTURE.md](ARCHITECTURE.md) for complete system design
5. ☁️ Deploy to Azure using [AZURE_DEPLOYMENT_GUIDE.md](../AZURE_DEPLOYMENT_GUIDE.md)

### Support

**Check API Documentation:**
http://localhost:8000/docs

**View Backend Logs:**
```bash
docker-compose -f TheHunter/docker-compose.yml logs -f backend
```

**Reset Everything:**
```bash
docker-compose -f TheHunter/docker-compose.yml down -v
bash common/scripts/setup-local.sh
```

---

**Ready to hunt some leads? 🎯 Go to http://localhost:4200**

### Project Structure

```
yashus/
├── common/                              # Shared infrastructure
│   ├── .github/workflows/
│   │   └── deploy.yml                  # CI/CD pipeline (manual trigger)
│   ├── scripts/
│   │   ├── setup-local.sh              # Local setup script
│   │   └── run-tests.sh                # Test runner
│   ├── .env.example                     # Environment template
│   └── config/                          # Shared configuration
│
├── TheHunter/                           # Main application
│   ├── backend/                         # FastAPI application
│   │   ├── app/
│   │   │   ├── main.py                 # FastAPI app entry point
│   │   │   ├── config.py               # Configuration
│   │   │   ├── database.py             # Database setup
│   │   │   ├── models.py               # SQLAlchemy models
│   │   │   ├── schemas.py              # Pydantic schemas
│   │   │   ├── services.py             # Business logic
│   │   │   └── routes.py               # API routes
│   │   ├── tests/                      # Test suite
│   │   ├── Dockerfile                  # Backend container
│   │   └── requirements.txt            # Python dependencies
│   │
│   ├── frontend/                        # Angular application
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── app.module.ts
│   │   │   │   ├── app.component.ts
│   │   │   │   ├── components/
│   │   │   │   │   └── calculator/
│   │   │   │   └── services/
│   │   │   │       └── calculator.service.ts
│   │   │   ├── main.ts
│   │   │   ├── index.html
│   │   │   └── styles.css
│   │   ├── Dockerfile                  # Frontend container
│   │   ├── nginx.conf                  # Nginx configuration
│   │   └── package.json                # Node dependencies
│   │
│   └── docker-compose.yml              # Local orchestration
│
├── README.md                             # Project documentation
└── LICENSE
```

### Available Commands

**Development:**
```bash
# Start all services
docker-compose -f ./TheHunter/docker-compose.yml up

# Stop all services
docker-compose -f ./TheHunter/docker-compose.yml down

# View logs
docker-compose -f ./TheHunter/docker-compose.yml logs -f

# Access API shell
docker-compose -f ./TheHunter/docker-compose.yml exec api bash
```

**Testing:**
```bash
# Run all tests
./common/scripts/run-tests.sh

# Backend tests only
docker-compose -f ./TheHunter/docker-compose.yml exec api pytest tests/ -v

# Frontend tests only
docker-compose -f ./TheHunter/docker-compose.yml exec frontend npm test
```

**Database:**
```bash
# Access PostgreSQL
docker-compose -f ./TheHunter/docker-compose.yml exec db psql -U hunter -d hunter_db

# Reset database
docker-compose -f ./TheHunter/docker-compose.yml exec api alembic downgrade base
docker-compose -f ./TheHunter/docker-compose.yml exec api alembic upgrade head
```

### CI/CD Pipeline

The GitHub Actions workflow is **manually triggered only** (no auto-trigger on commit).

**To trigger deployment:**
1. Go to: Actions → Build & Deploy - Manual Trigger
2. Click "Run workflow"
3. Select environment: `staging` or `production`
4. Workflow executes: Test → Code Quality → Build → Deploy

**Secrets Required (GitHub Settings → Secrets and variables → Actions):**
- `AZURE_CREDENTIALS`: Azure service principal JSON
- `AZURE_REGISTRY_USERNAME`: Container registry username
- `AZURE_REGISTRY_PASSWORD`: Container registry password
- `AZURE_RESOURCE_GROUP`: Azure resource group name
- `STAGING_DATABASE_URL`: Staging database connection string
- `DEPLOYED_URL`: Deployed application URL for smoke tests

### API Endpoints

**Calculator:**
- `POST /api/v1/calculator/calculate` - Perform calculation
  ```json
  {
    "operation": "add|subtract|multiply|divide",
    "operand1": 10,
    "operand2": 5
  }
  ```
- `GET /api/v1/calculator/history` - Get calculation history
- `GET /api/v1/calculator/calculation/{id}` - Get specific calculation
- `GET /api/v1/calculator/health` - Health check

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Configuration

Create a `.env` file in the `common/` directory (template: `.env.example`):

```env
# Backend
DATABASE_URL=postgresql://hunter:hunter_password@db:5432/hunter_db
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:3000
DEBUG=true
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# Frontend
API_BASE_URL=http://localhost:8000
```

### Troubleshooting

**Port already in use:**
```bash
# Find and kill process using port
lsof -i :8000  # for API
lsof -i :4200  # for Frontend
lsof -i :5432  # for Database
kill -9 <PID>
```

**Database connection issues:**
```bash
# Verify database is healthy
docker-compose -f ./TheHunter/docker-compose.yml ps

# Check database logs
docker-compose -f ./TheHunter/docker-compose.yml logs db
```

**Clear everything and restart:**
```bash
docker-compose -f ./TheHunter/docker-compose.yml down -v
docker system prune -a
./common/scripts/setup-local.sh
```

### Next Steps

1. **Run the calculator** to verify full stack works
2. **Understand the test coverage** in `TheHunter/backend/tests/`
3. **Implement The Hunter modules**:
   - Scraper (Google Maps)
   - Enricher (Website crawling)
   - Brain (LLM integration)
   - Output (Database & exports)
4. **Deploy to Azure** using the manual trigger workflow

### Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Angular 17, Tailwind CSS, RxJS
- **Infrastructure**: Docker, Docker Compose, Azure
- **Testing**: pytest, Jasmine/Karma
- **CI/CD**: GitHub Actions, Azure Container Registry, Azure App Service

### Support

For issues or questions, check:
1. Logs: `docker-compose logs -f`
2. API Docs: http://localhost:8000/docs
3. GitHub Issues: [Project Board]

---

**Happy Hunting! 🎯**
