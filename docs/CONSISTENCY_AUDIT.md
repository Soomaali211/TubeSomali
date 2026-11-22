# TubeSomali — Phase 0 Consistency Audit

**Reconciliation pass 2 · 2026-11-21 · DRAFT.** Documentation audit only — **not** an application test and it never counts toward any gate or test status (owner D-14).
**Scope:** `PRODUCT_SPEC`, `UX_REQUIREMENTS`, `ARCHITECTURE`, `GATES`, `ACCEPTANCE_TESTS`, `ROADMAP`, `DECISIONS`, `PHASE1_PLAN`, `DUAL_AUDIO_SPIKE_PLAN` (+ this file and `PROGRESS_REPORT`).
**Method:** (1) a full manual read of every document in its current on-disk state; (2) a cross-reference script (`doc_audit.py`, scratch Python, not part of the product) that checks identifier definitions/references (gates, facts, ADRs, questions, test IDs), the owner's phase order and titles, "Depends on"/"Stop condition" presence, status keywords, label collisions and stale wording; (3) re-reading the primary pages for the facts added in pass 1 (DECISIONS §8.6).

## 1. Script results (actual output; files in the session scratch area)
| Run | Documents | Findings | Notes |
|---|---|---|---|
| Pass 1 baseline (before any reconciliation edit) | 7 | **14** | Missing Phase 1b; label collision A1–A6; "optional spike"; "22 gates"; stale "Phase 6 spike"; legacy "Accepted" labels. |
| Pass 1 after edits | 9 | **6** | — |
| Pass 2 before edits | 9 | **6** | Re-run on the 2026-11-21 on-disk state. |
| Pass 2 after edits | 9 | **4** | All four are intentional historical wording (§3). |
| Pass 2 final (this file and PROGRESS_REPORT included) | 11 | **8 lines** | 0 real defects; the extra 4 lines are quotations inside this file (§1a). |

Defined at the pass-2 state: **24 gates · 28 facts (F1–F28) · 24 ADRs · 14 questions (Q1–Q14) · 13 phases (0,1,1b,2…11) · 152 test IDs** (CAP 14, CC 4, DA 10, FS 4, IN 30, NET 14, PR 10, SEC 12, SP 14, SY 9, TR 11, TTS 11, YT 9). Every referenced gate, fact, ADR, question and test ID resolves to a definition. All 13 roadmap phase titles and the order equal the owner's list; every phase has *Depends on* and *Stop condition*; every ADR has a status row; every gate has a status keyword; no PASS/FAIL cell exists in the acceptance tests.

### 1a. Final run

Actual output of the final run over all 11 documents (`audit_pass2_final.txt`): **8 findings, 0 real defects.**
- 4 finding lines (ACCEPTANCE_TESTS, ARCHITECTURE, DECISIONS, GATES) are the intentional historical quotes already listed in §3.
- 4 further finding lines are **in this file** (they total 6 hits: "Phase 6 spike" ×3, "optional" ×1, "G19–G22" ×1, "22 gates" ×1), because §1–§2 quote the old wording when describing earlier findings. They are quotations of defects that were already fixed, not live statements.
- Everything else passes: all identifiers resolve; phase order/titles equal the owner's; 24 gates, 24 ADR rows, 14 questions registered; 152 test IDs; no PASS/FAIL cells.
The script is deliberately literal (it cannot tell a quotation from a claim), which is why the manual read in §2 matters.

## 2. Conflicts found and fixed in pass 2 (visible edits, logged in each file's revision history)
| ID | Finding | Fix |
|---|---|---|
| C-01 | `GATES.md` G15 cited **AT-DA-10** as the "ramp/click" test; AT-DA-10 is the headphone/Bluetooth output-change test. The click/sweep test is **AT-DA-07**. | G15 now cites AT-DA-07, with a visible correction note. |
| C-02 | **Project copies were stale.** All 7 Project documents predated reconciliation 1 (no G23/G24, old roadmap order, no §8). | All documents re-synced to the Project in pass 2 (sync result reported with the deliverable). |
| C-03 | `DECISIONS.md` §1 said disk and Project were "identical" — true at the first check, false after the pass-1 edits. | Row corrected with explanation; original claim not silently deleted. |
| C-04 | `DECISIONS.md` Appendix B (Somali summary) still said "Q1–Q10 needed" and "A5 / Q10" although Q10 is DECIDED and A5 is mandatory. | Old text preserved and marked superseded; an updated Somali summary was added. |
| C-05 | `DECISIONS.md` K4 and the §0 table still described the spike as late/proposed. | Annotated "resolved: mandatory Phase 1b (D-11, ADR-021, G24)". |
| C-06 | **G2** and **G3** were referenced in no other document (script findings). | Cross-referenced from DECISIONS §8.1 rows 003 and 005. |
| C-07 | `DECISIONS.md` linked `CONSISTENCY_AUDIT.md` and `PROGRESS_REPORT.md`, which did not exist. | Both created (this file; `PROGRESS_REPORT.md`). |
| C-08 | `ROADMAP.md` Phase 0 claimed the audit script had been run. | Verified: the script and its outputs exist in the scratch area; the claim is now precise (§1) and the outputs are quoted here. |
| C-09 | Two unreferenced scratch media files exist in the scratch area (`original_fixture.mp4`, 30 s, H.264+AAC; `somali_standin.webm`, 30 s, Opus), created before pass 1. | Not part of the repository or any document; **no result was derived from them**; they are not Phase 1b fixtures (those are specified in DUAL_AUDIO_SPIKE_PLAN §5 and will be generated in Phase 1b). Recorded here so nobody mistakes them for evidence. |

