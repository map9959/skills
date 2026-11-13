---
name: opinionated-backend
description: Build and maintain Python backends with an opinionated stack of uv, Ruff, Pyrefly, pytest, FastAPI, Pydantic, SQLAlchemy, and Alembic. Use when creating or scaffolding a backend, API, MCP server, database layer, or Python service, or when choosing backend tooling. Pair with opinionated-frontend for full-stack apps. Respect explicit user requirements and do not migrate an existing stack without authorization.
---

# Opinionated Backend

Use this stack as the default for new backend work. Inspect an existing project's configuration before changing it; apply these choices within the requested scope rather than rewriting unrelated code.

## Minimal setup script

For a new project, run `scripts/setup.py` with Python 3.10+ and uv installed. Paths below are relative to this skill's directory:

```sh
python3 scripts/setup.py /path/to/backend
python3 scripts/setup.py /path/to/backend --scale scalable --cache --mcp
```

The script runs `uv init --bare`, installs the selected runtime packages plus Ruff, Pyrefly, and pytest, and creates `.env`, `.env.example`, and `.gitignore`. The default is SQLite with no cache or MCP. `--cache` adds cachetools for `small` or Valkey for `scalable`; `--mcp` adds FastMCP. It refuses non-empty targets. No application code, migrations, or services are scaffolded; implement those next. Edit placeholder PostgreSQL credentials before use.

The initial install resolves dependencies and writes `uv.lock`; commit that lockfile and use `uv sync --locked` for subsequent installs. Do not run the script against an existing application.

## Python tooling

- Use **uv** for Python versions, environments, dependency management, and command execution. Use `uv init` for a new project, `uv add` for runtime dependencies, `uv add --dev` for development dependencies, and `uv run` for commands. Do not introduce pip, Poetry, or a separate requirements-file workflow.
- Keep dependencies and tool configuration in `pyproject.toml`. Commit `uv.lock` for reproducible installs; use `uv sync --locked` in CI.
- Use **Ruff** for both linting and formatting, **Pyrefly** for type-checking, and **pytest** for unit tests. Do not add competing linters, formatters, or type-checkers by default.
- Add development tools with `uv add --dev ruff pyrefly pytest`. Add asynchronous testing support, such as `pytest-asyncio`, when tests need it.
- Use type annotations and address reported errors rather than broadly disabling checks.

## API and data models

- Use **FastAPI** for HTTP APIs.
- Use **Pydantic**, which comes with FastAPI, for validated request, response, and other boundary data models. Prefer explicit schemas over unstructured dictionaries.
- Use **FastMCP** when the application needs an MCP server. Do not add MCP infrastructure to an ordinary API unless it is needed.
- Keep blocking work out of asynchronous request handlers. Manage database and cache resources through application lifecycle hooks and dependency injection.

## Database and cache

Choose infrastructure according to the application's scale, not hypothetical future needs. Default to the local/small-app stack unless requirements indicate a scalable deployment; clarify if the choice materially affects the requested work.

| Application | Database | Async driver | Cache, only if needed |
| --- | --- | --- | --- |
| Local or small app | SQLite | `aiosqlite` | In-memory cache |
| Scalable app | PostgreSQL | `asyncpg` | Valkey |

- Use **SQLAlchemy** as the ORM and **Alembic** for schema migrations in either case. Only add database dependencies when the application needs persistence.
- Use SQLAlchemy's async engine and sessions with the selected driver. Use `sqlite+aiosqlite:///...` or `postgresql+asyncpg://...` connection URLs.
- Use SQLAlchemy's typed declarative models for persistence and Pydantic models for API validation and serialization.
- Use a session per request or unit of work, with explicit transaction boundaries and cleanup. Do not share a mutable session across concurrent tasks.
- Create and review Alembic migrations for schema changes. Configure Alembic to use the same database settings and model metadata as the application, with an async-compatible migration environment. Do not substitute startup-time `create_all()` for migrations.
- Keep SQLite-specific assumptions out of code intended for PostgreSQL. Test database-specific behavior against the actual target database.
- Add a cache only for a demonstrated need. A process-local in-memory cache is not shared across workers; use Valkey when shared cache state is required. Define expiration and invalidation behavior.

Example dependency commands, selecting only what is needed:

```sh
uv add fastapi 'uvicorn[standard]' pydantic-settings python-dotenv
uv add 'sqlalchemy[asyncio]' alembic aiosqlite  # Local/small app
# For a scalable app, use asyncpg instead of aiosqlite.
# Add fastmcp only when an MCP server is required.
```

## Configuration and secrets

- Never hardcode secrets in source, examples, tests, or migration files. Load local configuration from **`.env`** using **python-dotenv**, directly or through Pydantic Settings' dotenv integration.
- Centralize and validate settings with `pydantic-settings`. Let real environment variables override `.env` values so deployment configuration does not depend on a local file.
- Create **`.env.example`** containing the required variable names and safe placeholder values. Keep it synchronized with settings and document how to copy it to `.env`.
- Ensure **`.env` is gitignored**. Check `.gitignore` after `uv init`; do not assume initialization added the rule. Ignore other secret-bearing dotenv variants when used, while keeping `.env.example` trackable.
- Never overwrite an existing `.env` or print its secrets. Do not commit credentials, database passwords, or tokens, or log secret-bearing settings and connection URLs.

## Verification

Run the applicable checks before reporting completion:

```sh
uv run ruff check .
uv run ruff format --check .
uv run pyrefly check
uv run pytest
```

Use `uv run ruff format .` to apply formatting. Test business logic and failure cases; for database-backed work, verify migrations against an isolated test database. Never run destructive test setup against a user's live database.

Document setup, local startup, migration, and verification commands. Report which checks ran and any that could not run.
