---
name: opinionated-frontend
description: Build and maintain frontends using Svelte with TypeScript and Biome for linting and formatting, without SvelteKit. Use when creating or scaffolding a frontend, web UI, single-page app, or Svelte components, or when choosing frontend tooling. Pair with opinionated-backend when backend functionality is needed. Respect explicit user requirements and do not migrate an existing stack without authorization.
---

# Opinionated Frontend

Use **Svelte with TypeScript**, not SvelteKit. Backend functionality belongs in the separate backend described by `opinionated-backend`.

Inspect an existing project's configuration before changing it. Apply these defaults within the requested scope; do not migrate an existing application or replace unrelated tooling without authorization.

## Project setup

- For a new application, use **Vite's Svelte + TypeScript template** (`svelte-ts`), not a SvelteKit scaffold.
- Use the project's existing JavaScript package manager and lockfile. If starting from scratch with no preference, use npm; keep a single package-manager lockfile.
- Use TypeScript for application code and `<script lang="ts">` in Svelte components. Enable strict type-checking.
- Follow the installed Svelte version's idioms. Prefer current Svelte conventions for new projects rather than copying legacy patterns.
- Keep components focused and type their props, state, and API boundaries. Share reusable logic and API calls through ordinary TypeScript modules.

For minimal package setup, run `scripts/setup.py` with Python 3.10+ and a current supported Node.js/npm installation. Paths below are relative to this skill's directory:

```sh
python3 scripts/setup.py /path/to/frontend
```

The script runs `npm init`, installs Svelte, TypeScript, Vite, the Svelte Vite plugin, svelte-check, and Biome, initializes Biome with Svelte support, and adds lint/format scripts and `.gitignore`. It does not generate application code or a Vite/TypeScript scaffold; configure those next. TypeScript is constrained to a known compatible major for svelte-check.

The initial install resolves dependencies and writes `package-lock.json`; commit it and use `npm ci` for subsequent installs. The script refuses non-empty targets. Do not run it against an existing application; preserve that application's package manager and setup instead.

## Linting, formatting, and type-checking

- Use **Biome** for linting and formatting. Do not introduce ESLint or Prettier as default alternatives or run overlapping formatters.
- Commit a `biome.json` or `biome.jsonc` configuration and expose package scripts for linting, formatting, and CI checks.
- Verify the installed Biome version's Svelte support. Where required by that version, explicitly enable full HTML/Svelte support and HTML formatting. Do not claim complete `.svelte` coverage if the installed version cannot provide it.
- With Biome versions using the current experimental Svelte support, merge this into the generated configuration:

  ```json
  {
    "html": {
      "experimentalFullSupportEnabled": true,
      "formatter": {
        "enabled": true
      }
    }
  }
  ```

- Check these options against the installed version rather than blindly applying an incompatible configuration. If Svelte syntax is unsupported, report the limitation instead of silently adding another formatter or ignoring all Svelte files.
- Use **svelte-check** and **TypeScript** for type-checking; Biome does not replace the type-checker. Preserve the Vite template's TypeScript project references and checks.

Suggested package scripts, adapting to existing conventions:

| Script | Command |
| --- | --- |
| `lint` | `biome lint .` |
| `format` | `biome format --write .` |
| `check:biome` | `biome check .` |

Keep or add a separate `check` script that runs `svelte-check` and the template's TypeScript checks. Keep Vite's development and production build scripts.

## Backend boundary

- Treat this as a client-side frontend. Do not add SvelteKit routes, server hooks, server actions, or `+page.server.ts` files.
- Call the separate backend through a typed API layer. Use the `opinionated-backend` skill for backend implementation when it is available; do not move backend logic into a frontend development server.
- Keep API base URLs configurable. Use Vite's development proxy or intentionally configured backend CORS as appropriate; do not hardcode deployment hosts.
- Never put secrets in browser code or `VITE_*` environment variables, which are exposed to clients. Backend credentials and privileged operations stay on the backend.
- Model loading, empty, and error states explicitly. Use semantic HTML and accessible controls.
- Add client-side routing only if the UI needs it. Do not introduce SvelteKit just to get a router.

## Verification

Run Biome checks, Svelte/TypeScript checks, the production build, and any existing tests using the project's package scripts. Resolve failures introduced by the changes and report any checks that could not run.

For UI work, verify the affected interactions and layout at appropriate viewport sizes when browser tooling is available. Document development commands and how the frontend connects to the backend.
