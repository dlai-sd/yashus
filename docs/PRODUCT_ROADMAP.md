# Yashus Product Roadmap & Quick Reference

**Last Updated:** December 14, 2025  
**Status:** Architecture Finalized, Development Ready

---

## 🎯 Product Overview

**Yashus Digital Agents** = SaaS platform providing AI agents that autonomously generate, enrich, and personalize B2B leads.

**Target Market:** Enterprises and SMEs across 9 industries (Healthcare, Real Estate, Hotels, Retail, Food, Education, IT, Finance, Manufacturing)

**Revenue Model:** Subscription-based (₹4,999/month entry price with usage-based credits)

---

## 📦 Current Applications

### **AgentsHome** ✅ Live
- **What:** Landing page & marketing site
- **Where:** `/workspaces/yashus/AgentsHome`
- **URL:** http://localhost:4200
- **Tech:** Angular 17 + SCSS
- **Status:** Complete and deployed

### **TheHunter** 🏗️ In Development
- **What:** Development & testing environment for The Hunter agent
- **Where:** `/workspaces/yashus/TheHunter`
- **Backend:** Python FastAPI (port 8000)
- **Frontend:** Angular 17 (port 4200)
- **Tech:** FastAPI + PostgreSQL + Angular
- **Status:** Core structure ready, needs 3 main UI components

### **CustomerDashboard** 🎯 NEXT PRIORITY
- **What:** Post-signup self-service dashboard for paying customers
- **Where:** `/workspaces/yashus/CustomerDashboard` (to create)
- **Components:**
  1. ✅ Configure Agent for Run
  2. ✅ Monitor Business Outcomes
  3. ✅ Subscription Consumption & Balance
- **Tech:** Same as others (Angular 17 + FastAPI)
- **Timeline:** Start immediately after Phase 2 backend

### **AdminDashboard** 📋 Phase 5
- **What:** Internal monitoring and analytics for admins
- **Where:** `/workspaces/yashus/AdminDashboard` (to create)
- **Components:** Agent metrics, customer analytics, revenue tracking
- **Tech:** Same stack
- **Timeline:** Q1 2025

---

## 🔐 Authentication & Access

```
┌─────────────────────────────────────────────┐
│ Customer Journey                            │
├─────────────────────────────────────────────┤
│ 1. Visit AgentsHome landing page            │
│ 2. Click "Free Trial" or "Subscribe"        │
│ 3. OAuth/Email signup + Payment             │
│ 4. JWT token issued (auto-login)            │
│ 5. Redirected to CustomerDashboard          │
│ 6. Fully self-service from here             │
│                                             │
│ Admin Access:                               │
│ - Same login flow                           │
│ - Role checked (admin vs customer)          │
│ - Redirected to AdminDashboard              │
└─────────────────────────────────────────────┘
```

**Key Details:**
- JWT tokens: 7-day expiration
- Refresh tokens: 30-day expiration
- Storage: httpOnly cookies + localStorage
- Scope: Single sign-on across all 3 apps

---

## 💾 Data Architecture

### **Multi-Tenant Isolation**
```sql
-- Every table has customer_id (or accessed through relationship)
CREATE TABLE agents (
    id PRIMARY KEY,
    customer_id NOT NULL,  -- ⭐ Tenant key
    agent_type,
    configuration
);

-- Query pattern (always filtered)
SELECT * FROM agents WHERE customer_id = :current_user_id;
```

### **Data Model (Simplified)**
```
Customer
├─ User (email, password, role)
├─ Subscription (plan, billing_date, status)
├─ Agents (one per agent type)
│  └─ Leads (results from agent runs)
│  └─ Usage_Logs (credit consumption)
└─ Payment_Methods
```

---

## 💳 Billing Model

**Plan Structure:**
- **Entry Plan:** ₹4,999/month
- **Professional Plan:** ₹4,999/month (current)
- **Enterprise Plan:** ₹9,999/month (future)

**Credits & Consumption:**
```
Example: ₹4,999/month plan = ~49,990 credits
- 1 lead scraped = ₹0.10
- 1 email enriched = ₹0.05
- 1 message personalized = ₹0.05

Monthly Usage = Credits Consumed / Total Credits
Display: [████████░░░░░░░░░░] 42% (42.50 / 99.99 credits used)
```

---

## 🚀 Development Phases

### **Phase 1: AgentsHome** ✅ COMPLETE
- Landing page live
- Product showcase with 9 industries
- Customer signup integration

### **Phase 2: Backend Core** 🔄 IN PROGRESS
- User authentication (JWT)
- API structure and routes
- Database schema
- Subscription management
- **Timeline:** 2-3 weeks

### **Phase 3: CustomerDashboard MVP** 🎯 NEXT
- Configure Agent component
- Monitor Outcomes dashboard
- Consumption tracking
- **Timeline:** 3-4 weeks after Phase 2

