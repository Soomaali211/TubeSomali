# TubeSomali — Roadmap

**Revision 2 · reconciliation pass 1 · 2026-11-20 · DRAFT.** Phase order and titles follow the owner's Final Reconciliation brief (D-10). Gates are defined in `GATES.md`; tests in `ACCEPTANCE_TESTS.md`; decisions in `DECISIONS.md`.
**Rule for every phase:** code + tests + docs → run everything → report exact commands/output → update the gate register → **STOP and wait for "NEXT"**. Nothing is called working without a test result and a recorded environment.

### Revision history
| Date | Change |
|---|---|
| 2026-11-20 rev 2 | Phases per owner's rev-2 list; amendments A1–A6. |
| 2026-11-20 rev 2 / reconciliation 1 | **Re-sequenced to the owner's order** (Phase 1b now between 1 and 2 and **mandatory**; Phase 2 = authorized media import; Phase 3 = captions pipeline); phase titles aligned; every phase now has **Depends on** and **Stop condition**; Phase 1 gains backend access-control skeleton (G23); Phase 5 gains voice-preparation job model; amendment A5 marked ADOPTED; POC defect labels now P1–P12; dependency map added. **No deliverable removed** — content that moved is listed in §0. |
| 2026-11-21 rev 2 / reconciliation 2 | Phase 0 deliverables now complete on disk (`CONSISTENCY_AUDIT.md`, `PROGRESS_REPORT.md` added); Phase 0 "Done in this pass" wording made precise; no phase, order, dependency or stop condition changed. |

## 0. What moved, and amendments

### 0.1 Mapping from rev-2 phase titles to the owner's rev-3 order
| Owner order (rev 3) | Rev-2 title / content | Change |
|---|---|---|
| **0** Documentation reconciliation and approval | 0 Product vision, decisions, policy research, architecture, gate register | Retitled; content retained and extended. |
| **1** Repository scaffold | 1 Scaffold, app modes, structure, tests, docs | Retained; + backend access-control skeleton (G23), Q6/Q7 prerequisites. |
| **1b** Mandatory dual-audio feasibility checkpoint | 1b *optional* spike (A5) | **Now mandatory** (D-11); expanded scope per AT-SP-01…14. |
| **2** Authorized media import | 2 Media import, SRT/VTT, subtitle editing/export, safe URL validation | Split: media import, rights declaration, safe URL validation, format matrix stay in Phase 2; SRT/VTT parsing/editing/export move to Phase 3. **PROPOSED (ADR-023)** — owner to confirm. |
| **3** Captions pipeline | 3 Caption providers (interface, mock, research-only) | + SRT/VTT parse/normalize/edit/export and embedded-subtitle detection from rev-2 Phase 2. |
| **4** Somali translation | 4 Somali translation pipeline, editing, evaluation, licence verification | Retitled; content retained. **Blocked until G24 passes.** |
| **5** Somali TTS | 5 Somali TTS models, licence verification, voices and QA | Retitled; + voice-preparation job model (ADR-022). **Blocked until G24 passes.** |
| **6** Audio mixer and synchronization | 6 Authorized-media audio mixer, independent volumes, scheduler, synchronization, subtitle timing | Retitled; content retained. |
| **7** Player UX | 7 Full player UI, YouTube official embed, authorized player, fullscreen, captions, audio settings, mobile UX | Retitled; content retained; + voice-preparation UI (§9) and pairing/connection UI (§10). |
| **8** Security audit | 8 Security, privacy, legal/policy review, comprehensive QA | Retitled; privacy, legal/policy review, QA **kept inside Phase 8**. |
| **9** Performance and resource testing | 9 Local-first runtime, performance, memory, free-hosting evaluation | Retitled; local-first runtime guides and free-hosting evaluation **kept inside Phase 9**. |
| **10** PWA/APK packaging | 10 PWA and optional Android APK/native | Retitled; secure-context caveat added (F23). |
| **11** Release validation | 11 Release audit and handover | Retitled; handover kept. |

