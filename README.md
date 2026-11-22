# TubeSomali

Somali-language video app. **Status: Phase 1 repository scaffold only.** No translation, TTS, ASR, player,
pairing or transport is implemented. Phase 0 documents in `docs/` remain the source of truth; gates are
unchanged (see `docs/GATES.md`). Security is not claimed complete or audited.

## Layout
- `backend/` FastAPI skeleton: loopback bind, default-deny auth, Host/Origin allow-lists, error envelope, interface stubs.
- `frontend/` React + TypeScript + Vite shell: Somali home, two hard-separated modes (placeholders).
- `tools/guards/` guard scripts (no ASR, no secrets, YouTube/core boundaries, bundle check).
- `.github/workflows/ci.yml` CI definition (committed locally; not pushed, never run).
- `docs/PHASE1_REPORT.md` exact commands, results and what was NOT run.

## Local checks
Backend: `cd backend && pip install -r requirements-dev.txt && ruff check . && mypy && pytest`
Frontend: `cd frontend && npm install && npm run lint && npm run typecheck && npm test && npm run test:core && npm run build && npm run check:bundle`
Guards: `python tools/guards/check_no_asr.py`, `python tools/guards/check_secrets.py`, `node tools/guards/check_boundaries.mjs`

Open decisions (transport Q11, G24 policy Q12, host Q16, storage Q14) are not decided here. See `docs/DECISIONS.md`.
