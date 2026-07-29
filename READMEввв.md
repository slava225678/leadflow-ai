# LeadFlow AI

> AI-powered lead analysis service built with **FastAPI**, **SQLAlchemy
> 2**, and **OpenAI**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![Coverage](https://img.shields.io/badge/Coverage-91%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

------------------------------------------------------------------------

## Overview

LeadFlow AI is a backend portfolio project demonstrating modern Python
backend development practices.

The application accepts leads, stores them in PostgreSQL, performs AI
analysis in the background, and persists the generated results.

The project focuses on clean architecture, testability, dependency
injection, and maintainable code rather than feature count.

------------------------------------------------------------------------

## Features

-   REST API built with FastAPI
-   PostgreSQL + SQLAlchemy 2
-   Alembic migrations
-   Repository + Service architecture
-   Dependency Injection
-   Background lead analysis
-   LLM abstraction layer
-   OpenAI integration
-   Global exception handling
-   Request logging middleware
-   Unit and API tests
-   GitHub Actions CI
-   Ruff linting & formatting

------------------------------------------------------------------------

## Tech Stack

  Category     Technology
  ------------ -------------------------
  Language     Python 3.12
  Framework    FastAPI
  ORM          SQLAlchemy 2
  Database     PostgreSQL 17
  Migrations   Alembic
  Validation   Pydantic v2
  AI           OpenAI SDK
  Testing      pytest
  Linting      Ruff
  Containers   Docker & Docker Compose

------------------------------------------------------------------------

## Project Structure

``` text
app/
├── api/
├── core/
├── db/
├── dependencies.py
├── exceptions/
├── llm/
├── middleware/
├── models/
├── repositories/
├── schemas/
├── services/
├── workers/
└── main.py

tests/
alembic/
.github/workflows/
```

------------------------------------------------------------------------

## Architecture

``` text
                HTTP Request
                     │
                     ▼
                FastAPI Router
                     │
                     ▼
              Dependency Injection
                     │
                     ▼
                LeadService
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   LeadRepository          LLM Client
          │                     │
          ▼                     ▼
     PostgreSQL            OpenAI API
```

The application follows a layered architecture where business logic is
isolated from infrastructure concerns.

------------------------------------------------------------------------

## Getting Started

### Clone

``` bash
git clone <repository-url>
cd leadflow-ai
```

### Configure environment

Create a `.env` file.

``` env
POSTGRES_DB=leadflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

DATABASE_URL=postgresql+psycopg://postgres:password@db:5432/leadflow

OPENAI_API_KEY=your_api_key
```

### Start the application

``` bash
docker compose up --build
```

API:

    http://localhost:8000

Swagger:

    http://localhost:8000/docs

------------------------------------------------------------------------

## Database Migrations

``` bash
alembic upgrade head
```

Create a migration:

``` bash
alembic revision --autogenerate -m "description"
```

------------------------------------------------------------------------

## Running Tests

``` bash
pytest
```

Coverage:

``` bash
pytest --cov=app --cov-report=term-missing
```

Lint:

``` bash
ruff check .
ruff format --check .
```

------------------------------------------------------------------------

## API Flow

1.  Client creates a lead.
2.  Lead is stored with status **NEW**.
3.  Background worker starts analysis.
4.  OpenAI generates insights.
5.  Lead status becomes **COMPLETED**.
6.  Analysis is saved in the database.

------------------------------------------------------------------------

## Testing Strategy

The project separates business logic from infrastructure.

Covered:

-   Service layer
-   Repository layer
-   API endpoints
-   Background worker

External services are replaced with fakes during testing, allowing
deterministic and fast test execution.

Current test coverage:

**91%**

------------------------------------------------------------------------

## CI

Every push triggers:

-   Ruff
-   Formatting check
-   Unit tests
-   Coverage report

------------------------------------------------------------------------

## Future Improvements

-   Structured logging
-   Pre-commit hooks
-   Health check endpoint
-   Production configuration profiles

------------------------------------------------------------------------

## License

MIT
