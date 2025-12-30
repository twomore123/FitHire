# FitHire by Coach360

**Purpose:** Connect verified fitness professionals with relevant job opportunities and help clubs/studios identify aligned candidates using a deterministic FitScore ranking system.

---

## Overview

FitHire is a full-stack platform that streamlines the hiring process for fitness professionals and organizations. Coaches create verified profiles with certifications, experience, and availability. Clubs and studios post job listings with specific requirements and culture indicators. FitHire calculates a **FitScore** to rank matches between coaches and jobs, helping both sides find optimal alignment quickly.

### Key Features
- **Deterministic FitScore:** Transparent ranking based on certifications, experience, availability, culture, and engagement
- **Top-N Matching:** Top 20 matches for coaches and jobs
- **Admin Verification:** Manual verification ensures high data integrity
- **Multi-Tenant:** Multi-level access for brands, regions, and locations
- **Threshold-Based:** Display only relevant matches above configurable threshold

### Tech Stack
- **Backend:** Python + FastAPI + SQLAlchemy + PostgreSQL (Railway)
- **Frontend:** Next.js + TypeScript + Tailwind CSS + shadcn/ui (Vercel)
- **Database:** PostgreSQL on Neon (serverless)
- **Auth:** Clerk (JWT-based)
- **Storage:** Cloudflare R2 (S3-compatible)

---

## Project Structure

```
FitHire/
├── backend/            # FastAPI backend service
├── frontend/           # Next.js frontend application
├── docs/               # Project documentation
├── .env.example        # Environment variables template
├── CLAUDE.md           # Development guidelines
└── PROJECT_SPEC.md     # Complete project specification
```

---

## Quick Start

### Prerequisites
- **Backend:** Python 3.11+, Poetry
- **Frontend:** Node.js 18+, npm
- **Database:** Neon PostgreSQL account
- **Auth:** Clerk account
- **Storage:** Cloudflare R2 account

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/twomore123/FitHire.git
   cd FitHire
   ```

2. **Set up environment variables:**
   ```bash
   # Copy and fill in backend .env
   cp backend/.env.example backend/.env

   # Copy and fill in frontend .env.local
   cp frontend/.env.example frontend/.env.local
   ```

3. **Set up backend:**
   ```bash
   cd backend
   poetry install
   poetry run alembic upgrade head
   poetry run python -m app.main
   ```
   Backend runs on http://localhost:8000

4. **Set up frontend (in a new terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs on http://localhost:3000

---

## Documentation

- **[PROJECT_SPEC.md](PROJECT_SPEC.md)** - Complete product and engineering specification
- **[docs/architecture.md](docs/architecture.md)** - System architecture and technical design
- **[docs/project_status.md](docs/project_status.md)** - Current progress and milestones
- **[docs/changelog.md](docs/changelog.md)** - Version history
- **[CLAUDE.md](CLAUDE.md)** - Development guidelines and coding standards
- **[backend/README.md](backend/README.md)** - Backend setup and API documentation
- **[frontend/README.md](frontend/README.md)** - Frontend setup and component guide

---

## Development

### Backend
```bash
cd backend
poetry run python -m app.main           # Start dev server
poetry run pytest                       # Run tests
poetry run black .                      # Format code
poetry run ruff check .                 # Lint code
```

### Frontend
```bash
cd frontend
npm run dev                             # Start dev server
npm run lint                            # Lint code
npm run type-check                      # Type check
npm run build                           # Build for production
```

---

## Deployment

### Backend (Railway)
1. Connect GitHub repository to Railway
2. Configure environment variables
3. Deploy automatically on push to main

### Frontend (Vercel)
1. Connect GitHub repository to Vercel
2. Configure environment variables
3. Deploy automatically on push to main

---

## License

Proprietary - FitHire by Coach360

---

## Getting Help

- Read the [PROJECT_SPEC.md](PROJECT_SPEC.md) for detailed requirements
- Check [docs/architecture.md](docs/architecture.md) for technical details
- Review [CLAUDE.md](CLAUDE.md) for development guidelines
