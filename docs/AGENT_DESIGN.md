# Agent Design Specification

**Date:** December 14, 2025  
**Status:** Design Locked - Ready for Implementation

---

## 1. Agent Architecture Overview

```
AGENT (Customer Instance)
├─ Cookbook: Collection of recipes
│  ├─ Recipe 1: Executable workflow (AI + Action + Correspondence)
│  ├─ Recipe 2: Executable workflow
│  ├─ Recipe N: Executable workflow
│  └─ Subscription Recipe: MANDATORY (all agents must include)
└─ Configuration:
   ├─ execution_mode: "sequential" | "parallel"
   ├─ retry_policy: max_attempts, backoff_strategy
   ├─ alert_config: channels, recipients, triggers
   └─ rate_limits: per_customer_subscription_based
```

**Key Principles:**
- Agent composed of 1+ recipes + mandatory subscription recipe
- Each recipe executes independently or chained (based on config)
- All data flows via standardized JSON schema
- All components (AI, Action, Correspondence) are pluggable
- Async execution only (non-blocking)
- Per-customer isolation (multi-tenant)

---

## 2. The Hunter Agent - Recipe Specification

### **Recipe 1: Discovery (Scraper)**

**Purpose:** Discover leads from target criteria + AI-powered lead scoring & qualification

**Components:**
- **AI Component:** 
  - Decide scraping strategy (Google Maps vs LinkedIn vs web)
  - Score each discovered lead (0.0-1.0) based on:
    - Business maturity (website freshness, review count)
    - Intent signals (blog activity, content updates)
    - Fit match (industry, location, business size, target match)
  - Auto-expand keywords (if "dentists" → also "orthodontists", "dental clinics")
  - Filter low-quality leads (score < 0.6)
- **Model:** Groq or DeepSeek-lite (speed + cost)
- **Action Component:** Execute scraper (Playwright, APIs, etc.)

**Input Schema:**
```json
{
  "recipe_id": "discovery",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "payload": {
    "keywords": ["dentists", "orthodontists"],
    "location": "Mumbai, India",
    "business_type": "Healthcare",
    "depth": 3,
    "max_results": 200
  }
}
```

**Output Schema:**
```json
{
  "recipe_id": "discovery",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "status": "success|partial|failed",
  "data": {
    "leads": [
      {
        "id": "lead_123",
        "name": "Apollo Dental Clinic",
        "phone": "+91-9876543210",
        "address": "123 Main St, Mumbai",
        "website": "apollo-dental.com",
        "rating": 4.5,
        "source": "google_maps",
        "lead_score": 0.87,
        "score_breakdown": {
          "business_maturity": 0.9,
          "intent_signals": 0.85,
          "fit_match": 0.85
        },
        "quality_tier": "hot"
      }
    ],
    "summary": {
      "total_discovered": 200,
      "qualified_leads": 123,
      "filtered_out": 77
    }
  },
  "metadata": {
    "started_at": "2025-12-14T10:30:00Z",
    "completed_at": "2025-12-14T10:35:45Z",
    "duration_ms": 345000,
    "records_processed": 200,
    "records_succeeded": 195,
    "records_failed": 5,
    "credits_consumed": 2.15
  },
  "errors": [
    {
      "record_id": "lead_195",
      "error_code": "API_RATE_LIMIT",
      "error_message": "Google Maps API rate limit exceeded",
      "retryable": true
    }
  ]
}
```

**Secrets Required:** `google_maps_api_key`

**AI Model Cost:** Groq (scoring) = $0.02 per lead
**WOW Outcome:** Customer gets 123 qualified leads instead of 200 raw leads (37% reduction in noise)

---

### **Recipe 2: Intelligence (Enricher)**

**Purpose:** Enrich lead data with emails, metadata, and strategic intelligence

**Components:**
- **AI Component:** 
  - Decide enrichment level (basic/standard/premium) based on lead score from Discovery
  - High-score leads → Premium enrichment (all data sources)
  - Medium-score leads → Standard enrichment (email + basic metadata)
  - Low-score leads → Skip enrichment (save credits for hot leads)
- **Model:** Groq or DeepSeek-lite (routing decision)
- **Action Component:** Call enrichment APIs (email finders, content scrapers)

**Input Schema:**
```json
{
  "recipe_id": "intelligence",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "payload": {
    "leads": [
      {
        "id": "lead_123",
        "name": "Apollo Dental",
        "website": "apollo-dental.com",
        "source": "google_maps"
      }
    ],
    "enrichment_level": "standard"
  }
}
```

