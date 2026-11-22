# TubeSomali — Dual-Audio Feasibility Test Plan (Phase 1b)

**Version:** reconciliation pass 1 · 2026-11-20 · DRAFT · **Nothing in this plan has been executed.** Every result cell below is empty on purpose.
**Owner directives implemented:** D-05 (Web Audio GainNode or another verified mixing architecture; evaluate Media3; don't assume track selection plays two tracks), D-11 (mandatory checkpoint before Phase 4/5; investigate the listed items; compare approaches; document actual findings; start on the owner's Android device; no multi-device claim before two devices), D-14 (no PASS without execution and environment record).
**Gate:** G24 (blocks Phases 4 and 5). **Tests:** AT-SP-01…14 (ACCEPTANCE_TESTS §J). **Decision it feeds:** ADR-014 (BLOCKED until this report exists), tolerance proposals for ADR-015.

## 1. Question to answer
Can TubeSomali, on real Android devices, play **original audio** and a **Somali voice track** with **independent 0–100 % volumes**, keep the Somali audio synchronized to the video timeline through pause, seek (incl. repeated), speed change, buffering, fullscreen, headphone/Bluetooth output and backgrounding, with **no stale audio, no clipping and no audible clicks** — and which implementation approach does it best?

## 2. Scope
**In:** a throw-away-or-reusable test page with a video element, a Web Audio graph with two independent gains + master, generated stand-in audio, instrumentation, and measurement procedures.
**Out (deliberately):** real TTS, translation, captions UI, rights flow, backend, YouTube, polished UI, PWA packaging. The spike must not depend on any model or network service.

## 3. Preconditions
| Need | Status |
|---|---|
| Phase 1 tooling/repo exists (Q6, G8) | **OPEN** |
| An Android device the owner can use for testing (Q9: model, Android version, browser) | **OPEN** (owner has "an available device"; details not given) |
| Delivery of the test page to the phone (Q13): USB port forwarding preferred (F25: phone opens `localhost:<port>`, a secure context, no LAN exposure; prerequisite: remote debugging set up) | **OPEN** |
| Pass rule for the checkpoint (Q12) | **OPEN** (proposal in §10) |
| A way to capture output audio for T2 analysis (see §6) | **OPEN** — to be chosen with the owner |

## 4. Approaches under test
| ID | Approach | What is built for the spike | Included when |
|---|---|---|---|
| **A** | Per-cue scheduling: decoded `AudioBuffer` per Somali stand-in cue, started with `AudioBufferSourceNode.start(when)`; cancel on pause/seek | Scheduler keyed to the video element's `currentTime`; node bookkeeping; cancellation | Always |
| **B** | Pre-rendered Somali track played by a second media element (`<audio>`), routed through its own GainNode via `createMediaElementSource` (F17), kept in sync with the video (same `currentTime`/`playbackRate`; `preservesPitch` true by default, F19) | Sync controller with drift correction; shared gain graph | Always |
| **A′** | A plus time-stretch for speeds ≠ 1× (AudioWorklet/WASM) — because per-buffer `playbackRate` shifts pitch (F18) | Only if A is otherwise viable and speed/pitch is the deciding weakness | Conditional |
| **C** | Native Android (Media3 or two players). **Not assumed to support two simultaneous tracks;** whether two players in one app mix cleanly and stay in sync is **unverified** (F20 covers only system-level mixing/focus) | A minimal native test app **only if A and B both fail** on the first device | Conditional |

Both A and B use the **same graph**: `video → MediaElementSource → originalGain → masterGain → destination` and `Somali source → somaliGain → masterGain`. A user-gesture-initiated `AudioContext.resume()` is required (F16).

