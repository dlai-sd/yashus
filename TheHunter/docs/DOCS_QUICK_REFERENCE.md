# Documentation Quick Reference Card

## �� All Documentation at a Glance

### START HERE: README.md
**What**: Project overview and quick links  
**Size**: 2500 words  
**Time**: 5 minutes  
**Read if**: You're new to the project  
**Contains**: Vision, quick start, architecture, tech stack, troubleshooting  
**Link**: [README.md](/README.md)

---

### SETUP: QUICKSTART.md
**What**: 5-minute setup guide  
**Size**: 1500 words  
**Time**: 5 minutes  
**Read if**: You want to run the system locally  
**Contains**: Prerequisites, Groq API setup, Docker commands, testing, troubleshooting  
**Link**: [QUICKSTART.md](docs/QUICKSTART.md)

---

### CONFIGURE: ENVIRONMENT_SETUP.md
**What**: Complete configuration reference  
**Size**: 2500 words  
**Time**: 10 minutes  
**Read if**: You need to configure environment variables  
**Contains**: All variables explained, Groq API setup (detailed), setup methods, validation, troubleshooting, production deployment  
**Link**: [ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md)

---

### DEEP DIVE: ML_AND_SEARCH_SYSTEM.md
**What**: How AI search & ML scoring works  
**Size**: 3500 words  
**Time**: 20 minutes  
**Read if**: You want to understand the technical details  
**Contains**: System overview, AI pipeline, ML model details, fallback logic, troubleshooting, performance metrics  
**Link**: [ML_AND_SEARCH_SYSTEM.md](docs/ML_AND_SEARCH_SYSTEM.md)

---

### STATUS: DEVELOPMENT_STATUS.md
**What**: Current state and roadmap  
**Size**: 2500 words  
**Time**: 15 minutes  
**Read if**: You want to know what's done and what's next  
**Contains**: What works, Phase 2 roadmap, metrics, verification checklist, next steps  
**Link**: [DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md)

---

