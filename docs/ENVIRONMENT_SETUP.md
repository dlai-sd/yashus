# Environment Setup & Configuration Guide

**Last Updated:** December 14, 2025  
**Status:** Complete

---

## Quick Start

```bash
# 1. Copy example file
cp common/.env.example TheHunter/backend/.env

# 2. Get Groq API key (follow below)
# Add to .env: GROQ_API_KEY=gsk_your_key_here

# 3. Start the application
bash common/scripts/setup-local.sh

# 4. Application runs at:
# Frontend: http://localhost:4200
# Backend API: http://localhost:8000
```

---

## Environment Variables

### Database Configuration

**PostgreSQL Connection String**

```env
DATABASE_URL=postgresql://hunter:hunter_password@localhost:5432/hunter_db
```

| Component | Value | Notes |
|-----------|-------|-------|
| User | `hunter` | PostgreSQL user |
| Password | `hunter_password` | For local dev (change in production!) |
| Host | `localhost` | Docker service name when in Docker |
| Port | `5432` | Default PostgreSQL port |
| Database | `hunter_db` | Database name |

**Testing:**
```bash
# Verify connection
psql postgresql://hunter:hunter_password@localhost:5432/hunter_db -c "SELECT 1"
# Should return: ?column? = 1
```

### Groq API Configuration

**Required for AI-powered lead search**

```env
GROQ_API_KEY=gsk_your_api_key_here
```

**Getting Your API Key:**

1. Go to https://console.groq.com
2. Click "Sign Up" (or "Log In" if existing user)
3. Fill in details and verify email
4. In dashboard, click "API Keys" (left sidebar)
5. Click "Create New API Key"
6. Copy the key (format: `gsk_xxxxxxxxxxxx`)
7. Add to `.env` file

**Verify Key Works:**
```bash
cd TheHunter/backend
python3 << 'EOF'
from groq import Groq
import os

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ GROQ_API_KEY not set in .env")
    exit(1)

client = Groq(api_key=api_key)
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say 'Test successful'"}],
    max_tokens=20
)
print("✅ API Key is valid!")
print("Response:", response.choices[0].message.content)
EOF
```

**Free Tier Limits:**
- Requests per minute: 30
- Tokens per minute: 6,000
- Sufficient for development and testing

**Pricing (if exceeding free tier):**
- Pay-as-you-go: $0.0008 per 1K input tokens
- Estimated cost per lead search: $0.0004-$0.0008
- Annual estimate (50 searches/day): ~$9/year

### Google Custom Search (Optional)

**For real web search results (advanced feature)**

```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_cx_id_here
```

**Setup (only if you want web search integration):**

1. **Create Custom Search Engine**
   - Go to https://cse.google.com/cse/create/new
   - Select "Search the entire web"
   - Give it a name (e.g., "Hunter Lead Search")
   - Click "Create"
   - Copy the CX (Search Engine ID)

2. **Get API Key**
   - Go to https://console.developers.google.com
   - Create new project
   - Enable "Custom Search API"
   - Go to "Credentials"
   - Create "API Key"
   - Copy the key

3. **Add to .env**
   ```env
   GOOGLE_API_KEY=AIzaSy...
   GOOGLE_SEARCH_ENGINE_ID=12345:abcde...
   ```

**Pricing:**
- Free: 100 queries/day
- Paid: $5 per 1000 queries after free quota

**Note:** System uses Groq AI by default. Google Search is backup/alternative.

### Application Configuration

**Debug Mode**
```env
DEBUG=false
```
- `false`: Production mode (no stack traces in responses)
- `true`: Development mode (detailed error messages)

**Authentication**
```env
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
```
- `SECRET_KEY`: Used for JWT token signing (change in production!)
- `ALGORITHM`: JWT signing algorithm (keep as HS256)

**CORS Configuration**
```env
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:3000
```
- List of domains allowed to access API
- Comma-separated for multiple origins
- Prevents cross-origin request attacks

### Feature Flags (Optional)

```env
# Disable fallback to mock data (force real API or fail)
DISABLE_MOCK_FALLBACK=false

# Set Groq model variant
GROQ_MODEL=llama-3.3-70b-versatile

# Set API timeout
API_TIMEOUT_SECONDS=30
```

---