## 5. Fixtures (to be generated in Phase 1b; specification only — commands not written or tested)
| Fixture | Content | Purpose |
|---|---|---|
| **FX-VID** | ≥ 20 min video (configurable) with a visible running timecode and a **flash frame at known timestamps** (e.g., every few seconds); original audio track = **marker tone A** (e.g., short beeps at a fixed pitch) aligned to the flashes | Sync reference for T2 analysis; long-run drift (AT-SP-05, AT-SY-08 later) |
| **FX-SOM-CUES** | Somali stand-in: **marker tone B** (different pitch) bursts of varied durations at known cue times, as individual short audio files | Approach A input |
| **FX-SOM-TRACK** | The **same** content stitched into one continuous track (silence between bursts) | Approach B input (identical content ⇒ fair comparison) |
| **FX-LEVEL** | Calibration tones at known levels (including near full scale) | Gain mapping, headroom/clipping (AT-SP-02/03) |
| **FX-FMT** | Same clip in several container/codec combinations (e.g., MP4/H.264+AAC; WebM/VP9+Opus; others as available) | Format matrix start (G22) |
Fixtures contain no personal or third-party media.

## 6. Measurement methods and their limits
| Tier | Method | Captures | Limits |
|---|---|---|---|
| **T1** | In-page logging at intervals: `video.currentTime`, `audioCtx.currentTime`, `performance.now()`, `outputLatency`/`baseLatency`/`getOutputTimestamp()` where available (F27), AudioContext state, event log (`play/pause/seeking/seeked/ratechange/waiting/visibilitychange`) | Software-level offset and event order | Cannot see real acoustic/hardware latency; `outputLatency` is an *estimate*; Android behavior unverified (F27) |
| **T2** | Recording of the device output (options: Android internal-audio screen recording if the device supports it [U]; or a second device recording the speaker/headphone output) plus screen video; offline analysis detects marker tones and flash frames | Real relative timing between original, Somali and video; click/clip detection from the waveform | Internal capture may bypass Bluetooth latency; external mic adds noise/latency; method must be chosen per scenario and stated in the result |
| **T3** | Human observation notes (tester) | Audible glitches, ghost speech, perceived sync | Subjective — recorded as observation, not a measurement |
Derived metrics: per-channel level vs setting; peak/clipping count; **click metric** (relative discontinuity energy in the transition window; threshold proposed after data); **offset(t)** between channel markers and flashes; **stale-audio window** (ms between seek/pause event and the last sample of old-position audio); resync time; speed-change offset; observed CPU/memory/battery drift over a run.

## 7. Procedures (one per AT-SP test)
Common setup for all: record the environment (§8); fresh page load; user gesture to start audio; fixtures loaded; screen brightness/power mode noted; battery-saver state noted; output route stated.
| Test | Steps | Data captured | Result recorded as |
|---|---|---|---|
| AT-SP-01 Independent GainNodes | Play FX-VID + Somali source; set original gain to 0 then Somali to 0, alternating | T2 per-channel presence; T1 gain values | Observed per-channel behavior |
| AT-SP-02 0–100 % controls | Set each channel to 0, 30, 50, 100 % (linear mapping first; perceptual mapping optional); measure FX-LEVEL | Level (dBFS) per setting per channel; crosstalk | Table of levels |
| AT-SP-03 Master gain, clipping, headroom | Both at 100 % with loud FX-LEVEL; repeat with reduced master and with a limiter node | Peak values, clipping counts | Table per configuration |
| AT-SP-04 Smooth transitions | Fast 0→100→0 sweeps by (i) direct assignment, (ii) `setTargetAtTime` (F26) with candidate time constants, (iii) linear ramp | Waveform around transitions; click metric; tester notes | Table per method |
| AT-SP-05 Sync at 1× | Play ≥ 10 min (A and B separately) | T1 log; T2 offset(t) at intervals | Offset-vs-time series; drift slope |
| AT-SP-06 Pause/resume | 20 pause/resume cycles at random times | T1 events; T2 residual audio after pause; alignment after resume | Distribution of offsets and residuals |
| AT-SP-07 Seek / repeated seek | Seek forward/back (scrub, tap, 10 s jump) ×20 rapidly and slowly | Position after seek; T2 ghost audio | Offsets; count of ghost events |
| AT-SP-08 Stale-audio cancellation | Seek/pause during a Somali burst; analyze marker tone B after the event | Stale-audio window (ms) | Per approach |
| AT-SP-09 Speed | Each available rate (list what the device supports; candidate set 0.75×–1.5×, **not assumed**) at the start, mid-run and while paused | Offset after change; pitch observation (A vs B vs A′) | Per rate per approach |
| AT-SP-10 Buffering and background | Force a stall (large file/slow source); then: switch apps, lock screen, return, rotate | Event log; AudioContext state; audio continuing/stopping; resync result | Observed behavior + times |
| AT-SP-11 Headphone/Bluetooth | Repeat AT-SP-05 (short) and AT-SP-07 on speaker, wired, and Bluetooth (as available) | Offset vs speaker; `outputLatency` vs measured | Table per route |
| AT-SP-12 Fullscreen | Enter/exit fullscreen of the **container** repeatedly during playback | Sync before/after; glitches; state preserved | Observed + offsets |
| AT-SP-13 Two media elements | Run B with video + audio elements; observe startup alignment, CPU/memory, concurrent-playback behavior | T1 log; profiler/notes | Observed behavior |
| AT-SP-14 Comparison & recommendation | Fill §9 table from measured data only | — | Recommendation + proposed tolerances |