### **Phase 4: CustomerDashboard v2** 📋 PLANNED
- CSV/API exports
- CRM integrations (Salesforce, HubSpot)
- Advanced filtering
- **Timeline:** 2-3 weeks after MVP

### **Phase 5: AdminDashboard** 📊 PLANNED
- System overview & KPIs
- Agent performance metrics
- Customer analytics
- Revenue tracking
- **Timeline:** Q1 2025

---

## 📊 Key Components to Build

### **1. Configure Agent** (TheHunter & CustomerDashboard)
```
Inputs:
- Agent selection (Hunter, Enricher, Messenger)
- Keywords (multi-input)
- Location/Geography
- Business type filters
- Advanced settings (depth, tone, confidence)
- Schedule (one-time, daily, weekly)
- Config name (save as template)

Output:
- Save configuration to DB
- Option to "Run Now" or "Schedule"
```

### **2. Monitor Outcomes** (TheHunter & CustomerDashboard)
```
Display:
- Progress bar (0-100%)
- Live metrics (leads found, emails, messages)
- Quality score (average validity)
- Remaining credits
- Lead preview (first 3-5)
- Export options (CSV, CRM, email)

Updates:
- Real-time via WebSocket
- Refresh every 2-5 seconds
```

### **3. Consumption & Balance** (CustomerDashboard)
```
Current Usage:
- API calls (45,000 / 100,000)
- Credits (42.50 / 99.99)
- Leads generated (342)

Billing:
- Plan name & price
- Next billing date
- Payment method
- Upgrade option

History:
- Daily breakdown
- 7-day trend
- Cost per lead
```

---

## 🛠️ Tech Stack Reference

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Angular | 17.x |
| **Language** | TypeScript | 5.2+ |
| **Styling** | SCSS | - |
| **HTTP** | Angular HttpClient | 17.x |
| **State** | RxJS | 7.8+ |
| **Backend** | FastAPI | 0.104+ |
| **Language** | Python | 3.11+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Database** | PostgreSQL | 15+ |
| **Auth** | JWT + Passlib | - |
| **Containers** | Docker | Latest |
| **Orchestration** | Docker Compose | - |
| **Cloud** | Azure (App Service, Static Web Apps) | - |
| **Testing** | Jest (FE), pytest (BE) | - |

---

## 🔗 Important Links

**Documentation:**
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Complete design specification
- [ARCHITECTURAL_DECISIONS.md](docs/ARCHITECTURAL_DECISIONS.md) - All decisions & rationale
- [QUICKSTART.md](docs/QUICKSTART.md) - Local setup guide
- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - Folder organization

**Running Applications:**
- AgentsHome: `cd AgentsHome && npm start` → http://localhost:4200
- TheHunter: `docker-compose up` → Backend 8000, Frontend 4200

---

## ⚡ Quick Commands

### **Start AgentsHome**
```bash
cd /workspaces/yashus/AgentsHome
npm install  # (first time only)
npm start
# Opens at http://localhost:4200
```

### **Start TheHunter (Full Stack)**
```bash
cd /workspaces/yashus/TheHunter
docker-compose up
# Frontend at http://localhost:4200
# API at http://localhost:8000
```

### **Run Tests**
```bash
# Frontend tests
ng test

# Backend tests
pytest TheHunter/backend/tests/
```

---

## 🎯 Success Metrics

**For Customers:**
- Agent configuration < 5 minutes
- Lead generation 50+ per day
- Email validity > 90%
- Self-service without support tickets

**For Business:**
- Customer acquisition: 10+ per week
- Conversion rate: 40%+ (trial to paid)
- MRR growth: 15%+ month-over-month
- Customer lifetime value: > ₹50,000

---

## 📝 Decision Summary

| Area | Decision | Status |
|------|----------|--------|
| **Tech Stack** | Angular + FastAPI (unified) | ✅ Approved |
| **Authentication** | JWT + refresh tokens | ✅ Approved |
| **Multi-Tenancy** | Complete customer isolation | ✅ Approved |
| **Build Next** | CustomerDashboard | ✅ Approved |
| **Signup Flow** | AgentsHome → Payment → Dashboard | ✅ Approved |
| **Agent Execution** | Async + WebSocket updates | ✅ Approved |
| **Billing** | Credit system (monthly allocation) | ✅ Approved |
| **Admin Access** | View-only with audit logging | ✅ Approved |

---

## 🚀 Next Immediate Steps

1. **Backend Phase 2** (parallel with documentation review)
   - Create customer management API
   - Set up subscription table & logic
   - Implement agent orchestration framework

2. **Design CustomerDashboard**
   - Wireframes for 3 main components
   - API contract specifications
   - Component structure plan

3. **Setup CI/CD**
   - GitHub Actions workflow
   - Deployment automation
   - Testing pipeline

4. **Begin CustomerDashboard Development**
   - Start with "Configure Agent" component
   - Connect to backend APIs
   - Iterate with design

---

**Prepared by:** Engineering Team  
**Date:** December 14, 2025  
**Status:** Ready for development
