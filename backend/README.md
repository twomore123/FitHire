# FitHire Backend

FastAPI backend service for the FitHire platform.

## Tech Stack

- **Python** 3.11+
- **FastAPI** - Modern async web framework
- **SQLAlchemy** 2.0 - ORM with async support
- **Alembic** - Database migrations
- **Pydantic** v2 - Data validation
- **PostgreSQL** 15+ - Database (Neon hosted)
- **Clerk** - Authentication
- **Cloudflare R2** - File storage

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Settings management (Pydantic)
│   │
│   ├── api/                 # API layer
│   │   └── v1/
│   │       └── routes/      # API endpoints
│   │           ├── auth.py
│   │           ├── coaches.py
│   │           ├── jobs.py
│   │           ├── admin.py
│   │           └── brands.py
│   │
│   ├── core/                # Business logic
│   │   └── fitscore/        # FitScore calculation engine
│   │       ├── engine.py
│   │       ├── presets.py
│   │       └── explainer.py
│   │
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── db/                  # Database setup and session management
│   └── utils/               # Utility functions
│
├── tests/                   # pytest tests
├── alembic/                 # Database migrations
├── pyproject.toml           # Poetry dependencies
└── .env.example             # Environment variables template
```

## Setup

### Prerequisites

- Python 3.11+
- Poetry (dependency management)
- PostgreSQL database (Neon account)

### Installation

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```bash
   cd backend
   poetry install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

4. **Run database migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

## Development

### Run the development server:
```bash
poetry run python -m app.main
```

Or with uvicorn directly:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Code Formatting

Format code with Black:
```bash
poetry run black .
```

### Linting

Check code with Ruff:
```bash
poetry run ruff check .
```

Fix auto-fixable issues:
```bash
poetry run ruff check . --fix
```

### Testing

Run tests:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=app --cov-report=term-missing
```

### Database Migrations

Create a new migration:
```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
poetry run alembic upgrade head
```

Rollback migration:
```bash
poetry run alembic downgrade -1
```

## Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string (from Neon)
- `CLERK_SECRET_KEY` - Clerk authentication secret
- `R2_*` - Cloudflare R2 credentials
- `SECRET_KEY` - JWT signing secret (generate with `openssl rand -hex 32`)

## Pre-commit Checklist

Before committing:
1. ✅ Run `black .` to format code
2. ✅ Run `ruff check .` to check linting
3. ✅ Run `pytest` to ensure tests pass
4. ✅ Run `alembic check` to verify migrations

## API Documentation

When the development server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

See [../docs/architecture.md](../docs/architecture.md) for detailed system architecture.

## License

Proprietary - FitHire by Coach360