## 8. Environment record template (one per run)
| Field | Value |
|---|---|
| Date/time, tester | |
| Device make/model | |
| Android version / security patch | |
| Browser/WebView name + version | |
| App/spike commit hash | |
| Output route (speaker / wired / Bluetooth model) | |
| Power mode (battery saver?), screen lock timeout, "do not disturb" | |
| Fixture file(s): name, container, codec, duration | |
| Measurement tier(s) used (T1/T2/T3) and capture method | |
| Notes/anomalies | |

## 9. Results template (empty — to be filled only from real runs)
| Requirement | Approach A | Approach B | Approach A′ | Approach C |
|---|---|---|---|---|
| R1 Independent gains (AT-SP-01) | | | | |
| R2 0–100 % control mapping (AT-SP-02) | | | | |
| R3 No clipping at 100 %/100 % with headroom strategy (AT-SP-03) | | | | |
| R4 No audible clicks on transitions (AT-SP-04) | | | | |
| R5 Stable, non-accumulating sync at 1× (AT-SP-05) | | | | |
| R6 Pause/seek correct, no stale audio (AT-SP-06/07/08) | | | | |
| R7 Speed support, pitch acceptable (AT-SP-09) | | | | |
| R8 Buffering/background/BT/headphone behavior defined and acceptable (AT-SP-10/11) | | | | |
| R9 Fullscreen preserves sync/state (AT-SP-12) | | | | |
| R10 Resource use acceptable (AT-SP-13) | | | | |
Cell values allowed: *Meets (measured: …)* · *Partially (measured: …)* · *Fails (measured: …)* · *Not measured*.

## 10. Decision rules and pass rule (PROPOSED — Q12)
1. **Recommendation logic:** B meets R1–R9 → recommend B. Only A meets → recommend A (A′ if speed/pitch is the sole shortfall). Both partial → owner decision on trade-offs. Neither meets → evaluate C or change scope; **STOP**.
2. **Checkpoint pass (G24):** report delivered on **≥ 1 physical device**; the recommended approach has no *Fails* on R1, R3, R5, R6 with owner-approved tolerances; owner approves. This is recorded as **single-device feasibility**.
3. **Multi-device validation:** claimed only after the same protocol has been run on **two physical devices**; required before release (G11).
4. Tolerances (drift, click, stale-audio window, resync time) are **proposed from the data** in the report and become binding only on owner approval.

## 11. Delivery, safety, privacy
- Serve the test page via **USB port forwarding** (phone opens `localhost:<port>`; secure context; no LAN exposure; F23/F25). Fallback (ADR-024): a static file server on the LAN for the session only, clearly not the backend, stopped afterwards. No backend or credentials are involved.
- Use fixtures only; no personal media; no data leaves the devices.

## 12. Outputs and stop conditions
- **Outputs:** `docs/spike/PHASE_1B_REPORT.md` (filled §8/§9 tables, narrative, anomalies), raw logs and recordings stored outside Git (referenced by name/hash), recommended ADR-014 wording, proposed tolerances.
- **Stop conditions:** (a) no approach meets the rule → STOP and report; (b) device unavailable → report BLOCKED (B2), do not start Phase 4/5; (c) any result that contradicts a gate assumption is reported immediately.
- **After delivery:** STOP and wait for owner approval; Phase 4/5 remain locked until G24 passes.
