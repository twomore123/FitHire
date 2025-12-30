# FitHire System Architecture

**Version:** 1.0
**Last Updated:** 2025-12-30
**Status:** Phase 1 - In Development

---

## System Overview

FitHire is a full-stack web application built as a monorepo with separate backend and frontend services. The system uses a client-server architecture where the React-based frontend communicates with a Python REST API backend. All data is stored in a PostgreSQL database, with file assets hosted on Cloudflare R2.

### Core Purpose
Match fitness coaches with job opportunities using a deterministic FitScore algorithm that evaluates certifications, experience, availability, location, cultural fit, and engagement signals.

### Technology Stack

**Backend:**
- Language: Python 3.11+
- Framework: FastAPI (async REST API)
- ORM: SQLAlchemy 2.0
- Database: PostgreSQL 15+ (Neon hosted)
- Validation: Pydantic v2

**Frontend:**
- Framework: Next.js 14+ (React)
- Styling: Tailwind CSS
- Components: shadcn/ui
- State: React Context + Zustand

**Infrastructure:**
- Auth: Clerk (JWT-based)
- Storage: Cloudflare R2 (S3-compatible)
- Backend Hosting: Railway
- Frontend Hosting: Vercel
- Database Hosting: Neon (serverless PostgreSQL)

---

## Data Flow

### High-Level Request Flow

```
┌─────────┐          ┌─────────┐          ┌──────────┐          ┌────────────┐
│ Browser │ ────────>│ Next.js │ ────────>│  FastAPI │ ────────>│ PostgreSQL │
│ (User)  │ <────────│  (UI)   │ <────────│   (API)  │ <────────│    (DB)    │
└─────────┘   HTML   └─────────┘   REST   └──────────┘    SQL   └────────────┘
              /JSON                /JSON                           /Rows
                                     │
                                     │ S3 API
                                     ▼
                                ┌──────────┐
                                │ R2 (CDN) │
                                │  Files   │
                                └──────────┘
```

### Authentication Flow

```
1. User signs in via Clerk
   ├─> Clerk validates credentials
   └─> Returns JWT token

2. Browser includes JWT in API requests
   ├─> Authorization: Bearer <token>
   └─> FastAPI validates with Clerk

3. FastAPI checks user permissions
   ├─> Query user role from database
   ├─> Verify brand/region/location scope
   └─> Allow or deny request
```

### FitScore Calculation Flow (Phase 1)

```
1. Manager views candidates for job
   ├─> GET /api/v1/jobs/{id}/candidates

2. API queries database
   ├─> Fetch job details (requirements, preset, threshold)
   └─> Fetch all coaches in brand scope

3. FitScore Engine calculates scores
   ├─> For each coach:
   │   ├─> Calculate 6 sub-scores (certs, exp, avail, loc, culture, engage)
   │   ├─> Apply weighting preset
   │   └─> Return final FitScore (0.0 to 1.0)
   │
   ├─> Filter: score >= threshold
   ├─> Sort: by score DESC
   └─> Limit: top 20 results

4. API returns match list with explanations
   └─> Frontend displays ranked candidates
```

### File Upload Flow (Videos/Images)

```
1. User requests upload
   ├─> POST /api/v1/coaches/{id}/upload-video
   └─> API generates presigned R2 URL (1 hour expiry)

2. Browser uploads directly to R2
   ├─> PUT https://<account>.r2.cloudflarestorage.com/<key>
   └─> No data passes through API (saves bandwidth)

3. User confirms upload
   ├─> POST /api/v1/coaches/{id}/confirm-upload
   └─> API saves file URL to database

4. Viewing files
   ├─> API generates signed URL (1 year expiry)
   └─> Browser fetches from R2 CDN
```

---

## Component Architecture

