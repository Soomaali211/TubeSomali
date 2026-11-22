# TubeSomali — Product Specification

**Revision 2 · reconciliation pass 1 · 2026-11-20 · DRAFT for owner approval.** Supersedes the "caption tool" framing in rev 1. *Reconciliation 1 is additive:* §4.5 (voice preparation), §4.6 (backend connection model), §10 (status of requirements), gate list in §2 extended to G24; nothing removed. Evidence labels as in `DECISIONS.md`: **[V]** verified, **[U]** unverified, **[T]** tested (none yet).

## 1. Vision
TubeSomali is a **mobile-first video viewing app with Somali translation**: an in-app player where, for media the user is authorized to process, the viewer hears the original audio and/or a Somali voice, each with its own volume, with Somali captions on demand. It is **not** a subtitle-upload form or text translator; subtitles are a supporting feature of the player.

## 2. Two modes, hard-separated
| | **A. YouTube Mode** | **B. Authorized Media Mode** |
|---|---|---|
| Source | YouTube link | Local video/audio file or properly licensed media the user holds |
| Player | Official YouTube embed/IFrame API only | In-app `AuthorizedMediaPlayer` (own HTML media element) |
| Audio | YouTube's own, untouched | Original + Somali voice, independent gains, mixed |
| Captions | Official player's own CC/language features only. Custom Somali captions **gated** (G13) | Our `SubtitleRenderer`: Somali + original (if supplied) |
| Translation / TTS | Not applied to YouTube playback | Yes |
| Rights | Governed by YouTube terms/policies | User declaration recorded (G4, G20) |
| Gates | G1, G13, G14 (+ G23 if a backend is used) | G4–G7, G11, G12, G15–G24 |

Modes share no extraction, audio, or TTS code (ADR-013).

## 3. Mode A — YouTube
**Allowed / planned (subject to current policy re-check before release):**
- Official embedded player with its normal controls, ads, links, metadata; player at least 200×200 px, ≥480×270 recommended **[V F13]**.
- Play/pause, seek, volume, fullscreen, captions/language choices **through the official player UI**.
- Page-level features that do not touch the player: link input, history of links, notes.

**Gated (not built by default):**
- Custom Somali captions: **G13**. Verified constraint: no overlays/frames/elements in front of any part of the embedded player **[V F12]**; the API's documented caption options are only `fontSize` and `reload` **[V F15]** — there is no documented way to feed our own text to the official captions. Any custom display would therefore have to sit *outside* the player's rectangle, and even that needs written review.
- Retrieval of caption text from YouTube: **G14**. Retrieval via unofficial libraries stays **research-only** and disabled in every shipped build.
- User-supplied SRT/VTT used with a YouTube video: investigated only as part of G13; not assumed allowed.

**Prohibited (G1, permanent unless written YouTube authorization):** media download, audio extraction, alternate/replacement audio, mixing, mute-for-dubbing, Somali TTS synchronized or mixed with YouTube playback, scraping, cookie collection, proxies, IP rotation, PO-token bypass, restriction evasion.

**Compliant-by-design Somali route to evaluate:** the official player's own caption/auto-translate menu may offer Somali on some videos **[U — to be checked by hand in the player, not by code]**. If it does, the user gets Somali captions with zero custom code.

## 4. Mode B — Authorized Media
### 4.1 Required features (from owner brief)
1. Video plays inside TubeSomali.
2. Original audio independently controllable; Somali voice independently controllable.
3. Two real volume controls, each 0–100 %.
4. Channels can be mixed; original muted with Somali audible; Somali muted with original audible.
5. Somali captions open/close; original captions where supplied.
6. Fullscreen/expanded video; play/pause; progress/seek; playback speed.
7. Timing synchronization of the translated speech, including across pause, resume, seek, speed change, fullscreen enter/exit.
8. Translation editing; subtitle import/export (SRT/VTT).
9. Android-friendly controls; media library for the user's authorized files.

### 4.2 Source text: captions only (no ASR) — consequence
Authorized media with no subtitles cannot be auto-captioned (no ASR, by rule). The user must supply **SRT/VTT**, or the file must contain **embedded subtitle tracks** (extraction by a container tool is not speech recognition; feasibility **[U]**). A video with neither can still be played but cannot be translated (**G19**, Q8).

### 4.3 Video stays on the device
The video file is played from a local object URL; **it is not uploaded**. Only subtitle text (and requested TTS text) goes to the backend, and only if the backend is used for translation/TTS. Privacy-positive and avoids server storage of media. (ADR-018)

