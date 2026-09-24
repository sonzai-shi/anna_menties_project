FROM python:3.12-slim as builder

WORKDIR /app

ENV POETRY_VERSION=2.4.1 \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-ansi --only main

COPY . .

FROM python:3.12-slim as runtime

WORKDIR /app

RUN useradd -r appuser

COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.application:get_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]