### Backend Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Settings (env vars, constants)
│   │
│   ├── api/                     # API layer
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py      # Webhook handlers
│   │   │   │   ├── coaches.py   # Coach CRUD + matches
│   │   │   │   ├── jobs.py      # Job CRUD + candidates
│   │   │   │   ├── admin.py     # Verification, tagging
│   │   │   │   └── brands.py    # Org hierarchy
│   │   │   └── deps.py          # Dependencies (auth, DB)
│   │   └── middleware.py        # Auth, CORS, logging
│   │
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── coach.py
│   │   ├── job.py
│   │   ├── brand.py
│   │   └── audit.py
│   │
│   ├── schemas/                 # Pydantic schemas
│   │   ├── coach.py             # Request/response models
│   │   ├── job.py
│   │   └── match.py
│   │
│   ├── core/                    # Business logic
│   │   ├── fitscore/
│   │   │   ├── engine.py        # FitScore calculation
│   │   │   ├── presets.py       # Weighting configurations
│   │   │   └── explainer.py     # Generate explanations
│   │   ├── auth.py              # Clerk integration
│   │   └── storage.py           # R2 file operations
│   │
│   ├── db/                      # Database
│   │   ├── session.py           # SQLAlchemy setup
│   │   └── migrations/          # Alembic migrations
│   │
│   └── utils/                   # Utilities
│       ├── logging.py
│       └── exceptions.py
│
├── tests/
│   ├── test_fitscore.py         # FitScore engine tests
│   ├── test_auth.py
│   └── test_api.py
│
├── alembic.ini                  # Alembic config
├── pyproject.toml               # Poetry dependencies
└── .env                         # Environment variables
```

### Database Schema

```
brands
  └─── regions
        └─── locations
              └─── jobs

users
  ├─── user_scopes (region/location access)
  └─── coaches (1:1 relationship)

coaches ──< matches >── jobs
               │
               └─── match_events (for ML tracking)

audit_logs (tracks all changes)
```

**Key relationships:**
- Brand → Region → Location (hierarchy)
- User → Coach (1:1, not all users are coaches)
- Coach ↔ Job (many-to-many via matches)
- All entities scoped by `brand_id` for multi-tenancy

---

## Frontend Components

### Application Structure

```
frontend/
├── app/                         # Next.js App Router
│   ├── (auth)/                  # Auth layout group
│   │   ├── sign-in/
│   │   └── sign-up/
│   │
│   ├── (dashboard)/             # Protected routes
│   │   ├── layout.tsx           # Shared dashboard layout
│   │   ├── coach/
│   │   │   ├── page.tsx         # Coach dashboard
│   │   │   ├── profile/         # Edit profile
│   │   │   └── matches/         # View job matches
│   │   │
│   │   ├── manager/
│   │   │   ├── page.tsx         # Manager dashboard
│   │   │   ├── jobs/            # Manage jobs
│   │   │   └── candidates/      # View candidates
│   │   │
│   │   └── admin/
│   │       ├── page.tsx         # Admin dashboard
│   │       ├── verify/          # Verification queue
│   │       └── tags/            # Video tagging
│   │
│   ├── api/                     # Next.js API routes (minimal)
│   └── layout.tsx               # Root layout
│
├── components/                  # React components
│   ├── ui/                      # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── form.tsx
│   │   └── ...
│   │
│   ├── features/
│   │   ├── coaches/
│   │   │   ├── ProfileForm.tsx
│   │   │   ├── MatchCard.tsx
│   │   │   └── VideoUpload.tsx
│   │   │
│   │   ├── jobs/
│   │   │   ├── JobForm.tsx
│   │   │   ├── CandidateCard.tsx
│   │   │   └── FilterPanel.tsx
│   │   │
│   │   └── admin/
│   │       ├── VerificationQueue.tsx
│   │       └── TaggingInterface.tsx
│   │
│   └── shared/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── FitScoreDisplay.tsx
│
├── lib/                         # Utilities
│   ├── api.ts                   # API client (fetch wrapper)
│   ├── auth.ts                  # Clerk helpers
│   ├── utils.ts                 # General utilities
│   └── types.ts                 # TypeScript types
│
├── hooks/                       # Custom React hooks
│   ├── useMatches.ts            # Fetch coach matches
│   ├── useCandidates.ts         # Fetch job candidates
│   └── useAuth.ts               # Auth helpers
│
├── store/                       # State management
│   └── useStore.ts              # Zustand store
│
└── public/                      # Static assets
```

### Component Hierarchy

```
App Layout
├── Header
│   ├── Logo
│   ├── Navigation
│   └── UserMenu (Clerk)
│
└── Main Content
    ├── Sidebar (role-specific)
    │
    └── Page Content
        │
        ├── Coach Dashboard
        │   ├── ProfileCompleteness
        │   ├── MatchList
        │   │   └── MatchCard (×20)
        │   │       ├── FitScoreDisplay
        │   │       ├── JobDetails
        │   │       └── ExplanationTooltip
        │   └── FilterPanel
        │
        ├── Manager Dashboard
        │   ├── JobList
        │   ├── CandidateList
        │   │   └── CandidateCard (×20)
        │   │       ├── FitScoreDisplay
        │   │       ├── CoachSummary
        │   │       └── VideoPreview
        │   └── FilterPanel
        │
        └── Admin Dashboard
            ├── VerificationQueue
            │   └── VerificationItem (×N)
            └── TaggingInterface
                ├── VideoPlayer
                └── TagSelector
