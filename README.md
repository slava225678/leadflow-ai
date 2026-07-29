# LeadFlow AI

> AI-powered lead analysis service built with **FastAPI**, **SQLAlchemy
> 2**, and the **OpenAI API**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![Coverage](https://img.shields.io/badge/Coverage-91%25-brightgreen)

------------------------------------------------------------------------

## Highlights

-   Clean layered architecture
-   Repository & Service patterns
-   Dependency Injection
-   Background lead processing
-   OpenAI abstraction layer
-   91% test coverage
-   GitHub Actions CI
-   Dockerized development environment

------------------------------------------------------------------------

## Overview

LeadFlow AI is a backend portfolio project demonstrating modern Python
backend development practices.

The application accepts leads, stores them in PostgreSQL, analyzes them
using an LLM in the background, and persists the generated results.

The primary goal of the project is to showcase maintainable
architecture, testability, and clean separation of responsibilities.

------------------------------------------------------------------------

## Features

-   FastAPI REST API
-   PostgreSQL + SQLAlchemy 2
-   Alembic migrations
-   Repository + Service architecture
-   Dependency Injection
-   Background processing
-   OpenAI integration through an abstraction layer
-   Global exception handling
-   Request logging middleware
-   Unit & API tests
-   Ruff
-   GitHub Actions

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
Dependencies
      │
      ▼
 LeadService
   │        │
   ▼        ▼
Repository  LLMClient
   │        │
   ▼        ▼
PostgreSQL OpenAI API
```

------------------------------------------------------------------------

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/slava225678/leadflow-ai.git
cd leadflow-ai
```

### 2. Configure environment

Create a `.env` file from the provided template:

``` bash
cp .env.example .env
```

Edit the values if necessary.

### 3. Configure OpenAI

Lead analysis requires a valid OpenAI API key.

Set your API key in the `.env` file:

``` env
OPENAI_API_KEY=your_api_key
```

Without a valid API key, AI analysis will not work.

### 4. Build and start containers

``` bash
docker compose up --build -d
```

### 5. Apply database migrations

``` bash
docker compose exec api alembic upgrade head
```

The API will be available at:

    http://localhost:8000

Swagger UI:

    http://localhost:8000/docs

------------------------------------------------------------------------

## AI Integration

The application communicates with the language model through the
`LLMClient` interface.

This makes the business layer independent of any specific provider and
allows replacing OpenAI with another LLM implementation without changing
the service layer.

The project was developed and tested using:

-   Provider: OpenAI
-   Model: gpt-4.1-mini

------------------------------------------------------------------------

## Development

Create a migration:

``` bash
docker compose exec api alembic revision --autogenerate -m "description"
```

Apply migrations:

``` bash
docker compose exec api alembic upgrade head
```

Run tests:

``` bash
pytest --cov=app --cov-report=term-missing
```

Run linting:

``` bash
ruff check .
ruff format --check .
```

------------------------------------------------------------------------

## Testing

Business logic is tested independently from infrastructure.

Covered components include:

-   Service layer
-   Repository layer
-   Background worker
-   API endpoints

External dependencies are replaced with fakes, providing deterministic
and fast tests.

Current coverage: **91%**

------------------------------------------------------------------------

## CI

Every push and pull request runs:

-   Ruff linting
-   Formatting validation
-   Automated tests
-   Coverage reporting

------------------------------------------------------------------------

## Future Improvements

-   Structured logging
-   Pre-commit hooks
-   Health check endpoint
-   Production configuration profiles

------------------------------------------------------------------------

## License

MIT
