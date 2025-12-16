# Architectural Decisions Log

**Date:** December 14, 2025  
**Session:** Product Strategy & Development Planning  
**Status:** APPROVED ✅

---

## Decision 1: Unified Technology Stack

### **Decision**
All three applications (AgentsHome, CustomerDashboard, AdminDashboard) will use **identical tech stack**:
- **Frontend:** Angular 17 + TypeScript
- **Backend:** FastAPI + Python 3.11
- **Database:** PostgreSQL
- **Infrastructure:** Docker + Docker Compose

### **Rationale**
- Code reusability across projects (shared components, services, utilities)
- Simplified developer experience (single language per tier)
- Unified deployment pipeline (consistent build process)
- Reduced complexity in CI/CD automation
- Better knowledge sharing across teams

### **Approved:** ✅ YES

---

## Decision 2: Authentication & Authorization

### **Decision**
- **Method:** JWT-based authentication with refresh tokens (7-day JWT, 30-day refresh)
- **Entry Point:** AgentsHome (landing page)
- **Session Sharing:** Single login across AgentsHome, CustomerDashboard, AdminDashboard
- **Admin Access:** Separate admin role (not separate login)
- **Implementation:** FastAPI middleware + Angular HTTP interceptors
- **Token Storage:** httpOnly cookies + localStorage (hybrid approach)

### **Rationale**
- JWT is stateless (ideal for microservices and horizontal scaling)
- Single sign-on (SSO) improves user experience
- Refresh tokens prevent token expiration during long sessions
- httpOnly cookies prevent XSS attacks
- Consistent with modern SaaS best practices
- Simplifies backend (no session storage needed)

### **Approved:** ✅ YES

---

## Decision 3: Data Multi-Tenancy Strategy

### **Decision**
- **Isolation Level:** Complete logical separation (customer_id on every table)
- **Query Pattern:** All queries filtered by `customer_id` + user authentication
- **Access Control:** 
  - Customers see only their own agents and leads
  - Admins can view any customer's data (with audit logging)
- **Database Schema:** Denormalized `customer_id` on both parent and child tables for performance
- **Data Recovery:** Soft deletes with `deleted_at` timestamps

### **Rationale**
- Complete data isolation prevents accidental data leakage
- Filters at query level (not just presentation layer) ensure security
- Audit logging on admin access provides compliance trail
- Denormalization balances query performance with consistency
- Soft deletes allow data recovery without complex restoration

### **Approved:** ✅ YES

---

## Decision 4: Build Priority

### **Decision**
**Build CustomerDashboard NEXT (immediately after Phase 2 backend basics)**

### **Rationale**
1. **Revenue Impact:** Direct - enables paying customers to self-serve
2. **Reduces Support Load:** Self-service configuration eliminates support tickets
3. **Market Feedback:** Actual customer usage informs AdminDashboard design
4. **Faster to Revenue:** Live product generates early paying customers
5. **Foundation:** AdminDashboard will mirror CustomerDashboard (easy to build after)

**Timeline:**
- Phase 2 (Parallel): Core backend (user mgmt, API structure) - 2-3 weeks
- Phase 3 (Sequential): CustomerDashboard MVP - 3-4 weeks
- Phase 4 (Sequential): CustomerDashboard v2 (exports, CRM) - 2-3 weeks
- Phase 5 (Parallel): AdminDashboard - 4-5 weeks

### **Approved:** ✅ YES

---

## Decision 5: Customer Signup Flow

### **Decision**
1. Customer visits **AgentsHome** landing page
2. Clicks "Free Trial" or "Subscribe Now"
3. OAuth/Email signup via Razorpay/Stripe payment gateway
4. Account created in database with subscription status
5. JWT token issued (automatic login)
6. Redirected to **CustomerDashboard** (first experience is configuration screen)

### **Rationale**
- AgentsHome handles acquisition (conversion optimization)
- Payment processing happens during signup (proven checkout flow)
- No manual activation needed (instant access)
- Reduces friction between signup and first usage
- Supports free trial cohort testing

### **Approved:** ✅ YES

---

## Decision 6: Agent Execution Model

### **Decision**
- **Configuration:** Customer defines keywords, filters, schedule via UI
- **Execution:** Backend queues job, agents process asynchronously
- **Monitoring:** Real-time WebSocket updates to frontend (progress bar, metrics)
- **Results:** Leads saved to database, customer can preview/export
- **No Automatic Actions:** Messages are drafted but NOT sent automatically (customer reviews first)

### **Rationale**
- Asynchronous processing prevents UI blocking on long-running jobs
- WebSocket provides real-time feedback (better UX than polling)
- Manual review gate prevents spam complaints and bad reputation
- Complies with India's DND/TRAI regulations (no unsolicited messages)
- Customers maintain full control over outreach strategy

