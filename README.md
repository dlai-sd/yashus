# Yashus: AI Command Center
**Digital Marketing Agents for Yashus.in**

![Yashus Digital Marketing](yd.png)

---

## Quick Links

**New here?** Start with one of these:
- 🧮 **[See Calculator Running](https://github.com/dlai-sd/yashus)** - Click Codespace button to test
- 📖 **[Local Setup (5 min)](docs/QUICKSTART.md)** - Run locally on your machine  
- ☁️ **[Deploy to Azure](docs/AZURE_DEPLOYMENT_GUIDE.md)** - Live on the internet
- 🏗️ **[Full Architecture](docs/PROJECT_STRUCTURE.md)** - How it all fits together

---

## Business Vision

### **Transform Outbound Sales Into An Autonomous Revenue Engine**

Yashus is building a next-generation AI command center that replaces the traditional, inconsistent, and expensive approach to sales outreach. Rather than "renting" expensive databases (Apollo/ZoomInfo) and hiring humans to perform repetitive copy-paste tasks, we are shifting to owning proprietary digital assets that work 24/7. Our flagship agent, **"The Hunter,"** is an autonomous Python-based intelligence system that continuously scrapes fresh local leads, enriches them with contextual insights, and drafts hyper-personalized outreach messages—all for less than $10/month operational cost. This vision transforms Yashus from a service agency into a technology company with defensible, scalable IP.

### **Solving Three Critical Business Problems**

The agency industry suffers from a "feast or famine" cycle where sales teams cannot simultaneously hunt for leads and close deals, creating unpredictable cash flow and revenue dips every 60 days. Worse, most cold outreach is generic spam—"Hello Sir/Madam"—that achieves <10% open rates and damages domain reputation. Finally, data costs are prohibitive: enterprise tools charge $50-100 per user per month (₹1 Lakh/year for Indian SMEs) just for contact information before closing a single deal. **The Hunter** eliminates all three: it runs consistently 365 days/year, personalizes each message in 30 seconds (vs. 15 minutes manually), and sources fresh data for free using proprietary scraping technology. The result is lower Customer Acquisition Cost (CAC), predictable pipeline, and qualified prospects that sales teams actually want to engage.

### **The Architecture: Modular Intelligence With Human Control**

The Hunter operates as four integrated modules: (1) **The Scraper** uses Playwright to autonomously discover businesses on Google Maps based on niche keywords, extracting names, ratings, addresses, phone numbers, and websites; (2) **The Enricher** crawls homepages and contact pages to find emails and contextual "hooks" (e.g., "last blog update was 3 weeks ago"); (3) **The Brain** leverages cost-effective LLMs (DeepSeek/Groq) to generate personalized sales drafts under 75 words that reference specific website content—never clichés; (4) **The Output Engine** saves everything to SQLite (preventing duplicate scraping) and exports daily CSVs for human review. Critically, no message is sent automatically; the sales team reviews and approves every draft. This hybrid approach—autonomous discovery + human judgment—eliminates both the slowness of manual prospecting and the risk of AI hallucinations.

### **A Scalable Advantage That Adds Company Valuation**

Unlike traditional agencies that compete on labor costs, Yashus is building proprietary intellectual property—a lead-generation asset that improves with every iteration. The Hunter is positioned not as a script but as a strategic asset that can be white-labeled, licensed, or integrated into future product lines. With deployment costs under $11/month and the ability to generate 50+ qualified leads per day across any niche (Gyms, Dentists, Architects, E-commerce brands), the system creates sustainable margin expansion. Most importantly, The Hunter ensures the top of the sales funnel is never empty—regardless of team holidays, staff attrition, or motivation levels. This is the difference between owning a revenue engine and renting temporary capacity.

---

## Getting Started

### Option 1: Codespace (Fastest - No Setup)
Click the Codespace button in GitHub. Calculator runs at port 3000.

### Option 2: Local Development
```bash
git clone https://github.com/dlai-sd/yashus.git
cd yashus
bash common/scripts/setup-from-config.sh
# Opens at http://localhost:4200
```

### Option 3: Azure Deployment  
```bash
export AZURE_SUBSCRIPTION_ID='your-id'
export AZURE_TENANT_ID='your-tenant-id'
export AZURE_CLIENT_ID='your-client-id'
export AZURE_CLIENT_SECRET='your-secret'
bash azure/deploy-automated.sh
# Live on the internet in 3-5 minutes
```

---

## 📚 Documentation

All detailed documentation is available in the `docs/` folder:

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](docs/QUICKSTART.md) | Local development setup (5 min) |
| [AZURE_DEPLOYMENT_GUIDE.md](docs/AZURE_DEPLOYMENT_GUIDE.md) | Cloud deployment with automation |
| [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Codebase overview and file organization |
| [DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md) | Current features and roadmap |
| [INTEGRATION_SUMMARY.md](docs/INTEGRATION_SUMMARY.md) | Component integration details |

---

## 🚀 Config-Driven Infrastructure

The Hunter uses a configuration-driven approach with intelligent change detection:

- **Single Source of Truth**: `devconfig.yaml` defines all services, build configs, and deployments
- **Selective Image Promotion**: Only rebuilds and deploys services that have actual changes
- **Smart CI/CD Pipeline**: Manual triggers only, change detection, parallel builds where safe
- **Environment Support**: Local development, staging, and production configurations

### Technology Stack

**Frontend:**
- Angular 17
- TypeScript 5.2
- RxJS
- Responsive CSS

**Backend:**
- FastAPI (Python 3.11)
- SQLAlchemy 2.0
- PostgreSQL / SQLite
- Async/await

**Infrastructure:**
- Docker (multi-stage builds)
- Docker Compose (local)
- Azure Container Registry
- Azure Container Instances
- Azure PostgreSQL

**CI/CD:**
- GitHub Actions
- Change detection system
- Automated deployments
./common/scripts/setup-from-config.sh
```

This single command generates docker-compose, builds changed services, starts containers, and validates health checks.

---

## 🏗️ Technology Stack

- **Frontend**: Angular 17, TypeScript, RxJS, Nginx
- **Backend**: FastAPI, Python 3.11, SQLAlchemy, PostgreSQL
- **Infrastructure**: Docker, Docker Compose, GitHub Actions
- **Cloud**: Azure Container Registry, Azure App Service
- **Testing**: pytest, Jasmine/Karma, codecov
- **CI/CD**: GitHub Actions with manual workflow dispatch

---

## 📖 Key Features

✅ Config-driven infrastructure (all in `devconfig.yaml`)  
✅ Intelligent change detection (only promote changed images)  
✅ Complete boilerplate with working calculator MVP  
✅ Full-stack testing (backend + frontend)  
✅ Production-ready Docker setup  
✅ Azure deployment automation  
✅ Health checks and monitoring  
✅ Development and production environments  

---

## 🎯 Next Steps

1. Read [Quick Start Guide](docs/QUICKSTART.md) to run locally
2. Explore `devconfig.yaml` to understand the configuration
3. Check [Azure Deployment](docs/AZURE_DEPLOYMENT.md) for cloud setup
4. Review [Development Status](docs/DEVELOPMENT_STATUS.md) for roadmap

---

**Built by Yashus. Powered by AI. Owned by You.** 🚀
