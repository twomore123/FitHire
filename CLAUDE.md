# CLAUDE.md

## Architecture Overview

FitHire is a full-stack application with separate backend and frontend services:

- **Backend:** Python + FastAPI + SQLAlchemy + PostgreSQL (hosted on Railway)
- **Frontend:** Next.js + Tailwind CSS + shadcn/ui (hosted on Vercel)
- **Database:** PostgreSQL on Neon (serverless)
- **Auth:** Clerk (JWT-based authentication)
- **Storage:** Cloudflare R2 (S3-compatible object storage)

**Key architectural patterns:**
- Monorepo structure (`/backend` and `/frontend` folders)
- RESTful API with versioning (`/api/v1/`)
- Multi-tenant data isolation (brand_id scoping)
- FitScore calculation engine (deterministic matching algorithm)

See [docs/architecture.md](docs/architecture.md) for complete technical details.

## Design Style Guide 

**Tech stack:** Next.js (App Router), Tailwind CSS, Shadcn UI

**Visual style**
- Clean, minimal interface
- Use Shadcn components for consistency
- Responsive design
- No dark mode for MVP

**Component patterns:**
- Shadcn UI for all interactive elements (buttons, inputs, cards)
- Tailwind for layout and spacing
- Keep components focused and small

## Product & UX Guidelines

**Core UX principles:**

**Copy tone:**
- Casual, friendly user-focused
- Brief labels and instructions
- Helpful error messages that suggest next steps

## Constraints & Policies

**Security - MUST follow:**
- ALWAYS use environment variables for secrets
- NEVER commit '.env.local' or any file with API keys
- Validate and sanitize all user input

**Code quality:**
- TypeScript strict mode
- Run 'npm run lint' before committing
- No 'any' types without justification

**Dependencies:**
- Prefer Shadcn components over adding new UI libraries
- Minimize external dependencies for MVP

## Repository Etiquette

**Branching:**
- ALWAYS create a feature branch before starting major changes
- NEVER commit directly to 'main'
- Branch naming: 'feature/description' or 'fix/description'

**Git workflow for major changes:**
1. Create a new branch: 'git checkout -b feature/your-feature-name'
2. Develop and commit on the feature branch
3. Test locally before pushing:
   - 'npm run dev' - start dev server at localhost:3000
   - 'npm run lint' - check for linting errors
   - 'npm run build' - production build to catch type errors
4. Push the branch: 'git push -u origin feature/your-feature-name'
5. Create a PR to merge into 'main'
6. Use the '/update-docs-and-commit' slash command for commits - this ensures docs are updated alongside code changes

**Commits:**
- Write clear commit messages describing the change
- Keep commits focused on single changes

**Pull Requests:**
- Create PRs for all changes to 'main'
- NEVER force push to 'main'
- Include description of what changed and why

**Before pushing:**
1. Run 'npm run lint'
2. Run 'npm run build' to catch type errors

## Documentation

- [Project Spec](PROJECT_SPEC.md) - Full requirements, API specs, tech details
- [Architecture](docs/architecture.md) - System design and data flow
- [Changelog](docs/changelog.md) - Version history
- [Project Status](docs/project_status.md) - Current progress
- Update files in the docs folder after major milestones and major additions to the project.

---

## Backend Development (Python/FastAPI)

**Tech stack:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL

**Code style:**
- Use Black for code formatting: `black .`
- Use Ruff for linting: `ruff check .`
- Type hints required for all functions
- Follow PEP 8 naming conventions
- Docstrings for public functions (Google style)

**Project structure:**
```
backend/
├── app/
│   ├── api/v1/routes/    # API endpoints
│   ├── core/             # Business logic (FitScore engine)
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── db/               # Database setup
├── tests/                # pytest tests
└── alembic/              # Database migrations
```

**API Development:**
- Keep route handlers thin (business logic in `core/`)
- Use Pydantic for request/response validation
- FastAPI auto-generates OpenAPI docs at `/docs`
- Version all endpoints: `/api/v1/...`

**Database:**
- Use Alembic for migrations: `alembic revision --autogenerate -m "description"`
- Never edit migrations manually (regenerate if needed)
- Test migrations on staging before production
- All queries must filter by `brand_id` for multi-tenancy

**Testing:**
- Write tests for FitScore engine (70%+ coverage target)
- Test all API endpoints with pytest
- Use fixtures for database setup
- Run tests before committing: `pytest`

**Before pushing backend changes:**
1. Run `black .` to format code
2. Run `ruff check .` to check linting
3. Run `pytest` to run tests
4. Run `alembic check` to verify migrations

**Environment variables:**
- Store in `/backend/.env` (never commit)
- Document new vars in `.env.example`
- Use Pydantic Settings for config management

---

## Testing Requirements

**Backend (pytest):**
- **Unit tests:** FitScore engine, utility functions
- **Integration tests:** API endpoints with test database
- **Coverage target:** 70%+ for Phase 1, 80%+ for production
- **Run:** `pytest` or `pytest --cov=app`

**Frontend (Jest + Playwright):**
- **Unit tests:** Components, utilities (Phase 2+)
- **E2E tests:** Critical user flows (Phase 2+)
- **Phase 1:** Manual testing acceptable for MVP

**Test database:**
- Use separate test database (Neon branch or local PostgreSQL)
- Reset database between test runs
- Never run tests against production database

---

## Design System

**Colors (to be defined):**
- Primary: TBD
- Secondary: TBD
- Accent: TBD
- Use Tailwind's default palette for now

**Typography:**
- System fonts (no custom fonts for MVP)
- Tailwind default font sizes
- Use semantic HTML headings (h1, h2, h3)

**Spacing:**
- Use Tailwind spacing scale (4, 8, 16, 24, 32px)
- Consistent padding/margins across components

**Accessibility:**
- All interactive elements keyboard accessible
- ARIA labels where needed
- shadcn/ui components are accessible by default