### **Approved:** ✅ YES

---

## Decision 7: Usage Metering & Billing

### **Decision**
- **Tracked Metrics:** Per-agent runs, leads scraped, emails enriched, messages personalized
- **Credit System:** Each action consumes credits (e.g., 1 lead = ₹0.10 credit)
- **Monthly Allocation:** Plan includes monthly credit limit (e.g., ₹4,999 = 49,990 credits)
- **Tracking:** Every action logged to `usage_logs` table with timestamp and customer_id
- **Display:** Real-time consumption dashboard shows remaining balance
- **Overage:** Can exceed limit (rolls to next billing cycle or charges overage)

### **Rationale**
- Transparent pricing (customers know exact cost per action)
- Prevents runaway costs (monthly allocation creates guardrail)
- Enables usage-based optimization (customers monitor efficiency)
- Accurate financial reporting (every transaction tracked)
- Supports future tiering (different credit rates for different agents)

### **Approved:** ✅ YES

---

## Decision 8: Admin Dashboard Access Patterns

### **Decision**
- **Data Access:** Admins can view any customer's agents, leads, and usage
- **Audit Trail:** Every admin data access logged (user_id, timestamp, resource_id)
- **No Direct Modification:** Admins view data but cannot modify customer configurations
- **Exception Cases:** Admins can reset credits, refund usage for support requests
- **Segregated Views:** Admin Dashboard shows aggregated metrics (not individual leads)

### **Rationale**
- Admins need visibility to debug issues and monitor health
- Audit logging provides compliance and security trail
- Preventing direct modification reduces accidental data corruption
- Limited modification authority (only credits/refunds) reduces risk
- Aggregated metrics prevent information overload while enabling decision-making

### **Approved:** ✅ YES

---

## Decision 9: Deployment & Infrastructure

### **Decision**
- **Local Development:** Docker Compose with PostgreSQL + FastAPI + Angular
- **Staging:** Docker images pushed to Azure Container Registry
- **Production:** Azure Container Instances or App Service (managed scaling)
- **Database:** Managed PostgreSQL (Azure Database for PostgreSQL)
- **Frontend Hosting:** Azure Static Web Apps or Netlify (edge CDN)
- **CI/CD:** GitHub Actions with approval workflow (manual deployments)

### **Rationale**
- Docker Compose enables production-like environments locally
- Azure managed services reduce operational overhead
- Managed PostgreSQL ensures backups and high availability
- Static Web Apps provides edge caching (faster responses)
- Manual deployments reduce risk of accidental releases

### **Approved:** ✅ YES

---

## Decision 10: Feature Rollout Strategy

### **Decision**
1. **Phase 1 - AgentsHome (Complete):** Landing page live
2. **Phase 2 - Backend Core:** Authentication, API structure, database
3. **Phase 3 - CustomerDashboard MVP:** Configure + Monitor + Consumption
4. **Phase 4 - CustomerDashboard v2:** Exports, CRM integrations, history
5. **Phase 5 - AdminDashboard:** Analytics, customer management, monitoring
6. **Phase 6 - Advanced Features:** Team collaboration, webhooks, bulk operations

### **Rationale**
- MVP first (reduce time to revenue)
- Validates market demand before building complex features
- Customer feedback guides feature prioritization
- Incremental rollout allows rapid iteration
- Each phase adds value independently

### **Approved:** ✅ YES

---

## Summary of Key Decisions

| Decision | Choice | Approved |
|----------|--------|----------|
| Tech Stack | Angular + FastAPI (unified) | ✅ |
| Authentication | JWT with refresh tokens | ✅ |
| Multi-Tenancy | Complete customer isolation | ✅ |
| Build Priority | CustomerDashboard next | ✅ |
| Signup Flow | AgentsHome → Payment → Redirect | ✅ |
| Agent Execution | Async + WebSocket updates | ✅ |
| Billing Model | Credit system with monthly allocation | ✅ |
| Admin Access | View-only with audit logging | ✅ |
| Infrastructure | Docker + Azure managed services | ✅ |
| Feature Rollout | 6-phase incremental release | ✅ |

---

## Documentation Generated

✅ `/workspaces/yashus/docs/ARCHITECTURE.md` - Complete architectural specification  
✅ Updated README.md with product applications and architecture links  
✅ This decision log for reference

---

**Next Steps:**
1. Begin Phase 2 backend development (user management, API core)
2. Design API contracts for CustomerDashboard
3. Create database migrations for production schema
4. Set up GitHub Actions CI/CD pipeline

**Prepared by:** Engineering Team  
**Date:** December 14, 2025
