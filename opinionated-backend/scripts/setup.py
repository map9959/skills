#!/usr/bin/env python3
"""Initialize a bare uv project and install the opinionated backend stack."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--scale", choices=("small", "scalable"), default="small")
    parser.add_argument("--cache", action="store_true")
    parser.add_argument("--mcp", action="store_true")
    args = parser.parse_args()
    target = args.directory.absolute()
    if target.is_symlink() or (target.exists() and (not target.is_dir() or any(target.iterdir()))):
        parser.error("target must be a new or empty directory")
    if shutil.which("uv") is None:
        parser.error("install uv first")

    subprocess.run(
        ["uv", "init", "--bare", "--vcs", "none", "--no-workspace", str(target)], check=True
    )
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "sqlalchemy[asyncio]",
        "alembic",
        "aiosqlite" if args.scale == "small" else "asyncpg",
    ]
    if args.cache:
        packages.append("cachetools" if args.scale == "small" else "valkey")
    if args.mcp:
        packages.append("fastmcp")
    subprocess.run(["uv", "add", *packages], cwd=target, check=True)
    subprocess.run(["uv", "add", "--dev", "ruff", "pyrefly", "pytest"], cwd=target, check=True)

    (target / ".gitignore").write_text(".venv/\n__pycache__/\n.env\n.env.*\n!.env.example\n")
    url = "sqlite+aiosqlite:///./app.db"
    if args.scale == "scalable":
        url = "postgresql+asyncpg://app:REPLACE_ME@localhost:5432/app"
    environment = f"DATABASE_URL={url}\n"
    if args.cache and args.scale == "scalable":
        environment += "VALKEY_URL=redis://localhost:6379/0\n"
    (target / ".env.example").write_text(environment)
    with open(target / ".env", "x", opener=lambda path, flags: os.open(path, flags, 0o600)) as file:
        file.write(environment)
    print(f"Backend packages installed in {target}. Ready for the agent to implement the app.")


if __name__ == "__main__":
    main()
