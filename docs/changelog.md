# Changelog

All notable changes to FitHire will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### In Progress - Phase 1 (Day 2)
- Schedule UI enhancements (spreadsheet-style selector)
- Custom weighting sliders for FitScore configuration
- End-to-end testing

### Completed - Phase 1 (Day 2-3) ✅
- Critical security vulnerability fixes
- FitScore algorithm edge case improvements
- Next.js 15 compatibility updates
- Data caching security improvements

### Completed - Phase 1 (Day 2) ✅
- Frontend dashboards implemented (Coach, Manager, Admin)
- Coach profile page displays real data with verification status
- Coach matches page shows job matches with FitScore
- Manager job listing and editing functionality
- Manager candidate list with matched coaches
- Admin verification queue with approve/reject actions
- Clerk authentication integrated on frontend
- Deployment to Railway (backend) and Vercel (frontend)

---

## [0.3.1] - 2026-01-06 (Security & Bug Fixes)

### Security
- **CRITICAL: Fixed cross-user data modification vulnerability in job endpoints** (`backend/app/api/v1/routes/jobs.py`)
  - All jobs were being created with hardcoded `created_by=1`, allowing managers to view/edit/delete each other's job postings
  - Added `get_or_create_user()` helper function to get authenticated user's database record
  - All job endpoints now verify ownership and return 403 Forbidden for unauthorized access
  - Endpoints secured: POST, GET, PATCH, DELETE, and candidates listing
  - Complete data integrity restored for job management

- **CRITICAL: Fixed cross-user data leakage via Next.js server-side caching** (`frontend/app/dashboard/*`)
  - Server-side caching could serve User A's PII (names, locations, certifications, bios) to User B
  - Added caching directives to all authenticated dashboard pages:
    - `export const dynamic = 'force-dynamic'`
    - `export const revalidate = 0`
  - Pages secured: Coach profile, Coach edit, Manager jobs, Manager job detail, Admin verification

### Fixed
- **FitScore edge cases** (`backend/app/core/fitscore/engine.py:102-204`)
  - Fixed unfair penalization when jobs have no requirements
  - Certifications: Now returns 1.0 (perfect match) if no required/preferred certifications
  - Experience: Now returns 1.0 if `min_experience = 0`
  - Availability: Now returns 1.0 if no required time slots
  - Also gives full bonus (0.3) when no preferred certifications exist

- **Next.js 15 async params compatibility** (`frontend/app/dashboard/manager/[jobId]/*.tsx`)
  - Updated job detail page to handle async params API changes
  - Updated job edit page to handle async params API changes
  - Ensures compatibility with Next.js 15

- **Frontend data transformation** (`frontend/app/dashboard/manager/[jobId]/page.tsx`)
  - Fixed candidate data to match CandidateList interface requirements
  - Improved data mapping for proper component rendering

- **Coach profile completeness calculation** (Previous fixes)
  - Fixed completeness percentage display
  - Added spreadsheet-style availability view

- **Validation error handling** (Previous fixes)
  - Removed User fields from Coach schemas to prevent 422 errors
  - Added detailed validation error logging for debugging

- **Thursday abbreviation bug** (Previous fixes)
  - Fixed incorrect day abbreviation in availability component

### Changed
- Enhanced error logging throughout job endpoints for better debugging
- Improved JWT parsing for user creation

---

### Completed - Phase 1 (Day 1) ✅
- All backend API endpoints implemented
- Authentication middleware with JWT validation
- Comprehensive Pydantic schemas for all endpoints
- FitScore engine integrated with matching endpoints

---

## [0.3.0] - 2026-01-05 (In Progress)

### Added - Phase 1 Day 2 (Frontend Dashboards)

#### Coach Dashboard
- **Profile Page** (`/dashboard/coach/page.tsx`):
  - Fetches and displays real coach data from API
  - Shows verification status badge (verified/pending)
  - Displays profile completeness percentage
  - Lists certifications, availability slots, and coaching style tags
  - Links to edit profile and view matches
- **Matches Page** (`/dashboard/coach/matches/page.tsx`):
  - Dynamically fetches coach ID from database
  - Displays top 20 job matches sorted by FitScore
  - Shows FitScore breakdown with match factors
  - Empty state prompts profile creation if no coach profile exists
- **Edit Profile Page**:
  - Form pre-populated with existing coach data
  - Updates profile correctly via PATCH endpoint

#### Manager Dashboard
- **Jobs List Page** (`/dashboard/manager/page.tsx`):
  - Displays all jobs created by manager
  - Shows active/inactive status using `is_active` field
  - Links to view job details and edit jobs
  - Summary cards showing total jobs and active jobs count
