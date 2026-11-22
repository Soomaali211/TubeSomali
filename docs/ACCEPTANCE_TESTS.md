# TubeSomali — Acceptance Tests

**Revision 2 · reconciliation pass 1 · 2026-11-20.** Every test below is **NOT RUN**. Results are recorded only from real runs, with environment details. **No test may be marked PASS without actual execution and a recorded environment (owner D-14).**

*Reconciliation 1 is additive:* sections H (AT-NET), I (AT-PR), J (AT-SP) and explicit AT-SEC-01…12 were added; AT-IN-11…25 moved from Phase 2 to Phase 3 (ROADMAP ADR-023, proposed); the measurement rule now names Phase 1b. **All original IDs AT-DA-01…10, AT-SY-01…09, AT-CC-01…04, AT-FS-01…04, AT-YT-01…09, AT-IN-*, AT-CAP-*, AT-TR-*, AT-TTS-* are preserved with unchanged wording.**

*Pass 4 (2026-11-22) is additive:* AT-IN-31…34, AT-NET-15 and section K (AT-ENV-01…03) were added for owner decisions D-19, D-22, D-23, D-25, D-27; **no existing ID or wording changed.** All 160 tests are **NOT RUN**.

**Status legend:** NOT RUN · PASS · FAIL · BLOCKED (cannot be executed until a named prerequisite exists; e.g., device or installs). A test that is merely waiting for its phase is **NOT RUN**, not BLOCKED.

## 0. Conventions
- **Env record (mandatory per run):** device make/model, Android version, browser/WebView name + version, app commit, output route (speaker / wired / Bluetooth), file used (name, container, codec, duration).
- **Android rule:** tests tagged 📱 must pass on **actual Android devices** (≥2, owner to nominate: Q9). Desktop results are informational.
- **Measurement rule:** numeric tolerances (drift, latency, click level) are **set from Phase 1b spike measurements (re-confirmed in Phase 6) and approved by the owner before any test is marked pass/fail**; none is invented here. *(Reconciliation 1: previously said "Phase 6 spike"; the spike is Phase 1b.)*
- **Phase 1b results are early signal, not release evidence.** AT-SP-* results never count toward G11/G15/G16 (they feed G24 only). Multi-device validation is claimed only after **two physical devices** have actually been tested.
- **Measurable method:** where possible use a test fixture with a known audio signature (e.g., tone at a known frequency per channel, clicks at known timestamps) so the result is judged from a recording/analysis, not only by ear. Native-reviewer judgments are recorded separately.
- Status values: NOT RUN · PASS · FAIL · BLOCKED.

## A. Dual audio — Authorized Media (G11, G15) 📱
| ID | Setup | Action | Expected |
|---|---|---|---|
| AT-DA-01 | Fixture with original audio + Somali track ready | Original 100 %, Somali 0 % | Only original audible. |
| AT-DA-02 | same | Original 0 %, Somali 100 % | Only Somali audible. |
| AT-DA-03 | same | Original 30 %, Somali 100 % | Both audible; original clearly lower; level ratio consistent with gains (measured). |
| AT-DA-04 | same | Original 50 %, Somali 50 % | Both audible at equal gain setting (measured). |
| AT-DA-05 | same | Move each slider alone during playback | The other channel's level is unchanged (measured); no cross-coupling. |
| AT-DA-06 | same | Mute original / mute Somali toggles | Mute silences only that channel; un-mute restores previous level. |
| AT-DA-07 | same | Sweep slider 0→100→0 quickly | No audible clicks/zipper noise beyond owner-approved tolerance; value shown matches applied gain. |
| AT-DA-08 | Somali not yet generated | Open player | Original plays; Somali slider disabled with explanation. |
| AT-DA-09 | Backgrounding | Switch app / lock screen / return | Behavior defined and consistent (documented); no runaway audio. |
| AT-DA-10 | Audio output change | Plug/unplug headphones, connect Bluetooth | Playback continues or pauses per defined rule; sync re-measured. |

