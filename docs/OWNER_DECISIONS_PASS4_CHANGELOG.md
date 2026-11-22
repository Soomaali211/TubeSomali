# TubeSomali — Owner Decisions Pass 4: Changelog

**Date:** 2026-11-22 · **Branch:** `phase0-reconciliation` · **Scope:** documentation only. **No application code, no Phase 1, no Phase 1b test, no deployment and no push were done.** The commit that carries this file is reported in the hand-off message (a file cannot contain its own commit hash).
Status vocabulary: **DECIDED** · **PROPOSED** · **OPEN** · **BLOCKED** · **NOT VERIFIED**.

## 1. The owner's 13 decisions — where each one landed
| # | Decision (owner) | ID | Recorded as | Applied in |
|---|---|---|---|---|
| 1 | Commercial intent; verify licences/terms; assume nothing | D-18 | **DECIDED** intent · licences **NOT VERIFIED** | DECISIONS §8.8–§8.10 (consequence table); GATES G5; ROADMAP Phases 4/5; PRODUCT_SPEC §12; PHASE1_PLAN §9 (W1) |
| 2 | Explicit checkbox + confirmation before processing | D-19 | **DECIDED** (mechanism) · wording **OPEN** | DECISIONS Q3/ADR-016; GATES G4; ROADMAP Phase 2; UX §11; PRODUCT_SPEC §12; **new tests AT-IN-31…33** |
| 3 | Owner reviews Somali translation quality initially | D-20 | **DECIDED** (interim) · external reviewers **OPEN** (none claimed) | DECISIONS Q4; GATES G7 |
| 4 | Repo `Soomaali211/TubeSomali`, branch `phase0-reconciliation` | D-21 | **DECIDED** | DECISIONS Q6; ROADMAP §1; PHASE1_PLAN §2 |
| 5 | Android phone + GitHub Actions CI | D-22 | **DECIDED (selection)** · **NOT VERIFIED** (nothing configured) | DECISIONS Q7; GATES G8 (stays BLOCKED); ARCHITECTURE §14; PHASE1_PLAN §9; **new tests AT-ENV-01…03** |
| 6 | Translate only from supplied SRT/VTT or supported embedded subtitles; no ASR | D-23 | **DECIDED** · supported embedded formats **OPEN** (new Q15) | DECISIONS Q8/ADR-019/Q15; GATES G19; ROADMAP Phase 3; UX §11; **new test AT-IN-34** |
| 7 | Current Android phone first; second if available; record models later | D-24 | **DECIDED** · models/versions **OPEN** | DECISIONS Q9; GATES G11; SPIKE_PLAN §3 |
| 8 | Transport not decided; HTTPS = investigate; signing does not encrypt | D-25 | **PROPOSED** (not approved) | DECISIONS Q11; ARCHITECTURE **§11a** (options/trade-offs/limits); GATES G23; **new test AT-NET-15** |
| 9 | G24 policy decided by owner after reviewing the plan; document balanced and strict | D-26 | **OPEN** (not approved); G24 blocking | SPIKE_PLAN **§10a**; DECISIONS Q12; GATES G24 |
| 10 | Simplest phone test workflow; separate static harness; main repo private; nothing deployed without authorization | D-27 | **PROPOSED** (ADR-025) | DECISIONS §8.11–§8.12 (F29, F30, ADR-025); SPIKE_PLAN §11; ARCHITECTURE §14 |
| 11 | Recommend a default storage budget; leave unapproved | D-28 | **PROPOSED** (ADR-026) | DECISIONS §8.12; ARCHITECTURE §15; UX §11 |
| 12 | Phase 2 = media import + rights; Phase 3 = captions/subtitles | D-29 | **DECIDED** | DECISIONS ADR-023; ROADMAP §0.1, §7 |
| 13 | Phases 2–3 may proceed if 1b is delayed; 4/5 blocked until G24 passes with owner approval | D-30 | **DECIDED** | ROADMAP Phases 1b/2/3/4/5, §7; GATES G24; SPIKE_PLAN §12 |