## File Structure

### Where Configuration Lives

```
TheHunter/
├── backend/
│   ├── .env                    ← ENVIRONMENT VARIABLES HERE
│   ├── app/
│   │   ├── main.py             ← Loads from .env
│   │   ├── config.py           ← Reads environment
│   │   ├── components.py       ← Uses GROQ_API_KEY
│   │   └── ml/
│   │       └── feature_extractor.py  ← ML model setup
│   └── requirements.txt         ← Python dependencies
│
├── .env.example                ← TEMPLATE (don't use directly)
│
└── docker-compose.yml          ← Can override with .env
```

### Configuration Priority

```
1. Environment Variables (.env file) ← HIGHEST PRIORITY
2. .env.example file
3. Hardcoded defaults in code ← LOWEST PRIORITY
```

---

## Setup Instructions

### Method 1: Docker Compose (Recommended)

**Automatic setup with one command:**

```bash
cd /workspaces/yashus
bash common/scripts/setup-local.sh
```

**What it does:**
1. Creates `.env` file if missing
2. Starts PostgreSQL database
3. Starts FastAPI backend
4. Starts Angular frontend
5. Initializes database tables
6. Trains ML model
7. Runs health checks

**Verify Success:**
```bash
# All should show "healthy"
docker-compose -f TheHunter/docker-compose.yml ps

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Method 2: Manual Setup

**For development or customization:**

```bash
# 1. Navigate to backend
cd TheHunter/backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cat > .env << 'EOF'
DATABASE_URL=postgresql://hunter:hunter_password@localhost:5432/hunter_db
GROQ_API_KEY=gsk_your_key_here
DEBUG=false
SECRET_KEY=test-secret-key
ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:4200
EOF

# 5. Start backend
python3 -m uvicorn app.main:app --reload

# In another terminal:

# 6. Setup frontend
cd ../frontend
npm install
ng serve

# Access at:
# Frontend: http://localhost:4200
# API: http://localhost:8000
```

### Method 3: Environment File Template

**Use this to create your own `.env`:**

```env
# ============================================================================
# DATABASE
# ============================================================================
DATABASE_URL=postgresql://hunter:hunter_password@localhost:5432/hunter_db

# ============================================================================
# GROQ API (Required for AI-powered search)
# ============================================================================
# Get from: https://console.groq.com
GROQ_API_KEY=gsk_your_api_key_here

# ============================================================================
# GOOGLE CUSTOM SEARCH (Optional - for web search fallback)
# ============================================================================
# Get from: https://cse.google.com and https://console.developers.google.com
# GOOGLE_API_KEY=optional
# GOOGLE_SEARCH_ENGINE_ID=optional

# ============================================================================
# APPLICATION
# ============================================================================
DEBUG=false
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:3000

# ============================================================================
# FEATURES (Optional)
# ============================================================================
DISABLE_MOCK_FALLBACK=false
GROQ_MODEL=llama-3.3-70b-versatile
API_TIMEOUT_SECONDS=30
```

---

## Validation Checklist

### After Setup, Verify:

```bash
# ✅ 1. Database connected
curl http://localhost:8000/docs -o /dev/null && echo "✅ API running"

# ✅ 2. Groq API key working
docker-compose logs backend | grep "GROQ" | head -5

# ✅ 3. Frontend loaded
curl http://localhost:4200 -o /dev/null && echo "✅ Frontend running"

# ✅ 4. ML model trained
docker-compose logs backend | grep "Model\|trained"

# ✅ 5. Can make API call
curl -X GET http://localhost:8000/api/v1/recipes

# ✅ 6. PostgreSQL accessible
psql $DATABASE_URL -c "SELECT 1"
```

---

## Troubleshooting

### Problem: "GROQ_API_KEY not found"

**Check 1: File exists and readable**
```bash
ls -la TheHunter/backend/.env
# Should show: -rw-r--r-- ... .env
```

**Check 2: Key is set**
```bash
grep GROQ_API_KEY TheHunter/backend/.env
# Should print: GROQ_API_KEY=gsk_xxxxxxxxx
# Not: GROQ_API_KEY=
# Not: GROQ_API_KEY=gsk_xxx (placeholder)
```

**Check 3: Backend reloaded**
```bash
# Restart backend to load new .env
docker-compose -f TheHunter/docker-compose.yml restart backend
# Wait 5 seconds
docker-compose logs backend | head -20
```

### Problem: "DATABASE_URL connection refused"

**Check 1: PostgreSQL running**
```bash
docker-compose -f TheHunter/docker-compose.yml ps db
# Should show "Up"
```

**Check 2: Credentials correct**
```bash
docker-compose -f TheHunter/docker-compose.yml exec db \
  psql -U hunter -d hunter_db -c "SELECT 1"