## B. Synchronization and playback control (G12, G16) 📱
| ID | Action | Expected |
|---|---|---|
| AT-SY-01 | Pause | Video, original and Somali all stop; resume continues aligned. |
| AT-SY-02 | Seek forward/back (scrub, tap, 10 s jump) | Somali position matches new time; **no stale pre-seek Somali audio** audible. |
| AT-SY-03 | Rapid repeated seeks (×20) | No overlapping/ghost speech; no crash; state consistent. |
| AT-SY-04 | Playback speed change (each offered speed) | Both channels follow; drift stays within owner-approved tolerance and does not accumulate over a 10-minute run; Somali pitch behavior recorded. |
| AT-SY-05 | Speed change while paused, then play | Correct rate and alignment on resume. |
| AT-SY-06 | Cue with Somali speech longer than cue | Policy applied; warning shown; original times unchanged in data. |
| AT-SY-07 | Network/loading stall (waiting) | Somali holds with the video; resumes aligned. |
| AT-SY-08 | Long run (≥ 20 min) | Drift measured at intervals; recorded; no memory growth beyond recorded limits. |
| AT-SY-09 | Native reviewer watches 3 excerpts | Timing naturalness rated on a pre-agreed rubric (G12). |

## C. Captions and fullscreen (G16) 📱
| ID | Action | Expected |
|---|---|---|
| AT-CC-01 | Toggle Somali captions on/off during playback | Immediate effect (same frame/next cue); state persisted. |
| AT-CC-02 | Original captions toggle (when supplied) | Independent of Somali toggle. |
| AT-CC-03 | Font size / background / contrast options | Applied live; default contrast passes WCAG AA computed check. |
| AT-CC-04 | Caption timing vs original cue times | Display at source timestamps; edits don't change timing. |
| AT-FS-01 | Enter fullscreen while playing | Playback continues without gap; captions visible; audio panel reachable. |
| AT-FS-02 | Exit fullscreen | Same; state (position, volumes, caption toggles) preserved. |
| AT-FS-03 | Rotate portrait ↔ landscape in and out of fullscreen | Layout correct; no restart; no audio glitch. |
| AT-FS-04 | Fullscreen unsupported (feature detect) | Graceful fallback to expanded layout with message. |

## D. YouTube Mode compliance (G1, G13, G14)
| ID | Check | Expected |
|---|---|---|
| AT-YT-01 | DOM geometry test | No element of ours intersects the player rectangle (no overlays/frames in front of any part) **[F12]**. |
| AT-YT-02 | Player size | ≥ 200×200 on all supported viewports **[F13]**; 16:9 ≥ 480×270 where space allows. |
| AT-YT-03 | Bundle test | YouTube entry chunk contains no `AudioMixer`, `AudioScheduler`, TTS, media-file APIs. |
| AT-YT-04 | Runtime test | `YOUTUBE_MODE_AUDIO_ALLOWED=false`; no `AudioContext` created in YouTube mode; no calls to player `mute/setVolume` from our code. |
| AT-YT-05 | Network test | No requests to caption endpoints, media endpoints, proxies; no cookie reads. |
| AT-YT-06 | Official controls | Play/pause/seek/volume/fullscreen/CC work through the player's own UI on device 📱. |
| AT-YT-07 | Ads/links | Player embedded unmodified; ads and links not hidden or altered (visual check + code review). |
| AT-YT-08 | Somali via official menu | Manual check whether Somali is offered for sample videos; result recorded (informational). |
| AT-YT-09 | Retrieval disabled | Release config: research caption router not registered; research dependency absent from the release image. |

## E. Input, captions, security (from spec §10; phases 2–3)
| ID | Check | Phase |
|---|---|---|
| AT-IN-01…10 | URL forms (watch, youtu.be, shorts, embed, m.), look-alike domains, userinfo tricks, invalid IDs → canonical or reject | 2 |
| AT-IN-11…25 | SRT/VTT parse: BOM, CRLF, overlapping/out-of-order cues, huge file, cue cap, malformed timestamps, XSS payloads, round-trip export | 3 *(was 2; moved by ADR-023, proposed)* |
| AT-IN-26…30 | Media import: object-URL playback, unsupported format message, no upload occurs (network test), declaration required, declaration deletable | 2/6 |
| AT-CAP-01…12 | Provider interface cases from the spec using the **mock** provider: manual, auto, both, other language, multiple tracks, none, disabled, unavailable, timeout, 429, partial failure, upload path unaffected | 3 |
| AT-CAP-13 | No ASR dependency/route anywhere (dependency-graph scan) | 1+ |
| AT-CAP-14 | No media download in any code path | 3 |
| AT-SEC-* | SSRF, upload safety, XSS, CORS, secrets scan, log privacy (no transcript text) — *made explicit below as AT-SEC-01…12* | 8 |

**AT-SEC-01…12 (added, Phase 8; many can run earlier in CI):** 01 SSRF/URL handling (no user URL reaches a fetcher) · 02 upload safety (size/type/content, cue cap) · 03 XSS in rendered subtitles/titles · 04 CORS allow-list · 05 secrets scan of repo and images · 06 log privacy (no transcript text, tokens or secrets) · 07 dependency vulnerability audit · 08 rate limiting · 09 temp-file/cache cleanup and path safety · 10 Host-header / DNS-rebinding rejection · 11 security headers · 12 rights-declaration storage and deletion privacy.