## 2. Files changed
**Created:** `OWNER_DECISIONS_PASS4_CHANGELOG.md` (this file).
**Modified (additive; every edit is visible in the file's revision history or marked "pass 4"):** `DECISIONS`, `GATES`, `ROADMAP`, `ARCHITECTURE`, `PHASE1_PLAN`, `DUAL_AUDIO_SPIKE_PLAN`, `ACCEPTANCE_TESTS`, `UX_REQUIREMENTS`, `PRODUCT_SPEC` (clarifications only; approved scope unchanged), `CONSISTENCY_AUDIT`, `PROGRESS_REPORT`.
**Preserved unchanged:** all earlier text, directives D-01…D-17, Q1–Q14 text, ADR-001…024, all 152 earlier test IDs and wording, every gate row (G1–G24), POC appendix.

## 3. Documentation corrections made in this pass
| # | Correction | Why |
|---|---|---|
| 1 | ADR-023 wording "PROPOSED" for the Phase 2/3 split and "(PROPOSED)" sequencing rule now say **DECIDED** (annotated, original kept) | D-29, D-30 |
| 2 | Q6 and Q7 no longer listed as plain OPEN in ROADMAP §1 / PHASE1_PLAN §2 | D-21, D-22 |
| 3 | G8 text no longer implies that selecting an environment unblocks it — it states "selected, not configured, still BLOCKED" | D-22 |
| 4 | ARCHITECTURE and GATES made explicit that HTTP request signing **does not encrypt** subtitle text, and that pairing over plain HTTP is not safe against a LAN eavesdropper | D-25 |
| 5 | The earlier G24 "pass rule" (§10) is relabelled as one of two options, **not** an approved rule | D-26 |
| 6 | The Phase 1b delivery route (USB forwarding) is no longer presented as the only default: it needs a PC the owner has not listed; ADR-025 added for the phone-only route | D-22, D-27 |
| 7 | CI limits stated: GitHub-hosted runners cannot execute Android-device tests | D-22 (design statement, **[U]** until a run exists) |
| 8 | §8.1 register gained rows for ADR-025/026 (pass-4 audit finding) | Audit script finding, fixed |
| 9 | Document count wording: 11 Phase 0 documents + this changelog | New file |

## 4. Issues still OPEN / BLOCKED / NOT VERIFIED
**BLOCKED:** B1 environment not configured (no workflow, no CI run, no sandbox installs) · B2 device evidence (device details + a person to run tests) · B3 YouTube extras G13/G14 (written policy review) · B4 ADR-014 final audio approach (Phase 1b findings) · B5 model adoption (commercial licence verification; no candidate cleared) · **B6 Phases 4/5 start (G24 passed with owner approval)**.
**OPEN:** Q2/Q13/Q16 backend host and network (no PC listed) · Q3 wording/legal · Q4 external and TTS reviewers · Q5 · Q9 device models · Q11 transport · Q12 G24 policy · Q14 budget approval · Q15 embedded subtitle formats · Q6 branch convention · gate numbering (audit U-05) · authorization to create/publish a harness.
**NOT VERIFIED:** commercial eligibility of every model/voice/host/API · YouTube API terms for a commercial app · HTTPS enforcement on GitHub Pages and the owner's GitHub plan · GitHub Actions minutes/runner availability · certificate-trust behaviour on the owner's phone · Web Crypto in insecure contexts · whether browsers can read embedded subtitle tracks · single-phone audio-capture options (T2) · every design claim in ARCHITECTURE.

## 5. Tests and implementation — exact status
| Item | Status |
|---|---|
| Application code written | **None.** No frontend, no backend, no scaffold, no harness. |
| Application tests / builds / security tests / device validation | **None executed.** 160 acceptance tests defined (152 + 8 new), **160 NOT RUN**, 0 PASS, 0 FAIL. |
| Gates | 24: 0 PASSED · G1 CLOSED-BY-DESIGN · G8 BLOCKED · 22 OPEN. |
| What *was* run | `doc_audit.py` (documentation cross-reference script, scratch, not application code) — results in `CONSISTENCY_AUDIT.md` §7; web look-ups for F29/F30. |

## 6. Remaining owner decisions (concise)
1. **Approve Phase 0** (or amend) — and authorize or refuse **pushing** `phase0-reconciliation` (not pushed from this pass).
2. **Q11** transport: confirm HTTPS as the direction to investigate, or choose otherwise.
3. **Q12** G24 policy: **Balanced** or **Strict** (or hybrid); confirm that SPIKE_PLAN §9's R1–R10 are the intended R1–R10.
4. **Q16/Q13** Is there a PC (or other host) for the backend and models? Router/Wi-Fi details.
5. **Q9** phone model, Android version, browser; who runs tests; second device if any; and whether release validation still requires two devices (U-07).
6. **ADR-025** authorization to create a public harness repo, enable Pages and publish; the owner's GitHub plan (Free/Pro).
7. **Q14** storage budget: approve or change the proposed 500 MB default.
8. **Q3** declaration wording + legal review; **Q4** TTS/external reviewers; **Q15** which embedded subtitle formats; **Q6** branch convention; **U-05** gate numbering.
