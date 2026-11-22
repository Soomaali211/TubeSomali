# TubeSomali — Phase 1 Implementation Plan (Repository scaffold)

**Version:** reconciliation pass 1 · 2026-11-20 · DRAFT · *(pass 4, 2026-11-22: statuses annotated, see §9)* · **No Phase 1 code has been written.** This plan is for owner approval; commands named here are *intended* and untested.

## 1. Goal and non-goals
**Goal:** a clean, tested, boundary-enforcing scaffold on which every later phase builds — with the backend safe-by-default (G23) and the YouTube/Authorized separation enforced by tooling from day one.
**Non-goals (not in Phase 1):** models, translation, TTS, caption retrieval, audio/mixing, player UI, media import, pairing UI, PWA, Docker publishing. Those belong to later phases.

## 2. Preconditions (see DECISIONS §8.2)
| Needed | Why | Status |
|---|---|---|
| Owner approval of Phase 0 documents | Process rule | OPEN |
| **Q6** repository location / branch conventions | Where code goes; "preserve existing work" | OPEN → *(pass 4)* **DECIDED**: `Soomaali211/TubeSomali` (D-21); branch convention for Phase 1 still OPEN |
| **Q7** installs allowed (new chat) or tests run on owner's machine/CI | Cannot install or test in this sandbox (G8 BLOCKED) | OPEN → *(pass 4)* **DECIDED (selection)**: Android phone + GitHub Actions CI (D-22); **not configured, not verified**; G8 stays BLOCKED |
| **Q11** transport choice | Only affects the *later* pairing implementation; Phase 1 builds the default-deny skeleton regardless | PROPOSED *(pass 4: HTTPS = direction to investigate only, not approved; ARCHITECTURE §11a)* |
| **Q2/Q13** host OS and network | Run docs (Docker vs plain), LAN-mode tests | PROPOSED / OPEN *(pass 4: D-22 names a phone and CI but no PC — Q16 asks whether a PC exists)* |

## 3. Target repository layout (proposed)
```
/ (repo root)
├─ docs/                      # the Phase 0 documents (kept in repo)
├─ frontend/                  # React + TypeScript + Vite
│  ├─ src/
│  │  ├─ core/                # pure logic only (segments, i18n, storage interfaces) — no network, no media APIs
│  │  ├─ modes/
│  │  │  ├─ youtube/          # official-player adapter placeholder; MAY NOT import authorized/ or audio/TTS code
│  │  │  └─ authorized/       # authorized-media placeholders (player, subtitles, mixer, scheduler, rights)
│  │  ├─ app/                 # shell, routes, mode selection
│  │  └─ locales/so.ts        # Somali strings (draft, needs native review)
│  └─ tests/
├─ backend/
│  ├─ app/
│  │  ├─ main.py              # app factory
│  │  ├─ config.py            # settings (loopback default, LAN flag)
│  │  ├─ errors.py            # fixed error vocabulary + envelope
│  │  ├─ security/            # access control skeleton (default-deny, token interface, host/CORS allow-lists)
│  │  ├─ routers/             # health (+ pairing placeholder returning "not implemented")
│  │  ├─ translation/ tts/ subtitles/ jobs/   # empty module skeletons with interface stubs only
│  │  └─ research/            # empty; excluded from release config
│  └─ tests/
├─ .github/workflows/ (if GitHub)   # CI
├─ docker-compose.yml, backend/Dockerfile, frontend/Dockerfile (dev)
├─ .env.example, .gitignore, README.md, CONTRIBUTING.md (short)
```
Model weights, audio, recordings, `.env` and caches are git-ignored.