### ARCHITECTURE: ARCHITECTURE.md
**What**: Complete system design  
**Size**: 2000+ words  
**Time**: 20 minutes  
**Read if**: You need to understand the full system architecture  
**Contains**: Data models, user flows, technical stack, authentication, multi-tenancy  
**Link**: [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🎯 Choose Your Path

### I'm a New User (20 min total)
```
1. README.md (2 min)
   ↓
2. QUICKSTART.md (5 min)
   ↓
3. ENVIRONMENT_SETUP.md (3 min) - Get Groq API key
   ↓
4. Test at http://localhost:4200 (5 min)
   ↓
5. ML_AND_SEARCH_SYSTEM.md (5 min) - Optional deep dive
```

### I'm a Developer (30 min total)
```
1. README.md (5 min)
   ↓
2. ARCHITECTURE.md (15 min)
   ↓
3. ML_AND_SEARCH_SYSTEM.md (10 min)
```

### I'm DevOps/Infrastructure (15 min total)
```
1. QUICKSTART.md (5 min)
   ↓
2. ENVIRONMENT_SETUP.md (10 min)
```

### I'm Product/Manager (15 min total)
```
1. README.md (5 min)
   ↓
2. DEVELOPMENT_STATUS.md (10 min)
```

---

## 🔍 Find Documentation By Topic

### Getting Started
- Groq API setup: [ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md) → "Get Groq API Key"
- Docker setup: [QUICKSTART.md](docs/QUICKSTART.md) → "Setup & Start"
- Environment variables: [ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md) → "Environment Variables"

### How It Works
- AI search pipeline: [ML_AND_SEARCH_SYSTEM.md](docs/ML_AND_SEARCH_SYSTEM.md) → "AI-Powered Search Pipeline"
- ML scoring model: [ML_AND_SEARCH_SYSTEM.md](docs/ML_AND_SEARCH_SYSTEM.md) → "ML Scoring Model"
- Recipe pipeline: [README.md](/README.md) → "System Architecture"

### Troubleshooting
- Getting mock data: [ML_AND_SEARCH_SYSTEM.md](docs/ML_AND_SEARCH_SYSTEM.md) → "Troubleshooting"
- Setup issues: [QUICKSTART.md](docs/QUICKSTART.md) → "Troubleshooting"
- Configuration issues: [ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md) → "Troubleshooting"

### Development/Architecture
- System design: [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- What's completed: [DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md)
- What's next: [DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md) → "Phase 2 Planned"

### API Reference
- API endpoints: [QUICKSTART.md](docs/QUICKSTART.md) → "API Endpoints"
- Interactive docs: http://localhost:8000/docs (after setup)

---

## ⚡ Quick Commands

```bash
# Get system running
bash common/scripts/setup-local.sh

# Check if running
docker-compose -f TheHunter/docker-compose.yml ps

# View logs
docker-compose -f TheHunter/docker-compose.yml logs -f backend

# Test API
curl http://localhost:8000/docs

# Test frontend
open http://localhost:4200
```

---

## 📋 Verification Checklist

After setup, verify:
- [ ] Frontend loads at http://localhost:4200
- [ ] API responds at http://localhost:8000/docs
- [ ] Can execute search (not getting mock data)
- [ ] Results show `"source": "ai_search"` (not `"mock"`)
- [ ] ML scores appear on leads

See [DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md) → "Verification Checklist" for detailed commands.

---

## 🆘 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Getting mock data | Check GROQ_API_KEY in .env is set and valid |
| Port in use | Kill process: `lsof -i :8000; kill -9 <PID>` |
| Database error | Restart db: `docker-compose restart db` |
| Module not found | Rebuild: `docker-compose build --no-cache` |
| Can't connect | Check Docker is running: `docker ps` |

See individual docs → "Troubleshooting" sections for more details.

---

## 📈 Key Statistics

- **10,000+ words** of documentation
- **6 documents** covering all aspects
- **30+ code examples**
- **15+ troubleshooting scenarios**
- **5+ diagrams/flowcharts**
- **3 setup methods**
- **12+ environment variables**

---

## 🔗 Document Links Map

```
README.md (You are here)
├─ QUICKSTART.md
├─ ENVIRONMENT_SETUP.md
├─ ML_AND_SEARCH_SYSTEM.md
├─ DEVELOPMENT_STATUS.md
└─ ARCHITECTURE.md
```

Each document links to related documents and sections for easy navigation.

---

## ✅ What Each Document Contains

| Document | Primary Audience | Key Content |
|----------|-----------------|-------------|
| **README.md** | Everyone | Overview, vision, quick links |
| **QUICKSTART.md** | New users, developers | Setup in 5 minutes |
| **ENVIRONMENT_SETUP.md** | DevOps, backend devs | All configuration variables |
| **ML_AND_SEARCH_SYSTEM.md** | Technical leads, ML engineers | How AI search & ML work |
| **DEVELOPMENT_STATUS.md** | Product, managers, leads | What's done, roadmap |
| **ARCHITECTURE.md** | Architects, tech leads | Complete system design |

---

## 🚀 Next Steps

1. **Read** → Start with README.md (5 min)
2. **Setup** → Follow QUICKSTART.md (5 min)
3. **Configure** → Get Groq API key from ENVIRONMENT_SETUP.md (3 min)
4. **Test** → Run system at http://localhost:4200 (5 min)
5. **Learn** → Deep dive with ML_AND_SEARCH_SYSTEM.md (20 min)

**Total: 38 minutes from zero to fully functional system!**

---

## 📞 Need Help?

- **Setup issues**: Check [QUICKSTART.md](docs/QUICKSTART.md) → Troubleshooting
- **Config issues**: Check [ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md) → Troubleshooting
- **ML/Search issues**: Check [ML_AND_SEARCH_SYSTEM.md](docs/ML_AND_SEARCH_SYSTEM.md) → Troubleshooting
- **Architecture questions**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

**Last Updated**: December 14, 2025  
**Status**: ✅ Complete and Current  
**Total Documentation**: 10,000+ words across 6 documents
