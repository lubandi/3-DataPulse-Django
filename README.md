# DataPulse (Django)

## Overview

Upload datasets, define rules, run checks, track trends.
Built with Django	 REST Framework + PostgreSQL + Pandas + Docker.
(This is the Python/Django migration of the FAST API starter code).

## Quick Start

```bash
docker-compose up --build
```

API: http://localhost:8000

## API Endpoints

| Method | Endpoint                 | Status |
| ------ | ------------------------ | ------ |
| POST   | /api/auth/register       | Done   |
| POST   | /api/auth/login          | Done   |
| POST   | /api/datasets/upload     | Done   |
| GET    | /api/datasets            | Done   |
| POST   | /api/rules               | Done   |
| GET    | /api/rules               | Done   |
| PUT    | /api/rules/{id}          | TODO   |
| DELETE | /api/rules/{id}          | TODO   |
| POST   | /api/checks/run/{id}     | TODO   |
| GET    | /api/checks/results/{id} | TODO   |
| GET    | /api/reports/{id}        | TODO   |
| GET    | /api/reports/trends      | TODO   |

## Team Roles

### Backend (2-3 people)

- Complete checks and reports endpoints.
- Implement validation engine checks using Pandas.
- Implement scoring and report services.
- Add PUT/DELETE for rules.

### Data Engineers (1-2 people)

- Complete ETL pipeline transform/load in `data-engineering/`
- Build analytics schema
- Create Streamlit dashboard

### QA (1 person)

- Expand API tests in `qa/api-tests` (Make sure they test the Django API).
- Execute test plans
- Create edge case test data

### DevOps (1 person)

- Maintain CI/CD in `.github/`
- Optimize Docker setup
- Set up monitoring

## Env Vars

- DATABASE_URL (default: postgresql://datapulse:datapulse@db:5432/datapulse)
- SECRET_KEY (default: change-me-in-production)
