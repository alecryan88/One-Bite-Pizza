FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock .python-version /app/
COPY ./extract /app/extract
RUN uv sync --frozen

# Code will be mounted at runtime by scripts/docker/run.sh
ENTRYPOINT ["uv", "run"]

