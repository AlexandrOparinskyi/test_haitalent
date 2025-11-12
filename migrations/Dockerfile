FROM python:3.11-slim

WORKDIR /app

RUN pip install alembic environs asyncpg

# Копируем всё необходимое для миграций
COPY migrations/ ./migrations/
COPY alembic.ini .
COPY config.py .
COPY app/database/ ./app/database/

CMD ["alembic", "upgrade", "head"]