**Output Schema:**
```json
{
  "recipe_id": "intelligence",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "status": "success|partial|failed",
  "data": {
    "leads": [
      {
        "id": "lead_123",
        "name": "Apollo Dental",
        "website": "apollo-dental.com",
        "emails": [
          {
            "email": "rajesh@apollo-dental.com",
            "confidence": 0.94,
            "source": "hunter_io"
          }
        ],
        "phone_contacts": [
          {
            "name": "Dr. Rajesh Kumar",
            "email": "rajesh@apollo-dental.com",
            "phone": "+91-9876543210"
          }
        ],
        "website_metadata": {
          "last_updated": "2025-12-10",
          "blog_posts_count": 15,
          "content_freshness": "high",
          "tech_stack": ["WordPress", "WooCommerce"]
        }
      }
    ]
  },
  "metadata": {
    "started_at": "2025-12-14T10:36:00Z",
    "completed_at": "2025-12-14T10:42:30Z",
    "duration_ms": 390000,
    "records_processed": 195,
    "records_succeeded": 183,
    "records_failed": 12,
    "credits_consumed": 2.83
  },
  "errors": [
    {
      "record_id": "lead_145",
      "error_code": "EMAIL_NOT_FOUND",
      "error_message": "No email found for lead",
      "retryable": false
    }
  ]
}
```

**Secrets Required:** `hunter_io_key`, `rocketchat_key`, `clearbit_key`

**AI Model Cost:** Groq (routing) = $0.02 per lead
**WOW Outcome:** High-score leads get premium enrichment, saving credits on low-potential leads

---

### **Recipe 3: Personalization (Personalizer)**

**Purpose:** Generate AI-personalized, context-aware outreach messages (THE WOW FACTOR)

**Components:**
- **AI Component (CORE DIFFERENTIATOR):** 
  - Analyze website metadata (content, blog posts, tech stack, freshness, pain points)
  - Generate unique, personalized message for EACH lead
  - Reference specific business context (recent blog, tech choices, growth signals)
  - Vary message per industry (different angle for e-commerce vs dental vs manufacturing)
  - 75 words max (professional, compelling, non-spammy)
  - NO generic templates like "Hi Sir/Madam"
- **Model:** Claude or GPT-4 (high quality - customer sees this)
- **Action Component:** Call LLM API with website context

**Example Output:**
```
Instead of: "Hello, we generate qualified leads for your business"

AI Generates: "Hi Rajesh, Apollo Dental's recent blog on 
orthodontics trends shows strong content strategy. We help 
similar dental clinics generate 50+ qualified patient leads 
monthly through AI-personalized outreach. Would be great to 
discuss your growth plans for 2026."
```

**Input Schema:**
```json
{
  "recipe_id": "personalization",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "payload": {
    "leads": [
      {
        "id": "lead_123",
        "name": "Apollo Dental",
        "website": "apollo-dental.com",
        "website_metadata": {
          "last_updated": "2025-12-10",
          "blog_posts_count": 15
        },
        "emails": [{"email": "rajesh@apollo-dental.com"}]
      }
    ],
    "tone": "sales-focused",
    "max_length": 75,
    "template_context": "lead_generation"
  }
}
```

**Output Schema:**
```json
{
  "recipe_id": "personalization",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "status": "success|partial|failed",
  "data": {
    "leads": [
      {
        "id": "lead_123",
        "emails": [
          {
            "email": "rajesh@apollo-dental.com",
            "personalized_message": "Hi Rajesh, Apollo Dental's recent blog post on orthodontics caught our attention. We help dental clinics generate qualified patient leads...",
            "message_quality_score": 0.92,
            "model_used": "deepseek-v2"
          }
        ]
      }
    ]
  },
  "metadata": {
    "started_at": "2025-12-14T10:43:00Z",
    "completed_at": "2025-12-14T10:44:30Z",
    "duration_ms": 90000,
    "records_processed": 183,
    "records_succeeded": 183,
    "records_failed": 0,
    "credits_consumed": 0.92
  },
  "errors": []
}
```

**Secrets Required:** `deepseek_api_key`, `groq_api_key`, `claude_api_key`

**AI Model Cost:** Claude/GPT-4 (personalization) = $0.05 per message
**WOW Outcome:** 40-50% response rate vs 2-5% industry average for cold outreach

---

### **Recipe 4: Outreach (Correspondent)**

**Purpose:** Draft outreach messages for customer review (NO auto-send)

**Components:**
- **AI Component:** Decide channel and format (email/SMS/WhatsApp/FB/LinkedIn)
- **Correspondence Component:** Format message per channel
- **Action Component:** Save draft to database (awaiting customer approval)

**Input Schema:**
```json
{
  "recipe_id": "outreach",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "payload": {
    "leads": [
      {
        "id": "lead_123",
        "emails": [
          {
            "email": "rajesh@apollo-dental.com",
            "personalized_message": "Hi Rajesh..."
          }
        ]
      }
    ],
    "channels": ["email"],
    "send_mode": "draft_only",
    "draft_expiry_days": 7
  }
}
```

