# FitHire Project Status

**Last Updated:** 2025-12-30
**Current Phase:** Phase 1 - Day 1 (Backend Foundation)
**Target Completion:** Phase 1 by 2026-01-01

---

## Project Milestones

### Phase 0: Scope Lock & Setup ✅ (Complete)
**Timeline:** Dec 30, 2025
**Status:** ✅ Complete

**Objectives:**
- Define product requirements and scope
- Lock down technical architecture
- Set up development services
- Create project documentation

**Deliverables:**
- [x] Project Specification document (`PROJECT_SPEC.md`)
- [x] System Architecture document (`architecture.md`)
- [x] Environment configuration template (`.env.example`)
- [x] Clerk account setup with organizations enabled
- [x] Neon PostgreSQL database provisioned
- [x] Cloudflare R2 bucket created (`fithire`)
- [x] All API credentials secured
- [x] Project documentation structure established

---

### Phase 1: Core Profiles & Manual Matching 🔄 (In Progress)
**Timeline:** Dec 30, 2025 - Jan 1, 2026 (2 days)
**Status:** 🔄 In Progress - 50% Complete (Day 1 ✅, Day 2 pending)

**Objectives:**
- Build functional MVP with coach profiles, job postings, and matching
- Implement FitScore calculation engine
- Deploy working application to production

#### Day 1: Backend Foundation ✅
**Status:** ✅ Complete - 100%

**Tasks:**
- [x] Set up monorepo structure (`/backend`, `/frontend`)
- [x] Initialize FastAPI project with Poetry
- [x] Configure SQLAlchemy + Alembic
- [x] Create database schema (9 tables)
- [x] Run initial migrations on Neon database
- [x] Implement Clerk authentication middleware (JWT validation with python-jose)
- [x] Build FitScore engine with 6 sub-scoring functions
- [x] Write unit tests for FitScore engine (97% coverage achieved!)
- [x] Implement Pydantic schemas for all API requests/responses
- [x] Implement Coach CRUD endpoints (create, read, update, list with pagination)
- [x] Implement Job CRUD endpoints (create, read, update, delete, list with pagination)
- [x] Implement matching endpoints (`/coaches/{id}/matches`, `/jobs/{id}/candidates`)
- [x] Verify API structure (17 routes registered successfully)

#### Day 2: Frontend & Deployment 🔄
**Status:** Not Started

**Tasks:**
- [ ] Initialize Next.js project with TypeScript
- [ ] Set up Tailwind CSS + shadcn/ui
- [ ] Integrate Clerk authentication (sign-in/sign-up)
- [ ] Build Coach dashboard (profile form, match list)
- [ ] Build Manager dashboard (job form, candidate list)
- [ ] Build basic Admin panel (verification queue)
- [ ] Implement FitScore display component with explanations
- [ ] Add filtering UI (location, role type, availability)
- [ ] Connect frontend to backend API
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Configure environment variables in production
- [ ] End-to-end smoke test (create profile → create job → see match)

**Success Criteria:**
- [ ] Coach can create complete profile
- [ ] Manager can create job posting
- [ ] FitScore calculates correctly (0.0 to 1.0)
- [ ] Top 20 matches displayed, sorted by score
- [ ] Threshold filtering works
- [ ] Multi-unit access control enforced
- [ ] Admin can verify certifications
- [ ] Application deployed and accessible online

---

### Phase 2: Dynamic Scoring & Engagement 📅 (Planned)
**Timeline:** Week 2-3 (Jan 2-15, 2026)
**Status:** 📅 Planned

**Objectives:**
- Make FitScore reflect engagement and time decay
- Add async background workers for performance

**Key Features:**
- [ ] Engagement score decay (profile staleness penalty)
- [ ] Async workers (Celery + Redis) for background recalculation
- [ ] Pre-calculated matches table for instant queries
- [ ] Score recalculation triggers (profile update, job update)
- [ ] Email notifications (new match, profile viewed)
- [ ] Admin diagnostics dashboard

---

### Phase 3: Role-Specific Logic & Presets 📅 (Planned)
**Timeline:** Week 4-5
**Status:** 📅 Planned

**Objectives:**
- Support multiple scoring frameworks by role type
- Expand weighting presets
- Add admin tooling for managing scoring logic

