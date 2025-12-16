# Yashus AI Agents - Complete Architecture & Product Flow

**Document Version:** 1.0  
**Last Updated:** December 14, 2025  
**Status:** Active Design Document

---

## Table of Contents
1. [Product Vision](#product-vision)
2. [System Architecture](#system-architecture)
3. [User Journey & Workflows](#user-journey--workflows)
4. [Technical Stack](#technical-stack)
5. [Authentication & Authorization](#authentication--authorization)
6. [Data Multi-tenancy](#data-multi-tenancy)
7. [Development Phases](#development-phases)
8. [Component Specifications](#component-specifications)

---

## Product Vision

**Yashus Digital Agents** is a SaaS platform that provides autonomous AI agents to generate, enrich, and personalize business leads for enterprises and SMEs across 9+ industries.

**Core Value Proposition:**
- Replace expensive manual prospecting with 24/7 autonomous agents
- Generate 50+ qualified leads monthly with personalized outreach
- Own proprietary lead-generation IP vs. renting from expensive databases
- 3 complementary agents: The Hunter (lead generation), The Enricher (data enrichment), The Messenger (personalized outreach)

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOMER ECOSYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │  AgentsHome      │      │ CustomerDashboard│                 │
│  │ (Marketing SPA)  │      │   (Post-Login)   │                 │
│  │                  │      │                  │                 │
│  │ - Product Page   │      │ - Configure Agent│                 │
│  │ - Pricing        │      │ - Monitor Results│                 │
│  │ - Agent Showcase │      │ - Usage Tracking │                 │
│  │ - Signup/Payment │      │ - Lead Exports   │                 │
│  │                  │      │                  │                 │
│  └────────┬─────────┘      └────────┬─────────┘                 │
│           │                         │                           │
│           └───────────┬─────────────┘                           │
│                       │                                         │
│                ┌──────▼──────────────────────┐                 │
│                │   BACKEND API SERVICE       │                 │
│                │  (FastAPI + PostgreSQL)     │                 │
│                │                             │                 │
│                │ - User Management (JWT)     │                 │
│                │ - Agent Orchestration       │                 │
│                │ - Lead Storage & Retrieval  │                 │
│                │ - Subscription & Billing    │                 │
│                │ - Usage Metering            │                 │
│                └──────┬──────────────────────┘                 │
│                       │                                         │
│        ┌──────────────┼──────────────────┐                     │
│        │              │                  │                     │
│        ▼              ▼                  ▼                      │
│  ┌──────────┐   ┌──────────┐       ┌──────────┐              │
│  │  Hunter  │   │ Enricher │       │Messenger │              │
│  │ (Scraper)│   │(Data AI) │       │(Composer)│              │
│  └──────────┘   └──────────┘       └──────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ADMIN ECOSYSTEM                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│              ┌─────────────────────────────────┐                │
│              │    AdminDashboard (v2)          │                │
│              │                                 │                │
│              │ - Agent Performance (All)       │                │
│              │ - Customer Usage Analytics      │                │
│              │ - System Health & Monitoring    │                │
│              │ - Revenue & Subscription Mgmt   │                │
│              └────────────┬────────────────────┘                │
│                           │                                     │
│                     (Shares API with Customers)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## User Journey & Workflows

### **1. Customer Acquisition Flow (via AgentsHome)**

```
1. Discovery
   ├─ Customer visits AgentsHome landing page
   ├─ Views 9 industries with use cases
   ├─ Reads agent capabilities (Hunter Live, Others Coming Soon)
   └─ Sees pricing: ₹4,999/month

2. Signup
   ├─ Click "Free Trial" or "Subscribe Now"
   ├─ OAuth/Email signup (JWT token issued)
   ├─ Payment processing (Razorpay/Stripe)
   └─ Account created in database

3. Onboarding
   ├─ Redirected to CustomerDashboard
   ├─ Guided setup wizard (optional)
   └─ Ready to configure agents
```

### **2. Agent Configuration Flow (in CustomerDashboard)**

```
1. Select Agent
   ├─ Choose: The Hunter (lead generation)
   └─ Future: The Enricher, The Messenger

2. Configure for Run
   ├─ Input Keywords: "dentists in Mumbai"
   ├─ Geographic Filters: Mumbai, India
   ├─ Industry/Business Type: Healthcare
   ├─ Advanced Options: Scraping depth, enrichment level
   ├─ Schedule: One-time or recurring (daily/weekly)
   └─ Save Configuration for reuse

3. Preview & Launch
   ├─ Review configuration summary
   ├─ Confirm subscription credits available
   └─ Click "Run Agent"
```

### **3. Agent Execution & Monitoring (in CustomerDashboard)**

```
1. Execution Started
   ├─ Backend queues job
   ├─ Agents start working (scraping, enriching, personalizing)
   └─ Usage credits deducted in real-time

2. Real-Time Monitoring
   ├─ Progress bar: "Scraping 145/200 leads..."
   ├─ Live metrics:
   │  ├─ Leads found
   │  ├─ Email addresses extracted
   │  ├─ Messages personalized
   │  └─ Quality score average
   └─ Can stop/pause if needed

3. Results Available
   ├─ Lead preview with generated messages
   ├─ Export options:
   │  ├─ CSV download
   │  ├─ CRM webhook (Salesforce, HubSpot)
   │  └─ Email blast ready-to-send
   └─ Save results for later
```

### **4. Consumption & Billing (in CustomerDashboard)**

```
1. Current Usage
   ├─ API calls used this month: 45,000 / 100,000
   ├─ Credits consumed: $42 / $99
   ├─ Leads generated: 342
   └─ Progress bar visualization

2. Billing Info
   ├─ Plan: Professional ($4,999/month)
   ├─ Next billing date: Jan 14, 2025
   ├─ Payment method: **** 1234
   └─ Upgrade/Downgrade options

3. Usage History
   ├─ Daily breakdown of agent runs
   ├─ Credit consumption per agent
   ├─ Trend analysis: Usage increasing/stable
   └─ Cost per lead generated
```

### **5. Admin Oversight Flow (in AdminDashboard)**

```
1. System Overview
   ├─ Total agents running: 45
   ├─ Total customers: 23
   ├─ System uptime: 99.8%
   └─ Daily revenue: ₹112,000

2. Agent Performance (Aggregate)
   ├─ The Hunter:
   │  ├─ Avg leads/run: 187
   │  ├─ Avg email validity: 94%
   │  ├─ Success rate: 96%
   │  └─ Customer satisfaction: 4.7/5
   ├─ The Enricher: [Coming Soon]
   └─ The Messenger: [Coming Soon]

3. Customer Analytics
   ├─ Top 10 customers by spend
   ├─ Churn risk analysis
   ├─ Feature adoption rates
   └─ Support tickets queue

4. Business Metrics
   ├─ MRR (Monthly Recurring Revenue): ₹114,977
   ├─ Customer Acquisition Cost: ₹2,500
   ├─ Customer Lifetime Value: ₹89,988
   └─ Growth trends: +15% MoM
```

---

## Technical Stack

### **Consistency Principle**
All three applications (AgentsHome, CustomerDashboard, AdminDashboard) use **identical tech stack** for:
- Code reusability across projects
- Shared component libraries
- Unified deployment process
- Single authentication service

### **Frontend Stack**
| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Angular | 17.x |
| Language | TypeScript | 5.2+ |
| Styling | SCSS + CSS Custom Properties | - |
| UI State | RxJS | 7.8+ |
| HTTP Client | Angular HttpClient | 17.x |
| Routing | Angular Router | 17.x |
| Forms | Reactive Forms | 17.x |
| Testing | Jasmine + Karma | Latest |
| Build | Webpack (via Angular CLI) | - |

### **Backend Stack**
| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | FastAPI | 0.104+ |
| Language | Python | 3.11+ |
| Database | PostgreSQL | 15+ |
| ORM | SQLAlchemy | 2.0+ |
| Auth | JWT + Passlib | - |
| Testing | Pytest | 7.4+ |
| Server | Uvicorn | 0.24+ |
| API Docs | OpenAPI/Swagger | Auto-generated |

### **Infrastructure**
| Component | Technology |
|-----------|-----------|
| Containers | Docker + Docker Compose |
| Orchestration | Docker Compose (local), Kubernetes (production) |
| Database Hosting | PostgreSQL container / Managed Cloud |
| API Hosting | Azure Container Instances / AWS ECS / Heroku |
| Frontend Hosting | Azure Static Web Apps / Netlify / Vercel |
| CDN | CloudFlare (optional) |
| Monitoring | Prometheus + Grafana (future) |

---

## Authentication & Authorization

### **Architecture Decision: Unified JWT-Based Auth**

```
┌─────────────────────────────────────────────────────────────┐
│                  Authentication Flow                        │
├─────────────────────────────────────────────────────────────┤

1. LOGIN (via AgentsHome or CustomerDashboard)
   ├─ User submits email + password
   ├─ Backend validates against user table
   ├─ JWT token generated (exp: 7 days)
   ├─ Refresh token stored (exp: 30 days)
   └─ Frontend stores JWT in localStorage + httpOnly cookie

2. API REQUESTS
   ├─ All requests include Authorization: Bearer <JWT>
   ├─ Backend validates token
   ├─ Backend extracts user_id + role from payload
   └─ Request proceeds with user context

3. TOKEN REFRESH
   ├─ When JWT expires, use refresh token
   ├─ Backend issues new JWT without re-login
   └─ Seamless experience for user

4. LOGOUT
   ├─ Frontend clears localStorage + cookies
   ├─ Optional: Backend blacklists token
   └─ User redirected to login page
```

### **Role-Based Access Control (RBAC)**

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role ENUM ('customer', 'admin') NOT NULL,
    subscription_status ENUM ('active', 'trial', 'inactive'),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Permissions matrix
┌──────────────────┬──────────────┬──────────────┐
│ Resource         │ Customer     │ Admin        │
├──────────────────┼──────────────┼──────────────┤
│ Own Agents       │ ✅ CRUD      │ ✅ R (all)   │
│ Own Leads        │ ✅ CRUD      │ ✅ R (all)   │
│ Billing          │ ✅ R (own)   │ ✅ R (all)   │
│ Usage Analytics  │ ✅ R (own)   │ ✅ R (all)   │
│ Admin Dashboard  │ ❌           │ ✅ Full      │
│ System Health    │ ❌           │ ✅ R         │
│ User Mgmt        │ ❌           │ ✅ R (own)   │
└──────────────────┴──────────────┴──────────────┘
```

### **Implementation Details**

**Frontend Protection:**
```typescript
// app.module.ts
providers: [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
  { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true }
]

// auth.guard.ts
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(route: ActivatedRouteSnapshot): boolean {
    return this.authService.isLoggedIn() && 
           this.hasRole(route.data['roles']);
  }
}
```

**Backend Protection:**
```python
# FastAPI middleware
@app.get("/api/agents")
async def get_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Agent).filter(Agent.customer_id == current_user.id).all()
```

---

## Data Multi-tenancy

### **Principle: Strict Customer Isolation**

Every customer sees **only their own data**. This is enforced at:
1. **Database level** - customer_id filtering in all queries
2. **API level** - Authorization checks before data access
3. **Frontend level** - Role-based UI rendering

### **Database Schema (Multi-tenant)**

```sql
-- Customers (accounts)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    user_id INT REFERENCES users(id),
    subscription_id INT REFERENCES subscriptions(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agents (assigned per customer)
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id) NOT NULL,  -- ⭐ TENANT KEY
    agent_type ENUM ('hunter', 'enricher', 'messenger'),
    name VARCHAR(255),
    configuration JSONB,  -- Stores customer-specific config
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Leads (owned by customer through agent)
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    agent_id INT REFERENCES agents(id) NOT NULL,
    customer_id INT REFERENCES customers(id) NOT NULL,  -- ⭐ TENANT KEY (denormalized for performance)
    email VARCHAR(255),
    company_name VARCHAR(255),
    personalized_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage/Consumption (tracked per customer)
CREATE TABLE usage_logs (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id) NOT NULL,  -- ⭐ TENANT KEY
    agent_id INT REFERENCES agents(id),
    action VARCHAR(100),  -- 'scrape', 'enrich', 'personalize'
    credits_consumed DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Subscriptions
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id) NOT NULL,  -- ⭐ TENANT KEY
    plan_id INT REFERENCES plans(id),
    status ENUM ('active', 'trial', 'cancelled'),
    billing_cycle_start DATE,
    billing_cycle_end DATE,
    monthly_credits DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Query Pattern (Always Filtered)**

```python
# ❌ WRONG - Returns all agents (security breach!)
all_agents = db.query(Agent).all()

# ✅ CORRECT - Returns only current user's agents
user_agents = db.query(Agent).filter(
    Agent.customer_id == current_user.customer_id
).all()

# ✅ CORRECT - Lead access through agent ownership
user_leads = db.query(Lead).filter(
    Lead.customer_id == current_user.customer_id,
    Lead.agent_id == agent_id  # Additional validation
).all()
```

### **Admin Exception (View All Data)**

```python
# Admins can view any customer's data (with audit logging)
@app.get("/admin/customers/{customer_id}/agents")
async def admin_get_customer_agents(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify user is admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Log access (audit trail)
    log_admin_action(current_user.id, "viewed_customer_agents", customer_id)
    
    # Return all agents for customer
    return db.query(Agent).filter(Agent.customer_id == customer_id).all()
```

---

## Development Phases

### **Phase 1: AgentsHome ✅ COMPLETE**
- **Status:** Live on localhost:4200
- **Components:** Landing page, agent showcase, pricing, FAQ
- **Output:** Customer acquisition funnel
- **Timeline:** Completed Dec 14, 2025

### **Phase 2: Backend API Service (Partial)**
- **Status:** In Progress
- **Components:**
  - ✅ User authentication (JWT)
  - ✅ Basic FastAPI structure
  - ⏳ Customer management
  - ⏳ Agent orchestration
  - ⏳ Lead storage & retrieval
  - ⏳ Subscription management
  - ⏳ Usage metering
- **Timeline:** Concurrent with Phase 3

### **Phase 3: CustomerDashboard 🎯 NEXT PRIORITY**
- **Status:** Planned
- **Components:**
  1. **Configure Agent** - Keywords, filters, schedule
  2. **Monitor Outcomes** - Real-time results, lead preview
  3. **Consumption & Balance** - Usage tracking, billing
  4. **Lead Management** - Export, CRM integration
  5. **History & Analytics** - Past runs, trends
- **Tech Stack:** Angular 17 + same backend
- **Timeline:** Start immediately after Phase 2 basics
- **Revenue Impact:** Direct - enables customer self-service

### **Phase 4: AdminDashboard (Future)**
- **Status:** Planned
- **Components:**
  1. **System Overview** - KPIs, uptime
  2. **Agent Analytics** - Performance across all customers
  3. **Customer Management** - Usage, churn risk
  4. **Business Metrics** - MRR, CAC, LTV
  5. **Support & Monitoring** - System health
- **Tech Stack:** Angular 17 + same backend
- **Timeline:** After CustomerDashboard stable (Q1 2025)
- **Revenue Impact:** Indirect - operational efficiency, data-driven decisions

---

## Component Specifications

### **1. Configure Agent Component**

**Purpose:** Allow customers to set up agent execution parameters

**User Inputs:**
```typescript
interface AgentConfiguration {
  agent_id: string;              // Selected agent (hunter, enricher, etc.)
  keywords: string[];            // Search terms: ["dentists", "orthodontists"]
  location: string;              // Geographic filter: "Mumbai, India"
  business_type: string[];       // Industry filter: ["Healthcare", "Dental"]
  advanced_options: {
    scraping_depth: number;      // 1-5 (shallow to deep)
    enrichment_level: string;    // 'basic', 'standard', 'premium'
    personalization_tone: string;// 'formal', 'casual', 'sales-focused'
    min_confidence: number;      // 0.7-0.95 (email validity threshold)
  };
  schedule: {
    type: string;               // 'once', 'daily', 'weekly', 'monthly'
    run_at: string;             // "14:30" (timezone-aware)
    max_runs: number;           // Limit to prevent runaway costs
  };
  config_name: string;          // "Q4 Dentist Outreach" (save as template)
  is_template: boolean;         // Reusable for future runs
}
```

**Output:**
- Configuration saved to database
- Success toast notification
- Option to "Run Now" or "Schedule Later"

**UI Layout:**
```
┌────────────────────────────────────┐
│ Configure The Hunter                │
├────────────────────────────────────┤
│                                    │
│ [Agent Selection Dropdown]         │
│                                    │
│ Keywords Input (multi-field)       │
│ ┌──────────────────────────────┐   │
│ │ [dentists] [orthodontist]  X │   │
│ │ [+ Add More Keywords]        │   │
│ └──────────────────────────────┘   │
│                                    │
│ Location Picker                    │
│ [Select City/Region dropdown]      │
│                                    │
│ Business Type (Multi-select)       │
│ ☑ Healthcare  ☐ Technology        │
│ ☑ Dental      ☐ Finance           │
│                                    │
│ [Advanced Options] (collapsible)   │
│                                    │
│ Schedule                           │
│ ◉ Run Once  ○ Daily  ○ Weekly     │
│                                    │
│ Config Name [Save Dentists Q4]     │
│ ☐ Save as template                │
│                                    │
│ [Cancel] [Preview] [Run Now]       │
└────────────────────────────────────┘
```

---

### **2. Monitor Outcomes Component**

**Purpose:** Real-time dashboard showing agent execution results

**Live Metrics:**
```typescript
interface ExecutionMetrics {
  status: string;                  // 'running', 'completed', 'failed'
  progress: number;                // 0-100
  leads_found: number;             // 145
  emails_extracted: number;        // 142
  messages_personalized: number;   // 142
  avg_quality_score: number;       // 0.94 (94%)
  estimated_completion: string;    // "2:34 min remaining"
  credits_used_so_far: number;     // 2.34 / 5.00
}
```

**Lead Preview:**
```typescript
interface LeadPreview {
  id: string;
  company_name: string;
  contact_name: string;
  email: string;
  phone: string;
  website: string;
  personalized_message: string;    // Generated by agent
  quality_score: number;           // 0.94
  actions: {
    copy_message: boolean;
    export_to_crm: boolean;
    send_email: boolean;
    skip: boolean;
  }
}
```

**UI Layout:**
```
┌────────────────────────────────────────────┐
│ The Hunter - Live Execution                 │
├────────────────────────────────────────────┤
│                                            │
│ Status: RUNNING (Started 2:15 PM)          │
│                                            │
│ Progress: [████████░░░░░░░░░░] 62%         │
│ ETA: 2:34 remaining                        │
│                                            │
│ ┌──────────────────────────────────────┐   │
│ │ Leads Found:     145  ↑               │   │
│ │ Emails Valid:    142  (98%)           │   │
│ │ Personalized:    142  ✓               │   │
│ │ Avg Quality:     0.94 ⭐⭐⭐⭐⭐     │   │
│ │ Credits Used:    2.34 / 5.00 remaining   │
│ └──────────────────────────────────────┘   │
│                                            │
│ [Pause Run] [Stop] [Export Draft]          │
│                                            │
│ ─── Lead Preview (First 3) ───             │
│                                            │
│ 1️⃣  Apollo Dental Clinic                   │
│    Dr. Rajesh Kumar                        │
│    rajesh@apollo-dental.com                │
│    +91 98765 43210                         │
│    📧 Hi Rajesh,                           │
│       Apollo Dental is known for its ...   │
│    [Copy] [Export to Salesforce] [Skip]    │
│                                            │
│ 2️⃣  SmileCare Orthodontics                 │
│    ...                                     │
│                                            │
│ ─── View More Results                      │
│ [Download CSV] [Open Full List]            │
└────────────────────────────────────────────┘
```

---

### **3. Consumption & Balance Component**

**Purpose:** Track usage, credits, and billing information

**Data Structure:**
```typescript
interface UsageData {
  current_month: {
    api_calls_used: number;        // 45,000
    api_calls_limit: number;       // 100,000
    credits_consumed: number;      // 42.50
    credits_limit: number;         // 99.99
    leads_generated: number;       // 342
  };
  billing: {
    plan_name: string;             // "Professional"
    plan_price: number;            // 4999 (INR)
    currency: string;              // "INR"
    next_billing_date: string;     // "2025-01-14"
    auto_renew: boolean;           // true
    payment_method: string;        // "Mastercard ending in 1234"
    upgrade_available: boolean;    // true
  };
  usage_history: {
    date: string;
    agent: string;
    leads: number;
    credits: number;
    cost: number;
  }[];
}
```

**UI Layout:**
```
┌────────────────────────────────────────────┐
│ Subscription & Usage                        │
├────────────────────────────────────────────┤
│                                            │
│ 📊 CURRENT USAGE (Dec 1-14, 2025)          │
│                                            │
│ API Calls                                  │
│ [████████░░░░░░░░░░░░░░░] 45%              │
│ 45,000 / 100,000 used                      │
│                                            │
│ Credits                                    │
│ [████████░░░░░░░░░░░░░░░] 42%              │
│ ₹42.50 / ₹99.99 consumed                  │
│                                            │
│ Leads Generated: 342                       │
│ Avg Cost/Lead: ₹0.12                       │
│                                            │
│ ─────────────────────────────────────────  │
│ 💳 BILLING                                  │
│                                            │
│ Plan: Professional ($4,999/month)          │
│ Status: Active ✅                          │
│ Next Billing: Jan 14, 2025 (28 days)       │
│ Auto-Renew: Yes                            │
│                                            │
│ Payment Method: **** **** **** 1234        │
│ [Update Payment] [Change Plan]             │
│                                            │
│ ─────────────────────────────────────────  │
│ 📈 USAGE HISTORY (Last 7 Days)              │
│                                            │
│ Dec 14: The Hunter    → 47 leads, ₹5.64   │
│ Dec 13: The Hunter    → 42 leads, ₹5.04   │
│ Dec 12: No activity                        │
│ Dec 11: The Hunter    → 51 leads, ₹6.12   │
│ ...                                        │
│                                            │
│ [View Detailed Report] [Download Invoice]  │
│                                            │
│ ─────────────────────────────────────────  │
│ 🎁 UPGRADE OPTIONS                         │
│                                            │
│ Enterprise Plan: ₹9,999/month               │
│ 200,000 API Calls, All Agents              │
│ [View & Upgrade]                           │
└────────────────────────────────────────────┘
```

---

## Development Roadmap

### **Q4 2024 (Immediate - 2 weeks)**
- ✅ AgentsHome landing page (complete)
- Backend API core setup
- User authentication (JWT)
- Database schema v1

### **Q4 2024-Q1 2025 (3-4 weeks)**
- 🎯 **CustomerDashboard v1**
  - Configure Agent UI
  - Monitor Outcomes dashboard
  - Basic usage tracking

### **Q1 2025 (4-5 weeks)**
- CustomerDashboard v2
  - Consumption & Billing views
  - Export functionality
  - CRM integrations

### **Q1-Q2 2025 (Future)**
- AdminDashboard
- Advanced analytics
- Payment processing
- Production deployment

---

## Key Design Principles

1. **Self-Service First** - Customers need zero support to configure and monitor agents
2. **Real-Time Feedback** - Live progress, instant results, no waiting
3. **Multi-Tenant Isolation** - Complete data separation between customers
4. **Consistent Tech Stack** - Angular + FastAPI across all apps
5. **Progressive Enhancement** - Start with MVP, add features incrementally
6. **Cost Transparency** - Show exactly how many credits each action consumes
7. **Mobile Responsive** - Dashboard usable on phones, tablets, desktop
8. **Audit Trail** - Track all customer actions for compliance

---

## Success Metrics

### **Customer Acquisition**
- Signups from landing page: 10+ per week
- Free trial to paid conversion: 40%+
- Average subscription duration: 6+ months

### **Product Quality**
- Lead generation accuracy: 95%+
- Email validity rate: 90%+
- System uptime: 99.9%

### **Business**
- MRR growth: 15%+ month-over-month
- Customer acquisition cost: < ₹2,500
- Customer lifetime value: > ₹50,000

---

## Appendix: API Endpoints (Backend)

### **Authentication**
```
POST   /api/auth/signup           - Register new customer
POST   /api/auth/login            - Login + get JWT token
POST   /api/auth/refresh          - Refresh expired token
GET    /api/auth/me               - Get current user info
POST   /api/auth/logout           - Invalidate token
```

### **Agent Management**
```
GET    /api/agents                - List user's agents
POST   /api/agents                - Create new agent config
GET    /api/agents/{id}           - Get agent details
PUT    /api/agents/{id}           - Update agent config
DELETE /api/agents/{id}           - Delete agent
POST   /api/agents/{id}/run       - Execute agent
GET    /api/agents/{id}/status    - Get execution status
```

### **Leads**
```
GET    /api/leads                 - List user's leads
GET    /api/leads/{id}            - Get lead details
POST   /api/leads/export          - Export to CSV
POST   /api/leads/webhook         - Send to CRM
```

### **Usage & Billing**
```
GET    /api/usage/current         - Current month usage
GET    /api/usage/history         - Historical usage
GET    /api/subscription          - Subscription details
PUT    /api/subscription/upgrade  - Change plan
```

### **Admin Endpoints**
```
GET    /admin/customers           - All customers
GET    /admin/customers/{id}      - Customer details
GET    /admin/agents              - All agents (all customers)
GET    /admin/analytics           - System analytics
GET    /admin/revenue             - Revenue reports
```

---

**Document Owner:** Engineering Team  
**Last Review:** December 14, 2025  
**Next Review:** January 15, 2025