## 4. Work breakdown
| # | Work item | Acceptance (what must be shown) |
|---|---|---|
| W1 | **Dependency verification protocol:** for each dependency check the current stable version, licence and maintenance status from its official source *on the day*; record in `docs/DEPENDENCIES.md`; pin versions. Candidates (to be verified, not assumed): FastAPI, Pydantic, Uvicorn, pytest, httpx, ruff, mypy; React, TypeScript, Vite, Vitest, Testing Library, ESLint, a bundle-analysis tool | Table with version/licence/source/date for every dependency; no unlicensed or unverified package |
| W2 | Repo init per Q6 (new or existing), branch/commit conventions, `.gitignore`, `.env.example`, README | Clean checkout builds from README steps |
| W3 | **Backend skeleton:** app factory, settings, `/health`, structured error envelope with fixed codes (ADR-004), request IDs | pytest passes for health + error envelope |
| W4 | **Access-control skeleton (A7, G23):** bind loopback by default; LAN mode flag that **refuses to start** without access control; default-deny middleware (all routes except `/health` and pairing placeholder); token-validator *interface* with an in-memory test double; Host-header + CORS allow-list middleware; route-enumeration test | AT-NET-01, 02, 03, 10 (automated, loopback) pass; AT-NET-06/07 at interface level with the test double; **no pairing implementation yet unless Q11 is decided** |
| W5 | **Frontend skeleton:** Vite + React + TS strict; app shell; Home with two mode cards; routes for YouTube and Authorized placeholders; empty states; Somali locale file; mobile-first CSS reset at 360 px | `tsc`, `eslint`, `vitest` pass; manual check at 360/412 px recorded |
| W6 | **Boundary enforcement:** ESLint `no-restricted-imports` between `modes/youtube` and `modes/authorized`/audio/TTS; bundle test skeleton asserting the YouTube entry chunk lacks mixer/scheduler/TTS modules; `YOUTUBE_MODE_AUDIO_ALLOWED=false` constant + test | AT-YT-03, AT-YT-04 skeletons pass; a deliberate violation in a scratch branch is shown to fail (evidence recorded) |
| W7 | **Guards:** no-ASR dependency scan (AT-CAP-13); secrets scan (AT-SEC-05); "research router unregistered in release config" test skeleton (AT-YT-09) | Guard tests pass; sample violations shown to fail |
| W8 | **Interface stubs** (no behavior): `CaptionProvider`, `TranslationPipeline`, `TTSAdapter`, `AudioMixer`, `AudioScheduler`, `MediaRights`, `SubtitleRenderer`, `YouTubePlayerAdapter`, `AuthorizedMediaPlayer` as typed contracts per ARCHITECTURE §3 | Compiles; contract tests trivially pass; each stub states "not implemented" |
| W9 | **CI:** lint + type-check + tests for both halves; dependency audit; fails on guard violations | CI run (or equivalent local run) output reported |
| W10 | **Docker/dev run:** compose for backend + frontend dev; non-Docker instructions; README states loopback-default and LAN opt-in with warning | Documented steps executed on the owner's/CI machine and result reported (not claimed from this sandbox) |
| W11 | **Docs sync:** copy of Phase 0 docs in repo; `docs/PHASE1_REPORT.md` with commands, outputs, tree, gate updates | Report written from real outputs |
| W12 | **Gate register update:** G8, G23 (partial), boundary tests | `GATES.md` updated with evidence references |

## 5. Intended verification commands (names only; to be finalised and run in Phase 1)
Backend: `pytest`, `ruff check`, `mypy`. Frontend: lint, type-check, unit tests, production build. Guards: the dependency/secret/boundary scripts. Exact commands will be recorded in `docs/PHASE1_REPORT.md` **after** they have been run.

## 6. Definition of done
1. All W1–W12 acceptance items demonstrated with real output.
2. Every guard test shown to fail on a deliberate violation and pass on the clean tree.
3. No model, caption retrieval, or audio code exists.
4. `GATES.md` and `ACCEPTANCE_TESTS.md` updated: only tests actually run change status (to PASS/FAIL with environment record); everything else stays NOT RUN.
5. Report lists commands, outputs, what was **not** run (anything needing a device or sandbox network), and open questions.
6. **STOP**; wait for "NEXT" before Phase 1b.

## 7. Risks
| Risk | Mitigation |
|---|---|
| Installs unavailable in this sandbox (G8) | Run on owner's machine/CI or a new chat with installs enabled; never report unrun commands as passed |
| Repository location unknown (Q6) | Do not start until answered |
| Over-building (placeholder code becoming "real") | Stubs state "not implemented"; no behavior beyond health/auth skeleton |
| Auth skeleton weaker than intended | Default-deny + route-enumeration test + explicit LAN-mode refusal |
| Dependency licence surprises | W1 protocol before pinning |

## 8. Hand-off to Phase 1b
Phase 1b needs: a runnable frontend toolchain, a way to serve the test page to the phone (USB port forwarding, ADR-024), and the owner's device details (Q9). Phase 1 provides the toolchain only; no spike code is written in Phase 1.

## 9. Pass-4 updates (2026-11-22) — **plan only; Phase 1 has not started**
- **CI is GitHub Actions (D-22).** W9 becomes: create a workflow that runs lint, type-check, unit tests and the guard scripts for both halves, and report the **real run output**. Until a run exists the environment is *selected, not verified*. **[U]** runner availability and free-plan minutes for the owner's account (not checked).
- **Device tests cannot run in CI.** All 📱 tests stay manual on the owner's phone; Phase 1 must not claim otherwise.
- **W10 (Docker/dev run):** its text assumes the owner runs it on a machine. D-22 lists no PC. Q16 decides whether W10 targets a PC at all; if there is none, W10 is limited to CI and documentation, and the backend-on-phone-network scenarios (AT-NET with a physical phone over LAN) stay NOT RUN/BLOCKED.
- **W1 licence check** must now flag licences that are unsuitable for a **commercial** product (D-18) — e.g., non-commercial or strong-copyleft terms.
- **Out of Phase 1 (unchanged):** the test harness (ADR-025) belongs to Phase 1b and needs separate owner authorization; no harness repository is created in Phase 1; the rights checkbox/confirmation UI (D-19) belongs to Phase 2; storage-budget UI to Phases 5/7.
- **Definition of done is unchanged.** Phase 1 remains **unstarted** and waits for owner approval ("NEXT").