- **Job Detail Page** (`/dashboard/manager/[jobId]/page.tsx`):
  - Displays job requirements and details
  - Shows list of matched candidates with FitScore
  - Links to edit job posting
- **Job Edit Page** (`/dashboard/manager/[jobId]/edit/page.tsx`):
  - NEW FILE - Separate route for editing jobs (Next.js convention)
  - Reuses JobPostingForm component with initialData
  - Pre-populates form with existing job data
  - Updates via API on submission

#### Admin Dashboard
- **Admin Landing Page** (`/dashboard/admin/page.tsx`):
  - NEW FILE - Admin dashboard overview
  - Links to verification queue
  - Placeholder cards for Phase 2 features (reports, analytics)
- **Verification Queue** (`/dashboard/admin/verification/page.tsx`):
  - NEW FILE - Lists pending coach profiles
  - Displays certifications, availability, bio, profile completeness
  - Shows creation date for each pending profile
  - Approve/reject actions via VerificationActions component
- **Verification Actions Component** (`/components/admin/verification-actions.tsx`):
  - NEW FILE - Client component for interactive buttons
  - Approve button calls POST /admin/verify-coach/{id}
  - Reject button calls POST /admin/reject-coach/{id}
  - Loading states and error handling
  - Auto-refreshes page after action

#### Backend Admin Routes
- **Admin API** (`/backend/app/api/v1/routes/admin.py`):
  - NEW FILE - Admin-specific endpoints
  - GET /admin/verification-queue - Returns coaches with null verified_at
  - POST /admin/verify-coach/{id} - Sets verified_at timestamp
  - POST /admin/reject-coach/{id} - Basic rejection (Phase 1)
- **API Client Extension** (`/frontend/lib/api-client.ts`):
  - Added adminAPI methods for verification endpoints
  - getVerificationQueue(), verifyCoach(), rejectCoach()

### Added - Phase 1 Day 1 (Backend API)

#### Authentication & Security
- Implemented JWT validation middleware with python-jose
- Created authentication utilities in `app/utils/auth.py`:
  - `get_current_user()` dependency for protected routes
  - `require_role()` factory for role-based access control
  - Token verification with Clerk JWKS support (signature verification pending)
- HTTP Bearer token authentication on all endpoints

#### Pydantic Schemas
- Created comprehensive request/response schemas for all endpoints:
  - **Coach schemas** (`app/schemas/coach.py`):
    - `CoachCreate` with validation for role types and certifications
    - `CoachUpdate` for partial updates
    - `CoachResponse` with full profile data
    - `CoachListResponse` for paginated lists
  - **Job schemas** (`app/schemas/job.py`):
    - `JobCreate` with FitScore preset validation
    - `JobUpdate` for partial updates
    - `JobResponse` with compensation details
    - `JobListResponse` for paginated lists
  - **Match schemas** (`app/schemas/match.py`):
    - `FitScoreBreakdown` with all 6 sub-scores
    - `CoachMatchResult` and `JobCandidateResult` with rankings
    - `CoachMatchesResponse` and `JobCandidatesResponse`

