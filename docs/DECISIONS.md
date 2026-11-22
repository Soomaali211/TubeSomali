# TubeSomali — Decisions, Verification Log and Risk Register

**Phase 0 · Revision 2 · reconciliation pass 1 · 2026-11-20 · DRAFT — awaiting owner approval.** *(Pass 4, 2026-11-22: the owner's 13 Phase 0 decisions are applied — see §8.8–§8.12 and `OWNER_DECISIONS_PASS4_CHANGELOG.md`. Where §8.9 differs from §8.1/§8.2/§8.3, §8.9 is authoritative.)* No application code exists. Nothing here is a legal opinion.
Companion documents: `OWNER_DECISIONS_PASS4_CHANGELOG.md`, `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `UX_REQUIREMENTS.md`, `ACCEPTANCE_TESTS.md`, `GATES.md`, `ROADMAP.md`, `CONSISTENCY_AUDIT.md`, `PROGRESS_REPORT.md`, `PHASE1_PLAN.md`, `DUAL_AUDIO_SPIKE_PLAN.md`.

**Status vocabulary (owner-specified):** **DECIDED** = the owner has stated or approved it (source cited) · **PROPOSED** = architect proposal awaiting owner confirmation · **OPEN** = no owner information yet · **BLOCKED** = cannot progress until a named external prerequisite exists. *No item is marked DECIDED without a cited owner statement.*

### Revision history
| Date | Change |
|---|---|
| 2026-11-20 rev 1 | First Phase 0 (caption-tool framing). Superseded by rev 2 but its facts/POC audit retained. |
| 2026-11-20 rev 2 | Reframed to the two-mode video player vision (owner rev-2 brief). Facts F12–F22, ADR-013…019, Q8–Q10. |
| 2026-11-20 rev 2 / reconciliation 1 | **Additive:** status vocabulary; §8 reconciliation (owner-directive log D-01…D-17, ADR status register, Q1–Q14 register, BLOCKED register); facts F23–F28; key findings K7–K9; ADR-020…024; §1 inspected list. **Changed (visible):** POC finding labels `A1–A12` → `P1–P12` (collided with roadmap amendments `A1–A6`); §0 "G19–G22" text extended to G24; F22 annotated (partially verified). **Preserved unchanged:** all other rev-2 text, including legacy "Accepted" labels (superseded by §8.1) and §7 question text (superseded by §8.2). |
| 2026-11-21 rev 2 / reconciliation 2 | **Additive:** §8.6 re-verification log and §8.7 pass-2 note; K4 and §0 row annotated as resolved (spike now mandatory Phase 1b); G2/G3 cross-referenced in §8.1 rows 003/005; Appendix B gets an updated Somali summary. **Corrected (visible):** §1 state-check row (it said disk and Project were identical; after the pass-1 edits the Project copies were stale until synced on 2026-11-21). **Preserved unchanged:** everything else, including the old Appendix B text (marked superseded). |
| 2026-11-22 rev 2 / owner decisions (pass 4) | **Additive:** §8.8 directive log D-18…D-30 (the owner's 13 decisions, cited); §8.9 status overlay (Q1–Q14 plus new Q15, Q16 and ADR changes); §8.10 commercial-licence consequences (NOT VERIFIED); §8.11 facts F29–F30 (GitHub Pages limits, re-read from the primary page via a summarizing fetch); §8.12 ADR-025 (phone test delivery) and ADR-026 (storage budget), both PROPOSED. **Visible pointers added** to the §8.2 and §8.5 headings and the header. **Preserved unchanged:** every earlier row, ADR text, directive D-01…D-17, Q1–Q14 text, and Appendices A and B. No status was changed in §8.1/§8.2 text — the overlay in §8.9 carries the new statuses. |

**Evidence labels:** **[V]** verified this session against a named source · **[U]** unverified (handoff claim or general knowledge) · **[T]** tested by running code (**none exist yet**).
Web pages were read through a fetch tool that returns summaries; any item that gates a release must be re-read in primary text at review time.

## 0. What changed from revision 1
| Change | Why |
|---|---|
| Product reframed from "caption tool" to **video player with Somali translation**, with two hard-separated modes (YouTube / Authorized Media). | Owner's clarified vision. |
| New finding: **overlays in front of the YouTube player are prohibited**, and no documented way exists to feed custom captions into the official player (F12, F15). Custom Somali captions on YouTube are now gate **G13**, default *not built*. | Fetched *Required Minimum Functionality* and IFrame API reference. |
| Caption retrieval from YouTube is **research-only, disabled in every shipped build** (G14). Rev 1's "flag-gated adapter" was too permissive. | Owner's direction + ToS finding F6. |
| New architecture: dual-audio mixer (Web Audio gains), master clock, scheduler options A/B/C (ARCHITECTURE §4–5). | Owner's vision; verified Web Audio/pitch facts. |
| Gate register moved to `GATES.md`; G11–G18 added from owner's brief; G19–G22 added by me (G23–G24 added in reconciliation pass 1). | Owner's brief. |
| Roadmap phases re-ordered to owner's list; one extra de-risking spike proposed (A5). *(A5 was later adopted by the owner as the mandatory Phase 1b, D-11.)* | Owner's brief + risk analysis. |
| Retained unchanged: stack (React+TS+Vite / FastAPI), no-ASR, no paid APIs, local-first, TTS/MT licence findings, POC audit. | No evidence to change them. |

## 1. What was inspected
| Item | Result |
|---|---|
| Repository | None found (`/home/claude` empty, not git). Nothing overwritten. |
| Handoff docs (3) + caption POC zip | Read in full; POC not run. |
| Owner's rev-2 brief (text attachment) | Read in full; reflected throughout. |
| Owner's "Final Reconciliation (Rev 2)" brief (text attachment, 2026-11-20) | Read in full; reflected in reconciliation pass 1 (§8, GATES G23/G24, ROADMAP order, ACCEPTANCE AT-NET/AT-PR/AT-SP). |
| State check after session pause | *(Corrected in reconciliation 2.)* At the first check all 7 documents were identical on disk and in the Project. After the pass-1 edits the Project copies were **stale** (no G23/G24, old roadmap order, no §8); this was found on 2026-11-21 and the Project was re-synced (see CONSISTENCY_AUDIT.md C-02). No owner edits were found in either place. |
| Sandbox **[V]** | Python 3.13.18, Node 22.23.5, npm 10.9.9, git, docker binary, ffmpeg. No yt-dlp/FastAPI. youtube.com unreachable. Package installs disabled. **No Android device or emulator access** — so no audio/player claim can be tested here. |

## 2. Verified facts

### 2.1 YouTube policy / terms
| # | Fact | Source |
|---|---|---|
| F1 **[V]** | No downloading/caching/storing YouTube audiovisual content, no offline playback, without prior written approval (III.E.1.a/b). | https://developers.google.com/youtube/terms/developer-policies |
| F2 **[V]** | No separating/isolating/modifying audio or video components (III.I.7); "must not apply alternate audio tracks". | same |
| F3 **[V]** | No modifying/building upon/blocking player functionality (III.I.6); no altering player links (III.I.4); no modifying/replacing/blocking ads (III.I.5); no background-player audio features (III.I.9). | same |
| F4 **[V]** | Translations must not be added without user's consent; easy disable if default (III.C.3.b). | same |
| F5 **[V]** | `captions.download`: OAuth + permission to edit the video; 200 quota units; content-owner param is CMS-partner only. Not a route to arbitrary public captions. | https://developers.google.com/youtube/v3/docs/captions/download |
| F6 **[V]** | ToS prohibits downloading content unless permitted, circumventing the Service, and accessing it "using any automated means (such as robots, botnets or scrapers)" except search engines per robots.txt, with written permission, or where law permits. | https://www.youtube.com/static?gl=GB&template=terms |
| **F12 [V]** | *Required Minimum Functionality*: "You must not display overlays, frames, or other visual elements in front of any part of a YouTube embedded player"; also must not use them to obscure any part of the player; covers controls. The page does not address caption display. | https://developers.google.com/youtube/terms/required-minimum-functionality |
| **F13 [V]** | Embedded player viewport must be at least 200×200 px; 16:9 recommended ≥ 480×270. | same + IFrame API reference |
| **F14 [V]** | IFrame API provides `getCurrentTime`, `seekTo`, `setVolume` (0–100), `mute/unMute`, `setPlaybackRate` (only a *suggestion*, may not change), `onStateChange` (-1,0,1,2,3,5). | https://developers.google.com/youtube/js_api_reference |
| **F15 [V]** | Documented caption options via the `captions` module are only `fontSize` (−1…3) and `reload`. No documented API to supply custom caption text. | same |

### 2.2 Caption-retrieval tooling
| # | Fact | Source |
|---|---|---|
| F7 **[V]** | `youtube-transcript-api`: MIT; 1.2.5 released 2026-11-05; Python ≥3.8,<3.16; lists/fetches transcripts, manual vs auto filter, optional YouTube auto-translation, SRT/VTT formatters. | https://pypi.org/project/youtube_transcript_api · https://github.com/jdepoix/youtube-transcript-api |
| F8 **[V]** | README: YouTube "has started blocking most IPs that are known to belong to cloud providers"; proxies "don't guarantee" access; cookie auth currently unavailable. | GitHub README |
| F9 **[V]** | `yt-dlp` has open intermittent-403 reports tied to PO-token enforcement (#17395, media downloads; indicative of fragility only). | https://github.com/yt-dlp/yt-dlp/issues/17395 |

### 2.3 Translation / TTS models
| # | Fact | Source |
|---|---|---|
| F10 **[V]** | `Helsinki-NLP/opus-mt-en-cus`: Apache-2.0; Somali (`som`) among targets; only English→Somali score listed: **16.0 BLEU / 0.173 chrF (Tatoeba-test)**; target-token convention not stated; English-source only. | https://huggingface.co/Helsinki-NLP/opus-mt-en-cus |
| F11 **[V]** | NLLB-200-distilled-600M: CC-BY-NC 4.0 (non-commercial); `som_Latn` present. | https://huggingface.co/facebook/nllb-200-distilled-600M/blob/main/README.md |
| TTS table | `facebook/mms-tts-som` **CC-BY-NC 4.0 [V]** (via mirror `maanka2/mms-tts-som`; VITS 36.3M params; non-deterministic unless seeded). `Somali-tts/somali_tts_model`: **no licence stated [V]**, VITS 36.3M (hypothesis, unverified: may derive from MMS → NC), no data/limitations documented. `Zyroxx66/StyleTTS2-Somali`: **no licence stated [V]**, single real female speaker ~1h15m, fine-tuned from English LibriTTS, data source/consent unstated, early checkpoints soften X/C. `Somali-tts/Hussein_tts`: page failed to load — MIT claim **[U]**. `lakiLabs/omi-tts`: not fetchable/not found — all claims **[U]**. **No Somali TTS candidate has a verified permissive licence.** | HF pages as listed in rev 1 |

### 2.4 Web platform and Android audio
| # | Fact | Source |
|---|---|---|
| **F16 [V]** | An `AudioContext` created outside a user gesture starts `suspended`; call `resume()` from a gesture (or create it in the handler). | MDN Web Audio best practices |
| **F17 [V]** | `AudioContext.createMediaElementSource()` re-routes a media element's output into the Web Audio graph; play/pause remain on the element. | MDN |
| **F18 [V]** | `AudioBufferSourceNode.playbackRate` resamples → pitch changes with speed; no built-in time-stretch (needs AudioWorklet/WASM). | MDN |
| **F19 [V]** | `HTMLMediaElement.preservesPitch` default **true**, Baseline widely available (since Dec 2023). | MDN |
| **F20 [V]** | On Android the system mixes simultaneous streams from apps; audio focus is per app, cooperative before Android 12 and enforced from 12; apps targeting API 35 can request focus only if top app/foreground service. *Not stated:* how two players inside one app interact. | https://developer.android.com/media/optimize/audio-focus |
| **F21 [V]** | Fullscreen on non-video elements is not reliable on iPhone Safari (Apple forum thread through mid-2024: disabled in iOS 17.4 beta; `webkitEnterFullScreen` only for `<video>`). Android support table fetched was ambiguous → **must be tested on device [U]**. | https://developer.apple.com/forums/thread/133248 · caniuse |
| F22 **[U]** *(partially verified in reconciliation 1 — see F26)* | `GainNode.gain`: default 1, live `AudioParam`, abrupt changes can click, use scheduled/smoothed changes. (Relayed from spec knowledge by the fetch tool, not from the MDN page text.) | confirm in W3C spec |

### 2.5 Added in reconciliation pass 1 (2026-11-20)
| # | Fact | Source |
|---|---|---|
| **F23 [V]** | **Secure contexts:** only `https`/`wss`/`file` schemes and loopback/`localhost` hosts qualify. `http://192.168.x.x` is **not** a secure context; `https://192.168.x.x` is. Service workers can only be registered in secure contexts. *Not on the page (general knowledge, [U]):* PWA install and `getUserMedia` also depend on secure context. | https://developer.mozilla.org/en-US/docs/Web/Security/Secure_contexts |
| **F24 [V]** | **Chrome Local Network Access:** a permission prompt gates requests from a public site to local/loopback destinations (incl. 192.168.0.0/16); the permission can only be requested in secure contexts; page states the prompt launches in Chrome 142; whether it applies on Android is **not stated**. | https://developer.chrome.com/blog/local-network-access |
| **F25 [V]** | **Port forwarding:** Chrome DevTools remote debugging can map a port on the Android device to a port on the dev machine over USB, independent of network configuration; the phone then opens `localhost:<port>`. Prerequisite: remote debugging set up (details on a separate page, not read). | https://developer.chrome.com/docs/devtools/remote-debugging/local-server |
| **F26 [V]** | `AudioParam.setTargetAtTime(target, startTime, timeConstant)` moves a parameter exponentially toward the target (≈95 % after 3×timeConstant). The page does not itself discuss clicks; using it to avoid clicks is an **inference** ([U] until measured in the spike). | https://developer.mozilla.org/en-US/docs/Web/API/AudioParam/setTargetAtTime |
| **F27 [V]** | `AudioContext.outputLatency` estimates output-hardware latency (e.g., Bluetooth) and can be used to align video drawing with audio; Android-specific behavior is **not covered** by the page; `baseLatency`/`getOutputTimestamp` details were not on the page read. | https://web.dev/articles/audio-output-latency |
| **F28 [V]** | `BarcodeDetector` is marked experimental, limited availability, secure-context only; Android Chrome support not confirmed from the page. | https://developer.mozilla.org/docs/Web/API/Barcode_Detection_API |

## 3. Key findings that shape the design
1. **K1 — The full vision is only buildable in Authorized Media Mode.** On YouTube, Somali audio (F2, F3), custom overlays (F12) and unofficial caption retrieval (F6, F8) are each blocked or gated. The product's value therefore lives in Mode B, where the user's own file is played by our own element.
2. **K2 — Mode B has no ASR, so it needs a text source.** Videos with no supplied/embedded subtitles can't be translated (G19, Q8).
3. **K3 — Pitch vs speed decides the audio design.** Per-cue `AudioBufferSourceNode` playback shifts pitch at ≠1× (F18); a pre-rendered Somali track on a media element preserves pitch natively (F19). This is why ARCHITECTURE §4 keeps A and B open and recommends measuring.
4. **K4 — The riskiest unknown is Android dual-audio sync, and it's scheduled late (Phase 6).** A cheap early spike with generated tones would de-risk Phases 4–5 (roadmap A5). *(Resolved: the owner made the spike a mandatory Phase 1b checkpoint, D-11, ADR-021, G24.)*
5. **K5 — Licensing remains the commercial blocker.** No verified permissive Somali TTS; NLLB NC; MT candidate weak and English-only.
6. **K6 — Cannot test on Android here.** Every device-dependent gate (G11, G12, G15, G16, G18, G22) needs the owner's devices (Q9).
7. **K7 (reconciliation 1) — A LAN-HTTP backend is an insecure context (F23).** If the phone loads the app from `http://<PC-LAN-IP>:port`, service workers, secure-context-only APIs (incl. `BarcodeDetector`, F28; camera access is [U]) and, very likely, PWA install are unavailable, and the pairing token would travel in clear text on the LAN. This couples **G23**, **Phase 7/10 (PWA)**, and the pairing design (ARCHITECTURE §11). Options are laid out there; none is chosen yet (Q11).
8. **K8 — Serving the frontend from the public internet while the backend sits on the LAN triggers Chrome's Local Network Access prompt (F24) and mixed-content problems**; the proposed default is to serve the frontend from the backend itself (same origin) or from `localhost` via port forwarding (F25).
9. **K9 — Bluetooth/headphone latency is a first-class sync risk;** `outputLatency` exists as an estimate (F27) but Android behavior is unverified → covered by AT-SP-09 and AT-DA-10.

## 4. Unverified assumptions (do not rely on these)
Adapters actually returning captions from a home connection; manual/auto distinction in practice; `opus-mt-en-cus` target token, size, latency, real quality; Somali offered in YouTube's official caption menu for a given video; `opus-mt-cus-en` as pivot; on-device ML in WASM/ONNX on mid-range Android; free-tier hosting limits; `yt-dlp` licence; Docker daemon availability; whether the IFrame API embed places the app under API Services Terms for every clause (my reading: yes); two simultaneous media elements staying in sync on Android; container/codec coverage on target devices; embedded-subtitle extraction path; gain click behavior (F22); Hussein_tts and omi-tts claims.

## 5. Architecture decision records
> **Legacy status labels:** the word "*Accepted*" in ADR-001…019 below means *architect-accepted when written*, **not** owner approval. The authoritative status of every ADR is in **§8.1**. Original text is preserved unchanged.

**ADR-001 No ASR, structurally.** No speech-to-text dependency or route; CI dependency scan; provider interfaces accept no audio. *Accepted.*

**ADR-002 (revised) Input priority.** SRT/VTT import (Phase 2) feeds Mode B and the editor; it is infrastructure for the player, not the product. YouTube caption retrieval is **not** an input path in shipped builds (G14). *Accepted.*

**ADR-003 (revised) Caption providers = research-only.** Provider interface + mock provider ship; any unofficial adapter (first candidate `youtube-transcript-api`, rationale in rev 1: native manual/auto flag, structured segments) lives in `backend/research/`, is unregistered in release builds, needs an explicit research flag, and is exercised only on the owner's machine. No cookies/proxies/IP rotation/PO-token/evasion. *Accepted, pending G14.*

**ADR-004 Stack and contracts.** Monorepo `frontend/` `backend/` `docs/`; versions pinned in Phase 1 after fresh checks; fixed error vocabulary: `NO_CAPTIONS`, `CAPTIONS_UNAVAILABLE`, `LANGUAGE_NOT_AVAILABLE`, `VIDEO_UNAVAILABLE`, `RATE_LIMITED`, `PROVIDER_BLOCKED`, `NETWORK_TIMEOUT`, `PROVIDER_ERROR`, `POLICY_RESTRICTED`, `INVALID_URL`, `UNSUPPORTED_FILE`, `RIGHTS_NOT_DECLARED`, `AUDIO_UNAVAILABLE`. *Accepted.*

**ADR-005 Topology: local-first.** Backend self-run (Docker/Python) on owner's PC/home server; phone is client. Public hosted instance, if ever, must be consistent with G14 (no retrieval) and is evaluated in Phase 9. *Proposed (Q2).*

**ADR-006 (revised) YouTube Mode = official player + official controls only.** No overlay of ours in front of any part of the player (F12); no audio of ours (G1); our UI outside the player rectangle. Custom Somali captions beside the player only after G13 clears. *Accepted for development; release needs legal review.*

**ADR-007 Translation.** `TranslationPipeline` abstraction, local default; `opus-mt-en-cus` is a candidate to **measure**; English-only source → pivot/reject policy for other languages; output framed as an editable draft; NLLB baseline only if non-commercial confirmed (Q1). *Proposed.*

**ADR-008 TTS.** Voice registry (model id, pinned revision, licence, commercial flag, provenance, QA status, consent note). No voice exposed unless loaded, QA-passed, licensed (G17). No cloning without documented consent. `trust_remote_code` only after review/pin/isolation. *Proposed.*

**ADR-009 Storage/privacy/logging.** IndexedDB library; ephemeral server jobs; no transcript text in logs. *Accepted.*

**ADR-010 Security baseline.** Never pass user URL to a fetcher; arg-list subprocesses; upload limits and content checks; safe parsing; escaped rendering; CORS allow-list; secrets hygiene. *Accepted.*

**ADR-011 POC disposition.** Reference only; refactored into `backend/research/` in Phase 3 (Appendix A). *Accepted.*

**ADR-012 Process.** Each phase: code + tests + docs + exact-output report + gate-register update + STOP. *Accepted.*

**ADR-013 (new) Mode isolation by construction.** Separate frontend/ backend packages; lint + bundle tests prevent YouTube mode from importing mixer/scheduler/TTS/file APIs; `YOUTUBE_MODE_AUDIO_ALLOWED=false` asserted; research caption code unreachable in release. *Accepted.*

**ADR-014 (new) Dual-audio architecture.** Web Audio graph with independent gains (original/Somali) + master; Somali source via Option A (per-cue scheduling) or B (pre-rendered track on a media element) chosen by spike; Option C (native Media3) only if G11 fails in browser/WebView, and not assumed to support two simultaneous tracks. *Proposed; decided by measurement.*

**ADR-015 (new) Master clock and sync policy.** The media element's `currentTime` is the master; scheduler derives everything from it; explicit event handling; invariants tested (no stale audio after seek); drift thresholds set from measurement. Original timing never overwritten. *Proposed.*

**ADR-016 (new) Rights declaration.** Per-item local declaration (timestamp, hash, text version), deletable; no URL→file path in Mode B; honest limits stated; legal review in Phase 8. *Proposed (Q3).*

**ADR-017 (new) Fullscreen strategy.** Fullscreen the player *container* so captions/controls persist; feature-detect and fall back to expanded layout; Android is target, iPhone best-effort/non-goal (F21). *Proposed; verify on device.*

**ADR-018 (new) Media stays on device.** Local object URL playback; only text goes to backend. *Accepted.*

**ADR-019 (new) Captions in Mode B.** Our own `SubtitleRenderer`; text from supplied SRT/VTT or embedded tracks; no ASR (G19). *Proposed (Q8).*

### 5b. Added in reconciliation pass 1 (statuses are authoritative here)
**ADR-020 Backend connection security (G23) — PROPOSED.** Backend binds **loopback only by default**; LAN mode is an explicit opt-in that refuses to start without access control; every route except `/health` and the one-time pairing endpoint requires a per-device bearer credential; pairing by one-time secret shown as QR/URL on the PC (scanned with the phone's *native camera app*, which avoids the secure-context requirement for in-page scanning, F23/F28) plus a manual-code fallback with rate limiting and expiry; per-device revocable tokens stored hashed on the PC; Host-header and CORS allow-lists; transport protection decision pending (HTTPS with locally generated certificate vs. HTTP with signed requests and an explicit risk notice — Q11, ARCHITECTURE §11). No unauthenticated backend is ever exposed to the LAN (owner rule D-12).

**ADR-021 Dual-audio feasibility checkpoint — process DECIDED (D-11); details PROPOSED.** Phase 1b is mandatory and must produce measured findings (DUAL_AUDIO_SPIKE_PLAN.md, AT-SP-01…14) before Phase 4/5 implementation starts. Compared approaches: A (per-cue scheduling), B (pre-rendered track on a media element), optional A′ (A plus time-stretch), and C (native) only if both web approaches fail. First device = the owner's available Android device; **no multi-device claim until two physical devices are tested**. Final approach selection is **BLOCKED** on Phase 1b results.

**ADR-022 Voice-preparation job model — PROPOSED.** Preparation is a cancellable, resumable job with explicit states (UX_REQUIREMENTS §9); per-cue results cached by key (text hash + voice id + pinned revision + parameters) so retries and resume skip finished cues; storage estimate shown before generation and actual size after; partial failure leaves successful cues intact; playback with original audio is allowed while the voice is being prepared.

**ADR-023 Phase re-sequencing — order DECIDED (D-10); content split PROPOSED.** Order: 0, 1, 1b, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11. Proposed content split for Phases 2/3: Phase 2 = authorized media import, rights declaration, safe URL validation, format matrix; Phase 3 = captions pipeline (SRT/VTT parse/normalize/edit/export, embedded-subtitle detection, provider interface + mock, research-only adapter). Preserves every earlier deliverable; only the phase it belongs to moves (ROADMAP §0, CONSISTENCY_AUDIT U1).

**ADR-024 Spike delivery over localhost — PROPOSED.** Phase 1b should serve the test page to the phone via USB port forwarding (phone opens `localhost:<port>`, F25) so no server is exposed to the LAN and the page is a secure context (F23). Fallback if USB debugging is unavailable: serve static fixtures on the LAN for the duration of the test with an explicit note that this is a static dev server, not the backend, and is stopped afterwards (Q13).

## 6. Feasibility assessment
| Feature | Verdict |
|---|---|
| In-app **official** YouTube playback with official controls | **Feasible**; policy re-check before release. |
| Custom Somali captions over the YouTube player | **Not permitted as worded (F12).** |
| Custom Somali captions *beside* the player | **Unknown** — needs G13 review; not planned by default. |
| Somali via the official player's own caption menu | **Possible, unverified [U]** (user-side, no code). |
| YouTube caption retrieval for production | **Not planned (G14).** Research only. |
| Somali voice with YouTube video | **Not permitted (G1).** |
| Authorized local video in-app player, fullscreen, speed, seek | **Feasible** (standard web media); device/codec coverage unmeasured (G22). |
| Two independent volume controls + mixing | **Feasible in Web Audio** (F16–F19); **Android reliability unproven (G11)**. |
| Somali TTS sync across pause/seek/speed/fullscreen | **Plausible, unproven (G12)**; design options in ARCHITECTURE §4. |
| Authorized media with no subtitles | **Not possible without ASR** (K2); requires user-supplied/embedded subtitles. |
| English→Somali local translation | **Feasible but quality-unproven (G6).** |
| Somali TTS local & free | **Licence-constrained (G5, G17); quality unmeasured.** |
| Android APK | **Optional**; WebView path first; native Media3 only if needed (ARCHITECTURE §4 C). |
| "Unlimited free cloud inference" | **Not promisable.** |

## 7. Open questions for the owner
> *Superseded by the §8.2 register (statuses, owner-provided information, new questions Q11–Q14). Original text preserved below.*

1. **Q1** Personal/non-commercial or commercial? (gates MMS TTS, NLLB eligibility.)
2. **Q2** Where does the backend run: your PC/home server, cloud VM, other? Where should TTS run (also G21)?
3. **Q3** What exactly counts as "authorized media" (own recordings, licensed, permission letters…) and what declaration text/legal wording do you want?
4. **Q4** Native Somali reviewers (and dialect focus)?
5. **Q5** Is checking Somali availability in the *official YouTube player's* caption menu acceptable as a manual test? (Replaces rev 1's question about scraping auto-translate, which is now out.)
6. **Q6** Where is the existing GitHub repo, and should the scaffold go there?
7. **Q7** Can package installs be enabled (new chat), or will tests run on your machine/CI?
8. **Q8** Confirm: authorized videos with no subtitles require user-supplied SRT/VTT (or embedded tracks) because ASR is out of scope.
9. **Q9** Which physical Android devices (model, Android version) will be used for G11/G15/G16/G18/G22 tests, and who runs them?
10. **Q10** Approve optional roadmap amendment **A5** (early Android dual-audio spike with generated test tones)?

## 8. Reconciliation (pass 1, 2026-11-20)
*Purpose:* reconcile Q1–Q7 and later questions with what the owner has actually written, without inventing approvals. Sources: **rev-2 brief** ("Product Vision Clarification and Architecture Amendments") and **rev-3 brief** ("Phase 0 Final Reconciliation (Rev 2)"). Quotes are paraphrased with section numbers.

### 8.1 ADR status register (authoritative)
| ADR | Topic | Status | Basis / what remains |
|---|---|---|---|
| 001 | No ASR, structurally | **DECIDED** | D-09 (owner: "No ASR/transcription of audio; captions only"). Mechanism (CI scan) PROPOSED. |
| 002 | Input priority (SRT/VTT feeds Mode B; no YouTube retrieval input in shipped builds) | **PROPOSED** | Consistent with D-03; phase assignment changed by ADR-023. |
| 003 | Caption providers research-only | **DECIDED** (policy) / **PROPOSED** (adapter choice) | D-03. First adapter `youtube-transcript-api` is my proposal; G14 clearance **BLOCKED** on policy review (G2 is folded into G14). |
| 004 | Stack and contracts | **DECIDED** (React+TS+Vite, FastAPI) / **PROPOSED** (monorepo layout, error vocabulary) | D-06. |
| 005 | Local-first topology | **PROPOSED** | D-08 prioritises local processing; D-12 presumes an Android-to-PC backend; topology not explicitly confirmed (Q2, Q13). Cloud-IP blocking (G3) is moot while G14 keeps retrieval disabled. |
| 006 | YouTube Mode = official player/controls only | **DECIDED** | D-02. Custom captions beside player remain **OPEN** (G13). |
| 007 | Translation abstraction, candidate model | **PROPOSED** | Model adoption **BLOCKED** until Q1, G6, G7. |
| 008 | TTS voice registry, no unverified voices | **PROPOSED** (registry) / **DECIDED** (no unverified model presented as working voice, D-09) | G17. |
| 009 | Storage/privacy/logging | **PROPOSED** | — |
| 010 | Security baseline | **PROPOSED** | — |
| 011 | POC disposition | **PROPOSED** | — |
| 012 | Phase process (stop and wait for approval) | **DECIDED** | Owner instruction in every brief. |
| 013 | Mode isolation by construction | **DECIDED** (intent: D-07 "must not share unsafe extraction functionality") / **PROPOSED** (lint/bundle mechanisms) | — |
| 014 | Dual-audio architecture | **PROPOSED**; final choice **BLOCKED** | On Phase 1b findings (D-05, D-11). |
| 015 | Master clock and sync policy | **PROPOSED** | Tolerances **OPEN** until measured and owner-approved. |
| 016 | Rights declaration | **DECIDED** (scope, D-17) / **OPEN** (wording, legal review) | Q3. |
| 017 | Fullscreen strategy | **PROPOSED** | Verify on device (AT-FS-*). |
| 018 | Media stays on device | **PROPOSED** | — |
| 019 | Captions in Mode B (no ASR consequence) | **PROPOSED** | Q8. |
| 020 | Backend connection security | **PROPOSED** | D-12 is DECIDED (never expose unauthenticated backend); mechanism and transport PROPOSED (Q11). |
| 021 | Dual-audio feasibility checkpoint | **DECIDED** (mandatory, D-11) / **PROPOSED** (details) | Q12 for pass rule. |
| 022 | Voice-preparation job model | **PROPOSED** | D-13 requires the UX states to be documented. |
| 023 | Phase re-sequencing | **DECIDED** (order, D-10) / **PROPOSED** (Phase 2/3 split) | — |
| 024 | Spike delivery over localhost | **PROPOSED** | Needs Q13 (adb/USB debugging availability). |
| 025 | *(pass 4)* Phone test delivery via a separate static harness over HTTPS | **PROPOSED** | D-27; needs explicit owner authorization to create/publish anything; details in §8.12. |
| 026 | *(pass 4)* Cache/storage budget default | **PROPOSED** | D-28; unapproved; Q14; details in §8.12. |

### 8.2 Owner-question register (Q1–Q14)
*Pass-4 pointer: statuses below are the pass-1 statuses and are preserved as history; the current statuses are in §8.9.*
| ID | Topic | Owner-provided information (cited) | Status | Blocks |
|---|---|---|---|---|
| Q1 | Personal/non-commercial vs commercial; model licences | Rev-2 §8: "Model licenses, commercial restrictions, memory usage, quality and latency must be verified before adoption." **Intent not stated.** | **OPEN** | Model adoption in Phases 4/5 (G5, G17). |
| Q2 | Where the backend (and TTS) runs | Rev-3 §5 speaks of "Android-to-PC/local backend"; rev-2 §8 "prioritize local processing", no paid hosting. **PC as host is implied, not confirmed; PC OS/specs unknown.** | **PROPOSED** (PC/local host) | Backend run docs (Phase 1); G21. |
| Q3 | What counts as authorized media; declaration | Rev-2 §1B: media the user owns or has permission to process, incl. local video/audio files and properly licensed media; "record user declaration of ownership/permission where appropriate". | **DECIDED** (scope) · **OPEN** (declaration wording, legal review) | G4 closure; Phase 2 UI text. |
| Q4 | Native Somali translation and TTS reviewers | Rev-3 §2 asks that reviewers be tracked; **none named.** | **OPEN** | G7 → quality claims in Phases 4, 5, 8; release. |
| Q5 | Manual check whether Somali appears in the official YouTube player's caption menu | None. | **OPEN** (low priority) | Nothing critical. |
| Q6 | Location of the existing repository / where scaffold goes | Rev-3 §Objective: "Preserve all existing project work" — implies a repo; **location not provided.** | **OPEN** | Start of Phase 1. |
| Q7 | Package installs / where tests run | None. Sandbox facts: installs disabled, no device. | **OPEN** (G8 **BLOCKED** in this sandbox) | Automated tests run here; Phase 1 verification. |
| Q8 | Authorized video with no subtitles ⇒ needs supplied/embedded subtitles | Follows from DECIDED no-ASR (D-09) and from rev-2 §1B "subtitle import/export" and "original captions … where supplied"; **owner has not explicitly confirmed the UX consequence.** | **PROPOSED** | G19; Phase 2/3 import UX. |
| Q9 | Android devices for physical testing | Rev-3 §4: "Start by testing on the owner's available Android device"; §2: **minimum two physical devices for release validation.** Model/Android version/who runs tests **not provided.** | **DECIDED** (≥2 devices for release; first device = owner's available one) · **OPEN** (nomination: model, Android version, browser) | Phase 1b execution; G11, G15, G16, G18, G22. |
| Q10 | Approve A5 early spike | Rev-3 §4: spike is a **mandatory checkpoint** before Phase 4/5 investment. | **DECIDED** (mandatory; now Phase 1b) | — |
| **Q11** | Android↔PC connection and secure pairing: confirm QR/one-time pairing + per-device tokens; choose transport (HTTPS with local certificate vs HTTP + signed requests + risk notice) | Rev-3 §5 lists LAN, QR/one-time pairing, authentication, unauthorized-access prevention, reconnection, offline, data, credentials; **no transport preference given.** | **PROPOSED** (ADR-020) | Phase 1 backend skeleton; G23. |
| **Q12** | Dual-audio checkpoint pass rule: what result lets Phase 4/5 start (proposal: ≥1 physical device, no blocking failure on AT-SP-01…14 subset, owner-approved tolerances; release still needs 2 devices) | Rev-3 §4: mandatory, start on owner's device, no multi-device claim until two tested. **Pass rule not stated.** | **OPEN** (rule) · **DECIDED** (mandatory) | Start of Phases 4/5; G24. |
| **Q13** | Deployment & network environment: PC OS; same Wi-Fi? router client isolation? USB debugging/adb available? firewall policy? any public HTTPS hosting wanted? | None. | **OPEN** | ADR-005, ADR-024, G23, G10. |
| **Q14** | TTS cache/storage budget and resume expectations (how much phone/PC storage may generated audio use; resume after app kill?) | Rev-3 §6 requires cached results, storage warning, resume "where supported". **No budget given.** | **OPEN** (low) | UX_REQUIREMENTS §9 thresholds; Phase 5/7. |

### 8.3 BLOCKED register
| # | Blocked item | Waiting for |
|---|---|---|
| B1 | Any automated test run in this sandbox (G8) | Installs enabled in a new chat, or tests run on the owner's machine (Q7). |
| B2 | All device-dependent evidence (G11, G12, G15, G16, G18, G22, AT-SP-*, AT-NET device tests) | Owner's Android device(s) and a person to run tests (Q9). |
| B3 | YouTube extras: custom captions (G13), caption retrieval (G14) | Written policy review by the owner. |
| B4 | ADR-014 final audio approach | Phase 1b findings (G24). |
| B5 | Model adoption (MT/TTS) | Q1, G6/G7/G17 evidence. |

### 8.4 Owner-directive log (what is DECIDED, with source)
| ID | Directive | Source |
|---|---|---|
| D-01 | Two media modes: YouTube Mode and Authorized Media Mode. | Rev-2 §1 |
| D-02 | YouTube Mode uses the official embedded player/API only and complies with current policies; no download, audio extraction, alternate audio, mixing, mute manipulation for dubbing, scraping, cookie collection, proxies, IP rotation, PO-token bypass or restriction evasion; no Somali TTS synchronized/mixed with YouTube playback without written authorization + compliance review. | Rev-2 §1A |
| D-03 | Unofficial transcript scraping is not a production default; unofficial caption retrieval is research-only and gated pending policy review; custom Somali captions on YouTube gated. | Rev-2 §1A |
| D-04 | Authorized Media Mode required features (in-app video, independent original and Somali audio, two 0–100 % volumes, mixing, mutes, caption toggles, fullscreen, play/pause, seek, speed, sync across pause/resume/seek/speed/fullscreen, translation editing, SRT/VTT import/export, Android controls). | Rev-2 §1B |
| D-05 | Dual-audio via a real mixing pipeline (Web Audio GainNode or another verified architecture); evaluate native Android Media3; do not assume track-selection APIs can play two tracks simultaneously; player timeline controls both video and TTS scheduler. | Rev-2 §2 |
| D-06 | Keep React+TypeScript+Vite and FastAPI unless investigation shows a compelling reason. | Rev-2 §4 |
| D-07 | Media abstractions (YouTubePlayerAdapter, AuthorizedMediaPlayer, SubtitleRenderer, TranslationPipeline, TTSAdapter, AudioMixer, AudioScheduler, MediaRights); YouTube and authorized pipelines must not share unsafe extraction functionality. | Rev-2 §4 |
| D-08 | Free-first: no paid APIs, subscriptions, credits, hidden paid fallbacks or paid hosting; no false promise of unlimited free cloud inference; prioritise local processing; measure device performance. | Rev-2 §8 |
| D-09 | Preserved constraints: no ASR; no invented results; no unverified model presented as a working voice; no YouTube scraping/bypass/extraction/alternate audio; clearly distinguish verified/unverified/implemented/tested. | Rev-2 §9; rev-3 |
| D-10 | Phase order: 0, 1, 1b, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 with titles per rev-3 §7; maintain dependencies and stop conditions. | Rev-3 §7 |
| D-11 | Dual-audio feasibility spike (Phase 1b) is a **required checkpoint before investing in Phase 4 and 5**; investigates independent GainNodes, 0–100 % controls, master gain, clipping/headroom, smooth transitions, sync with `currentTime`, pause/seek/repeated seek/speed/buffering, Bluetooth/headphones, backgrounding, scheduling/stale-audio cancellation; compares approaches and documents actual findings; start on owner's Android device; no multi-device claim before two physical devices; minimum two for release validation. | Rev-3 §2, §4 |
| D-12 | Dedicated security gate for Android↔PC/local backend connectivity; **do not expose an unauthenticated backend to the local network.** | Rev-3 §5 |
| D-13 | Document TTS-preparation UI states (preparing translation/voice, progress, cancel, retry, resume, cached results, storage warning, ready, error). | Rev-3 §6 |
| D-14 | Acceptance Tests Rev 2 are the source of truth; none marked PASS without execution and recorded environment; tolerances approved before pass/fail; every test NOT RUN until executed. | Rev-3 §3 |
| D-15 | Status vocabulary DECIDED / PROPOSED / OPEN / BLOCKED. | Rev-3 §2 |
| D-16 | Gates G11–G18 and the dual-audio acceptance criteria. | Rev-2 §6, §7 |
| D-17 | Authorized-media definition and recorded declaration (see Q3). | Rev-2 §1B, §4 |

### 8.5 Not decided by the owner (so not marked DECIDED anywhere)
*Pass-4 pointer: Q1, Q4 (interim), Q6, Q7, Q9 (first device) and part of Q3/Q8 are now answered — see §8.9. The list below is the pass-1 text, preserved; items still undecided after pass 4 are listed in §8.9 under "Still not decided".*
Commercial vs non-commercial intent (Q1) · backend host hardware and OS (Q2, Q13) · reviewers (Q4) · repository location (Q6) · installs/test environment (Q7) · device models (Q9) · transport security choice (Q11) · checkpoint pass rule (Q12) · storage budget (Q14) · declaration wording (Q3) · whether our own UI may call the YouTube player's documented `setVolume` (current stance, PROPOSED: no custom YouTube volume UI in v1; official controls only).

### 8.6 Re-verification log (reconciliation 2, 2026-11-21)
The facts added in pass 1 were re-read from their primary pages (fetch tool summaries) before this document is re-issued. Results: **F23** confirmed (`http://192.168.x.x` not a secure context; `localhost` is; service workers need a secure context) · **F24** confirmed (prompt for public-site requests to local addresses; Chrome 138 testing, launch stated for Chrome 142; secure-context restricted; **Android behavior not stated**) · **F25** confirmed (USB port forwarding to `localhost:<port>`; prerequisites: remote debugging, "Discover USB devices", "Enable port forwarding") · **F26** confirmed (exponential approach; 63.2 % per time constant, ≈95 % at 3×; **page does not mention clicks**, so click-avoidance stays an inference until AT-SP-04) · **F27** confirmed (`outputLatency` is an *estimate* of output-hardware latency e.g. Bluetooth; **no Android specifics**) · **F28** confirmed (BarcodeDetector experimental, not Baseline, secure-context only; Android Chrome support not stated). Nothing in F23–F28 was changed. All are still read via summarizing fetches; release-gating items must be re-read in primary text at review time.

### 8.7 Pass-2 note
Pass 2 found no change of any owner directive (D-01…D-17) and changed no status in §8.1/§8.2. Unresolved items that need an owner decision are listed in `CONSISTENCY_AUDIT.md` §4 (U-01…U-06).

## 8.8–8.12 Pass 4 — owner decisions applied (2026-11-22)
*Source of every directive below: the owner's "Phase 0 Owner Decisions Reconciliation (Pass 4)" brief, decisions 1–13. Nothing here is an inference; where the brief leaves a point open it is listed as OPEN or PROPOSED, never DECIDED.*

### 8.8 Owner-directive log, continued (D-18…D-30)
| ID | Directive (paraphrased from the brief) | Source |
|---|---|---|
| D-18 | **Commercial intent:** the app may be commercial. Review licences, model restrictions, voice licences and deployment terms accordingly. **Do not assume commercial use is permitted until verified.** | Pass-4 §1 |
| D-19 | **Media rights:** in Authorized Media mode the user must confirm ownership or authorization through an **explicit checkbox and confirmation before any processing** of the media. | Pass-4 §2 |
| D-20 | **Translation review:** initially the **owner** reviews Somali translation quality. Do not claim external reviewers have been nominated. | Pass-4 §3 |
| D-21 | **Repository:** `Soomaali211/TubeSomali`, branch `phase0-reconciliation`. | Pass-4 §4 |
| D-22 | **Build/test environment:** **Android phone + GitHub Actions CI** is selected. Not to be described as configured or verified until tested. | Pass-4 §5 |
| D-23 | **Subtitles:** translation only when supplied SRT/VTT or **supported** embedded subtitles exist. **No ASR, no transcription.** | Pass-4 §6 |
| D-24 | **Devices:** the owner's current Android phone for initial validation; a second device if available; models and Android versions to be recorded when known. | Pass-4 §7 |
| D-25 | **Transport:** no final choice. HTTPS is the preferred direction **for investigation** only. Document options, trade-offs, certificate/trust requirements, pairing security and fallback limits. **HTTP request signing does not encrypt subtitle text.** | Pass-4 §8 |
| D-26 | **G24:** the owner decides the acceptance policy after reviewing the completed test plan. Document balanced and strict options. G24 stays a blocking gate for Phases 4 and 5. | Pass-4 §9 |
| D-27 | **Phone test delivery:** recommend the simplest viable workflow; investigate a separate static harness deployed through GitHub Actions over HTTPS; main repo stays private; any public harness holds only isolated test code and synthetic fixtures. **No publishing or deployment without authorization.** | Pass-4 §10 |
| D-28 | **Storage budget:** the owner wants a recommended default; propose one; leave unapproved. | Pass-4 §11 |
| D-29 | **Phase split:** Phase 2 = media import and rights handling; Phase 3 = captions/subtitle pipeline. | Pass-4 §12 |
| D-30 | **Sequencing:** Phases 2 and 3 may proceed if Phase 1b is delayed; Phases 4 and 5 stay blocked until G24 passes **with owner approval**. | Pass-4 §13 |

### 8.9 Status overlay after pass 4 (authoritative over §8.1–§8.3 where they differ)
| ID | Topic | Pass-4 status | Basis and what remains |
|---|---|---|---|
| Q1 | Commercial vs non-commercial | **DECIDED** (intent: may be commercial; D-18) · **NOT VERIFIED** (licence/terms eligibility of every model, voice, host and API) | Consequences in §8.10. G5 stays OPEN. |
| Q2 | Where the backend/TTS runs | **PROPOSED** (PC/local host) — **now in tension** with D-22, which names a phone and CI but **no PC** | Tracked as Q16. |
| Q3 | Authorized media definition and declaration | **DECIDED** (scope D-17; mechanism D-19: explicit checkbox **and** confirmation before processing) · **OPEN** (exact Somali wording; legal review) | G4, G20. Tests AT-IN-31…33 (new). |
| Q4 | Reviewers | **DECIDED** (interim: owner reviews Somali **translation** quality; D-20) · **OPEN** (external reviewers: none nominated; who reviews **TTS** naturalness was not stated; G12 needs a native-reviewer rating) | G7 stays OPEN. No claim of independent review may be made. |
| Q5 | Official-player caption-menu check | **OPEN** (unchanged) | — |
| Q6 | Repository | **DECIDED** (D-21). Before the first Phase 0 commit the repository existed but was empty (observed on clone: no branches, no files). Branch convention for Phase 1 and later: **OPEN** | — |
| Q7 | Where tests run | **DECIDED** (selection: Android phone + GitHub Actions CI; D-22) · **NOT VERIFIED** (no workflow exists; nothing has run). **G8 stays BLOCKED** until a workflow exists and has run; the CI runner cannot execute device tests (see ARCHITECTURE §14). | Phase 1 W9/W10. |
| Q8 | No-subtitle videos | **DECIDED** (D-23) · **OPEN**: which embedded subtitle formats count as "supported", and whether the browser can read them without a backend (Q15) | G19 owner-confirmed; evidence pending (Phases 2/3). |
| Q9 | Android devices | **DECIDED** (first device = owner's current phone; second "if available"; D-24; earlier owner rule D-11: minimum two physical devices for **release validation** — not weakened, see audit U-07) · **OPEN** (model, Android version, browser, who runs tests) | Phase 1b execution. |
| Q10 | Early spike | **DECIDED** (mandatory Phase 1b) — unchanged | — |
| Q11 | Transport security | **PROPOSED** (HTTPS = preferred direction **to investigate**; not approved; D-25). Options and trade-offs: ARCHITECTURE §11a | G23 cannot pass without a recorded decision. |
| Q12 | G24 acceptance policy | **OPEN** (owner decides after reviewing the completed plan; D-26). Balanced and strict options: DUAL_AUDIO_SPIKE_PLAN §10. Mandatory-checkpoint status **DECIDED** | G24 blocks Phases 4/5. |
| Q13 | Deployment and network environment | **OPEN**. D-22 does not mention a PC, router, or LAN — see Q16 | ADR-005, ADR-020, G10, G23. |
| Q14 | Cache/storage budget | **PROPOSED** (default recommended in ADR-026; not approved; D-28) | UX §9 thresholds. |
| **Q15** *(new)* | Which embedded subtitle formats/tracks are "supported" (e.g., text tracks in MP4/MKV/WebM) and where they are extracted (browser vs backend) | **OPEN** | G19; Phase 3 investigation. **NOT VERIFIED** that a browser can read embedded tracks. |
| **Q16** *(new)* | Is there a PC or other always-on machine that can host the backend (and later TTS/translation models)? If not, how do Phases 4/5 run on a phone-only setup? | **OPEN** | ADR-005, ADR-020, G21, G23; Phases 1 (W10), 4, 5. |
| ADR-016 | Rights declaration | **DECIDED** (scope + checkbox/confirmation before processing) · wording **OPEN** | — |
| ADR-019 | Captions in Mode B | **DECIDED** (translation only from supplied/embedded subtitles; no ASR) · embedded support **OPEN** (Q15) | — |
| ADR-020 | Backend connection security | **PROPOSED** — transport still **not decided**; "never an unauthenticated LAN backend" stays DECIDED (D-12) | — |
| ADR-021 | Checkpoint | **DECIDED** (mandatory) · acceptance policy **OPEN** (Q12) | — |
| ADR-023 | Phase sequencing | **DECIDED** (order D-10; Phase 2/3 split D-29; relaxed sequencing D-30). Former "PROPOSED" wording in §8.1 is superseded | — |
| ADR-024 | Spike delivery over localhost | **PROPOSED** (needs a PC with USB debugging; see ADR-025 for the phone-only route) | — |
| ADR-025 *(new)* | Phone test delivery via a separate static harness | **PROPOSED** (§8.12) | Needs explicit owner authorization to create/publish anything. |
| ADR-026 *(new)* | Storage budget default | **PROPOSED** (§8.12), unapproved | — |
**BLOCKED after pass 4 (additions to §8.3):** B1 is restated: the **selected** environment (phone + Actions) is **not configured** — blocked on a workflow file existing and on a first CI run (Phase 1, W9). B2 is restated: device evidence waits for device details (Q9) and a person to run tests. B6 *(new)*: Phase 4/5 start waits for **G24 passed with owner approval**. B5 is restated: commercial intent (D-18) means NC-licensed models cannot be adopted for a commercial product without separate permission.
**Still not decided (after pass 4):** transport choice (Q11) · G24 acceptance policy (Q12) · storage budget approval (Q14) · declaration wording (Q3) · external reviewers and TTS reviewer (Q4) · device models/versions (Q9) · supported embedded subtitle formats (Q15) · backend host (Q2/Q13/Q16) · branch/commit workflow after Phase 0 (Q6) · approval to create or publish any test harness (ADR-025) · gate numbering G19–G24 (audit U-05).

### 8.10 Commercial-intent consequences (D-18) — all **NOT VERIFIED** for commercial use
| Item | What is verified (from §2) | Consequence |
|---|---|---|
| `Helsinki-NLP/opus-mt-en-cus` | Apache-2.0 on its model card (F10) | Licence text permits commercial use in principle; **quality (16.0 BLEU / 0.173 chrF, English→Somali only) and training-data terms are not verified** for a commercial product. |
| NLLB-200-distilled-600M | CC-BY-NC 4.0 (F11) | **Non-commercial.** Cannot be adopted for a commercial product without separate permission. |
| `facebook/mms-tts-som` | CC-BY-NC 4.0 via a mirror (TTS table) | **Non-commercial.** Same consequence; original-model licence also to be re-read. |
| `somali_tts_model`, `StyleTTS2-Somali` | No licence stated | **Cannot be assumed usable** commercially (or at all) — no licence means no granted rights. |
| `Hussein_tts`, `omi-tts` | Unverified [U] | Not usable until verified. |
| Result | **No Somali TTS candidate has a verified commercially usable licence** (G5, G17). | Phase 5 may end with *no adoptable voice*; options for the owner then are: obtain permission, commission/own-train a voice with documented speaker consent, or release non-commercially. **None of these is chosen.** |
| YouTube API Services | Policy facts F1–F6 concern mode restrictions | Whether a commercial/monetized app has extra YouTube API terms obligations is **NOT VERIFIED** — re-read at Phase 8. |
| Hosting | GitHub Pages is not allowed as a free host for a commercial SaaS (F30); other free tiers' terms **not read** | Free hosting for a *commercial* product is **NOT VERIFIED**; the Pages harness (ADR-025) is a test page only. Phase 9 (G10) re-reads terms. |
| Dependencies | Not yet enumerated | Phase 1 W1 licence check must flag copyleft/NC terms for commercial distribution. |

### 8.11 Pass-4 facts (re-read this session, via summarizing fetch tools)
| # | Fact | Source |
|---|---|---|
| F29 **[V]** | GitHub Pages: **GitHub Free and Free-for-organizations can publish only from public repositories**; Pro, Team, Enterprise can publish from private ones. Published sites ≤ 1 GB; deployments time out after 10 min; soft 100 GB/month bandwidth; soft 10 builds/hour (not for sites published by a custom GitHub Actions workflow). Whether the owner's account is on Free or a paid plan is **not known**. | https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/what-is-github-pages · https://docs.github.com/pages/getting-started-with-github-pages/github-pages-limits |
| F30 **[V]** | GitHub Pages "is not intended for or allowed to be used as a free web-hosting service" for an online business, e-commerce or commercial SaaS; sites must not handle sensitive transactions. The pages read did not state whether HTTPS is enforced (the "Secure site with HTTPS" article was **not** read) — so "Pages serves HTTPS" is **[U]** here. | same page |

### 8.12 New ADRs (pass 4)
**ADR-025 Phone test delivery via a separate static harness — PROPOSED (D-27).** *Recommendation (simplest viable for a phone + GitHub Actions workflow):* a **separate, public repository** (proposed name `tubesomali-spike-harness`; not created) containing only a static test page, a fixture-generation script and **synthetic fixtures** (generated tones, test patterns — no third-party or user media), plus a GitHub Actions workflow that publishes it to GitHub Pages; the phone opens the HTTPS URL in Chrome (secure context, F23), runs the AT-SP procedures, shows results on screen and lets the tester **copy/export a JSON record** to send back. The main `TubeSomali` repository stays **private** (D-27); a public harness is needed because Pages from a private repo is not available on the Free plan (F29, plan of the owner's account unknown). *Rules:* no application secrets, no user media, no backend, no shared code from the private repo except what the owner approves case by case; harness code is disposable. *Alternatives:* (a) USB port forwarding (ADR-024) — needs a PC and adb; (b) static LAN server — needs a PC; (c) another free static host — terms **not read**; (d) opening files from the phone's storage via `file://` — origin/secure-context behaviour **[U]**, fragile. *Open points:* HTTPS on Pages is **[U]** (F30); whether CI can generate fixtures (e.g., needs ffmpeg on the runner **[U]**) or small generated fixtures are committed; T2 (output recording) capture with a single phone is limited — see DUAL_AUDIO_SPIKE_PLAN §6/§11. **Nothing has been created, published or deployed; creating the repo, enabling Pages and publishing each need the owner's explicit authorization.**

**ADR-026 Cache/storage budget default — PROPOSED (D-28), unapproved.** *Arithmetic (not measured):* uncompressed mono 16-bit speech audio is 32 kB/s at 16 kHz and 48 kB/s at 24 kHz, i.e. ≈ 115 MB and ≈ 173 MB per hour of audio; compressed storage (if an encoder is available in the browser **[U]**) would be an order of magnitude smaller; translation text is kilobytes. Model weights are separate (measured in Phases 4/5). *Proposed default:* **500 MB** phone cache cap for generated Somali voice tracks (≈ 2–4 hours of uncompressed audio), user-adjustable presets **250 MB / 500 MB / 1 GB / 2 GB**; **warn** when an estimated job exceeds the remaining budget or when free device storage after the job would be below max(1 GB, 2× the job); evict only with user consent (offer "delete the oldest unused voice tracks"); never evict the item being played or any item the user marked *keep*; the user's source video is not counted (it stays where the user keeps it, ADR-018). If a PC backend exists, give it a separate cache cap (proposal: 5 GB excluding model weights). *Trade-offs:* a larger cap means fewer regenerations (less CPU/battery) but uses scarce phone storage; a smaller cap increases regeneration. Real sizes, free-space APIs and eviction behaviour on the owner's phone are to be **measured** in Phases 5/9 (G18). **Owner confirmation required (Q14).**

## Appendix A — Audit of the existing caption POC (read, not run)
*(Finding labels renamed `A1–A12` → `P1–P12` in reconciliation pass 1 to avoid colliding with roadmap amendments `A1–A6`; wording unchanged.)*

| # | Finding | Severity |
|---|---|---|
| P1 | `HttpUrl` accepts any http(s) URL passed to `yt-dlp` (many extractors + generic) → arbitrary-fetch/SSRF primitive. Replace with video-ID extraction + canonical rebuild. | **High** |
| P2 | No `--` terminator before URL. | Low |
| P3 | `--write-subs --write-auto-subs` share a filename template; manual/auto provenance lost; precedence unverified. | High |
| P4 | `--list-subs` returned as raw text; "listing_returned" isn't an availability decision. | Med |
| P5 | Raw VTT only; no timestamp normalization/dedupe of rolling auto-captions. | Med |
| P6 | All failures → `RuntimeError`→502 with up to 1,500 chars of raw stderr (info leak, no taxonomy). | High |
| P7 | `paths[0]` arbitrary file pick. | Low |
| P8 | Single language code, no fallback/variants/track selection. | Med |
| P9 | Blocking subprocess, 90 s, no concurrency cap/cancel/rate limit. | Med |
| P10 | Unpinned `>=` requirements. | Low |
| P11 | No automated tests; never run on a real link. | Info |
| P12 | Positives: no media-download flags, no ASR, tempdir cleanup, arg-list subprocess. | — |
Disposition: moves to `backend/research/`, off in release (ADR-003, ADR-011).

## Appendix B — Kooban Soomaali ah
- Muuqaalka: **YouTube** = ciyaaryahanka rasmiga ah oo keliya; ma jiro codka Soomaaliga, ma jiro qoraal lagu dul dhigo ciyaaryahanka (F12), helista qoraalka waa lagu xiray (G14).
- **Warbaahin la oggol yahay** = halkan ayaa ka shaqaynaya dhammaan: muuqaal, cod asal ah + cod Soomaali ah oo laba xakame leh (0–100%), qoraal, shaashad buuxda, xawaare.
- Qoraalka la'aanta: ASR ma jiro, sidaa darteed muuqaalka waa in uu leeyahay SRT/VTT (Q8).
- Khatarta ugu weyn: isku-xiga codadka oo Android ah — waxaan soo jeedinayaa tijaabo hore (A5, Q10).
- Waxaan u baahanahay jawaabaha Q1–Q10 kahor Phase 1.

*(Qoraalka sare waa nooca rev-2 oo la ilaaliyey; waxaa beddelaya kooban cusub oo hoose — reconciliation 2, 2026-11-21.)*
**Kooban cusub (reconciliation 2):**
- Tijaabada codka labada xakame (Phase 1b) hadda waa **qasab** ka hor Phase 4 iyo 5 (D-11, G24); waxaa lagu bilaabayaa taleefanka Android ee aad hadda haysato; lama sheegayo xaqiijin badan-aaladeed ilaa **laba taleefan oo jidheed** la tijaabiyo.
- Isku-xirka Android↔PC: **ma jiri doono backend aan lahayn xaqiijin** oo ku furan shabakadda (G23, D-12); isku-xirid QR/koodh hal-mar ah iyo token qalab walba leh.
- Su'aalaha furan ee ugu muhiimsan: **Q6** (halka repo-gu yahay), **Q7** (installs/tijaabo), **Q9** (magacaabista taleefannada), **Q11** (ammaanka gudbinta), **Q13** (shabakadda/PC), iyo **Q1** (ganacsi mise ma ahan).
- Wax tijaabo ah lama fulin: **152 tijaabo oo la qeexay, 0 la socodsiiyey**.

### Appendix B-3 — Kooban Soomaali ah (Pass 4, 2026-11-22; ku dar, midka hore lama tirin)
- Go'aamada 13-ka ah ee milkiilaha waa la dhaqan geliyay dukumentiyada (D-18…D-30). Wax koodh ah lama qorin, wax imtixaan ah lama fuliyey: **160 tijaabo oo la qeexay, dhammaantood NOT RUN**.
- **DECIDED:** ujeeddada ganacsi waa suurtagal (laakiin ruqsadaha moodooyinka lama xaqiijin); sanduuq xaqiijin + xaqiijin cad ka hor marka warbaahinta la shaqeeyo; milkiilaha ayaa dib u eegaya tarjumaadda Soomaaliga (hadda); repo-ga `Soomaali211/TubeSomali`; taleefanka Android + GitHub Actions (lama dhisin weli); tarjumaad kaliya marka SRT/VTT la bixiyo; Wareegga 2 = soo dejinta warbaahinta, Wareegga 3 = captions; Wareegyada 2–3 way socon karaan haddii 1b dib dhaco.
- **PROPOSED / OPEN:** habka ammaanka isku-xirka (HTTPS = hage lagu baaro kaliya); xeerka G24 (Balanced vs Strict) — milkiilaha ayaa go'aamin doona; miisaaniyadda kaydinta (500 MB oo la soo jeediyey); goobta tijaabada taleefanka (ADR-025); weydiimaha cusub Q15 (qaabka subtitles-ka la taageeray) iyo Q16 (ma jiraa PC?).
- G24 weli waxay xannibaysaa Wareegyada 4 iyo 5 ilaa ay ku gudbaan oggolaanshaha milkiilaha.
