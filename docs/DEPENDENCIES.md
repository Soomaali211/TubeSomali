# Dependencies (Phase 1, W1 — PARTIAL)
Status: **NOT VERIFIED** except where marked. Bash network was off, so registry versions and licences could not be looked up. Commercial eligibility (D-18) is **not assessed**.

| Package | Where | Declared range | Version/licence evidence |
|---|---|---|---|
| fastapi, uvicorn | backend runtime | >=0.115, >=0.30 | UNVERIFIED (not installed locally) |
| httpx | backend dev | >=0.27 | UNVERIFIED |
| pytest | backend dev | >=8 | installed 9.1.1, licence MIT (local metadata) |
| mypy | backend dev | >=1.11 | installed 2.3.1, licence MIT (local metadata) |
| ruff | backend dev | >=0.6 | CLI present; licence metadata not read |
| react, react-dom | frontend | ^19 | UNVERIFIED |
| vite, @vitejs/plugin-react, vitest, jsdom | frontend dev | ^6, ^4.3, ^3, ^25 | UNVERIFIED |
| typescript, eslint, typescript-eslint, @eslint/js, @testing-library/react, @types/* | frontend dev | ^5.6, ^9, ^8, ^9, ^16, ^19 | UNVERIFIED. Local global `tsc` is 7.0.2, which differs from the declared range |

No lockfiles exist, so installs are **not reproducible**. CI installs with `npm ci` when a lockfile exists, else `npm install` with a warning, and uploads the generated lockfile as an artifact. No ASR/Whisper/TTS/translation packages are declared (guard: `tools/guards/check_no_asr.py`, manifest and source scan only, no transitive scan).
