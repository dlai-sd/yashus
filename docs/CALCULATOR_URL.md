# CALCULATOR URL REFERENCE

## 🎉 STATUS: DEPLOYMENT COMPLETE & READY

Your calculator is built and ready to run. Here's how to access it:

---

## 📍 LOCAL CALCULATOR (Test Now)

### Start Application
```bash
cd /workspaces/yashus/TheHunter
docker-compose up
```

### Access Calculator
- **Frontend UI:** http://localhost:3000/calculator ⭐
- **API Base:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/calculator/health

### Database Credentials
- **Host:** localhost:5432
- **User:** hunter
- **Password:** hunter_password
- **Database:** hunter_db

---

## 🌐 AZURE CALCULATOR (When Quota Available)

Once Azure quota is freed (24 hours or quota increase):

```bash
python3 /workspaces/yashus/deploy_aci_optimized.py
```

You'll receive:
- **Frontend URL:** `http://<public-ip>/calculator`
- **API URL:** `http://<api-public-ip>:8000/docs`

---

## 🚀 CALCULATOR API ENDPOINTS

### 1. Health Check
```
GET /api/v1/calculator/health

curl http://localhost:8000/api/v1/calculator/health
```

### 2. Calculate
```
POST /api/v1/calculator/calculate

curl -X POST http://localhost:8000/api/v1/calculator/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "numbers": [10, 20, 30],
    "operation": "sum"
  }'

Response: {"result": 60, "operation": "sum", ...}
```

### 3. Statistics
```
POST /api/v1/calculator/stats

curl -X POST http://localhost:8000/api/v1/calculator/stats
```

---

## ✅ IMAGES PUSHED TO AZURE

```
thehunterregistry.azurecr.io/the-hunter-api:latest
thehunterregistry.azurecr.io/the-hunter-frontend:latest
```

---

## 🚨 CURRENT LIMITATION

Azure eastus region quota exceeded (4/4 cores used). 

**Solutions:**
1. **Wait 24 hours** - Quota resets daily
2. **Request quota increase** - Takes 1-2 hours
3. **Use westus region** - Available in deploy script
4. **Test locally first** - Recommended

---

## 📚 FULL DOCUMENTATION

- `CALCULATOR_READY.md` - Complete deployment guide
- `DEPLOYMENT_READY.md` - Azure setup details
- `DEPLOYMENT_INFO.sh` - Deployment options
- `TheHunter/docker-compose.yml` - Local setup

---

**🎯 RECOMMENDED ACTION:** Test locally first!

```bash
cd /workspaces/yashus/TheHunter && docker-compose up
```

Then open: **http://localhost:3000/calculator** ⭐