**Output Schema:**
```json
{
  "recipe_id": "outreach",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "status": "success|partial|failed",
  "data": {
    "outreach_jobs": [
      {
        "id": "outreach_123",
        "lead_id": "lead_123",
        "channel": "email",
        "draft_message": "Hi Rajesh, Apollo Dental's recent blog...",
        "recipient": "rajesh@apollo-dental.com",
        "status": "draft_pending_review",
        "created_at": "2025-12-14T10:45:00Z",
        "draft_expires_at": "2025-12-21T10:45:00Z",
        "awaiting_customer_approval": true
      }
    ]
  },
  "metadata": {
    "started_at": "2025-12-14T10:45:00Z",
    "completed_at": "2025-12-14T10:45:15Z",
    "duration_ms": 15000,
    "records_processed": 183,
    "records_succeeded": 183,
    "records_failed": 0,
    "credits_consumed": 0.18
  },
  "errors": []
}
```

**Secrets Required:** `smtp_creds`, `facebook_token`, `linkedin_token`, `twilio_key`

**Alerts Triggered:**
- `outreach_pending_review` (notify customer to approve drafts)
- `outreach_failed`

---

### **Recipe 5: Subscription (MANDATORY)**

**Purpose:** Monitor subscription usage, track credits, send alerts

**Components:**
- **AI Component:** Analyze subscription thresholds
- **Action Component:** Log metrics, queue alerts

**Input Schema:**
```json
{
  "recipe_id": "subscription",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "payload": {
    "credits_used_this_run": 6.88,
    "api_calls_this_run": 378
  }
}
```

**Output Schema:**
```json
{
  "recipe_id": "subscription",
  "execution_id": "exec_abc123",
  "customer_id": "cust_001",
  "status": "success",
  "data": {
    "subscription_status": {
      "plan_id": "professional",
      "monthly_credits_total": 99.99,
      "credits_used_this_month": 42.50,
      "credits_remaining": 57.49,
      "api_calls_limit": 100000,
      "api_calls_used_this_month": 45378,
      "api_calls_remaining": 54622,
      "billing_cycle_ends": "2025-12-31"
    },
    "alerts": [
      {
        "id": "alert_123",
        "type": "approaching_limit",
        "threshold_type": "percentage",
        "threshold_value": 20,
        "triggered": false,
        "message": "You are using 42% of your monthly credits"
      }
    ]
  },
  "metadata": {
    "started_at": "2025-12-14T10:46:00Z",
    "completed_at": "2025-12-14T10:46:05Z",
    "duration_ms": 5000,
    "records_processed": 1,
    "records_succeeded": 1,
    "records_failed": 0,
    "credits_consumed": 0
  },
  "errors": []
}
```

**Secrets Required:** None

**Alerts Triggered:**
- `subscription_approaching_limit` (at 80%)
- `subscription_exceeded` (over limit)
- `subscription_trial_ending` (7 days before expiry)

---

## 3. Standard JSON Schema for Data Flow

All recipe outputs follow this structure:

```typescript
interface RecipeOutput {
  recipe_id: string;                    // "discovery", "intelligence", etc.
  execution_id: string;                 // Unique per agent run
  customer_id: string;                  // Multi-tenant isolation
  status: "success" | "partial" | "failed";
  
  data: {
    // Recipe-specific output structure
    [key: string]: any;
  };
  
  metadata: {
    started_at: string;                 // ISO8601
    completed_at: string;               // ISO8601
    duration_ms: number;
    records_processed: number;
    records_succeeded: number;
    records_failed: number;
    credits_consumed: number;
  };
  
  errors: Array<{
    record_id: string;                  // Which record failed
    error_code: string;                 // "API_RATE_LIMIT", "EMAIL_NOT_FOUND"
    error_message: string;              // Human readable
    retryable: boolean;                 // Can be retried?
  }>;
  
  next_recipe_input?: RecipeInput;      // Pre-formatted for next recipe
}

interface RecipeInput {
  recipe_id: string;
  execution_id: string;
  customer_id: string;
  payload: any;                         // Recipe-specific input
}
```

---

## 4. Component Definitions

### **AI Component Interface**

```python
class AIComponent:
    """
    Analyzes context and makes decisions for recipe execution.
    Pluggable - can be swapped (LLM, rules engine, heuristics).
    """
    
    def decide(self, context: dict) -> dict:
        """
        Args:
            context: {
                "recipe_id": "personalization",
                "lead_data": {...},
                "config": {...}
            }
        
        Returns:
            {
                "strategy": "use_deepseek",
                "parameters": {...},
                "confidence": 0.92
            }
        """
        pass
```

### **Action Component Interface**

```python
class ActionComponent:
    """
    Executes external integrations (APIs, scraping, etc).
    Pluggable - swap implementations per integration.
    """
    
    def execute(self, decision: dict, secrets: dict) -> dict:
        """
        Args:
            decision: Strategy from AI component
            secrets: API keys, tokens, credentials
        
        Returns:
            {
                "status": "success",
                "data": {...},
                "credits_consumed": 1.5
            }
        """
        pass
```

### **Correspondence Component Interface**