### 0.2 Amendments
| # | Amendment | Status |
|---|---|---|
| A1 | `GATES.md` is re-signed at the end of every phase. | PROPOSED |
| A2 | Phase 3 builds provider **interface + mock + research-only adapter**; YouTube retrieval not enabled in any shipped build. | **DECIDED** in substance (D-03); adapter choice PROPOSED |
| A3 | Phase 4 includes a source-language policy (English-only vs pivot vs reject). | PROPOSED |
| A4 | Phase 7 treats YouTube mode as "official player, nothing in front of it"; custom captions only if G13 clears. | **DECIDED** (D-02) / G13 OPEN |
| **A5** | Android dual-audio feasibility spike with generated tones and a stock video, no TTS/translation. | **ADOPTED — now mandatory Phase 1b (D-11)** |
| A6 | Media-format matrix (G22) and subtitle-source (G19) checks folded into import (Phases 1b/2/3). | PROPOSED |
| A7 | *(new)* Phase 1 includes backend access-control skeleton (default loopback bind, default-deny auth middleware, pairing design tests) so no later phase can accidentally expose an unauthenticated backend (G23). | PROPOSED |

## 1. Prerequisites before Phase 1 (status from DECISIONS §8.2)
| Prerequisite | Status |
|---|---|
| Owner approval of Phase 0 documents | **OPEN** (this deliverable) |
| **Q6** repository location | **OPEN** |
| **Q7** installs / where tests run (G8) | **OPEN** — **BLOCKED in this sandbox** |
| **Q11** transport/pairing design confirmation | **PROPOSED** (needed to finish the backend skeleton; the skeleton can start with default-deny + loopback regardless) |
| **Q2/Q13** backend host and network environment | PROPOSED / OPEN |
| **Q9** first Android device (needed for 1b, not for 1) | OPEN (nomination) |

## 2. Phases (in execution order)

### Phase 0 — Documentation reconciliation and approval
- **Deliverables:** `DECISIONS`, `ROADMAP`, `GATES`, `PRODUCT_SPEC`, `ARCHITECTURE`, `UX_REQUIREMENTS`, `ACCEPTANCE_TESTS`, plus `CONSISTENCY_AUDIT`, `PROGRESS_REPORT`, `PHASE1_PLAN`, `DUAL_AUDIO_SPIKE_PLAN`.
- **Done in this pass:** documents reconciled; documentation cross-reference script (`doc_audit.py`, scratch, not application code) run in pass 1 (before/after) and pass 2 (before/after), outputs quoted in `CONSISTENCY_AUDIT.md`; Phase 0 completion calculation in `PROGRESS_REPORT.md` (documentation checks are **not** application tests).
- **Not done:** owner approval; any application test; any device test; POC execution.
- **Depends on:** — · **Stop condition:** owner approves (or amends) the documents and answers the blocking questions.

