# Changelog

All notable changes to FitHire will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Coach profile creation and management
- Job listing creation and management
- FitScore calculation engine
- Top 20 match display
- Admin verification workflow
- Multi-unit organizational hierarchy
- Threshold-based filtering

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