## F. Translation and TTS (phases 4–5)
| ID | Check |
|---|---|
| AT-TR-01…10 | Somali orthography (X, C, Q, DH, KH), names, numbers, dates, acronyms, empty/short/long cues, batch consistency, ids/timing preserved, retranslate/edit/restore. |
| AT-TR-11 | Benchmark report filled only with measured values and named reviewers. |
| AT-TTS-01…10 | Registry completeness; model loads; X/C/Q phonemes; numbers/names; long text chunking; clipping/silence; repeatability (seeded); sample rate/duration metadata; failure → voice not shown; licence notice for NC models. |
| AT-TTS-11 | Pre-render speed on the chosen host for a reference video length (G21). |

## G. Resource and device checks (G18, G22) 📱
Measure and record: app start time, peak memory during playback + pre-render, storage per model/asset, battery/thermal notes over a 20-minute session, format matrix (container/codec → plays yes/no), behavior under low memory and background kill.

## H. Backend connection security — Android ↔ PC (G23; ARCHITECTURE §11) *(added in reconciliation 1)*
Tests marked 📱 need a physical Android phone and a real LAN; "2nd device" means another, **unpaired** device on the same LAN.
| ID | Check | Expected |
|---|---|---|
| AT-NET-01 | Start backend with defaults; connect from another host on the LAN | Connection refused/unreachable (loopback-only default). |
| AT-NET-02 | Enable LAN mode without access control configured | Server refuses to start with an explanatory error. |
| AT-NET-03 | Automated route enumeration | Every registered route except `/health` and the pairing endpoint rejects requests without a valid token. |
| AT-NET-04 📱 | From a 2nd, unpaired LAN device request a data route | 401/denied; nothing leaked in the response body. |
| AT-NET-05 📱 | Pair the phone by scanning the QR with the phone's camera app | Token issued; subsequent authenticated calls succeed; pairing screen shows success. |
| AT-NET-06 | Replay a used pairing secret | Rejected. |
| AT-NET-07 | Use an expired pairing secret | Rejected with "expired" message; new code can be requested. |
| AT-NET-08 | Brute-force manual codes | Attempt limit, backoff/lockout observed; counts recorded. |
| AT-NET-09 📱 | Revoke the device on the PC | Phone enters *access revoked* state, prompts to re-pair, **no retry loop**. |
| AT-NET-10 | Request with an unexpected `Host`, and a request from a foreign `Origin` | Rejected (DNS-rebinding/CORS protection). |
| AT-NET-11 | Scan logs after a full test session | No tokens, pairing secrets, or transcript text. |
| AT-NET-12 | Inspect credential storage | PC stores token **hashes** only, with restricted permissions; phone token not present in any URL or log. |
| AT-NET-13 📱 | Toggle Wi-Fi, put PC to sleep, return | States shown (reconnecting/unreachable/connected), automatic reconnection with backoff, offline features keep working, no tight retry loop (request rate recorded). |
| AT-NET-14 📱 | Verify the transport protection chosen under Q11 | If HTTPS: certificate validation behaves as documented; if HTTP+signing: replayed/modified requests rejected and credential not visible in a packet capture. Result recorded; **gate cannot pass until Q11 is decided.** |

## I. Voice-preparation UX and cache (UX_REQUIREMENTS §9; ADR-022) *(added in reconciliation 1)*
| ID | Check | Expected |
|---|---|---|
| AT-PR-01 | Open an unprepared item | Idle state with a storage **estimate** clearly marked as estimate. |
| AT-PR-02 | Estimated size exceeds free space/budget | Storage warning blocks until the user chooses (continue/free space/cancel). |
| AT-PR-03 | Translation stage | Determinate progress by cues; skipped when translation exists. |
| AT-PR-04 | Voice stage | Progress by cues (and seconds when known); no time-remaining estimate before enough data. |
| AT-PR-05 | Cancel mid-voice | Synthesis stops; finished cues kept; user told what was kept and its size. |
| AT-PR-06 | Partial failure then "Retry failed" | Only failed cues are re-synthesized (verified by counting synthesis calls). |
| AT-PR-07 📱 | Interrupt (lose connection / background / kill app) then resume | Cached cues skipped; if resume unsupported for that reason, UI states so. |
| AT-PR-08 | Re-open unchanged item; edit one cue | Cache hit for unchanged cues; only the edited cue regenerates. |
| AT-PR-09 | Ready state | Somali slider enabled; change announced to assistive tech. |
| AT-PR-10 | Each error category | Plain-Somali message mapped from the fixed vocabulary; no raw stack traces/tool output. |

