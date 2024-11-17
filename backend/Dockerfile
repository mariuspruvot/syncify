# backend/Dockerfile
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Les fichiers sont à la racine du contexte (dossier backend)
COPY pyproject.toml ./
COPY uv.lock ./

# Install all dependencies and project
RUN uv sync --frozen

# Copy the rest
COPY . .

# Environment setup
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]