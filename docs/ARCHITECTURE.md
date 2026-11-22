# TubeSomali — Architecture

**Revision 2 · reconciliation pass 1 · 2026-11-20 · DRAFT. No code exists; this document defines contracts and decisions to be validated.** Frontend: React + TypeScript + Vite. Backend: Python FastAPI. Both retained from rev 1 (no finding justifies changing them).

*Revision note (reconciliation 1):* additive — new §4a (headroom/clipping/smoothing), §11 (backend connection security, G23), §12 (voice-preparation jobs), §13 (feasibility checkpoint). Changed in place (visible): "Phase 6 spike measurements" → "Phase 1b spike measurements" (§5); PWA caveat added to §9. Everything else is unchanged.

## 1. Context

```
                      ┌──────────────────────── Frontend (PWA, Android-first) ────────────────────────┐
 Home / Mode select ─▶│  modes/youtube/                    modes/authorized/                          │
                      │   YouTubePlayerAdapter              AuthorizedMediaPlayer ─┐                  │
                      │   (official IFrame only)            SubtitleRenderer       │                  │
                      │                                     AudioMixer ◀── AudioScheduler ◀─ clock   │
                      │  core/ (shared, pure)               MediaRights flow        │                  │
                      │   Segment, subtitles parse/export, i18n, library (IndexedDB)                  │
                      └──────────────┬──────────────────────────────────┬───────────────────────────┘
                                     │ subtitle text only (never video)   │
                      ┌──────────────▼──────────────┐       ┌────────────▼────────────┐
                      │ Backend (FastAPI, local-first) │      │ on-device option [U]    │
                      │  translation/ TranslationPipeline │   │ (WASM/ONNX — unproven) │
                      │  tts/ TTSAdapter + voice registry │   └─────────────────────────┘
                      │  captions/ (research-only, OFF)   │
                      │  jobs/, security/                 │
                      └───────────────────────────────────┘
```

## 2. Hard boundary between modes (ADR-013)
- Frontend: `modes/youtube/` **may not import** `AudioMixer`, `AudioScheduler`, `TTS*`, `SubtitleRenderer` overlay code, or any file/media API. Enforced by an ESLint `no-restricted-imports` rule **and** a bundle-analysis test that fails if the YouTube entry chunk contains those modules.
- Backend: caption research code lives in `backend/research/` and is not importable from production routers; the router for it is not registered unless an explicit research flag is set, and the build/CI test asserts it is absent in release config.
- `core/` contains only pure logic (segments, SRT/VTT, i18n, storage). Nothing in `core/` fetches from YouTube.
- A constant `YOUTUBE_MODE_AUDIO_ALLOWED = false` is asserted by test; the YouTube screen renders an explanation instead of audio controls.

## 3. Component contracts (conceptual)
| Component | Responsibility | Must **not** |
|---|---|---|
| `YouTubePlayerAdapter` | Create official IFrame player; expose state events (`onStateChange`), `getCurrentTime`, official controls pass-through **[V F14]**. Size ≥ 200×200 **[V F13]**. | Mute/alter volume for dubbing, draw anything in front of the player **[V F12]**, load TTS, touch media. |
| `AuthorizedMediaPlayer` | Wrap an `HTMLVideoElement` fed from a local object URL; expose `play/pause/seek/rate/currentTime`; emit events; is the **master clock** for the page. | Upload the file; accept URLs. |
| `SubtitleRenderer` | Render cues for the current time from the Segment list; styles from settings. | Own timing; mutate segments. |
| `TranslationPipeline` | Translate batches (context-aware), per-cue retranslate, edit, restore; preserves ids and timing. | Change cue timestamps. |
| `TTSAdapter` | `synthesize(text, voiceId) → audio + duration metadata` for registry voices only. | Expose a voice absent from the registry or failing QA. |
| `AudioMixer` | Web Audio graph with two independent gains + master; smooth gain changes; mute states. | Decide timing. |
| `AudioScheduler` | Aligns Somali speech to the master clock across play/pause/seek/rate; cancels stale audio; applies timing policy. | Rewrite original timestamps (stored separately from adjusted timing). |
| `MediaRights` | Capture, store, display, delete the user's declaration. | Claim to verify rights. |

## 4. Dual-audio design (G11) — options to be decided by measurement

