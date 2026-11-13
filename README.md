# Michael Paciullo's Skills

I found that I often told my agents the same stuff every time I start a new project. I'm writing it all down so I don't have to. Hopefully, you find this useful as well.

## Minimal setup scripts

Requires Python 3.10+, uv for the backend, and Node.js/npm for the frontend:

```sh
python3 opinionated-backend/scripts/setup.py ./my-app/backend
python3 opinionated-frontend/scripts/setup.py ./my-app/frontend
# Optional PostgreSQL, Valkey cache, and FastMCP instead of the SQLite default:
python3 opinionated-backend/scripts/setup.py ./service --scale scalable --cache --mcp
```

These initialize package management and install dependencies in a new or empty directory. An agent (or you) should be able to pick it up afterward. Backend setup also creates gitignored `.env` and tracked `.env.example` files so you can keep track of which environment variables are being used. Commit generated lockfiles; subsequent installs use `uv sync --locked` or `npm ci`.
