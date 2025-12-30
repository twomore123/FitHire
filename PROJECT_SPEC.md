# FitHire v1 Project Specification

**Version:** 1.0
**Last Updated:** 2025-12-30
**Status:** Phase 0 - Pre-Development

---

## Table of Contents
1. [Product Requirements](#product-requirements)
2. [Engineering Design](#engineering-design)
3. [Phase 1 Scope](#phase-1-scope)
4. [Data Models](#data-models)
5. [FitScore Algorithm](#fitscore-algorithm)
6. [Success Criteria](#success-criteria)

---

# Product Requirements

## 1. Product Definition

### Purpose
FitHire is a decision-support platform that connects verified fitness professionals with relevant job opportunities using a deterministic FitScore ranking system. It helps clubs and studios identify aligned candidates while enabling coaches to discover roles that match their qualifications and values.

### Core Functionality
- **Structured Matching:** Compare coach profiles against job requirements across multiple dimensions (certifications, experience, availability, location, culture, engagement)
- **Deterministic Scoring:** Calculate transparent, explainable FitScores (0.0 to 1.0) using weighted criteria
- **Threshold-Based Display:** Show only above-threshold matches (top 20 max) to reduce noise
- **Multi-Level Access:** Support complex organizational hierarchies (Brand → Region → Location)
- **Human-Verified Quality:** Admin-verified certifications, tags, and performance videos ensure data integrity

### Jobs to Be Done

**For Coaches:**
- "Help me find roles that match my certifications and experience level"
- "Show me opportunities that align with my availability and location"
- "Connect me with studios that value my coaching style and cultural fit"
- "Let me know I'm qualified before I apply"

**For Hiring Managers:**
- "Help me discover qualified candidates who meet my requirements"
- "Rank applicants by objective criteria, not just resumes"
- "Filter for cultural alignment and availability overlap"
- "Focus my time on top-tier matches, not unqualified applicants"

**For Multi-Unit Operators:**
- "Manage hiring across multiple locations with appropriate access controls"
- "Maintain data isolation between brands while supporting regional oversight"
- "Scale hiring processes without losing quality or consistency"

---

## 2. Target Users

### Primary Personas

**Persona 1: Sarah (Fitness Coach)**
- **Background:** 3 years as group fitness instructor, NASM-CPT certified, specializes in HIIT and cycling
- **Goals:** Find full-time role at premium studio, values community-driven culture, needs weekend availability flexibility
- **Pain Points:** Wastes time applying to jobs she's underqualified for, unclear which studios match her style, can't showcase movement quality easily
- **Success Metric:** Sees 10-15 relevant job matches with clear fit explanations

**Persona 2: Michael (Studio Manager)**
- **Background:** Manages boutique cycling studio (3 locations), hires 5-10 instructors per quarter
- **Goals:** Hire instructors who embody high-energy brand culture, fill weekend AM slots, reduce time-to-hire
- **Pain Points:** Receives 100+ applications with varying quality, hard to assess culture fit from resumes, time-consuming phone screens
- **Success Metric:** Reviews top 20 ranked candidates with clear FitScore breakdowns, makes hiring decisions faster

**Persona 3: Jessica (Regional Director)**
- **Background:** Oversees 8 studios across Northeast region for national fitness brand
- **Goals:** Maintain consistent hiring quality across locations, support local managers, identify regional talent
- **Pain Points:** Each location has different hiring standards, can't see talent pipeline across region, hard to identify transferable candidates
- **Success Metric:** View regional candidate pool, support location managers with centralized quality control

---

## 3. Problems Solved

### For Coaches
❌ **Before FitHire:** Blind applications to 20+ studios, unclear qualification requirements, no feedback on fit
✅ **After FitHire:** See only relevant matches above threshold, understand why they're a good fit, showcase verified skills

### For Hiring Managers
❌ **Before FitHire:** Manual resume screening, subjective culture assessment, time-consuming outreach
✅ **After FitHire:** Pre-ranked candidates by objective criteria, culture tags visible, focus on top 20 matches

### For Multi-Unit Operators
❌ **Before FitHire:** Fragmented hiring across locations, inconsistent standards, no cross-region visibility
✅ **After FitHire:** Centralized talent pool with scoped access, consistent FitScore methodology, regional oversight

---

## 4. What the Product Does

### Core Workflows

#### Workflow 1: Coach Views Job Matches
1. Coach completes profile (certifications, experience, availability, location, optional video)
2. Admin verifies certifications and tags performance video (if uploaded)
3. Coach logs in and views dashboard
4. System calculates FitScore for all active jobs within their brand scope
5. Coach sees top 20 matches above threshold (e.g., 0.60+), sorted by FitScore
6. Each match shows: Job title, FitScore, key alignment factors (e.g., "✓ Required certs met, ✓ 3/3 availability slots match")
7. Coach clicks to view full job details

#### Workflow 2: Hiring Manager Views Candidates
1. Hiring manager creates job listing (role type, requirements, schedule, culture tags, weighting preset)
2. System calculates FitScore for all coaches with complete profiles
3. Manager views top 20 candidates above threshold, sorted by FitScore
4. Each candidate shows: Name, FitScore, certification summary, verified video link
5. Manager filters by location, availability, or experience level
6. Manager clicks to view full coach profile

#### Workflow 3: Admin Verifies Coach
1. Coach submits profile with certification details and optional performance video
2. Admin reviews certification documentation (license number, expiration date)
3. Admin marks certification as "verified" or requests correction
4. If video uploaded, admin watches and assigns tags (e.g., "high-energy", "technical-precision", "community-focused")
5. Admin approves profile → coach now appears in searches

---

## 5. Functional Requirements (Phase 1)

### Must Have (Phase 1)
- ✅ Coach profile creation with required fields (name, email, location, certifications, experience, availability)
- ✅ Job listing creation with required fields (title, role type, location, required certs, min experience, availability, preset)
- ✅ Admin verification workflow for certifications and manual tagging
- ✅ FitScore calculation using embedded synchronous engine
- ✅ Top 20 matches display for coaches (above threshold)
- ✅ Top 20 candidates display for hiring managers (above threshold)
- ✅ Threshold filtering (default 0.60, adjustable by manager between 0.40-0.80)
- ✅ Multi-unit hierarchy (Brand → Region → Location) with scoped access
- ✅ Four weighting presets (Balanced, Experience-Heavy, Culture-Heavy, Availability-Focused)
- ✅ Basic filtering (by location, role type, availability)
- ✅ Authentication and role-based access control (via Clerk + custom DB roles)

### Nice to Have (Phase 1)
- 🟡 Profile completeness indicator (encourages coaches to add optional fields)
- 🟡 Admin dashboard showing pending verifications
- 🟡 Simple FitScore explanation tooltip (e.g., "85% match: Strong certification and culture alignment")

### Explicitly Out of Scope (Phase 1)
- ❌ Engagement score decay over time (Phase 2)
- ❌ Async background workers for score recalculation (Phase 2)
- ❌ Application/hiring workflow (apply button, status tracking) (Phase 3)
- ❌ Messaging between coaches and managers (Phase 3)
- ❌ Email notifications (Phase 3)
- ❌ Advanced analytics and reporting (Phase 4)
- ❌ AI-powered video analysis (v2 - Gemini integration planned)
- ❌ Predictive performance or retention modeling (out of v1 entirely)

---

## 6. User Roles & Permissions

### Role Definitions

| Role | Access Scope | Permissions |
|------|-------------|-------------|
| **Coach** | Own profile only | Create/edit profile, view own matches, view job details |
| **Location Manager** | Single location | Create jobs for location, view candidates for location jobs, verify coaches applying to location |
| **Regional Director** | All locations in region | View all jobs in region, view all candidates across region, support location managers |
| **Brand Admin** | Entire brand | Full access to all regions/locations, manage hierarchy, approve admins, configure presets |
| **Platform Admin** | All brands | System-wide access, manage brands, view all data, configure global settings |

### Access Control Rules
- All data scoped by `brand_id` at database level
- Users can only query data within their brand unless Platform Admin
- Regional Directors can view but not modify location-specific jobs (read-only across region)
- Location Managers can only create/edit jobs for their assigned location
- Coaches can only see jobs from brands they've applied to or been invited by

---

# Engineering Design

## 1. Tech Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (async, auto-generated OpenAPI docs)
- **ORM:** SQLAlchemy 2.0 (declarative models, async support)
- **Validation:** Pydantic v2 (type safety, data validation)
- **Database:** PostgreSQL 15+ (relational, JSONB support for flexible fields)
- **Migrations:** Alembic (SQLAlchemy migration tool)
- **Testing:** pytest, pytest-asyncio, coverage
- **Deployment:** Railway (managed hosting, includes Redis for Phase 2)

### Frontend
- **Framework:** Next.js 14+ (App Router, React Server Components)
- **Styling:** Tailwind CSS (utility-first, rapid development)
- **Components:** shadcn/ui (accessible, customizable components)
- **State Management:** React Context + Zustand (simple state, no Redux overhead)
- **Forms:** React Hook Form + Zod (validation matching backend Pydantic schemas)
- **API Client:** Native fetch with typed interfaces
- **Deployment:** Vercel (automatic deployments, edge functions)

### Database
- **Hosting:** Neon (serverless PostgreSQL, autoscaling, generous free tier)
- **Backup Strategy:** Neon automated daily backups + point-in-time recovery
- **Connection Pooling:** SQLAlchemy async engine + Neon pooling

### Authentication
- **Provider:** Clerk (organizations, multi-tenant, webhooks)
- **Strategy:** Clerk handles auth only, all roles/hierarchy in database
- **Session Management:** JWT tokens via Clerk, validated in FastAPI middleware

### File Storage
- **Provider:** Cloudflare R2 (S3-compatible, zero egress fees)
- **Use Cases:** Coach performance videos, profile images, certification documents
- **Access:** Presigned URLs for direct browser uploads, signed URLs for viewing
- **CDN:** Cloudflare CDN (automatic, included with R2)

### Future ML/DS Stack (Phase 2+)
- **Data Processing:** pandas, numpy
- **ML Framework:** scikit-learn (initial models), PyTorch (advanced models)
- **Video Analysis:** Google Gemini API (planned v2 feature)
- **Job Queue:** Celery + Redis (async task processing)
- **Experiment Tracking:** MLflow or Weights & Biases

---

## 2. Architecture Overview

### System Architecture (Phase 1)

```
┌─────────────────────────────────────────────────────────────┐
│                         User Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Next.js Frontend (Vercel)                                  │
│  - Coach Dashboard   - Manager Dashboard   - Admin Panel    │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTPS/REST API
                 ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Railway)                      │
├─────────────────────────────────────────────────────────────┤
│  Authentication Middleware (Clerk JWT validation)           │
│  ├─── /api/v1/coaches      (CRUD, matches)                  │
│  ├─── /api/v1/jobs         (CRUD, candidates)               │
│  ├─── /api/v1/admin        (verification, tagging)          │
│  └─── FitScore Engine      (embedded calculation)           │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
             ▼                       ▼
┌─────────────────────┐   ┌──────────────────────┐
│  PostgreSQL (Neon)  │   │  Cloudflare R2       │
│  - Coaches          │   │  - Videos            │
│  - Jobs             │   │  - Images            │
│  - Matches          │   │  - Docs              │
│  - Audit Logs       │   │                      │
└─────────────────────┘   └──────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Clerk (Auth Provider)                     │
│  - User Authentication   - Session Management                │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: FitScore Calculation (Phase 1)

```
1. Coach updates profile
   ↓
2. API validates with Pydantic
   ↓
3. Save to PostgreSQL
   ↓
4. When manager views candidates for job:
   ↓
5. Query all coaches in brand scope
   ↓
6. For each coach:
   FitScoreEngine.calculate_match(coach, job, preset)
   ↓
7. Filter: score >= threshold
   ↓
8. Sort by score DESC
   ↓
9. Return top 20 matches
   ↓
10. Frontend displays with explanations
```

---

## 3. Database Schema (Phase 1)

### Core Entities

#### Brands
```sql
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Regions
```sql
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(brand_id, slug)
);
```

#### Locations
```sql
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    region_id INTEGER NOT NULL REFERENCES regions(id),
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
    brand_id INTEGER REFERENCES brands(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL, -- 'coach', 'location_manager', 'regional_director', 'brand_admin'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### User Scopes (for Regional/Location access)
```sql
CREATE TABLE user_scopes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    scope_type VARCHAR(50) NOT NULL, -- 'region', 'location'
    scope_id INTEGER NOT NULL, -- region_id or location_id
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, scope_type, scope_id)
);
```

#### Coaches
```sql
CREATE TABLE coaches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
    brand_id INTEGER NOT NULL REFERENCES brands(id),

    -- Basic Info
    bio TEXT,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,

    -- Experience
    years_experience INTEGER NOT NULL,
    certifications JSONB NOT NULL, -- [{"name": "NASM-CPT", "verified": true, "expiration": "2025-12-31"}]
    specialties JSONB, -- ["HIIT", "Cycling", "Strength Training"]

    -- Availability (stored as array of time slots)
    available_times JSONB NOT NULL, -- ["Mon AM", "Wed PM", "Fri AM", "Sat AM"]

    -- Culture/Style Tags (admin-assigned)
    lifestyle_tags JSONB, -- ["wellness", "community", "high-energy"]
    movement_tags JSONB, -- ["technical-precision", "dynamic-flow"]
    instruction_tags JSONB, -- ["motivational", "educational", "hands-on"]

    -- Media
    profile_image_url VARCHAR(500),
    verified_video_url VARCHAR(500),
    social_links JSONB, -- {"instagram": "...", "youtube": "..."}

    -- Metadata
    profile_completeness DECIMAL(3,2), -- 0.00 to 1.00
    verified_at TIMESTAMP,
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),

    -- Indexes
    CONSTRAINT coaches_brand_fk FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE INDEX idx_coaches_brand_city ON coaches(brand_id, city);
CREATE INDEX idx_coaches_completeness ON coaches(profile_completeness);
```

#### Jobs
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    location_id INTEGER NOT NULL REFERENCES locations(id),
    created_by INTEGER NOT NULL REFERENCES users(id),

    -- Job Details
    title VARCHAR(255) NOT NULL,
    role_type VARCHAR(100) NOT NULL, -- 'group_fitness_instructor', 'personal_trainer', 'yoga_instructor', 'pilates_instructor'
    description TEXT,

    -- Requirements
    required_certifications JSONB NOT NULL, -- ["NASM-CPT", "ACE"]
    preferred_certifications JSONB, -- ["RYT-200"]
    min_experience INTEGER NOT NULL, -- years
    required_availability JSONB NOT NULL, -- ["Mon AM", "Wed PM", "Fri AM"]

    -- Location
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,

    -- Culture
    culture_tags JSONB, -- ["community", "high-energy", "wellness"]

    -- Scoring
    weighting_preset VARCHAR(50) NOT NULL DEFAULT 'balanced', -- 'balanced', 'experience_heavy', 'culture_heavy', 'availability_focused'
    fitscore_threshold DECIMAL(3,2) DEFAULT 0.60, -- 0.00 to 1.00

    -- Compensation (optional, not used in scoring v1)
    compensation_min INTEGER,
    compensation_max INTEGER,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT jobs_brand_fk FOREIGN KEY (brand_id) REFERENCES brands(id),
    CONSTRAINT jobs_location_fk FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE INDEX idx_jobs_brand_active ON jobs(brand_id, is_active);
CREATE INDEX idx_jobs_location_active ON jobs(location_id, is_active);
CREATE INDEX idx_jobs_role_type ON jobs(role_type);
```

#### Matches (Pre-calculated scores - Phase 2, but schema ready)
```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    coach_id INTEGER NOT NULL REFERENCES coaches(id),
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    brand_id INTEGER NOT NULL REFERENCES brands(id),

    -- Score
    fitscore DECIMAL(5,3) NOT NULL, -- 0.000 to 1.000

    -- Sub-scores (for explanation)
    cert_score DECIMAL(3,2),
    experience_score DECIMAL(3,2),
    availability_score DECIMAL(3,2),
    location_score DECIMAL(3,2),
    culture_score DECIMAL(3,2),
    engagement_score DECIMAL(3,2),

    -- Metadata
    calculated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(coach_id, job_id),
    CONSTRAINT matches_brand_fk FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE INDEX idx_matches_job_score ON matches(job_id, fitscore DESC);
CREATE INDEX idx_matches_coach_score ON matches(coach_id, fitscore DESC);
```

#### Audit Logs
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    user_id INTEGER REFERENCES users(id),

    -- Event Details
    event_type VARCHAR(100) NOT NULL, -- 'profile_updated', 'job_created', 'match_viewed', 'score_recalculated'
    entity_type VARCHAR(50), -- 'coach', 'job', 'match'
    entity_id INTEGER,

    -- Changes (JSONB for flexibility)
    changes JSONB, -- {"old_score": 0.75, "new_score": 0.82, "reason": "certification_added"}

    -- Metadata
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(50)
);

CREATE INDEX idx_audit_brand_timestamp ON audit_logs(brand_id, timestamp DESC);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
```

#### Match Events (for future ML)
```sql
CREATE TABLE match_events (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id),
    coach_id INTEGER NOT NULL REFERENCES coaches(id),
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    brand_id INTEGER NOT NULL REFERENCES brands(id),

    -- Event
    event VARCHAR(50) NOT NULL, -- 'viewed', 'applied', 'interviewed', 'hired', 'rejected'
    fitscore_at_event DECIMAL(5,3), -- Score when event occurred

    -- Actor
    triggered_by INTEGER REFERENCES users(id), -- Who caused this event

    -- Metadata
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_match_events_job ON match_events(job_id, timestamp DESC);
CREATE INDEX idx_match_events_coach ON match_events(coach_id, timestamp DESC);
```

---

## 4. API Design (Phase 1)

### API Structure
```
/api/v1/
  ├── /auth/          # Clerk webhook handlers
  ├── /coaches/       # Coach CRUD + matches
  ├── /jobs/          # Job CRUD + candidates
  ├── /admin/         # Verification, tagging
  ├── /brands/        # Brand/Region/Location management
  └── /health/        # Health check
```

### Key Endpoints

#### Coach Endpoints
```python
GET    /api/v1/coaches/{coach_id}                # Get coach profile
POST   /api/v1/coaches                           # Create coach profile
PATCH  /api/v1/coaches/{coach_id}                # Update coach profile
GET    /api/v1/coaches/{coach_id}/matches        # Get top job matches
POST   /api/v1/coaches/{coach_id}/upload-video   # Get presigned URL for video upload
```

#### Job Endpoints
```python
GET    /api/v1/jobs/{job_id}                     # Get job details
POST   /api/v1/jobs                              # Create job listing
PATCH  /api/v1/jobs/{job_id}                     # Update job listing
DELETE /api/v1/jobs/{job_id}                     # Deactivate job
GET    /api/v1/jobs/{job_id}/candidates          # Get top coach matches
```

#### Admin Endpoints
```python
GET    /api/v1/admin/pending-verifications       # List coaches awaiting verification
POST   /api/v1/admin/verify-certification        # Verify a certification
POST   /api/v1/admin/tag-video                   # Add tags to performance video
PATCH  /api/v1/admin/coaches/{coach_id}/approve  # Approve coach profile
```

#### Brand Management
```python
GET    /api/v1/brands                            # List brands (scoped by user)
GET    /api/v1/brands/{brand_id}/regions         # List regions in brand
GET    /api/v1/brands/{brand_id}/locations       # List locations in brand
POST   /api/v1/brands                            # Create brand (platform admin only)
```

### Request/Response Examples

#### POST /api/v1/coaches
```json
// Request
{
  "bio": "Passionate group fitness instructor specializing in HIIT and cycling.",
  "city": "New York",
  "state": "NY",
  "years_experience": 3,
  "certifications": [
    {"name": "NASM-CPT", "expiration": "2025-12-31"},
    {"name": "ACE", "expiration": "2026-06-15"}
  ],
  "specialties": ["HIIT", "Cycling", "Strength Training"],
  "available_times": ["Mon AM", "Wed PM", "Fri AM", "Sat AM"]
}

// Response
{
  "id": 42,
  "user_id": 123,
  "brand_id": 1,
  "profile_completeness": 0.75,
  "verified_at": null,
  "created_at": "2025-12-30T10:30:00Z"
}
```

#### GET /api/v1/coaches/42/matches
```json
// Response
{
  "matches": [
    {
      "job_id": 15,
      "title": "Weekend Morning HIIT Instructor",
      "location": "NYC Tribeca",
      "fitscore": 0.87,
      "explanation": {
        "strengths": [
          "All required certifications met",
          "3/3 availability slots match",
          "Strong culture alignment (community, high-energy)"
        ],
        "gaps": []
      },
      "details": {
        "role_type": "group_fitness_instructor",
        "required_certifications": ["NASM-CPT"],
        "required_availability": ["Sat AM", "Sun AM"]
      }
    },
    {
      "job_id": 22,
      "title": "Cycling Instructor - Multiple Locations",
      "location": "NYC Upper West Side",
      "fitscore": 0.82,
      "explanation": {
        "strengths": [
          "Cycling specialty matches job focus",
          "Required certifications met"
        ],
        "gaps": [
          "Only 1/3 availability slots match"
        ]
      }
    }
  ],
  "total_above_threshold": 12,
  "threshold": 0.60
}
```

---

## 5. FitScore Algorithm Specification

### Weighting Presets

```python
WEIGHTING_PRESETS = {
    "balanced": {
        "certifications": 0.25,
        "experience": 0.20,
        "availability": 0.15,
        "location": 0.15,
        "cultural_fit": 0.15,
        "engagement": 0.10
    },
    "experience_heavy": {
        "certifications": 0.20,
        "experience": 0.35,
        "availability": 0.10,
        "location": 0.10,
        "cultural_fit": 0.15,
        "engagement": 0.10
    },
    "culture_heavy": {
        "certifications": 0.15,
        "experience": 0.15,
        "availability": 0.10,
        "location": 0.10,
        "cultural_fit": 0.40,
        "engagement": 0.10
    },
    "availability_focused": {
        "certifications": 0.20,
        "experience": 0.15,
        "availability": 0.35,
        "location": 0.10,
        "cultural_fit": 0.10,
        "engagement": 0.10
    }
}
```

### Scoring Functions (Detailed Logic)

#### 1. Certification Score (0.0 to 1.0)
```python
def score_certifications(coach: Coach, job: Job) -> float:
    """
    Required certs: MUST have all (else return 0.0)
    Preferred certs: Bonus points for each matched

    Base score: 0.7 (has all required)
    Bonus: +0.3 max (for preferred certs)
    """
    required = set(job.required_certifications)
    preferred = set(job.preferred_certifications or [])
    coach_certs = set([c['name'] for c in coach.certifications])

    # Must have all required
    if not required.issubset(coach_certs):
        return 0.0

    # Calculate preferred match percentage
    if preferred:
        preferred_match = len(coach_certs & preferred) / len(preferred)
        bonus = 0.3 * preferred_match
    else:
        bonus = 0.0

    return 0.7 + bonus
```

#### 2. Experience Score (0.0 to 1.0)
```python
def score_experience(coach: Coach, job: Job) -> float:
    """
    Min experience: MUST meet (else return 0.0)
    Years over min: Diminishing returns (max +0.3 for 10+ years over)

    Base score: 0.7 (meets minimum)
    Bonus: +0.3 max (for additional experience)
    """
    if coach.years_experience < job.min_experience:
        return 0.0

    years_over = coach.years_experience - job.min_experience
    bonus = min(years_over / 10, 0.3)  # Cap at 0.3

    return 0.7 + bonus
```

#### 3. Availability Score (0.0 to 1.0)
```python
def score_availability(coach: Coach, job: Job) -> float:
    """
    Required slots: MUST cover all (else return 0.0)
    Extra availability: Bonus for flexibility

    Base score: 0.7 (covers all required)
    Bonus: +0.3 max (for extra flexibility)
    """
    required_slots = set(job.required_availability)
    coach_slots = set(coach.available_times)

    # Must cover all required slots
    if not required_slots.issubset(coach_slots):
        return 0.0

    # Bonus for additional availability
    extra_slots = len(coach_slots - required_slots)
    flexibility_bonus = min(extra_slots / 10, 0.3)

    return 0.7 + flexibility_bonus
```

#### 4. Location Score (0.0 to 1.0)
```python
def score_location(coach: Coach, job: Job) -> float:
    """
    Phase 1: Simple city match
    Same city = 1.0
    Different city = 0.0

    Phase 2+: Add distance calculation with graduated scoring
    """
    if coach.city.lower() == job.city.lower() and coach.state == job.state:
        return 1.0
    else:
        return 0.0
```

#### 5. Cultural Fit Score (0.0 to 1.0)
```python
def score_culture(coach: Coach, job: Job) -> float:
    """
    Compare lifestyle/style tags assigned by admins
    Tag overlap percentage = score

    No job culture tags = 1.0 (no requirements)
    """
    job_tags = set(job.culture_tags or [])

    if not job_tags:
        return 1.0  # No culture requirements

    coach_tags = set(coach.lifestyle_tags or [])
    overlap = coach_tags & job_tags

    return len(overlap) / len(job_tags)
```

#### 6. Engagement Score (0.0 to 1.0)
```python
def score_engagement(coach: Coach) -> float:
    """
    Base: 0.5
    + Profile completeness (90%+ = +0.2)
    + Recently updated (<30 days = +0.2)
    + Verified video (+0.1)

    Max: 1.0
    """
    score = 0.5

    # Profile completeness bonus
    if coach.profile_completeness >= 0.9:
        score += 0.2

    # Recent activity bonus
    if coach.last_updated > (datetime.now() - timedelta(days=30)):
        score += 0.2

    # Verified video bonus
    if coach.verified_video_url:
        score += 0.1

    return min(score, 1.0)
```

### Complete FitScore Calculation

```python
class FitScoreEngine:
    def calculate_match(self, coach: Coach, job: Job) -> MatchScore:
        """
        Calculate weighted FitScore (0.0 to 1.0)
        Returns detailed breakdown for explanations
        """
        preset = WEIGHTING_PRESETS[job.weighting_preset]

        # Calculate sub-scores
        cert_score = self.score_certifications(coach, job)
        exp_score = self.score_experience(coach, job)
        avail_score = self.score_availability(coach, job)
        loc_score = self.score_location(coach, job)
        culture_score = self.score_culture(coach, job)
        engage_score = self.score_engagement(coach)

        # Weighted sum
        fitscore = (
            preset["certifications"] * cert_score +
            preset["experience"] * exp_score +
            preset["availability"] * avail_score +
            preset["location"] * loc_score +
            preset["cultural_fit"] * culture_score +
            preset["engagement"] * engage_score
        )

        return MatchScore(
            fitscore=round(fitscore, 3),
            cert_score=cert_score,
            experience_score=exp_score,
            availability_score=avail_score,
            location_score=loc_score,
            culture_score=culture_score,
            engagement_score=engage_score
        )
```

---

## 6. Authentication & Authorization

### Clerk Integration

#### User Registration Flow
1. User signs up via Clerk (email/password or OAuth)
2. Clerk webhook fires → POST /api/v1/auth/webhook
3. Backend creates User record with `clerk_user_id`
4. User selects role (coach, manager) during onboarding
5. Frontend redirects to role-specific dashboard

#### Authorization Middleware
```python
from fastapi import Depends, HTTPException
from clerk_sdk import Clerk

clerk = Clerk(api_key=settings.CLERK_SECRET_KEY)

async def get_current_user(authorization: str = Header(...)) -> User:
    """Validate Clerk JWT and return User"""
    try:
        # Verify JWT
        session = clerk.sessions.verify_token(authorization)

        # Get user from database
        user = await db.get_user_by_clerk_id(session.user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_role(*allowed_roles: str):
    """Decorator to enforce role-based access"""
    def decorator(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return decorator
```

#### Usage in Routes
```python
@router.get("/jobs/{job_id}/candidates")
async def get_candidates(
    job_id: int,
    user: User = Depends(require_role("location_manager", "regional_director", "brand_admin"))
):
    """Only managers can view candidates"""
    # Verify user has access to this job's location/region/brand
    job = await db.get_job(job_id)

    if not user.has_access_to_job(job):
        raise HTTPException(status_code=403, detail="No access to this job")

    # ... return candidates
```

### Access Control Logic

```python
class User:
    def has_access_to_job(self, job: Job) -> bool:
        """Check if user can access this job"""
        if self.role == "brand_admin":
            return self.brand_id == job.brand_id

        elif self.role == "regional_director":
            # Check if job's location is in user's region(s)
            user_regions = [scope.scope_id for scope in self.scopes if scope.scope_type == "region"]
            return job.location.region_id in user_regions

        elif self.role == "location_manager":
            # Check if job is at user's location(s)
            user_locations = [scope.scope_id for scope in self.scopes if scope.scope_type == "location"]
            return job.location_id in user_locations

        return False

    def can_create_job_at_location(self, location_id: int) -> bool:
        """Check if user can create jobs at this location"""
        if self.role == "brand_admin":
            location = db.get_location(location_id)
            return self.brand_id == location.brand_id

        elif self.role == "location_manager":
            user_locations = [scope.scope_id for scope in self.scopes if scope.scope_type == "location"]
            return location_id in user_locations

        return False
```

---

## 7. File Upload Strategy

### Cloudflare R2 Setup

```python
import boto3
from botocore.config import Config

# R2 client (S3-compatible)
s3_client = boto3.client(
    's3',
    endpoint_url=settings.R2_ENDPOINT,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)

BUCKET_NAME = "fithire-media"
```

### Upload Flow (Presigned URLs)

```python
@router.post("/coaches/{coach_id}/upload-video")
async def get_video_upload_url(
    coach_id: int,
    filename: str,
    content_type: str,
    user: User = Depends(get_current_user)
):
    """
    Generate presigned URL for direct browser upload to R2
    """
    # Verify user owns this coach profile
    if user.role != "coach" or user.id != coach_id:
        raise HTTPException(status_code=403)

    # Generate unique key
    file_key = f"coaches/{coach_id}/videos/{uuid.uuid4()}_{filename}"

    # Generate presigned POST URL (browser uploads directly to R2)
    presigned_post = s3_client.generate_presigned_post(
        Bucket=BUCKET_NAME,
        Key=file_key,
        Fields={"Content-Type": content_type},
        Conditions=[
            {"Content-Type": content_type},
            ["content-length-range", 0, 500_000_000]  # Max 500MB
        ],
        ExpiresIn=3600  # 1 hour
    )

    return {
        "upload_url": presigned_post["url"],
        "fields": presigned_post["fields"],
        "file_key": file_key
    }

@router.post("/coaches/{coach_id}/confirm-video-upload")
async def confirm_video_upload(
    coach_id: int,
    file_key: str,
    user: User = Depends(get_current_user)
):
    """
    After successful upload, save video URL to coach profile
    """
    # Generate signed URL for viewing (expires in 1 year)
    signed_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': file_key},
        ExpiresIn=31_536_000  # 1 year
    )

    # Update coach profile
    await db.update_coach(coach_id, verified_video_url=signed_url)

    return {"video_url": signed_url}
```

---

# Phase 1 Scope

## Phase 1 Deliverables (2-Day Build)

### Day 1: Backend Foundation
- ✅ Monorepo structure setup
- ✅ Database schema created (Alembic migrations)
- ✅ FastAPI project structure
- ✅ Clerk authentication middleware
- ✅ Core models (Coach, Job, User, Brand, Region, Location)
- ✅ FitScore engine implementation (all 6 sub-scores)
- ✅ Unit tests for FitScore engine
- ✅ Coach CRUD endpoints
- ✅ Job CRUD endpoints
- ✅ Matching endpoints (coaches/{id}/matches, jobs/{id}/candidates)

### Day 2: Frontend + Integration
- ✅ Next.js project setup with shadcn/ui
- ✅ Clerk authentication integration
- ✅ Coach dashboard (view profile, see matches)
- ✅ Manager dashboard (create jobs, view candidates)
- ✅ Basic admin panel (pending verifications list)
- ✅ Profile creation forms (Coach, Job)
- ✅ Match display with FitScore + explanations
- ✅ Filtering UI (location, role type, availability)
- ✅ Deploy backend to Railway
- ✅ Deploy frontend to Vercel
- ✅ E2E smoke test (create profile → create job → see match)

---

## Phase 1 MVP Features

### Coach Features
1. **Profile Creation**
   - Name, location, bio
   - Certifications (select from dropdown: NASM-CPT, ACE, ACSM, RYT-200, RYT-500, PMA, STOTT)
   - Years of experience (number input)
   - Availability (multi-select: Mon AM/PM, Tue AM/PM, Wed AM/PM, Thu AM/PM, Fri AM/PM, Sat AM/PM, Sun AM/PM)
   - Specialties (multi-select: HIIT, Cycling, Yoga, Pilates, Strength Training, etc.)
   - Optional: Bio, social links

2. **View Matches**
   - See top 20 jobs sorted by FitScore
   - Filter by location, role type
   - Each match shows:
     - Job title, location, role type
     - FitScore (as percentage, e.g., "87% Match")
     - Key strengths (e.g., "✓ Required certs met, ✓ 3/3 availability slots")
     - Gaps (e.g., "⚠ Only 1/3 culture tags match")

3. **Profile Management**
   - Edit profile (updates trigger FitScore recalculation on next match view)
   - View profile completeness percentage
   - See verification status (pending, verified)

### Hiring Manager Features
1. **Job Posting**
   - Job title, role type (select: Group Fitness Instructor, Personal Trainer, Yoga Instructor, Pilates Instructor)
   - Location (select from user's accessible locations)
   - Required certifications (multi-select)
   - Preferred certifications (multi-select)
   - Min experience (years)
   - Required availability (multi-select time slots)
   - Culture tags (multi-select: community, high-energy, wellness, technical-precision, etc.)
   - Weighting preset (select: Balanced, Experience-Heavy, Culture-Heavy, Availability-Focused)
   - FitScore threshold (slider: 0.40 to 0.80, default 0.60)

2. **View Candidates**
   - See top 20 coaches sorted by FitScore
   - Filter by location, certifications, experience, availability
   - Each candidate shows:
     - Name, photo, location
     - FitScore (as percentage)
     - Certification summary
     - Years of experience
     - Availability overlap visual
     - Link to verified video (if uploaded)

3. **Job Management**
   - Edit job posting (triggers recalculation)
   - Deactivate job (removes from coach searches)
   - View applicant pipeline (Phase 2 feature - placeholder UI)

### Admin Features
1. **Verification Queue**
   - List of coaches pending verification
   - View certification details, documentation
   - Approve or request corrections
   - Mark certifications as "verified"

2. **Video Tagging** (Manual - Phase 1)
   - Watch uploaded performance videos
   - Assign tags:
     - Movement quality: technical-precision, dynamic-flow, creative
     - Instruction style: motivational, educational, hands-on
     - Lifestyle: wellness, community, high-energy
   - Save tags to coach profile

3. **Brand Management**
   - Create brands, regions, locations
   - Assign users to roles and scopes

---

## Phase 1 Exclusions (Explicitly NOT Building)

### Deferred to Phase 2+
- ❌ Engagement score decay (profile staleness penalty)
- ❌ Async background workers (Celery)
- ❌ Pre-calculated matches table (calculate on-demand only)
- ❌ Email notifications
- ❌ Application workflow (apply button, status tracking)
- ❌ Messaging between coaches and managers
- ❌ Advanced analytics dashboard
- ❌ Distance-based location scoring (just city match)
- ❌ Role-specific custom scoring (all roles use standard FitScore)

### Out of v1 Entirely
- ❌ AI video analysis (Gemini integration planned for v2)
- ❌ Predictive performance modeling
- ❌ Automated hiring recommendations
- ❌ Social media scraping
- ❌ Unlimited match lists (cap at top 20)

---

# Success Criteria

## Phase 1 Success Metrics

### Functional Completeness
- [ ] Coach can create complete profile with all required fields
- [ ] Manager can create job posting with all required fields
- [ ] FitScore calculation returns logical scores (0.0 to 1.0)
- [ ] Top 20 matches displayed correctly (sorted by FitScore DESC)
- [ ] Threshold filtering works (only shows scores >= threshold)
- [ ] Multi-unit access control enforced (users can't see other brands' data)
- [ ] Admin can verify certifications and tag videos
- [ ] Filters work (location, role type, availability)

### Quality Checks
- [ ] FitScore engine has 70%+ test coverage
- [ ] All required certifications met → score > 0 for cert component
- [ ] Missing required certification → total FitScore = 0
- [ ] Same city → location score = 1.0
- [ ] Different city → location score = 0.0
- [ ] All 4 weighting presets produce different scores for same coach/job pair

### User Experience
- [ ] Forms validate inputs (Zod schemas match Pydantic)
- [ ] Error messages are clear and actionable
- [ ] Match explanations are understandable (non-technical language)
- [ ] Dashboard loads in <2 seconds (with 50 coaches/jobs)
- [ ] Mobile-responsive UI (Tailwind CSS)

### Deployment
- [ ] Backend deployed to Railway with PostgreSQL
- [ ] Frontend deployed to Vercel with custom domain
- [ ] Environment variables secured (no secrets in code)
- [ ] Database migrations run successfully
- [ ] Health check endpoint returns 200 OK

---

## Long-Term Success Indicators (Post-Phase 1)

### Business Metrics (Phase 2+)
- High-FitScore matches lead to more applications
- Managers spend less time reviewing unqualified candidates
- Time-to-hire decreases for roles using FitScore
- Coach retention higher when hired via high FitScore match

### Technical Metrics (Phase 2+)
- API response time <500ms for match queries
- Database query optimization (no N+1 queries)
- 90%+ test coverage on critical paths
- Zero downtime deployments

---

# Appendix

## Data Dictionary

### Role Types (Supported in Phase 1)
- `group_fitness_instructor` - Leads group classes (HIIT, cycling, bootcamp, etc.)
- `personal_trainer` - 1-on-1 or small group training
- `yoga_instructor` - Yoga classes (various styles)
- `pilates_instructor` - Pilates classes (mat or equipment)

### Certifications (Supported in Phase 1)
- `NASM-CPT` - National Academy of Sports Medicine Certified Personal Trainer
- `ACE` - American Council on Exercise
- `ACSM` - American College of Sports Medicine
- `RYT-200` - Registered Yoga Teacher 200-hour
- `RYT-500` - Registered Yoga Teacher 500-hour
- `PMA` - Pilates Method Alliance
- `STOTT` - STOTT Pilates Certification

### Time Slots (Availability)
```
Mon AM, Mon PM
Tue AM, Tue PM
Wed AM, Wed PM
Thu AM, Thu PM
Fri AM, Fri PM
Sat AM, Sat PM
Sun AM, Sun PM
```
(14 total slots)

### Culture Tags
```
community         - Values team/group culture
high-energy       - Fast-paced, intense environment
wellness          - Holistic health focus
technical-precision - Detail-oriented, form-focused
motivational      - Inspirational coaching style
educational       - Teaching-focused approach
hands-on          - Physical corrections, tactile cues
dynamic-flow      - Creative, varied programming
boutique-luxury   - Premium experience focus
beginner-friendly - Welcoming to new clients
```

---

## Example Organization Hierarchy

```
Brand: Peak Fitness Studios (brand_id: 1)
├── Region: Northeast (region_id: 1)
│   ├── Location: NYC Tribeca (location_id: 1)
│   ├── Location: NYC Upper West Side (location_id: 2)
│   └── Location: Boston Back Bay (location_id: 3)
└── Region: West Coast (region_id: 2)
    ├── Location: LA Venice (location_id: 4)
    └── Location: SF Mission District (location_id: 5)

Users:
- Sarah (Coach, brand_id: 1) → sees jobs from all Peak Fitness locations
- Michael (Location Manager, location_id: 1) → creates jobs only for NYC Tribeca
- Jessica (Regional Director, region_id: 1) → views all Northeast locations, can't edit
- David (Brand Admin, brand_id: 1) → full access to all Peak Fitness data
```

---

## Future Enhancements Roadmap

### Phase 2 - Dynamic Scoring (Week 2-3)
- Engagement score decay (profile staleness penalty)
- Async workers for background score recalculation
- Pre-calculated matches table for performance
- Email notifications (new match, profile viewed)

### Phase 3 - Hiring Workflow (Week 4-5)
- Application system (coaches apply to jobs)
- Application status tracking (pending, interviewed, hired, rejected)
- Messaging between coaches and managers
- Interview scheduling

### Phase 4 - Analytics & Reporting (Week 6-7)
- Manager analytics dashboard (time-to-hire, application funnel)
- Regional analytics (hiring trends, candidate pipeline)
- FitScore effectiveness analysis (do high scores correlate with hires?)

### v2 - AI & ML Features (Month 2+)
- Gemini AI video analysis (auto-tag movement quality, instruction style)
- Recommendation engine (suggest jobs to coaches proactively)
- Predictive hiring (forecast which matches will convert)
- Churn prediction (identify at-risk placements)

---

## Technology Migration Path

### Current (Phase 1): Embedded Synchronous Scoring
```python
# Calculate on-demand when manager views candidates
@app.get("/jobs/{job_id}/candidates")
def get_candidates(job_id: int):
    coaches = db.query(Coach).all()
    scored = [engine.calculate_match(coach, job) for coach in coaches]
    return sorted(scored, reverse=True)[:20]
```

### Future (Phase 2): Async Background Workers
```python
# Pre-calculate and cache scores
@app.get("/jobs/{job_id}/candidates")
def get_candidates(job_id: int):
    # Return pre-calculated scores from matches table
    return db.query(Match).filter_by(job_id=job_id).order_by(Match.fitscore.desc()).limit(20)

# Background worker recalculates when data changes
@celery.task
def recalculate_job_matches(job_id: int):
    job = db.get_job(job_id)
    coaches = db.query(Coach).filter_by(brand_id=job.brand_id).all()
    for coach in coaches:
        score = engine.calculate_match(coach, job)
        db.upsert_match(coach.id, job.id, score)
```

### Future (v2): ML-Enhanced Scoring
```python
# Hybrid: Deterministic base + ML boost
class MLFitScoreEngine(FitScoreEngine):
    def calculate_match(self, coach: Coach, job: Job) -> float:
        base_score = super().calculate_match(coach, job)

        # ML model predicts likelihood of successful hire
        ml_boost = ml_model.predict_success(coach, job)  # 0.0 to 0.2 boost

        return min(base_score + ml_boost, 1.0)
```

---

## Questions & Assumptions

### Assumptions Made
1. **Single brand per coach:** Coaches belong to one brand at a time (can change later)
2. **US-only:** All locations in United States initially
3. **English-only:** UI and content in English (i18n deferred)
4. **No compensation matching:** Salary not used in FitScore calculation (transparency concerns)
5. **Manual verification only:** No automated cert validation (requires 3rd party APIs)
6. **City-level location:** No ZIP code or geolocation initially

### Open Questions (for stakeholder review)
1. **Should coaches see their own FitScore?** (Pro: transparency, Con: gaming the system)
2. **Should coaches see which jobs viewed their profile?** (Pro: engagement, Con: privacy)
3. **How often should engagement scores decay?** (30 days, 60 days, 90 days?)
4. **Should there be a minimum profile completeness to appear in searches?** (e.g., 70%)
5. **What happens when a certification expires?** (Auto-hide from matches? Warning to coach?)
6. **Should FitScore weights be visible to coaches?** (Pro: transparency, Con: optimization)

---

## Glossary

- **FitScore:** Numerical score (0.0 to 1.0) representing alignment between coach and job
- **Threshold:** Minimum FitScore required for a match to be displayed (set by hiring manager)
- **Preset:** Pre-configured weighting scheme for FitScore calculation
- **Brand:** Top-level organization (e.g., Equinox, SoulCycle)
- **Region:** Geographic subdivision of a brand (e.g., Northeast, West Coast)
- **Location:** Physical studio/gym within a region
- **Multi-tenancy:** Architecture pattern where each brand's data is isolated
- **Deterministic:** Same inputs always produce same outputs (no randomness or ML in v1)
- **Engagement Signals:** Behavioral data that indicates coach quality/readiness (profile updates, videos, etc.)
- **Verified:** Admin-confirmed data (certifications checked, videos reviewed)

---

**End of Specification**