```

---

## API Layer

### RESTful Endpoints

#### Authentication
```
POST   /api/v1/auth/webhook          # Clerk user sync
```

#### Coaches
```
GET    /api/v1/coaches/{id}          # Get profile
POST   /api/v1/coaches               # Create profile
PATCH  /api/v1/coaches/{id}          # Update profile
GET    /api/v1/coaches/{id}/matches  # Get job matches
POST   /api/v1/coaches/{id}/upload   # Get presigned upload URL
```

#### Jobs
```
GET    /api/v1/jobs/{id}             # Get job
POST   /api/v1/jobs                  # Create job
PATCH  /api/v1/jobs/{id}             # Update job
DELETE /api/v1/jobs/{id}             # Deactivate job
GET    /api/v1/jobs/{id}/candidates  # Get coach candidates
```

#### Admin
```
GET    /api/v1/admin/pending         # Pending verifications
POST   /api/v1/admin/verify-cert     # Verify certification
POST   /api/v1/admin/tag-video       # Tag video
PATCH  /api/v1/admin/coaches/{id}    # Approve profile
```

#### Organizations
```
GET    /api/v1/brands                # List brands (scoped)
GET    /api/v1/brands/{id}/regions   # List regions
GET    /api/v1/brands/{id}/locations # List locations
```

### API Request/Response Pattern

**Request:**
```http
GET /api/v1/coaches/42/matches?limit=20&min_score=0.6
Authorization: Bearer <clerk-jwt>
```

**Response:**
```json
{
  "matches": [
    {
      "job_id": 15,
      "title": "Weekend HIIT Instructor",
      "location": "NYC Tribeca",
      "fitscore": 0.87,
      "explanation": {
        "strengths": ["Required certs met", "3/3 availability match"],
        "gaps": []
      }
    }
  ],
  "total": 12,
  "threshold": 0.60
}
```

### Authentication Middleware

```python
# Every protected route:
1. Extract JWT from Authorization header
2. Validate with Clerk SDK
3. Query user from database by clerk_user_id
4. Check role and scope permissions
5. Inject user into request context
```

---

## Library Modules

### Core Libraries (Backend)

**FastAPI** - Web framework
- Async request handling
- Automatic OpenAPI docs
- Built-in validation (Pydantic)
- Dependency injection

**SQLAlchemy** - ORM
- Declarative models
- Relationship mapping
- Query building
- Connection pooling

**Alembic** - Database migrations
- Version-controlled schema changes
- Automatic migration generation
- Rollback support

**Pydantic** - Data validation
- Request/response schemas
- Type safety
- Automatic serialization
- Settings management

**Clerk SDK** - Authentication
- JWT validation
- Webhook handling
- User management

**boto3** - AWS SDK (for R2)
- S3-compatible API
- Presigned URL generation
- File upload/download

### Core Libraries (Frontend)

**Next.js** - React framework
- Server-side rendering
- File-based routing
- API routes
- Image optimization

**Clerk React** - Auth UI
- Pre-built sign-in/sign-up components
- User profile widgets
- Session management hooks

**Tailwind CSS** - Styling
- Utility-first CSS
- Responsive design
- Custom design system

**shadcn/ui** - Component library
- Accessible components
- Radix UI primitives
- Customizable styles

**Zod** - Validation
- Type-safe schemas
- Form validation
- Matches backend Pydantic schemas

**Zustand** - State management
- Simple global state
- Minimal boilerplate
- React hooks API

---

## Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare (CDN)                         │
│  ┌─────────────────┐              ┌─────────────────┐      │
│  │  Static Assets  │              │   R2 Storage    │      │
│  │   (Next.js)     │              │  (Media Files)  │      │
│  └─────────────────┘              └─────────────────┘      │
└──────────┬─────────────────────────────────┬───────────────┘
           │                                 │
           ▼                                 │
┌─────────────────────┐                      │
│  Vercel (Frontend)  │                      │
│  - Next.js SSR      │                      │
│  - Edge Functions   │                      │
└──────────┬──────────┘                      │
           │                                 │
           │ HTTPS/REST                      │
           ▼                                 │
┌─────────────────────┐                      │
│ Railway (Backend)   │                      │
│ - FastAPI Service   │──────────────────────┘
│ - Redis (Phase 2)   │              S3 API
└──────────┬──────────┘
           │
           │ PostgreSQL Protocol
           ▼
┌─────────────────────┐
│  Neon (Database)    │
│  - PostgreSQL 15+   │
│  - Connection Pool  │
└─────────────────────┘
```