```python
class CorrespondenceComponent:
    """
    Formats messages for different channels (email, SMS, WhatsApp, etc).
    Channel-agnostic message generation.
    """
    
    def format(self, message: str, channel: str, context: dict) -> str:
        """
        Args:
            message: Base personalized message
            channel: "email" | "sms" | "whatsapp" | "facebook" | "linkedin"
            context: Customer preferences, brand guidelines
        
        Returns:
            Formatted message for channel (with platform-specific constraints)
        """
        pass
```

### **Reusable Generic Components**

```python
class ErrorHandlerComponent:
    """
    Handles action failures with configurable retry logic.
    """
    def handle(self, error: Exception, retry_config: dict) -> dict:
        """
        Returns: {
            "action": "retry" | "fallback" | "alert",
            "retry_at": "2025-12-14T11:00:00Z" (if action=retry)
        }
        """
        pass

class SecretsManagerComponent:
    """
    Retrieves encrypted secrets from vault.
    """
    def get_secret(self, customer_id: str, secret_key: str) -> str:
        """Decrypt and return secret"""
        pass

class RateLimiterComponent:
    """
    Enforces per-customer API rate limits based on subscription.
    """
    def check_quota(self, customer_id: str, api_name: str) -> dict:
        """
        Returns: {
            "allowed": true | false,
            "remaining": 500,
            "resets_at": "2025-12-14T23:59:59Z"
        }
        """
        pass

class AuditLoggerComponent:
    """
    Logs all actions for compliance and debugging.
    """
    def log(self, customer_id: str, action: str, details: dict):
        """
        Stores in database with timestamp, actor, action, result.
        """
        pass

class StateManagerComponent:
    """
    Maintains customer conversation state (for multi-turn dialogue).
    """
    def get_state(self, customer_id: str, key: str) -> dict:
        """Retrieve previous conversation context"""
        pass
    
    def set_state(self, customer_id: str, key: str, value: dict):
        """Store context for next interaction"""
        pass
```

---

## 5. Execution Configuration

### **Recipe Execution Modes**

```json
{
  "execution_mode": "sequential",
  "recipes": [
    {
      "id": "discovery",
      "required": true,
      "continue_on_failure": false
    },
    {
      "id": "intelligence",
      "required": true,
      "continue_on_failure": false
    },
    {
      "id": "personalization",
      "required": true,
      "continue_on_failure": false
    },
    {
      "id": "outreach",
      "required": false,
      "continue_on_failure": true
    },
    {
      "id": "subscription",
      "required": true,
      "continue_on_failure": false
    }
  ]
}
```

**Sequential:** Recipe A completes → Recipe B starts (output of A feeds to input of B)  
**Parallel:** Recipes A, B, C start simultaneously (requires independent inputs)  
**Continue on Failure:** If recipe fails, proceed to next (non-critical recipes)

### **Retry Configuration**

```json
{
  "retry_policy": {
    "max_attempts": 3,
    "backoff_strategy": "exponential",
    "backoff_base_ms": 1000,
    "backoff_max_ms": 30000,
    "retryable_errors": [
      "API_RATE_LIMIT",
      "TIMEOUT",
      "CONNECTION_ERROR"
    ],
    "non_retryable_errors": [
      "EMAIL_NOT_FOUND",
      "INVALID_INPUT",
      "AUTHENTICATION_FAILED"
    ]
  }
}
```

**User-Driven:** Customer configures retry behavior per recipe  
**Default:** 3 attempts, exponential backoff (1s, 2s, 4s)

---

## 6. Alert & Notification System

### **Alert Configuration**

```json
{
  "alerts": [
    {
      "id": "alert_rate_limit",
      "trigger": "discovery_rate_limit",
      "severity": "warning",
      "channels": ["email", "app_notification"],
      "recipients": ["customer", "admin"],
      "template": "custom_or_default",
      "enabled": true
    },
    {
      "id": "alert_recipe_failed",
      "trigger": "recipe_failed",
      "severity": "error",
      "channels": ["email", "sms", "whatsapp"],
      "recipients": ["customer"],
      "template": "default_recipe_failure",
      "enabled": true,
      "max_frequency_hours": 1
    },
    {
      "id": "alert_subscription_threshold",
      "trigger": "subscription_approaching_limit",
      "severity": "warning",
      "channels": ["email", "app_notification"],
      "recipients": ["customer"],
      "threshold_percentage": 80,
      "enabled": true
    }
  ]
}
```

### **Alert Delivery Channels**

```python
class AlertDelivery:
    """
    Routes alerts to appropriate channels.
    """
    
    def send_email(recipient: str, subject: str, body: str):
        """Via SMTP"""
        pass
    
    def send_whatsapp(phone: str, message: str):
        """Via Twilio WhatsApp API"""
        pass
    
    def send_sms(phone: str, message: str):
        """Via Twilio SMS"""
        pass
    
    def send_app_notification(customer_id: str, notification: dict):
        """Via WebSocket push to app"""
        pass
```

### **Alert Schema**

