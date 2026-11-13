#!/usr/bin/env python3
"""Initialize npm and install Svelte, TypeScript, Vite, and Biome. No app scaffold."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    target = args.directory.absolute()
    if target.is_symlink() or (target.exists() and (not target.is_dir() or any(target.iterdir()))):
        parser.error("target must be a new or empty directory")
    if shutil.which("npm") is None:
        parser.error("install Node.js and npm first")

    target.mkdir(parents=True, exist_ok=True)
    subprocess.run(["npm", "init", "--yes"], cwd=target, check=True)
    subprocess.run(["npm", "install", "svelte"], cwd=target, check=True)
    subprocess.run(
        [
            "npm",
            "install",
            "--save-dev",
            "typescript@^5.9",
            "vite",
            "@sveltejs/vite-plugin-svelte",
            "svelte-check",
            "@biomejs/biome",
        ],
        cwd=target,
        check=True,
    )
    subprocess.run(["npx", "--no-install", "biome", "init"], cwd=target, check=True)
    config_path = target / "biome.json"
    config = json.loads(config_path.read_text())
    config["html"] = {"experimentalFullSupportEnabled": True, "formatter": {"enabled": True}}
    config_path.write_text(json.dumps(config, indent=2) + "\n")

    package_path = target / "package.json"
    package = json.loads(package_path.read_text())
    package["type"] = "module"
    package["private"] = True
    package["scripts"] = {
        "lint": "biome lint .",
        "format": "biome format --write .",
        "check:biome": "biome check .",
    }
    package_path.write_text(json.dumps(package, indent=2) + "\n")
    (target / ".gitignore").write_text("node_modules/\ndist/\n.env\n.env.*\n!.env.example\n")
    print(
        f"Frontend packages installed in {target}. Ready for the agent to configure Vite and build the UI."
    )


if __name__ == "__main__":
    main()