## J. Phase 1b — Dual-audio feasibility checkpoint (G24; DUAL_AUDIO_SPIKE_PLAN.md) *(added in reconciliation 1)*
All 📱, first on the owner's available Android device; each run records the environment per §0. **Early signal only — not G11/G15/G16 evidence.** Numeric thresholds are proposed from these measurements and approved by the owner afterwards (Q12).
| ID | Investigates | Notes |
|---|---|---|
| AT-SP-01 | Original and Somali audio on **independent GainNodes** | Per-channel marker tones; confirm each gain controls only its channel. |
| AT-SP-02 | **0–100 % controls** and slider→gain mapping | Measured levels at 0/30/50/100 % per channel; crosstalk check. |
| AT-SP-03 | **Master output gain, clipping prevention, headroom** | Peaks with both channels at 100 % with/without master reduction or limiter. |
| AT-SP-04 | **Smooth gain transitions without clicks** | Direct assignment vs. scheduled automation; waveform discontinuity analysis. |
| AT-SP-05 | **Synchronization with video `currentTime`** at 1× | Drift over ≥10 min, per approach. |
| AT-SP-06 | **Pause/resume** alignment | Both channels stop/resume together. |
| AT-SP-07 | **Seek and repeated seek** (single, ×20) | Position correct; no ghost audio. |
| AT-SP-08 | **Scheduling and stale-audio cancellation** | Residual audio window after seek/pause measured with marker tones. |
| AT-SP-09 | **Playback speed** (set of rates) | Sync and pitch behavior per approach. |
| AT-SP-10 | **Buffering/stall** and **backgrounding/screen-lock/return** | Behavior defined; AudioContext state; resync after return. |
| AT-SP-11 | **Headphone and Bluetooth output** | Offset vs speaker; `outputLatency` value read and compared with measurement. |
| AT-SP-12 | **Fullscreen** enter/exit (container) while playing | Sync and state preserved. |
| AT-SP-13 | **Two simultaneous media elements** (video + audio) on the device | Concurrency behavior, start-up sync, CPU/memory observations. |
| AT-SP-14 | **Approach comparison and recommendation** | Filled comparison table for A / B (/ A′ / C if reached), measured data only, recommendation and proposed tolerances for owner approval. |

## K. Pass-4 additions (owner decisions D-19, D-22, D-23, D-25, D-27) *(all NOT RUN)*
| ID | Test | Expected | Phase |
|---|---|---|---|
| AT-IN-31 | Authorized Media: import a local file, leave the ownership/authorization **checkbox unticked**, try to continue | Cannot continue; the media is not processed (no translation, TTS or backend job can be started for it) | 2 |
| AT-IN-32 | Open the declaration step | The checkbox is **not pre-ticked**; an explicit separate **confirmation** action is required after ticking; text is shown in Somali (draft wording, Q3); confirmation stored locally per item (timestamp, file name, hash) and deletable | 2 |
| AT-IN-33 | Network/log inspection from file selection until confirmation | **No** processing request, no upload and no backend call occurs before confirmation; after confirmation, only subtitle text — never the media file — may be sent (ADR-018) | 2 |
| AT-IN-34 | Authorized item with **no** supplied SRT/VTT and no supported embedded subtitles | Translation/voice actions are unavailable with a Somali explanation that subtitles must be supplied; **no ASR/transcription path exists or is offered** (also AT-CAP-13) | 3 |
| AT-NET-15 | If an HTTP-with-signing fallback exists (T2, ARCHITECTURE §11a): enable it | An opt-in screen states in Somali that subtitle text is **not encrypted**; it is off by default; if no such fallback exists the test is recorded as *not applicable* with the reason (not PASS) | 1/8 |
| AT-ENV-01 | A push triggers the GitHub Actions workflow | The workflow runs lint, type-check, unit tests and guard scripts for both halves; the run log (URL or pasted output) is recorded. **Until a run exists: NOT RUN** | 1 |
| AT-ENV-02 📱 | The owner's phone opens the test harness over HTTPS | The page loads in a secure context; audio context can start after a user gesture; environment record filled. **Requires an authorized harness deployment** | 1b |
| AT-ENV-03 | Inspect the public harness repository and its published files | Contains **only** isolated test code and synthetic fixtures — no application secrets, user media, private documents, tokens or code copied from the private repository without approval; secrets scan clean | 1b |