```json
{
  "id": "alert_123",
  "customer_id": "cust_001",
  "trigger_type": "recipe_failed",
  "severity": "error",
  "title": "Discovery Recipe Failed",
  "message": "Your lead discovery job failed after 3 retries. Error: API rate limit exceeded.",
  "context": {
    "recipe_id": "discovery",
    "execution_id": "exec_abc123",
    "error_code": "API_RATE_LIMIT"
  },
  "action_required": true,
  "suggested_action": "Upgrade your subscription plan for higher API limits",
  "created_at": "2025-12-14T10:35:00Z",
  "expires_at": "2025-12-15T10:35:00Z",
  "read": false
}
```

---

## 7. Mandatory Subscription Component

**Every Agent must include Subscription recipe with these responsibilities:**

1. **Credit Tracking:**
   - Log every action's cost
   - Deduct from customer's balance real-time
   - Prevent execution if insufficient credits

2. **Quota Enforcement:**
   - API call limits per subscription tier
   - Queue recipes when limit approached
   - Retry when quota resets

3. **Alerts:**
   - Notify when 80% consumed
   - Notify when limit exceeded
   - Notify 7 days before trial expiry
   - Notify upgrade opportunities

4. **Audit Trail:**
   - Log all credit deductions (per action, per lead)
   - Timestamp, customer_id, recipe_id, amount
   - Exportable for billing/analytics

5. **Multi-Tenant Isolation:**
   - Each customer's credits isolated
   - No cross-customer visibility
   - Separate rate limit buckets

---

## 8. Data Isolation & Multi-Tenancy

**Customer Isolation Rules:**

1. Every table has `customer_id` or accessed through customer relationship
2. Every query filters by `customer_id` at query level (not presentation)
3. Admin access logged with audit trail
4. Secrets encrypted per customer
5. State/context isolated per customer

```python
# ✓ CORRECT
def get_recipes(customer_id: str):
    return db.query(Recipe).filter(Recipe.customer_id == customer_id).all()

# ✗ WRONG
def get_recipes():
    return db.query(Recipe).all()  # Exposes all customers' recipes!
```

---

## 9. Admin Dashboard - Forensic & Runtime View

### **Admin Access Model**

Admin users have **view-only access to all agents, recipes, subscriptions across all customers** with complete audit trail.

```json
{
  "admin_access": {
    "view_all_customers": true,
    "view_all_agents": true,
    "view_all_recipes": true,
    "view_all_executions": true,
    "view_audit_logs": true,
    "modify_customer_data": false,
    "send_alerts": true,
    "access_logged": true,
    "audit_trail_required": true
  }
}
```

### **Admin Views**

**1. Customers & Subscriptions View**

```json
{
  "view": "admin_customers",
  "data": [
    {
      "customer_id": "cust_001",
      "company_name": "Apollo Dental Clinic",
      "subscription": {
        "plan_id": "professional",
        "status": "active",
        "started_at": "2025-11-01",
        "expires_at": "2025-12-01",
        "credits_total": 99.99,
        "credits_used": 42.50,
        "credits_remaining": 57.49,
        "agents_count": 3,
        "active_recipes": 12
      },
      "last_activity": "2025-12-14T10:46:00Z",
      "health_status": "healthy|warning|error",
      "alerts_active": 0
    }
  ]
}
```

**2. Agents by Customer View**

```json
{
  "view": "admin_agents",
  "customer_id": "cust_001",
  "data": [
    {
      "agent_id": "agent_001",
      "agent_name": "The Hunter - Lead Gen",
      "recipes_count": 5,
      "recipes": [
        {
          "recipe_id": "discovery",
          "name": "Discovery",
          "status": "active",
          "last_run": "2025-12-14T10:30:00Z",
          "success_rate": 0.96,
          "last_execution_status": "success"
        },
        {
          "recipe_id": "intelligence",
          "name": "Intelligence",
          "status": "active",
          "last_run": "2025-12-14T10:36:00Z",
          "success_rate": 0.93,
          "last_execution_status": "partial"
        }
      ],
      "configuration": {
        "execution_mode": "sequential",
        "max_retries": 3
      },
      "created_at": "2025-11-15",
      "modified_at": "2025-12-10"
    }
  ]
}
```

**3. Runtime Execution Monitor View**

```json
{
  "view": "admin_runtime",
  "filters": {
    "time_range": "last_24_hours",
    "status": "all|running|completed|failed",
    "customer_id": "all|specific"
  },
  "data": [
    {
      "execution_id": "exec_abc123",
      "customer_id": "cust_001",
      "agent_id": "agent_001",
      "recipe_sequence": ["discovery", "intelligence", "personalization", "outreach", "subscription"],
      "current_recipe": "personalization",
      "status": "running",
      "progress": {
        "started_at": "2025-12-14T10:30:00Z",
        "estimated_completion": "2025-12-14T10:47:00Z",
        "recipes_completed": 2,
        "recipes_total": 5,
        "percentage": 40
      },
      "metrics": {
        "records_processed_total": 195,
        "records_succeeded": 183,
        "records_failed": 12,
        "credits_consumed": 4.68,
        "api_calls_made": 378
      },
      "alerts": [
        {
          "recipe_id": "intelligence",
          "severity": "warning",
          "message": "Email enrichment confidence low for 5 records"
        }
      ]
    }
  ]
}
```

