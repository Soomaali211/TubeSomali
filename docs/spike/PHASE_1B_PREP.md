# Phase 1b — preparation status
**Authorized scope (owner, 2026-11-24):** preparation of the test tooling only. **No AT-SP test was executed. No device was used. G24 is OPEN. No harness repository or site was created or published.** Branch `phase1b-prep` (from `phase1-scaffold`).

## What exists (see `spike/README.md`)
Harness page (Approaches A and B), pure helpers, fixture generator (FX-VID, FX-SOM-CUES, FX-SOM-TRACK, FX-LEVEL, FX-FMT as mp4 and webm where ffmpeg has the encoders), environment-record form, JSON export, CI job `spike`.

## Status split
| Category | State |
|---|---|
| Implemented | harness page, helpers, fixture generator, tests, CI job definition |
| Locally tested (sandbox) | helper unit tests 8/8; fixture tests 4/4 (ffmpeg present); headless-Chromium software smoke 12/12 for approaches A and B (audio graph runs, gains apply, Somali audio cancelled on pause, B tracks video within 0.25 s). Local desktop only |
| CI tested | see PHASE1_REPORT / hand-off (only if the branch is pushed) |
| Device tested | **none** |
| Not built | A', C, T2 analysis scripts, phone delivery route |
| Blocked | all AT-SP-01…14 execution (needs the owner's phone and a person to run it: Q9); T2 capture method undecided; delivery route undecided (Q13/Q16, ADR-025) |
| Owner decision required | Q9 device details; Q12 policy (Balanced/Strict); delivery route and authorization to create/publish a harness (ADR-025); whether T2 is feasible with one phone |

## Mapping of what was checked to AT-SP
None of the 14 AT-SP tests is run. The smoke test exercises the *harness*, not Android. In particular it says nothing about clicks, clipping at real levels, drift over time, Bluetooth, backgrounding or fullscreen on a device. AT-SP-01…14 remain **NOT RUN**; gate G24 and G11 are unchanged.

## Issue found while building
The page could miss `loadedmetadata` if cue decoding outlasted the video load, so start hung (found by the smoke test, fixed by checking `readyState`).

## Next step for the owner
Provide phone model, Android version and browser (Q9); choose the delivery route (USB forwarding needs a PC; otherwise authorize a separate public static harness, ADR-025); choose Balanced or Strict (Q12). Then a person runs the plan in `docs/DUAL_AUDIO_SPIKE_PLAN.md` section 7 and the results go in `docs/spike/PHASE_1B_REPORT.md`.
