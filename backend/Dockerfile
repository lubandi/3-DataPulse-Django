FROM python:3.11-slim

WORKDIR /app

# Don't write .pyc files — keeps image clean
ENV PYTHONDONTWRITEBYTECODE 1
# Force stdout/stderr to be unbuffered — important for Docker log visibility
ENV PYTHONUNBUFFERED 1

# Install system dependencies required by psycopg2 (PostgreSQL adapter)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the uploads directory exists inside the container
# This mirrors the FastAPI Dockerfile's: RUN mkdir -p /app/uploads
RUN mkdir -p /app/uploads

# Document the port the container listens on
EXPOSE 8000

# Development server — replace with gunicorn for production:
#   CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