### Environment Separation

| Environment | Backend | Frontend | Database | Purpose |
|-------------|---------|----------|----------|---------|
| **Development** | localhost:8000 | localhost:3000 | Local/Neon | Local dev |
| **Staging** | Railway (staging) | Vercel (preview) | Neon (staging) | Testing |
| **Production** | Railway (prod) | Vercel (prod) | Neon (prod) | Live users |

---

## Security Considerations

### Authentication & Authorization
- JWT tokens validated on every API request
- Role-based access control (RBAC) enforced in API
- Brand-level data isolation via `brand_id` filtering
- Clerk handles password security (bcrypt, rate limiting)

### Data Protection
- All API requests over HTTPS only
- Database connections use SSL/TLS (sslmode=require)
- Sensitive env vars never committed to git
- API secrets rotated regularly

### File Upload Security
- Presigned URLs expire after 1 hour
- File type validation (videos/images only)
- File size limits enforced (500MB max)
- Signed URLs for viewing (1 year expiry)

### Multi-Tenancy Isolation
- Every query filters by `brand_id`
- SQLAlchemy row-level security
- Users cannot access other brands' data
- Audit logs track all access

---

## Future Architecture Evolution

### Phase 2: Async Workers (Weeks 2-3)
```
Add Celery + Redis:
- Background FitScore recalculation
- Pre-compute matches table
- Email notifications queue
```

### Phase 3: Application Workflow (Weeks 4-5)
```
Add real-time features:
- WebSocket/SSE for notifications
- Chat system (coaches ↔ managers)
- Application status tracking
```

### Phase 4: Analytics (Weeks 6-7)
```
Add analytics infrastructure:
- Time-series data (TimescaleDB extension)
- Data warehouse (PostgreSQL analytics schema)
- Dashboard aggregations
```

### v2: ML Integration (Month 2+)
```
Add ML pipeline:
- Feature store (ML-ready data)
- Model serving (FastAPI endpoint)
- A/B testing framework
- Gemini API for video analysis
```

---

## Performance Targets

### Phase 1 (Current)
- API response time: < 2 seconds (calculate on-demand)
- Page load time: < 3 seconds (full dashboard)
- Database queries: < 100ms (with proper indexes)
- File uploads: Direct to R2 (no API bottleneck)

### Phase 2+ (Future)
- API response time: < 500ms (pre-calculated scores)
- Match recalculation: < 30 seconds (background job)
- Real-time updates: < 1 second (WebSocket latency)

---

**End of Architecture Document**