**Web Audio facts relied on:** an `AudioContext` created outside a user gesture is `suspended` until `resume()` from a gesture **[V]**; `createMediaElementSource` reroutes the element's audio into the graph **[V]**; `AudioBufferSourceNode.playbackRate` resamples, changing pitch with speed **[V]**; `HTMLMediaElement.preservesPitch` defaults to true and is widely available **[V]**; `GainNode.gain` is a live `AudioParam`, default 1, and abrupt value changes can click — use scheduled/smoothed changes **[U — from spec knowledge relayed by the fetch tool; confirm in the Web Audio spec]**; one `createMediaElementSource` call per element **[U]**; cross-origin media needs CORS for graph output **[U, irrelevant for same-origin object URLs]**.

**Target graph (all options):**
```
<video> ──▶ MediaElementSource ──▶ GainNode(original) ─┐
Somali speech source ───────────▶ GainNode(somali)  ───┼─▶ Master gain ─▶ destination
```

| Option | Somali speech source | Seek / pause | Playback speed | Edits | Risks |
|---|---|---|---|---|---|
| **A. Per-segment scheduling** | Decoded `AudioBuffer` per cue, started with `AudioBufferSourceNode.start(when)` | Cancel all pending sources, recompute from master time | Pitch shifts unless a time-stretch (AudioWorklet/WASM) is added **[V pitch behavior]** | Re-synthesize one cue only | Many nodes; clock drift between audio clock and media clock; most scheduler logic |
| **B. Pre-rendered Somali track** | One stitched audio track (speech + silence) rendered from the cue plan, played by a second `<audio>` element | Set `currentTime` (like the video); same `playbackRate`; `preservesPitch` handles speed | Native | Re-render affected span/stitch again | Needs full pre-render before use; two media elements must stay in sync; concurrent-element behavior on Android **[U]** |
| **C. Native Android (Media3 / two players)** | Second native player or custom audio sink | Native | Native | As B | Android *system* mixes simultaneous streams **[V]**, but whether one app can cleanly run two Media3 players/tracks in sync is **[U]**; do not assume track-selection plays two tracks at once (owner's note). Only pursue if A/B fail on device. Duplicates logic if used alongside a web UI. |

**Architect's leaning (to be confirmed by spike, not asserted):** B as primary candidate (handles speed/seek/pitch with platform behavior), A as fallback when per-cue flexibility is needed, C only if G11 fails in WebView/Chrome. All options use the **same gain graph and the same `Segment` plan**, so the choice is isolated behind `AudioScheduler`.

### 4a. Gains, headroom, smoothing (added in reconciliation 1; to be **measured** in Phase 1b)
- Graph: `original gain` and `somali gain` (each 0–1 mapped from the 0–100 % sliders) → `master gain` → destination. The slider→gain mapping (linear vs. perceptual curve) is a UX decision to evaluate on device; no curve is asserted here.
- **Clipping/headroom:** two full-scale sources summed at gain 1.0 each can exceed full scale **[U — general signal-processing fact; to be measured]**. Candidates: master gain below 1.0 as default headroom, and/or a limiter/compressor node on the master bus. Choice made from measured peak levels in AT-SP-03.
- **Smooth transitions:** apply gain changes with scheduled automation rather than direct assignment; `setTargetAtTime` is a candidate (F26 verified for its behavior; click-avoidance is an inference until AT-SP-04 measures it).
- **Pause/seek safety:** on pause or seek, Somali source is stopped/ducked before position change so no stale audio plays (AT-SP-08).

## 5. Synchronization model
- **Master clock = the media element's `currentTime`** (not wall time). All Somali audio positions derive from it.
- Events handled explicitly: `play`, `pause`, `seeking/seeked`, `ratechange`, `waiting/stalled`, `visibilitychange`, fullscreen change, audio device change.
- **Invariant tests:** after `seeked`, no audio belonging to a pre-seek position is audible; after `pause`, all sources silent within one audio render quantum plus output latency; after `ratechange`, Somali follows the new rate.
- Drift handling: continuous low-cost measurement of (Somali position − master position); **resync when exceeding a threshold that is set from Phase 1b spike measurements (re-confirmed in Phase 6) and owner-approved** (no number is asserted here). `AudioContext.baseLatency/outputLatency` are read and recorded per device **[U — available; values unmeasured]**; Bluetooth output latency is a known risk to measure.
- Timing policies for speech longer than its cue: fit (rate within limits), spill into following gap, overlap/duck, or hold video (user-selectable); warnings surfaced per cue. Original cue times are never overwritten; adjusted times are separate fields.

## 6. Data model
`Segment { id, source_start, source_end, source_text, translated_text?, edited, warnings[], speaker?, adjusted_start?, adjusted_end?, tts_duration?, tts_asset_id? }`
`MediaItem { id, local_handle, title, duration, rights_declaration{ts, hash, text_version}, subtitle_source, segments_ref }`
`VoiceProfile { id, model_id, revision, licence, licence_url, commercial_ok, provenance, qa_status }`
Storage: IndexedDB (items, segments, small generated assets); large files referenced by handle, not duplicated; clear/export controls.

## 7. Backend
Modules: `translation/`, `tts/`, `subtitles/`, `jobs/` (cancellable), `security/`, `research/captions` (off). Backend receives **text only** from the player for translation/TTS. *(Reconciliation 1:)* it binds to loopback by default, requires per-device authentication on every data route, and is reachable from the LAN only in an explicit, paired LAN mode (§11, G23). Heavy model inference location depends on Q2/G21: on the owner's PC/home server (default), on-device (unproven), or hosted (unlikely to fit free tiers **[U]**). TTS output returned as audio assets with duration metadata.

## 8. Security and privacy boundaries
No user URL reaches any fetcher (YouTube links are parsed to a video ID for the embed only). Uploads of subtitle files: size/type/content checks, safe parsing. Video never uploaded. No transcript text in logs. CORS allow-list, secure headers, rate limits, no secrets in repo, dependency audit in CI. Model downloads to a cache dir outside the repo, with disk-space warning and explicit user action. `trust_remote_code` models are not run without review and a pinned revision.

## 9. Browser/device matrix (target)
Android: Chrome and Chromium-based browsers, installed PWA, WebView (for a later Capacitor APK). Tested on **real devices** (≥2; Q9) at ≥2 Android versions, with speaker, wired, and Bluetooth output. Desktop browsers are development aids only; they do not count for G11/G15/G16. iPhone is a non-goal **[V F21]**.

**PWA caveat (reconciliation 1):** a page loaded from plain `http://<LAN-IP>` is not a secure context, so service workers (and therefore offline caching) are unavailable, and installability is doubtful **[V F23 for service workers; PWA install [U]]**. Phase 10 PWA work therefore depends on the transport decision in §11 (HTTPS with a locally generated certificate, or loading from `localhost` via port forwarding, F25). Until then no "offline PWA" claim is made.

## 10. Open technical questions
1. Do two simultaneous media elements (or element + Web Audio) stay in sync acceptably on target Android devices? (G11/G12)
2. Which containers/codecs play on those devices? (G22)
3. Can any candidate TTS voice be synthesized fast enough to pre-render a typical video on the chosen host? (G21)
4. Are embedded subtitle tracks extractable in-browser or only via backend tooling? (G19)
5. *(added)* Which transport protection can be achieved on a home LAN with Android clients, and with what user effort? (G23, Q11)
6. *(added)* Does gain smoothing remove audible clicks on target devices, and is a limiter needed for headroom? (AT-SP-03/04)
7. *(added)* Does audio continue/stop predictably when the app is backgrounded or the screen locks, and how does Chrome/WebView treat two media elements then? (AT-SP-10)

## 11. Backend connection security — Android ↔ PC/local backend (G23, ADR-020; added in reconciliation 1)
**Rule (owner D-12): never expose an unauthenticated backend to the local network.**

**Threat model:** other devices on the same Wi-Fi (guests, compromised IoT, other users) must not be able to read or use the backend, read transcripts, trigger heavy jobs, or sniff credentials; a malicious web page open on the phone must not be able to call the backend (CORS/DNS-rebinding); a lost/stolen phone must be revocable.

| Topic | Design (PROPOSED unless noted) |
|---|---|
| Default exposure | Bind to loopback (`127.0.0.1`/`::1`) by default. **LAN mode is an explicit opt-in**; the server refuses to start in LAN mode unless access control is configured. Printed notice when LAN mode is on. |
| Authentication | Every route except `GET /health` (no data) and the one-time pairing endpoint requires `Authorization: Bearer <device token>`. Default-deny middleware; a test enumerates all registered routes and fails if any is unprotected. |
| Pairing (QR / one-time) | PC shows a QR (and a copyable URL) containing host, port, and a **one-time pairing secret** (high entropy, short expiry, single use, carried in the URL **fragment** so it is not sent in the HTTP request line/logged by servers). The phone's **native camera app** opens the URL in the browser — this avoids in-page camera access, which needs a secure context (F23) and `BarcodeDetector` is experimental (F28). Manual fallback: a longer code typed on the phone, with attempt limits and lockout. |
| Device token | Exchange pairing secret → random 256-bit device token. Server stores only a hash; phone stores the token (IndexedDB; never in URLs or logs). Tokens are per device, listable and **revocable from the PC**; optional expiry/rotation. |
| Transport | **OPEN (Q11).** Options: (1) HTTPS with a locally generated certificate (tooling and Android trust steps [U] — to be investigated in Phase 1); (2) plain HTTP on the LAN with request signing (HMAC with a per-device key, timestamp + nonce, replay window) and a clear risk notice — protects credentials but **not** the confidentiality of subtitle text from a LAN sniffer; (3) USB port forwarding to `localhost` for development/testing only (F25). No option is chosen yet; the gate cannot pass without a recorded decision. |
| Host/CORS | Validate `Host` against an allow-list (defence against DNS rebinding); CORS allow-list of the app's own origin only; no wildcard; no credentials via cookies. |
| Rate limiting | Per-IP and per-secret limits on pairing and on auth failures; exponential backoff; audit log of failures without secrets. |
| Where the frontend comes from | Served by the backend itself (same origin) or from `localhost` (F25) — **not** from a public site calling into the LAN, which triggers Chrome's Local Network Access prompt and mixed-content issues (F24, K8). |
| Connection status & reconnection | States: *not paired · pairing · connected · reconnecting · unreachable · unauthorized (token revoked/expired)*. Automatic reconnection with backoff; user-visible status and a manual retry; token errors send the user to re-pair, never to loop. (UX_REQUIREMENTS §10) |
| Offline behavior | Library, player, already-generated captions and voice assets remain usable offline (they live on the phone, ADR-018). Translation/TTS actions that need the backend are disabled with an explanation or queued **only if the user chose to queue**; no silent retries that drain battery. |
| Data sent to backend | Subtitle/translation text, voice id and synthesis parameters, job control messages. **Never** the video/audio file, never the user's rights-declaration text beyond what a job needs (none). Responses: translated text, synthesized audio assets, durations. |
| Privacy & credentials | No transcript text in logs; no tokens in logs; token hashes stored with restricted file permissions on the PC; secrets never in the repo; clear "unpair/forget this device" on both sides. |
| Failure posture | Any auth/config doubt → deny. |

**Related facts:** F23 (secure contexts), F24 (Local Network Access), F25 (port forwarding), F28 (BarcodeDetector). **Tests:** AT-NET-01…14 (ACCEPTANCE_TESTS §H).

## 12. Voice-preparation jobs (ADR-022; added in reconciliation 1)
`prepare(item, voice)` is a **job** on the backend (or local worker) with states `queued → preparing_translation → preparing_voice → ready` and branches `cancelled`, `failed(code)`, `interrupted(reason)`. Progress is measurable by cue count (cues finished / total) and, once synthesis durations are known, audio seconds generated; no time-remaining estimate is shown until enough cues have been measured. Results are **cached per cue** keyed by (normalized text hash, voice id, pinned revision, parameters); resume = skip cached cues. Storage: estimate before start (flagged as an estimate), actual after; warning when free space is below a threshold set from Q14. Jobs are cancellable at any point; cancel stops synthesis and keeps completed cues unless the user chooses to discard. UI mapping: UX_REQUIREMENTS §9. Tests: AT-PR-01…10.

## 13. Dual-audio feasibility checkpoint (G24, ADR-021; added in reconciliation 1)
Phase 1b is a **mandatory checkpoint** before Phase 4/5 implementation. Scope, methods, fixtures, device protocol, decision criteria and stop conditions are in `DUAL_AUDIO_SPIKE_PLAN.md`; the test IDs are AT-SP-01…14. The spike's code is disposable or reusable only by explicit decision; its findings feed ADR-014 and the tolerance proposals.