### Phase 1 — Repository scaffold
- **Build:** monorepo; FastAPI shell (`/health`, settings, structured error envelope with fixed codes); **backend access-control skeleton (A7): loopback default, LAN mode opt-in that refuses to start without access control, default-deny auth middleware, route-enumeration test**; React+TS+Vite shell with **mode selection** (Home → YouTube | Authorized Media), Somali locale file, route skeleton for player screens (empty states only); module skeletons matching ARCHITECTURE §2–3 (`modes/youtube`, `modes/authorized`, `core`, `backend/{translation,tts,subtitles,jobs,security,research}`); Docker Compose + non-Docker run; `.env.example`; `.gitignore` (secrets, weights, temp, audio); CI.
- **Boundary enforcement from day one:** ESLint restricted-imports rule, bundle test skeleton (AT-YT-03), `YOUTUBE_MODE_AUDIO_ALLOWED=false` test, no-ASR dependency scan (AT-CAP-13), secrets scan.
- **First step:** check current stable versions/licences of each dependency and pin them. Full plan: `PHASE1_PLAN.md`.
- **Tests:** pytest + Vitest smoke; ruff/mypy/eslint/tsc; AT-NET-01…03, 06, 07, 10 at unit/integration level (loopback). **No** models, no caption extraction, no audio.
- **Depends on:** Phase 0 approval; Q6; Q7 (or tests run on the owner's machine). · **Stop condition:** all commands pass with output reported, or failures reported; STOP. Gates touched: G8, G23 (partially).

### Phase 1b — Mandatory dual-audio feasibility checkpoint
- **Build/measure:** minimal player + `AudioMixer` with two independent gains, master gain/headroom, smoothing; generated Somali stand-in audio (no TTS, no translation); approaches **A** (per-cue scheduling), **B** (pre-rendered track on a media element), optional **A′**, **C only if A and B fail**; measurements AT-SP-01…14; full protocol in `DUAL_AUDIO_SPIKE_PLAN.md`.
- **Order of testing:** the owner's available Android device first; **no multi-device claim until two physical devices have been tested**.
- **Output:** measurements report with environment records; recommendation (A / B / A′ / C / none); proposed tolerances for owner approval; format matrix start (G22).
- **Depends on:** Phase 1 (tooling, repo); Q9 (first device); Q13 (how the page reaches the phone: USB port forwarding preferred, ADR-024). · **Gate:** **G24**.
- **Stop condition:** report delivered **and** owner approves recommendation + tolerances. **If no approach meets owner-approved requirements on the first device → STOP; do not start Phases 4/5; report options (C, redesign, scope change).**
- **Sequencing rule (PROPOSED):** Phases 2–3 do not technically depend on 1b; if device access is delayed the owner may authorize them to proceed while 1b waits. **Phases 4 and 5 may not start until G24 is passed.**

### Phase 2 — Authorized media import
- **Build:** URL parser/validator for YouTube links (watch, youtu.be, shorts, embed, m.; reject non-YouTube hosts and tricks; canonical rebuild); **local media import** (object URL, **no upload**) with format check/messages; **rights declaration flow** (G4, G20; wording per Q3); media library skeleton (IndexedDB); format matrix (G22) started; Somali UI for these screens.
- **Tests:** AT-IN-01…10, AT-IN-26…30 (including "no upload" network test and declaration required/deletable).
- **Depends on:** Phase 1; (1b by sequencing rule). · **Stop condition:** tests pass and results reported.

### Phase 3 — Captions pipeline
- **Build:** SRT/VTT parsers → `Segment`; exporters; upload limits and safe parsing; subtitle editor (list, edit, restore original); embedded-subtitle detection investigation (G19); `CaptionProvider` ABC; mock provider; error mapping; diagnostics script; research adapter under `backend/research/` (default candidate `youtube-transcript-api`), unregistered in release; POC defects **P1–P10** closed or explicitly waived (G9).
- **Rules:** YouTube retrieval stays disabled until G14 clears (D-03); no scraping bypasses; live checks only on the owner's machine with an explicit research flag.
- **Tests:** AT-IN-11…25, AT-CAP-01…14, AT-YT-05, AT-YT-09.
- **Depends on:** Phase 2. · **Stop condition:** mocked suite green; live-test results or an explicit "not run".

### Phase 4 — Somali translation
- **Build:** `TranslationPipeline`, batching/context, protection of numbers/names/acronyms, per-cue retranslate/edit/restore, whole-track translate with cancel/progress; model cache dir, disk-space warning, explicit download action; source-language policy (A3).
- **First step:** re-read model cards; determine the target-language token **by test**; record real Somali samples; check any second model's licence against Q1.
- **Evaluation:** benchmark template with empty cells; native reviewers (G7). **Tests:** AT-TR-01…11. First phone→backend feature use: run AT-NET-04, 05, 09, 13, 14 on a physical phone (G23).
- **Depends on:** **G24 passed**; Phase 3 (segments); Q1; Q4 for quality claims; Q11 decided for any phone→backend use. · **Stop condition:** measured results or a blocker report; no model adopted on unverified claims.

### Phase 5 — Somali TTS
- **Build:** `TTSAdapter`, **voice registry**, evaluation CLI (fixed Somali set), seed control, chunking, duration metadata; **voice-preparation job model (ADR-022): cancel, retry, resume, per-cue cache, storage estimate** (UI later in Phase 7); pre-render speed measurement on the chosen host (G21).
- **Candidates:** MMS (NC), `somali_tts_model`, StyleTTS2-Somali, `Hussein_tts`, `omi-tts` — each re-read on the day; remote code reviewed/pinned/isolated.
- **Tests:** AT-TTS-01…11, AT-PR-04…08 (backend side).
- **Depends on:** **G24 passed**; Q1; Q4; Q2 (host). · **Stop condition:** measured comparison or blocker report; no voice exposed unless it passes (G17).

### Phase 6 — Audio mixer and synchronization
- **Build:** production `AudioMixer`, `AudioScheduler` (approach chosen by Phase 1b findings), master-clock handling, timing policies with warnings, `SubtitleRenderer` timing, drift measurement, stale-audio guards.
- **Tests:** deterministic scheduler tests with a fake clock (automated) + **device acceptance AT-DA-01…10, AT-SY-01…09, AT-FS-01…04 on real Android, ≥2 devices for release claims** (G11, G12, G15, G16).
- **Depends on:** Phase 5 (voices), Phase 1b recommendation, Phases 2–3. · **Stop condition:** recorded device results; tolerances approved by owner.

### Phase 7 — Player UX
- **Build:** per `UX_REQUIREMENTS.md`: player-centric layouts (portrait/landscape/expanded), audio settings panel, subtitle settings, library, **voice-preparation UI (§9)**, **pairing and connection status (§10)**; `YouTubePlayerAdapter` (official only; nothing over the player; explanation instead of audio controls); fullscreen via container with fallback.
- **Tests:** component/a11y/breakpoint tests; AT-YT-01…08; AT-CC-*; AT-PR-01…10; device re-run of AT-FS-* and AT-NET-05, 09, 13.
- **Depends on:** Phase 6; Phase 2. · **Stop condition:** tests pass; screenshots at phone width.

### Phase 8 — Security audit
- Security audit (AT-SEC-01…12, AT-NET-01…14 full physical run); privacy-policy draft; terms text for rights declaration (G20); **legal/policy review** (re-read YouTube policy text; re-check G1, G13, G14); comprehensive QA; release-blocker table. Any open BLOCKER ⇒ not production-ready.
- **Depends on:** Phase 7. · **Stop condition:** audit report with measured evidence.

### Phase 9 — Performance and resource testing
- Measured resource use on devices (G18), local Docker/non-Docker runtime guides, backend free-hosting fit (G10) with current free-tier limits re-read, pre-render latency (G21); split architecture if inference is too heavy; no public endpoint before gates clear.
- **Depends on:** Phases 6–7. · **Stop condition:** recorded measurements; no promise beyond them.

### Phase 10 — PWA/APK packaging
- PWA install/offline behavior with the transport decision (F23: secure context needed for service workers); APK via WebView wrapper only if wanted and PWA passed on devices; native Media3 path only if G11 failed in the browser path **and** a native two-stream design is verified on device. No APK claim without a successful build.
- **Depends on:** Phase 9; Q11. · **Stop condition:** packaged build runs on a real device or the claim is withdrawn.

### Phase 11 — Release validation
- Feature matrix (implemented / tested / not tested / blocked), model-and-licence inventory with revisions, device test records (≥2 devices), gate register final state, setup steps, handover and concise Somali summary.
- **Depends on:** all earlier phases. · **Stop condition:** owner sign-off.

## 3. Dependency map
```
0 ─▶ 1 ─▶ 1b ═▶ (G24) ═▶ 4 ─┐
        │      │             ├─▶ 6 ─▶ 7 ─▶ 8 ─▶ 9 ─▶ 10 ─▶ 11
        │      └─▶ 2 ─▶ 3 ───┤
        │                    5 ┘ (also needs G24)
        └─ backend access-control skeleton (G23) feeds every phase that uses the backend
```
`═▶` = hard stop condition (Phases 4 and 5 cannot start until G24 passes). Phases 2–3 follow 1b in order but have no technical dependency on it (see sequencing rule).

## 4. Test strategy
| Layer | Rule |
|---|---|
| Unit/integration (CI) | Deterministic, offline, mocks for providers/models, fake clock for the scheduler. |
| Device (📱) | Real Android devices; environment record per run; recorded results only; **two devices before any multi-device claim.** |
| Live/research | Opt-in, owner's machine, off in release. |
| Model evaluation | Measured values only; named reviewers. |
| Documentation checks | `CONSISTENCY_AUDIT.md` script results are *documentation* checks and never count as application tests. |
| Guards | No-ASR scan; no media download; YouTube-mode isolation (lint + bundle + runtime); no transcript text in logs; no secrets; default-deny backend routes. |

## 5. Gate summary at end of Phase 0 (reconciliation 1)
24 gates. **G1 CLOSED-BY-DESIGN; G8 BLOCKED (this sandbox); all others OPEN; none PASSED.** Release-critical: G4, G5, G11, G12, G17, G19, G23, G24 (+ G13/G14 only for YouTube extras). See `GATES.md`.

## 6. Recommended next step
**Single next action:** owner reviews and approves (or amends) the Phase 0 documents and answers the blocking questions Q6, Q7, Q9 (device nomination), Q11, Q13. Then Phase 1 per `PHASE1_PLAN.md`, followed immediately by Phase 1b per `DUAL_AUDIO_SPIKE_PLAN.md`.