# If works: Shows "1"
```

**Check 3: Tables exist**
```bash
docker-compose -f TheHunter/docker-compose.yml exec db \
  psql -U hunter -d hunter_db -c "\dt"
# Should list: customers, agents, recipes, lead_feedback, etc.
```

### Problem: "Invalid API Key"

**Check 1: Key format**
```bash
grep GROQ_API_KEY TheHunter/backend/.env
# Must start with: gsk_
# Example: gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (redacted)
```

**Check 2: Key is active**
- Go to https://console.groq.com/keys
- Check that key shows "Active" status
- Check that you have remaining API quota

**Check 3: Test key directly**
```bash
python3 << 'EOF'
from groq import Groq

api_key = input("Enter your Groq API key: ")
client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "test"}],
        max_tokens=10
    )
    print("✅ Key is valid!")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### Problem: "Port already in use"

**For port 4200 (frontend):**
```bash
lsof -i :4200
kill -9 <PID>  # Kill the process using port
docker-compose -f TheHunter/docker-compose.yml up frontend
```

**For port 8000 (backend):**
```bash
lsof -i :8000
kill -9 <PID>
docker-compose -f TheHunter/docker-compose.yml up backend
```

**For port 5432 (PostgreSQL):**
```bash
lsof -i :5432
kill -9 <PID>
docker-compose -f TheHunter/docker-compose.yml up db
```

### Problem: "Module not found" or "Import Error"

**Solution:**
```bash
# Reinstall dependencies
cd TheHunter/backend
pip install --upgrade -r requirements.txt

# Or if using Docker:
docker-compose -f TheHunter/docker-compose.yml build --no-cache backend
docker-compose -f TheHunter/docker-compose.yml up backend
```

---

## Production Deployment

### Change for Production

**Never use development settings in production!**

```env
# ❌ Development
DEBUG=true
SECRET_KEY=dev-secret

# ✅ Production
DEBUG=false
SECRET_KEY=<generate-strong-random-key>
```

**Generate Strong Secret Key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: abc123def456ghi789jkl012mno345pqr678stu901vwx
```

**Update ALLOWED_ORIGINS:**
```env
# Development
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:3000

# Production
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

**Use Managed Database:**
```env
# Local (dev)
DATABASE_URL=postgresql://hunter:hunter_password@localhost:5432/hunter_db

# Production (Azure PostgreSQL)
DATABASE_URL=postgresql://user:password@servername.postgres.database.azure.com:5432/hunter_db?sslmode=require
```

---

## Advanced Configuration

### Custom ML Model Path

```env
ML_MODEL_PATH=/custom/path/to/model.pkl
```

### Custom Groq Model

```env
GROQ_MODEL=llama-3.1-405b-reasoning  # Different model
```

### API Rate Limiting

```env
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600  # Per hour
```

### Logging Configuration

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=/var/log/hunter/api.log
```

---

## Verification Checklist

- [ ] `.env` file created in `TheHunter/backend/`
- [ ] `GROQ_API_KEY` set with valid key (format: `gsk_...`)
- [ ] `DATABASE_URL` points to PostgreSQL
- [ ] All required variables set
- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:4200
- [ ] Can execute search query without mock data
- [ ] API responses show `"source": "ai_search"`
- [ ] Backend logs show no "API Error" messages

---

## Next Steps

1. ✅ Create `.env` file with all variables
2. ✅ Get Groq API key from console.groq.com
3. ✅ Run `bash common/scripts/setup-local.sh`
4. ✅ Test search at http://localhost:4200
5. ✅ Verify results are real, not mock (check `source` field)

**Having issues?** Check the [Troubleshooting](#troubleshooting) section or review backend logs:
```bash
docker-compose logs -f backend
```