### **Forensic & Audit Logging**

Every action is immutable logged with complete context:

```json
{
  "audit_log_entry": {
    "id": "audit_123456",
    "timestamp": "2025-12-14T10:30:00Z",
    "actor": {
      "type": "system|customer|admin",
      "id": "cust_001|admin_user_123",
      "ip_address": "203.0.113.45",
      "user_agent": "Mozilla/5.0..."
    },
    "action": {
      "type": "recipe_executed|recipe_configured|credit_deducted|alert_triggered|admin_accessed",
      "resource": "agent|recipe|subscription",
      "resource_id": "agent_001|recipe_discovery"
    },
    "changes": {
      "before": {"credits": 99.99},
      "after": {"credits": 97.49},
      "delta": -2.50
    },
    "context": {
      "customer_id": "cust_001",
      "agent_id": "agent_001",
      "execution_id": "exec_abc123",
      "recipe_id": "intelligence"
    },
    "result": {
      "status": "success|failed|warning",
      "details": {...},
      "error_code": null
    },
    "admin_access": {
      "accessed_by": "admin_user_123",
      "access_reason": "customer_support|investigation|compliance",
      "accessed_at": "2025-12-14T14:20:00Z"
    }
  }
}
```

**Audit Log Searchability:**
- By timestamp (date range)
- By customer_id
- By agent_id
- By action_type
- By actor (who performed action)
- By resource_id
- By status (success/failed)
- By admin access (who viewed what)

### **Forensic Query Capabilities**

Admin can answer questions like:
- "Show me all agents for customer X"
- "Show me all recipes in agent Y"
- "Show me runtime status of all agents running now"
- "Show me all failed executions in last 24 hours"
- "Show me all credit deductions for customer X"
- "Show me who accessed customer Y's data and when"
- "Show me all admin accesses (with timestamp and access reason)"
- "Replay execution history for execution_id ABC"
- "Export audit trail for customer X (date range)"

### **Admin Audit Trail for Admin Actions**

When admin views customer data, it's logged:

```json
{
  "admin_audit_entry": {
    "id": "admin_audit_789",
    "timestamp": "2025-12-14T14:20:00Z",
    "admin_id": "admin_user_123",
    "action": "viewed_customer_agents",
    "customer_id": "cust_001",
    "resources_accessed": [
      "agent_001",
      "agent_002",
      "agent_003"
    ],
    "access_justification": "customer_support_ticket_123",
    "ip_address": "203.0.113.100",
    "duration_seconds": 45,
    "data_exported": false
  }
}
```

### **Real-Time Monitoring Dashboard**

