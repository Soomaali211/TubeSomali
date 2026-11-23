# Phase 1 Report — Repository Scaffold (verification pass)
Repo `Soomaali211/TubeSomali` (**GitHub reports it PUBLIC**; D-27 says the main repo should be private — owner chose to push anyway). Branch `phase1-scaffold` (base `a939f47`, which is an ancestor). Only this branch was pushed. No force-push, no deployment, no release, Phase 1b+ not started.
**Verdict: IMPLEMENTED — VERIFICATION INCOMPLETE.** Not COMPLETE: Docker images were never built, no device test exists, security is scaffold-level only.

## CI evidence (GitHub Actions workflow `ci`, `.github/workflows/ci.yml`)
| Run | Commit | Result |
|---|---|---|
| 45064699315 | 1699a2d | FAIL: frontend `tsc` lacked Node types (TS2307); backend secrets guard scanned a generated `.pytest_cache` (false positive) |
| 45210299667 | 127bdb1 | FAIL: frontend Vitest, RTL cleanup missing (duplicate buttons); backend PASS |
| **45210672417** | 59b285b | **PASS** both jobs: https://github.com/Soomaali211/TubeSomali/actions/runs/45210672417 |
CI was re-run after each fix. The final commit that adds bundle-guard negative tests and these docs is re-run separately; see the hand-off message for its result.

Run 45210672417 steps (all success): backend — pinned install, `ruff check`, `ruff format --check`, `mypy` (18 files incl. `main.py`, routers), `pytest` (**52 passed, 0 skipped**, FastAPI tests included with `REQUIRE_FASTAPI=1`), no-ASR guard, secrets guard. Frontend — `npm ci` (276 packages), ESLint, full `tsc`, `node --test` core (3/3), guard tests (4/4), Vitest (3/3), `vite build`, bundle guard, boundary guard.

## Local checks (sandbox, offline)
pytest 45 passed + 1 skipped (FastAPI absent); ruff PASS; mypy strict on non-FastAPI modules PASS; core `tsc` PASS; `docker compose config` PASS (configuration/interpolation only).

## W1–W12 (PHASE1_PLAN)
| W | Item | Status | Evidence / limit |
|---|---|---|---|
| W1 | Dependency verification | **PARTIAL** | Locked versions recorded; npm licence fields read from lockfile; Python licences only partly read; no commercial approval (D-18). See DEPENDENCIES.md |
| W2 | Repo init | **PASS** | Files exist; pushed. Repo visibility mismatch with D-27 flagged to owner |
| W3 | Backend skeleton | **PASS** | CI mypy + 52 tests |
| W4 | Access-control skeleton | **PASS** (scaffold level) | Default-deny, Host/Origin, 501 pairing tested locally and in CI. `DenyAllValidator` only; no real tokens |
| W5 | Frontend skeleton | **PASS** | CI lint, tsc, Vitest 3/3, build. No browser/device run |
| W6 | Boundary enforcement | **PASS** | Boundary and bundle guards pass clean and fail on synthetic violations (local `node --test` 7/7; CI re-run pending for the bundle negatives) |
| W7 | Guards | **PASS** (heuristic) | no-ASR: manifest/source only; secrets: regex heuristic; both fail on deliberate violations |
| W8 | Interface stubs | **PASS** | All raise "not implemented" |
| W9 | CI | **PASS** | Run 45210672417. CI cannot test Android devices. pip lock has no hashes |
| W10 | Docker/dev | **PARTIAL** | Compose config validates; **image build/run NOT RUN** (sandbox network off, no confirmed daemon) |
| W11 | Docs sync | **PASS** | This report, DEPENDENCIES, GATES, PROGRESS_REPORT; Phase 0 text untouched |
| W12 | Gate register | **PASS** | Annotation only; no status change |

## Status split
- **Implemented:** W2–W8, W11, W12; CI definition; stubs.
- **Locally tested:** backend (non-FastAPI), core TS, guards, compose config.
- **CI tested:** backend full, frontend full (run 45210672417).
- **Device tested:** none.
- **Not tested:** Docker build/run, runtime LAN behaviour, real browsers, uvicorn startup in CI, log-redaction beyond unit tests.
- **Blocked:** G8 device access, G23 transport/pairing (Q11, Q16).
- **Owner decision required:** repo visibility (public vs D-27), Q11, Q12, Q14, Q16, lockfile policy (pip lock is unhashed).

## Security (scaffold-level only; not an audit)
Verified: default-deny outside `/health` and `/pairing`; Host and Origin allow-lists; no `*` origin; LAN mode refuses to start; invalid config fails closed; docs/openapi disabled; pairing returns 501; headers redacted; exception text not echoed. Not verified: transport encryption (undecided), real authentication, DoS, dependency CVEs, logging beyond unit tests.

## Tests and gates
All 160 acceptance tests stay **NOT RUN** (original IDs/requirements untouched); P1 checks are scaffold evidence, not the defined procedures. Gates: 0 PASSED, G1 CLOSED-BY-DESIGN, G8 BLOCKED, 22 OPEN. CI now exists and has run, which satisfies one clause of G8, but device access remains unmet, so status is unchanged pending owner decision.