**Key Features:**
- [ ] Custom scoring logic for specific roles (if needed)
- [ ] Additional weighting presets (beyond 4 initial)
- [ ] Admin UI to adjust preset weights
- [ ] Validation rules to prevent misconfiguration
- [ ] Score explanation improvements

---

### Phase 4: Multi-Unit Hierarchy & Access Control 📅 (Planned)
**Timeline:** Week 6-7
**Status:** 📅 Planned

**Objectives:**
- Full enterprise support for multi-location operators
- Advanced permission-aware views

**Key Features:**
- [ ] Brand/Regional/Location role enforcement
- [ ] Scoped search and ranking views
- [ ] Regional analytics dashboard
- [ ] Cross-region talent visibility (for Regional Directors)
- [ ] Bulk operations for Brand Admins

---

### Phase 5: Refinement & Trust Layer 📅 (Future)
**Timeline:** Post-V1
**Status:** 📅 Backlog

**Objectives:**
- Improve usability and build user confidence
- Provide transparency without exposing weights

**Key Features:**
- [ ] High-level FitScore explanations visible to coaches
- [ ] Coach-facing feedback (why they didn't match certain jobs)
- [ ] Operational tooling for moderators
- [ ] Application workflow (apply, track status)
- [ ] Messaging between coaches and managers
- [ ] Interview scheduling integration

---

## What's Been Accomplished

### ✅ Completed Work

#### Project Planning & Documentation
- **PROJECT_SPEC.md** - Comprehensive 1,400+ line specification
  - Product requirements (personas, workflows, problems solved)
  - Engineering design (tech stack, database schema, API design)
  - Complete FitScore algorithm with 6 sub-scoring functions
  - Phase 1 scope and success criteria
  - Future roadmap through v2

- **architecture.md** - System architecture documentation
  - High-level system overview
  - Data flow diagrams
  - Component architecture (backend + frontend)
  - API layer specification
  - Deployment architecture

- **project_status.md** - This document
  - Milestone tracking
  - Task breakdowns
  - Progress monitoring

- **changelog.md** - Version history tracking
  - Follows Keep a Changelog format
  - Ready for first release notes

- **.env.example** - Environment configuration template
  - All required environment variables documented
  - Setup instructions for each service
  - Security best practices

#### Service Setup
- **Clerk** - Authentication platform configured
  - Organizations enabled for multi-tenant support
  - Email/password authentication configured
  - Roles created (coach, location_manager, regional_director, brand_admin)
  - API keys secured

- **Neon** - PostgreSQL database provisioned
  - Serverless PostgreSQL 15+ database created
  - Connection pooling configured
  - Connection string secured

- **Cloudflare R2** - Object storage configured
  - Bucket `fithire` created
  - API token generated with read/write permissions
  - S3-compatible endpoint configured
  - Zero egress fees for video streaming

#### Architecture Decisions
- **Tech stack finalized:**
  - Backend: Python + FastAPI + SQLAlchemy + Pydantic v2 + PostgreSQL
  - Frontend: Next.js + Tailwind CSS + shadcn/ui
  - Auth: Clerk (auth only, hierarchy in DB)
  - Storage: Cloudflare R2
  - Deployment: Railway (backend) + Vercel (frontend) + Neon (database)

- **FitScore algorithm defined:**
  - 6 sub-scores: certifications, experience, availability, location, culture, engagement
  - 4 weighting presets: balanced, experience_heavy, culture_heavy, availability_focused
  - Default threshold: 0.60 (adjustable 0.40-0.80)
  - Phase 1: Embedded synchronous calculation
  - Phase 2: Async workers with pre-calculation

- **Database schema designed:**
  - 9 core tables: brands, regions, locations, users, user_scopes, coaches, jobs, matches, audit_logs, match_events
  - Multi-tenant with brand_id isolation
  - Proper indexes for FitScore queries
  - Audit logging built-in

---

## What's Next

### Immediate Next Steps (Dec 31, 2025)

#### 1. Set Up Monorepo Structure 🎯
**Priority:** Critical
**Estimated Time:** 30 minutes

- Create `/backend` and `/frontend` folders
- Initialize FastAPI project with Poetry
- Initialize Next.js project with TypeScript
- Set up `.gitignore` for Python and Node
- Split `.env` into backend and frontend versions
- Create README files for each folder

#### 2. Database Schema Implementation 🎯
**Priority:** Critical
**Estimated Time:** 1-2 hours

- Set up Alembic migrations in backend
- Create SQLAlchemy models for all 9 tables
- Generate initial migration
- Run migration on Neon database
- Verify schema with database explorer

#### 3. FitScore Engine Implementation 🎯
**Priority:** Critical
**Estimated Time:** 2-3 hours

- Implement `FitScoreEngine` class
- Implement 6 sub-scoring functions
- Define 4 weighting presets
- Write unit tests (pytest)
- Test with sample data

#### 4. API Endpoints Implementation 🎯
**Priority:** Critical
**Estimated Time:** 3-4 hours

- Set up FastAPI application structure
- Implement Clerk auth middleware
- Build Coach endpoints (CRUD + matches)
- Build Job endpoints (CRUD + candidates)
- Build Admin endpoints (verification)
- Test with API client

#### 5. Frontend Dashboard Implementation 🎯
**Priority:** Critical
**Estimated Time:** 3-4 hours

- Set up Next.js with Clerk
- Build Coach dashboard UI
- Build Manager dashboard UI
- Build Admin panel UI
- Implement API integration
- Test user flows

#### 6. Deployment 🎯
**Priority:** Critical
**Estimated Time:** 1 hour

- Deploy backend to Railway
- Deploy frontend to Vercel
- Configure production environment variables
- Test production deployment
- Run smoke tests

---

## Blockers & Risks

### Current Blockers
None - all services set up and ready to build.

### Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **FitScore calculation too slow** | High | Start embedded (Phase 1), migrate to async workers (Phase 2) |
| **Clerk webhook delays** | Medium | Queue webhook events, process async |
| **R2 upload failures** | Medium | Implement retry logic, show clear error messages |
| **Database connection limits** | Medium | Use connection pooling, Neon handles this automatically |
| **Multi-tenant data leakage** | High | Enforce brand_id filtering at ORM level, write tests |
| **Tight 2-day timeline** | Medium | Prioritize core features, defer nice-to-haves |

---

## Team & Resources

### Team
- **Developer:** Solo full-stack developer (data theory major, first full-stack project)
- **AI Assistant:** Claude (architecture, coding support, documentation)

### Resources
- **Documentation:** PROJECT_SPEC.md, architecture.md
- **Services:** Clerk, Neon, Cloudflare R2, Railway, Vercel
- **Tools:** VSCode, Git, Postman, Chrome DevTools

### Support
- Clerk documentation: https://clerk.com/docs
- FastAPI documentation: https://fastapi.tiangolo.com
- Next.js documentation: https://nextjs.org/docs
- shadcn/ui documentation: https://ui.shadcn.com

---

## Success Metrics

### Phase 1 Success Criteria

**Functional:**
- [ ] Coach can create profile and see top 20 job matches
- [ ] Manager can create job and see top 20 candidates
- [ ] FitScore calculation is accurate and deterministic
- [ ] Threshold filtering works correctly
- [ ] Multi-tenant access control enforced (no data leakage)

**Technical:**
- [ ] 70%+ test coverage on FitScore engine
- [ ] API response time < 2 seconds for match queries
- [ ] Zero SQL N+1 queries
- [ ] All environment variables secured (no secrets in code)

**Deployment:**
- [ ] Backend deployed to Railway with health check
- [ ] Frontend deployed to Vercel with custom domain
- [ ] Database migrations run successfully
- [ ] End-to-end smoke test passes

---

## Questions & Decisions Log

### Open Questions
- Should coaches see their own FitScore? (Deferred to Phase 2)
- How often should engagement scores decay? (30/60/90 days - TBD)
- Should FitScore weights be visible to coaches? (No - decided)

### Key Decisions Made
- ✅ Clerk handles auth only, hierarchy lives in database
- ✅ Phase 1 uses embedded FitScore calculation (sync)
- ✅ Cloudflare R2 for file storage (cost savings)
- ✅ Multi-tenant with brand_id isolation
- ✅ REST API with versioning (/api/v1/)
- ✅ Monorepo structure (not separate repos)
- ✅ 4 initial role types: Group Fitness, Personal Trainer, Yoga, Pilates
- ✅ 7 certifications supported: NASM-CPT, ACE, ACSM, RYT-200, RYT-500, PMA, STOTT

---

**End of Project Status Document**