```
┌─────────────────────────────────────────┐
│ ADMIN DASHBOARD - Live Execution View   │
├─────────────────────────────────────────┤
│                                         │
│ Active Executions: 7                    │
│ Customers: 23                           │
│ System Health: 99.8% uptime            │
│                                         │
│ ┌─ Running Jobs ──────────────────────┐ │
│ │ exec_abc123: Apollo Dental           │ │
│ │  └─ Discovery 40% [████░░░░░░]      │ │
│ │ exec_def456: SmileCare               │ │
│ │  └─ Intelligence 80% [████████░░]   │ │
│ │ exec_ghi789: MediDental              │ │
│ │  └─ Personalization 100% [██████]   │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─ Alerts (Last 24h) ────────────────┐ │
│ │ 🔴 3 Failed executions               │ │
│ │ 🟡 5 Low confidence emails           │ │
│ │ 🟢 12 Successful completions         │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─ Audit Log ────────────────────────┐ │
│ │ 14:20:00 admin_user_123 viewed...   │ │
│ │ 14:19:45 cust_001 executed recipe   │ │
│ │ 14:19:30 credits deducted: 2.50     │ │
│ │ [View Details] [Export Log]         │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### **Compliance & Data Retention**

- All audit logs immutable (append-only)
- Retention: 1 year minimum (configurable)
- Admin access requires justification/reason code
- Exported audit trails digitally signed
- Automated alerts on suspicious access patterns

---

## 9. AI Integration Strategy: The WOW Factor

### **Why AI? Customer Outcomes**

The Hunter's competitive advantage isn't automation—it's **intelligent personalization at scale**.

**Without AI (Generic Approach):**
- Template-based outreach (5-10% response rate)
- Spray-and-pray lead generation
- High unsubscribe rates
- Wasted credits on low-intent leads
- Compliance risk (SPAM reputation)

**With AI (The Hunter Approach - 3-5x Better):**
- Context-aware personalized messages (35-45% response rate)
- Smart lead qualification (skip low-quality before spend)
- Relevance-driven outreach (customer actually cares)
- Efficient credit spend (80%+ on qualified leads)
- Brand safety (professional, thoughtful engagement)

### **AI Model Selection & Costs**

| Recipe | AI Model | Purpose | Cost/Lead | Use Case |
|--------|----------|---------|-----------|----------|
| Discovery | Groq DeepSeek-lite | Lead scoring (fit, intent, maturity) | $0.01-0.02 | Filter noise early |
| Intelligence | Groq DeepSeek-lite | Smart routing (premium vs skip) | $0.01-0.02 | Optimize spend on hot leads |
| Personalization | Claude 3.5 Sonnet | Context-aware message generation | $0.03-0.05 | **DIFFERENTIATOR** |
| Outreach | GPT-4 Turbo | Draft optimization (rare) | $0.02-0.04 | Optional polish |
| **Total per Lead** | **Mixed** | **Quality + Speed** | **$0.07-0.12** | **500x margin at $4,999/mo** |

**Cost Justification:**
- Customer pays $4,999/month for 200 leads (discovery) → $25/lead
- AI cost: $0.10/lead
- Margin: 99.6% (250x ROI on AI spend)
- Response rates: 35-45% (vs 5-10% templates) = 4-9x better outcomes

### **The Hunter 5-Recipe AI Flow**

```
┌─ DISCOVERY (AI Scoring) ─────────────────────────────────┐
│ 1. Scrape candidates (Google Maps, LinkedIn, etc)        │
│ 2. AI scores: lead_score (0.0-1.0) on:                   │
│    - Industry fit (vs customer target)                    │
│    - Company size/maturity (vs deal sweet spot)           │
│    - Recent hiring/growth signals (intent)                │
│    - Decision maker seniority                             │
│ 3. Filter output: Only quality_tier >= "silver" (0.6+)   │
│ Output: 200 raw → 140 qualified leads                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─ INTELLIGENCE (Smart Routing) ────────────────────────────┐
│ 1. Enrich leads: email, phone, company profile            │
│ 2. AI decision:                                            │
│    - "Gold" leads (0.85+): Full enrichment (premium APIs) │
│    - "Silver" leads (0.60-0.85): Quick enrichment (free)  │
│    - Below 0.60: Skip (already filtered)                  │
│ 3. Route to next recipe                                   │
│ Cost Optimization: 60% less API spend on low-confidence   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─ PERSONALIZATION (AI as Differentiator) ──────────────────┐
│ 1. Fetch 5-10 data points:                                │
│    - Company news, recent funding, executive bios         │
│    - LinkedIn activity, hiring announcements              │
│    - Industry trends, market position                     │
│ 2. Claude/GPT-4 generates UNIQUE message:                 │
│    - NOT template ("Hi [First Name]...")                  │
│    - Context-aware ("I noticed you closed Series B...")   │
│    - Value prop aligned with their current challenge      │
│    - Specific ask (not generic)                           │
│ 3. QA: Score message relevance (0-1) before showing       │
│ Example Output:                                            │
│   "Hi Sarah - Saw Apollo Dental just opened 3 new         │
│    locations in CA. That rapid scaling typically creates  │
│    huge hiring & training bottlenecks. We've helped       │
│    50+ dental DSOs streamline onboarding. Worth 15 mins?" │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─ OUTREACH (Customer Review) ──────────────────────────────┐
│ 1. Prepare messages for customer review (NO AUTO-SEND)    │
│ 2. Compliance: Verify opt-in status, GDPR compliance      │
│ 3. Customer can edit, defer, or approve before send       │
│ 4. Track intent: Which messages customer chooses to send  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─ SUBSCRIPTION (Credit Tracking & Alerts) ────────────────┐
│ 1. Log every step: Discovery ($0.02), Intelligence        │
│    ($0.02), Personalization ($0.04) per lead              │
│ 2. Deduct: $0.08/lead from credits                        │
│ 3. Alert: "200 leads processed, $16 credits used"         │
│ 4. Next batch quota available when customer approves      │
└─────────────────────────────────────────────────────────────┘
```

### **AI Decision Points & Trade-offs**

**Decision 1: Discovery Scoring - Filter Early**
- **Question:** How aggressively filter low-quality leads?
- **Option A:** Strict (0.75+ threshold) = 50% leads, highest quality
- **Option B:** Balanced (0.60+ threshold) = 70% leads, good ROI
- **Option C:** Permissive (0.50+ threshold) = 90% leads, more volume
- **Recommendation:** Balanced (0.60+) - customer can adjust threshold
- **AI Cost:** $0.02/lead screened (negligible vs enrichment costs)

**Decision 2: Intelligence Routing - Spend Smart**
- **Question:** Which leads get premium enrichment APIs?
- **Option A:** All leads (expensive, $1-2 per lead enrichment)
- **Option B:** Top 50% by score (balanced, $0.50-1.00 avg)
- **Option C:** Top 20% only (lean, $0.02-0.04 avg, miss deals)
- **Recommendation:** Top 50% (gold + premium silver) - 80% of deals in top half
- **AI Cost:** $0.02 routing decision, saves $0.80 per lead on skip list

**Decision 3: Personalization - AI as Core Differentiator**
- **Question:** How critical is unique personalization vs templates?
- **Option A:** Every lead gets Claude personalization (max WOW, $0.04/lead)
- **Option B:** Gold leads Claude, others templated ($0.02 avg)
- **Option C:** All templated (cost $0, outcomes -80%)
- **Recommendation:** Every lead gets Claude ($0.04) - this IS the product
- **AI Cost:** $0.04/lead, drives 4-9x response rate improvement = $4k+ annual value per customer

**Decision 4: Message Ranking - Prioritization**
- **Question:** Which prospects should customer contact first?
- **AI Output:** Rank by relevance_score + lead_score
- **Example:** High-intent + high-confidence = contact today
- **Impact:** Customer focuses on highest-probability deals first
- **Cost:** Free (reuse scores from Discovery)

### **Complete Example: Single Lead Journey**

**Input:** Customer wants leads for dental DSOs in California

**Step 1: Discovery** (2.5 seconds, $0.02 cost)
```
Raw lead: "Sarah Chen, Apollo Dental, San Francisco"

