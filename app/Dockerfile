FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir app 

COPY ../app /app
WORKDIR /app
RUN uv sync

ENTRYPOINT ["uv", "run", "app/main.py"]