## 3. Accepted script findings (intentional historical wording — not defects)
- `ARCHITECTURE.md` revision note quotes the old phrase "Phase 6 spike measurements" to describe the change to "Phase 1b".
- `ACCEPTANCE_TESTS.md` §0 says "previously said 'Phase 6 spike'" for the same reason.
- `DECISIONS.md` (2×) and `GATES.md` (1×) say "G19–G22" when recording that those four gates were architect-added; G23/G24 are described separately in the same sentences.

## 4. Unresolved items that need an owner decision (not silently resolved)
| ID | Item | Where | Why unresolved |
|---|---|---|---|
| U-01 | **Phase 2 / Phase 3 content split.** Rev-2 Phase 2 contained media import *and* SRT/VTT parsing/editing/export; the owner's rev-3 titles are "Authorized media import" (2) and "Captions pipeline" (3). Docs place SRT/VTT in Phase 3 (ADR-023 PROPOSED). | ROADMAP §0.1; ACCEPTANCE §E | Owner has not said which phase owns SRT/VTT. |
| U-02 | **Strict vs. relaxed order around Phase 1b.** The owner's order lists 1b before 2, but a *hard stop* is specified only for Phases 4/5. Docs propose that Phases 2–3 may proceed if device access is delayed (sequencing rule PROPOSED). | ROADMAP Phase 1b | Owner approval needed; default if unanswered = strict order (no Phase 2 until 1b done). |
| U-03 | **Transport protection for LAN pairing (Q11)** undecided; G23 cannot pass without it; PWA/service-worker behavior depends on it (F23, K7). | ARCHITECTURE §11 | Needs Q11/Q13. |
| U-04 | **Spike delivery fallback** (static fixture server on the LAN if USB debugging is unavailable) vs. the spirit of D-12. It serves only fixtures, not the backend, for the session, then stops. | DUAL_AUDIO_SPIKE_PLAN §11; ADR-024 | Owner should confirm acceptable (Q13). |
| U-05 | **Gate numbering.** G19–G24 are the architect's labels (G23/G24 formalise the owner's requested content). | GATES header | Approval of numbering/wording. |
| U-06 | **Checkpoint pass rule (Q12)**: one physical device passes G24 as *single-device feasibility*; release needs two (D-11, G11). Owner has not stated the pass rule itself. | DECISIONS Q12; SPIKE_PLAN §10 | OPEN. |

Notes (not conflicts): documents are written in English with a short Somali summary; all Somali UI strings are *draft labels needing native review*. A Somali-language version of the documents can be produced on request.

## 5. Coverage of the owner's Final Reconciliation brief
| Brief item | Where it is covered |
|---|---|
| 1 Review all documents for consistency | This audit (§1–§4). |
| 2 DECISIONS to Rev 2; reconcile Q1–Q7; statuses DECIDED/PROPOSED/OPEN/BLOCKED; add Q9, Android↔PC pairing, dual-audio checkpoint, reviewers, licences, deployment/network | DECISIONS §8.1 (ADR statuses), §8.2 (Q1–Q14 with cited owner information), §8.3 (BLOCKED register), §8.4 (directive log D-01…D-17), §8.5 (not decided). |
| 3 Acceptance tests preserved; none PASS | ACCEPTANCE_TESTS (all IDs preserved; 152 NOT RUN); section §0 rules. |
| 4 Dual-audio feasibility mandatory checkpoint | ROADMAP Phase 1b; GATES G24; ADR-021; DUAL_AUDIO_SPIKE_PLAN; AT-SP-01…14. |
| 5 Backend connection security | GATES G23; ARCHITECTURE §11; ADR-020; AT-NET-01…14; UX §10; PRODUCT_SPEC §4.6. |
| 6 TTS preparation UX | UX_REQUIREMENTS §9; ARCHITECTURE §12; ADR-022; AT-PR-01…10; PRODUCT_SPEC §4.5. |
| 7 Roadmap order, dependencies, stop conditions | ROADMAP §2 and §3 (dependency map). |
| 8 Progress report | PROGRESS_REPORT. |
| 9 Final deliverable list | Delivered with this audit; Phase 1 plan = PHASE1_PLAN; spike plan = DUAL_AUDIO_SPIKE_PLAN. |

## 6. What this audit cannot show
It cannot show that any claim is *true* — only that the documents agree with each other. External facts are labelled [V]/[U] and were read through summarizing fetches; nothing has been implemented, no test has been run, no device has been used, and no repository exists in this session.