### 4.4 Rights/authorization flow (G4, G20)
- Before first import, show a plain-Somali declaration: the user owns the media or has permission to process it, including translating and voicing it.
- Store the declaration locally (timestamp, file name, hash), per item, with the ability to delete.
- No "paste a URL → fetch media" path exists anywhere in Mode B.
- Honest limit: a declaration records what the user says; it cannot technically prove rights, and users could import a copy of third-party content. The app's terms text must say that this is prohibited and that the user is responsible. *This is product design, not legal advice; legal review is a Phase 8 deliverable.*

### 4.5 Somali voice preparation (user-visible behavior; D-13, ADR-022)
Before the Somali voice can be heard, the app **prepares** it: translation (if not already done) then voice synthesis. The user always sees which stage is running, can cancel, can retry failures, and can resume after an interruption where possible; finished work is cached so re-opening the same item does not redo it. States (details in UX_REQUIREMENTS §9): *idle · preparing translation · preparing Somali voice (with progress when measurable) · paused/interrupted · cancelled · failed (with explanation) · ready to play*. A storage estimate/warning is shown before generation. While preparing, the video remains playable with its original audio; the Somali slider is disabled with an explanation. Measured storage and speed numbers are shown only after they have been measured (G18, G21).

### 4.6 Backend connection model (user-visible behavior; D-12, ADR-020)
Translation and voice generation run on the owner's PC/local backend (Q2, PROPOSED). The phone must be **paired** with it once (scan a QR with the phone camera, or type a code), after which the phone is remembered until the user unpairs it or the PC revokes it. The backend is not reachable from the network without pairing. The app shows the connection state (connected, reconnecting, unreachable, unauthorized), keeps working offline for everything that is already on the phone, and says clearly what needs the PC. Only text (subtitles, synthesis requests) is sent; the video never leaves the phone. Transport protection is an open decision (Q11); until it is decided, no claim of "secure" is made beyond what ARCHITECTURE §11 states.

## 5. Non-goals
Auto-transcription; YouTube downloading; Somali dubbing of YouTube; voice cloning of real people without documented consent; paid-API dependency; iOS-specific polish (iPhone fullscreen for non-video elements is unreliable **[V F21]**; Android + Chromium browsers are the target); cloud-scale hosting promises.

## 6. Languages
UI primarily Somali (strings in a locale file; copy needs native review). Translation direction in the first model candidate is **English → Somali only [V F10]**; non-English sources require a pivot or are rejected with a clear message (ADR-007).

## 7. Free-first and local-first
No required paid API/subscription/credits/hosting; no automatic fallback to paid services. Prefer local processing; measure before promising anything (G18, G10, G21). Optional free-tier services (if ever added) are off by default with quota warnings.

## 8. Success definition
"Works" means the acceptance tests in `ACCEPTANCE_TESTS.md` passed in the recorded environment, on real Android devices for audio/player behavior. Nothing is called working before that.

## 9. Constraints preserved from the original handoff
No ASR/Whisper; no invented results/voices/APIs; no unverified model presented as a voice; no secrets in repo; no large weights in Git; IndexedDB-local history by default; no transcript text in logs; accessibility and low-data mode; Somali UI; staged delivery with STOP after each phase.

## 10. Requirement status (reconciliation 1) — nothing here is implemented or tested
| Requirement area | Written spec | Implemented | Tested | Gate(s) |
|---|---|---|---|---|
| Two modes, isolation | ✔ | ✘ | ✘ | G1, ADR-013 |
| YouTube official player only | ✔ | ✘ | ✘ | G13, G14 |
| Authorized media player, rights flow | ✔ | ✘ | ✘ | G4, G20 |
| Dual audio + two 0–100 % controls | ✔ | ✘ | ✘ | G11, G15, G24 |
| TTS sync across pause/seek/speed/fullscreen | ✔ | ✘ | ✘ | G12, G16 |
| Captions (Somali/original), settings, fullscreen | ✔ | ✘ | ✘ | G16 |
| Translation + editing | ✔ | ✘ | ✘ | G6, G7 |
| Somali TTS voices | ✔ | ✘ | ✘ | G5, G17, G21 |
| Voice-preparation states | ✔ | ✘ | ✘ | AT-PR-* |
| Backend pairing/auth | ✔ | ✘ | ✘ | G23 |
| Performance/resource limits | ✔ | ✘ | ✘ | G18 |