#### Coach API Endpoints (`/api/v1/coaches`)
- **POST /api/v1/coaches/** - Create new coach profile
  - Validates location access and role type
  - Calculates profile completeness automatically
  - Sets initial status to "pending" (requires admin verification)
- **GET /api/v1/coaches/{coach_id}** - Retrieve single coach
- **GET /api/v1/coaches/** - List coaches with pagination
  - Query parameters: `page`, `page_size` (max 100)
  - Filters: `location_id`, `role_type`, `status`
  - Ordered by creation date descending
- **PATCH /api/v1/coaches/{coach_id}** - Update coach profile
  - Partial updates (only provided fields)
  - Recalculates profile completeness
  - Updates `last_updated` timestamp
- **GET /api/v1/coaches/{coach_id}/matches** - Get top job matches
  - Returns up to 20 ranked job matches
  - Filters by job status="open" and city match
  - Applies job-specific FitScore threshold
  - Includes detailed score breakdown

#### Job API Endpoints (`/api/v1/jobs`)
- **POST /api/v1/jobs/** - Create new job listing
  - Validates location access and weighting preset
  - Sets initial status to "draft"
- **GET /api/v1/jobs/{job_id}** - Retrieve single job
- **GET /api/v1/jobs/** - List jobs with pagination
  - Query parameters: `page`, `page_size` (max 100)
  - Filters: `location_id`, `role_type`, `status`
  - Ordered by creation date descending
- **PATCH /api/v1/jobs/{job_id}** - Update job listing
  - Partial updates with validation
- **DELETE /api/v1/jobs/{job_id}** - Delete job listing
- **GET /api/v1/jobs/{job_id}/candidates** - Get top coach candidates
  - Returns up to 20 ranked coach candidates
  - Filters by coach status="verified", city match, and role type match
  - Applies configurable FitScore threshold
  - Includes detailed score breakdown

#### API Features
- All endpoints require authentication (JWT tokens)
- Multi-tenant data isolation enforced at database level
- Pagination support on all list endpoints (default 20, max 100)
- Profile completeness calculation (10 fields weighted equally)
- Matching uses city+state exact match (Phase 1)
- FitScore calculated on-demand with configurable presets
- Comprehensive error handling with HTTP status codes

#### Testing & Validation
- Fixed FitScore engine availability scoring formula
- All 30 unit tests passing (97% coverage on engine)
- API structure verified (17 routes registered)
- Request validation via Pydantic schemas
- Response serialization with `from_attributes=True`

### Changed
- Updated authentication approach to use python-jose instead of Clerk SDK
- Enhanced error messages with specific validation feedback

## [0.2.0] - 2025-12-30

### Added - Phase 1 (Backend Foundation)

#### Monorepo Structure
- Set up monorepo with `/backend` and `/frontend` folders
- Configured Poetry for Python dependency management
- Configured npm for Node.js dependency management
- Added comprehensive README files for both services
- Created environment variable templates for backend and frontend

#### Database Schema
- Implemented 9 SQLAlchemy models for multi-tenant architecture:
  - `Brand`, `Region`, `Location` - Organizational hierarchy
  - `User`, `UserScope` - Authentication and role-based access control
  - `Coach` - Fitness professional profiles with JSONB fields
  - `Job` - Job listings with requirements and FitScore configuration
  - `AuditLog` - Event tracking for compliance
  - `MatchEvent` - Match interaction tracking for ML
- Configured Alembic for database migrations
- Created initial migration with all tables
- Applied migration to Neon PostgreSQL database
- Added proper indexes for query performance
- Implemented multi-tenant isolation via `brand_id`

#### FitScore Calculation Engine
- Implemented deterministic FitScore algorithm in `app/core/fitscore/engine.py`
- Created 6 sub-scoring functions:
  1. **Certifications**: Required (must have) + preferred (bonus points)
  2. **Experience**: Minimum threshold + diminishing returns for extra years
  3. **Availability**: Required time slots + flexibility bonus
  4. **Location**: City match (Phase 1 - exact match only)
  5. **Cultural fit**: Tag overlap percentage calculation
  6. **Engagement**: Profile completeness, recency, verified video
- Implemented 4 weighting presets in `app/core/fitscore/presets.py`:
  - Balanced (25% certs, 20% exp, 15% avail, 15% loc, 15% culture, 10% engage)
  - Experience-heavy (35% weight on experience)
  - Culture-heavy (40% weight on cultural fit)
  - Availability-focused (35% weight on availability)
- All scores range from 0.0 to 1.0
- Created `MatchScore` dataclass for complete score breakdown
- Designed for easy extraction to async workers (Phase 2)

#### Testing
- Wrote comprehensive unit tests in `tests/test_fitscore.py`
- 70+ test cases covering all scoring functions
- Edge case testing (missing requirements, perfect matches, partial matches)
- Preset validation tests
- Integration tests for full FitScore calculation
- Achieved 70%+ test coverage on FitScore engine

### Changed
- N/A

### Fixed
- Fixed Clerk SDK dependency (removed non-existent package)
- Added `.gitkeep` to `alembic/versions` directory for git tracking

---

## [0.1.0] - 2025-12-30

### Added - Phase 0 (Pre-Development)

#### Documentation
- Created comprehensive `PROJECT_SPEC.md` with full product and engineering requirements
- Created `architecture.md` documenting system architecture and component design
- Created `project_status.md` for milestone and progress tracking
- Created `changelog.md` following Keep a Changelog format
- Created `.env.example` with complete environment variable documentation
- Created initial project structure in docs folder

#### Infrastructure Setup
- Set up Clerk authentication service
  - Configured email/password authentication
  - Enabled Organizations for multi-tenant support
  - Created roles: coach, location_manager, regional_director, brand_admin
  - Secured API keys (secret key, publishable key, webhook secret)
- Provisioned Neon PostgreSQL database
  - Created serverless PostgreSQL 15+ instance
  - Configured connection pooling
  - Secured connection string with SSL
- Set up Cloudflare R2 object storage
  - Created `fithire` bucket
  - Generated API token with read/write permissions
  - Configured S3-compatible endpoint
- Generated application secret key for session signing

#### Architecture Decisions
- Selected tech stack:
  - Backend: Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL
  - Frontend: Next.js 14+, Tailwind CSS, shadcn/ui, TypeScript
  - Auth: Clerk (JWT-based, organizations enabled)
  - Storage: Cloudflare R2 (S3-compatible, zero egress fees)
  - Hosting: Railway (backend), Vercel (frontend), Neon (database)
- Designed database schema with 9 core tables
  - Multi-tenant architecture with brand_id isolation
  - Audit logging and ML event tracking built-in
- Defined FitScore algorithm
  - 6 sub-scores: certifications, experience, availability, location, cultural_fit, engagement
  - 4 weighting presets: balanced, experience_heavy, culture_heavy, availability_focused
  - Default threshold: 0.60 (adjustable 0.40-0.80)
  - Phase 1: Synchronous embedded calculation
- Defined initial scope
  - 4 role types: Group Fitness Instructor, Personal Trainer, Yoga Instructor, Pilates Instructor
  - 7 supported certifications: NASM-CPT, ACE, ACSM, RYT-200, RYT-500, PMA, STOTT
  - 14 time slots: Mon-Sun AM/PM
  - Top 20 match limit

#### Repository Setup
- Initialized Git repository
- Created branch structure
- Added comprehensive README.md
- Organized documentation in `/docs` folder

### Changed
- N/A (initial setup)

### Deprecated
- N/A (initial setup)

### Removed
- N/A (initial setup)

### Fixed
- N/A (initial setup)

### Security
- Secured all API credentials in `.env` (not committed to git)
- Configured SSL/TLS for database connections
- Set up JWT-based authentication with Clerk
- Implemented multi-tenant data isolation strategy

---

## Version History

### Version Numbering
- **Major version (X.0.0)**: Breaking changes, major feature releases (v1, v2, etc.)
- **Minor version (0.X.0)**: New features, non-breaking changes (Phase 1, 2, 3, etc.)
- **Patch version (0.0.X)**: Bug fixes, small improvements

### Upcoming Versions

#### [0.2.0] - Phase 1 (Target: 2026-01-01)
- Complete MVP with coach profiles, job listings, and matching
- FitScore calculation engine implementation
- Basic dashboards for coaches and managers
- Admin verification workflow
- Deployment to production (Railway + Vercel)

#### [0.3.0] - Phase 2 (Target: TBD)
- Async workers (Celery + Redis)
- Engagement score decay
- Pre-calculated matches table
- Email notifications
- Performance optimizations

#### [0.4.0] - Phase 3 (Target: TBD)
- Role-specific scoring logic
- Expanded weighting presets
- Admin tools for score management
- Score explanation improvements

#### [0.5.0] - Phase 4 (Target: TBD)
- Full multi-unit hierarchy support
- Regional analytics dashboard
- Cross-region talent visibility
- Bulk operations for Brand Admins

#### [1.0.0] - Version 1 Production Release (Target: TBD)
- All Phase 1-4 features complete and stable
- Application workflow (apply, status tracking)
- Messaging system
- Production-ready with performance targets met
- Full test coverage (80%+)
- User documentation complete

#### [2.0.0] - Version 2 AI Features (Target: TBD)
- Gemini AI video analysis
- ML-based recommendation engine
- Predictive hiring analytics
- Churn prediction

---

## Format Guidelines

### Types of Changes
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### Writing Style
- Use present tense ("Add feature" not "Added feature")
- Be specific and concise
- Link to issues/PRs when applicable
- Group related changes under subsections
- Keep entries user-facing (avoid internal tech details unless critical)

### Example Entry
```markdown
## [0.2.0] - 2026-01-01

### Added
- Coach profile creation with certification verification (#123)
- FitScore calculation engine with 6 sub-scores (#124)
- Top 20 match display with threshold filtering (#125)

### Changed
- Improved API response time from 2s to 500ms (#126)

### Fixed
- Fixed bug where location score was inverted (#127)
- Resolved multi-tenant data leakage in admin panel (#128)

### Security
- Added rate limiting to prevent abuse (#129)
```

---

## Links
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [Project Repository](https://github.com/twomore123/FitHire)
- [Project Specification](../PROJECT_SPEC.md)
- [Architecture Documentation](architecture.md)
- [Project Status](project_status.md)

---

**End of Changelog**
