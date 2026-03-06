FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files
COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY apps/worker/pyproject.toml apps/worker/pyproject.toml
COPY packages/connectors/pyproject.toml packages/connectors/pyproject.toml
COPY packages/core/pyproject.toml packages/core/pyproject.toml
COPY packages/databases/pyproject.toml packages/databases/pyproject.toml

# Install dependencies into system python
ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the code
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

