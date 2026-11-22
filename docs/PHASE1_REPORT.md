# Phase 1 Report — Repository Scaffold
Branch `phase1-scaffold` (from `a939f47`). **Not pushed. No CI run exists.** Phase 1b/2+ not started.
Overall status: **PARTIALLY IMPLEMENTED — VERIFICATION INCOMPLETE** (FastAPI/httpx, npm packages, Docker and GitHub Actions unavailable here).

## Checks run locally
| ID | Check | Command | Result | Limitation |
|---|---|---|---|---|
| P1-01 | Backend unit tests (config, middleware via framework-free ASGI harness, AST boundaries, contracts, guards) | `cd backend && python3 -m pytest -q -p no:cacheprovider` | PASS: 45 passed, 1 skipped | The skipped module is the FastAPI app test |
| P1-02 | FastAPI app tests | same | NOT RUN (fastapi/httpx not installed); CI sets `REQUIRE_FASTAPI=1` so a missing dependency fails | |
| P1-03 | ruff lint + format | `ruff check .`; `ruff format --check .` | PASS | |
| P1-04 | mypy strict | `python3 -m mypy --strict app/config.py app/errors.py app/contracts.py app/security` | PASS (7 files) | `main.py`, `routers/*` NOT type-checked |
| P1-05 | No-ASR guard | `python3 tools/guards/check_no_asr.py` | PASS | Manifest/source only |
| P1-06 | Secrets guard | `python3 tools/guards/check_secrets.py` | PASS | Heuristic, not an audit |
| P1-07 | Boundary guard (clean tree) | `node tools/guards/check_boundaries.mjs` | PASS | |
| P1-08 | Guards fail on deliberate violations | `pytest tests/test_guards.py`; `node --test tests/guards.test.mjs` (frontend) | PASS (backend within P1-01; frontend 4/4) | |
| P1-09 | Frontend core tests | `node --test "src/core/*.test.ts"` | PASS 3/3 | |
| P1-10 | Core type-check | `tsc --noEmit -p tsconfig.core.json` | PASS | TS 7.0.2, not the declared ^5.6 |
| P1-11 | CI YAML parses | `yaml.safe_load` | PASS | Syntax only; not executed by GitHub |
| P1-12 | ESLint, full `tsc`, Vitest, `vite build`, `check_bundle.mjs` | `npm run ...` | NOT RUN (no node_modules; network off) | check_bundle.mjs untested |
| P1-13 | Docker build / compose | | NOT RUN | |
| P1-14 | GitHub Actions run | | NOT RUN (not pushed) | |

## Decisions not made
Transport (Q11), LAN pairing, HTTP fallback, backend host (Q16): untouched. LAN mode refuses to start. Pairing returns 501.

## Acceptance tests and gates
All 160 acceptance tests stay **NOT RUN**: P1 checks are scaffold-level evidence, not the defined AT procedures. Gates unchanged (0 PASSED, G8 BLOCKED, G23 OPEN). No device tests run.
