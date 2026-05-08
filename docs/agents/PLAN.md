# Architecture & Deployment Plan

## 1. Repository Strategy: Monorepo with Unified Versioning

**Decision:** Use a "Unified Versioning" strategy (CalVer) for the entire repository.
**Reasoning:**

- **Tight Coupling:** The API, Worker, and ML models evolve together.
- **Simplified Tooling:** `uv` workspaces allow local path dependencies, removing the need to publish internal packages to a private PyPI.
- **Release Consistency:** One Git Tag (`2026.01.0`) represents a validated state of the entire platform.

## 2. Workspace Structure (uv)

The project uses `uv` workspaces defined in `pyproject.toml`.

### Components

- **Root:** Orchestration, Dev Tooling, Shared Config.
- **packages/**: Shared libraries (e.g., `packages/core`, `packages/ml-utils`).
    - *Dependency Mode:* Referenced via workspace resolution (no version pinning needed locally).
- **apps/**: Deployable services (e.g., `apps/api`, `apps/worker`).
    - *Dependency Mode:* Depend on `packages/*` via workspace.

## 3. Runtime Architecture (Docker Compose)

Although the code is unified, the runtime is distributed into separate containers:

1. **API Service:** Runs FastAPI. Handles HTTP requests.
2. **Worker Service:** Runs Arq/Celery. Handles heavy geospatial processing.
3. **Database:** PostGIS (PostgreSQL + GIS extensions).
4. **Cache/Broker:** Redis (for task queues and caching).
5. **Frontend:** (Future) Nginx/Node container.

## 4. Versioning & Release Strategy

**Tool:** `bump-my-version` (already configured).

**Workflow:**

1. **Dev:** Commits use `latest` or `git-sha` tags.
2. **Release:** Run `bump-my-version bump release`.
    - Updates `pyproject.toml` (root).
    - Updates `Makefile.variables`.
    - Creates Git Tag (e.g., `river-levels-app-2026.01.1`).
3. **CI/CD:** Builds Docker images for all apps using the new tag.

## 5. Docker Strategy

**Pattern:** "Build from Root".
**Image Strategy:** Single "Backend" image containing all code (`apps/` and `packages/`).

### The "Volume Mount" Challenge

In development, we want to mount `.` to `/app` to edit code live. However, if `uv` installs dependencies into `/app/.venv` inside the image, mounting the host directory will hide them (or conflict with local Mac/Windows venvs).

**Solution:**

- Configure `uv` in Docker to install dependencies into the **System Python** (or a specific path like `/usr/local`).

- This separates *code* (mounted) from *dependencies* (baked in image).

- **Context:** The Docker build context must be the **project root**.

- **Reason:** Apps in `apps/` need to import code from `packages/`.

- **Dockerfiles:** Located in `docker/<app_name>/Dockerfile`.

### Service Definitions (Compose)

1. **api:**
    - Command: `uv run --package river-api uvicorn src.main:app ...`
2. **worker:**
    - Command: `uv run --package river-worker arq src.worker:WorkerSettings ...`
    - *Note:* Both services use the same `build: .` context and Dockerfile.

### Example Build Command

```bash
docker build -f docker/api/Dockerfile . -t my-registry/api:2026.01.0
```

## 5. Risk Analysis

- **Build Context Size:** Building from root sends all files to Docker daemon.
    - *Mitigation:* Strict `.dockerignore` is required (ignore `data/`, `venv/`, `.git/`).
- **Dependency Conflicts:** Shared environment in dev vs isolated in prod.
    - *Mitigation:* `uv sync` ensures lockfile consistency.