AI Scoring:
- industry_fit: 0.95 (dental DSO ✓)
- company_maturity: 0.92 (Series B funded ✓)
- growth_signals: 0.88 (3 locations recently ✓)
- decision_maker: 0.90 (VP Operations ✓)

Result: lead_score = 0.91 (quality_tier: "gold")
Status: QUALIFIED → Pass to Intelligence
```

**Step 2: Intelligence** (4 seconds, $0.02 cost)
```
Score = 0.91 (gold lead)
Decision: Use premium enrichment APIs

Enriched data:
- Email: sarah.chen@apollodental.com
- Phone: +1-415-555-0123
- LinkedIn URL, company growth metrics, recent funding
- 5 employees hired in past month
- Recent blog post on "Scaling Operations"

Status: ENRICHED → Pass to Personalization
```

**Step 3: Personalization** (8 seconds, $0.04 cost)
```
Context provided to Claude:
- Company: Apollo Dental (Series B, 3 locations)
- Person: Sarah Chen (VP Operations)
- Recent signals: Rapid hiring, scaling blog post
- Customer's value prop: Onboarding automation

Generated Message:
"Hi Sarah – Congrats on the new CA locations. I saw 
you just hired 5 team members in the past month, 
which typically means onboarding chaos. We've helped 
50+ DSOs cut training time 60%. Worth a quick chat?"

Relevance score: 0.94 (personalized, specific, valuable)
Status: READY FOR REVIEW
```

**Step 4: Outreach** (0.5 seconds, $0 cost)
```
Customer reviews message:
[✓] "Great message, send it"
or
[ ] "Can I tweak this?"
or
[ ] "Not interested in this lead"

Status: AWAITING CUSTOMER DECISION
```

**Step 5: Subscription** (0.1 seconds, $0.08 total)
```
Credits logged:
- Discovery: -$0.02
- Intelligence: -$0.02
- Personalization: -$0.04
- Total: -$0.08 per lead

Customer credits: $500.00 → $499.92
Message: "Processed 1 lead (gold), used $0.08 credits"

Next batch available when customer confirms sends.
```

**Outcome Tracking:**
```
Message sent → Tracked response → 
If "Replied": Lead marked "hot" (future Discovery upweighting)
If "No reply": Analyzed why → Feed into model improvement
```

### **The WOW Expression**

**What customers say:**
> "These aren't generic templates. Each message feels like we spent an hour researching each lead. And we only contact the ones who actually fit."

**Why it works:**
1. **Personalization at scale** (not possible manually)
2. **Quality filtering** (saves time and money)
3. **Compliance-first** (customer controls outreach)
4. **Transparent costs** (exact credit spend per lead)
5. **Outcome tracking** (know what's working)

---

## 10. Implementation Priority

**Phase 1 (Core Framework):**
- Recipe execution engine (sequential mode)
- Standard JSON schema validation
- Generic component interfaces
- Secrets manager
- Audit logger (basic)

**Phase 2 (The Hunter Agent):**
- Discovery recipe (Google Maps scraper)
- Intelligence recipe (email enricher)
- Personalization recipe (LLM integration)
- Outreach recipe (draft generation)

**Phase 3 (Subscription & Alerts):**
- Subscription recipe (credit tracking)
- Alert system (email, app notifications)
- Rate limiter enforcement

**Phase 4 (Admin & Forensics):**
- Admin dashboard (customer/agent/recipe views)
- Forensic audit logging (complete)
- Runtime monitoring view
- Audit export & compliance

**Phase 5 (Advanced):**
- Parallel execution mode
- Error recovery & fallbacks
- A/B testing framework
- Multi-turn dialogue state management

---

**Ready for development.**
