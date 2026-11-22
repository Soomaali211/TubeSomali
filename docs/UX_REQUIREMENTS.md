# TubeSomali — UX Requirements

**Revision 2 · reconciliation pass 1 · 2026-11-20 · DRAFT.** *Reconciliation 1 is additive:* screens 12–13 in §1, new §9 (voice-preparation states) and §10 (backend pairing and connection status). Nothing removed. Design principle: **the player is the product.** Screens are organized around watching a video, not around a form or text-translator layout. Somali strings below are *draft working labels* that need native-speaker review before use.

## 1. Screen inventory
1. **Home** — two clear mode cards (*YouTube* / *Warbaahin la oggol yahay* [draft: "Authorized media"]); YouTube link field; "Import file" button; recent items. No translation form on this screen.
2. **Rights declaration** (first import, per item) — short Somali text, explicit checkbox + confirm; link to terms.
3. **Import & prepare** (Mode B) — shows file, detected subtitle source (supplied SRT/VTT / embedded / none), language, status of translation and voice generation with progress + cancel.
4. **Player (portrait)** — video on top (16:9), controls under it, subtitle area handled per mode, bottom sheet for settings.
5. **Player (landscape / expanded)** — video fills screen; controls auto-hide; captions and audio panel remain available.
6. **Audio settings panel** — opens during playback without stopping it (bottom sheet in portrait, side sheet in landscape).
7. **Subtitle settings** — language, font size, background/contrast.
8. **Caption/translation editor** — separate screen reached from the player; list of cues with timestamps; edit Somali; re-translate selected; restore original.
9. **Library** — the user's authorized files (metadata + declaration + generated assets), delete/export.
10. **Settings** — language, low-data mode, model cache, privacy, licences, version.
11. **Error/empty/loading states** for each of the above.
12. **Pair with PC (backend)** *(added)* — shows how to pair (scan QR with the phone camera / type a code), current connection state, paired-device name, "forget this PC" (§10).
13. **Prepare Somali voice** *(added)* — the preparation screen/sheet described in §9; reachable from Import & prepare and from the player.

## 2. Player controls — Mode B (Authorized Media)
| Control | Requirement |
|---|---|
| Play/pause | Single large target; pauses video **and** Somali voice **and** original audio together. |
| Seek bar | Shows buffered/position; dragging scrubs; on release audio resynchronizes; no stale Somali audio after seek. |
| Playback speed | Discrete options (set from measured behavior; candidate 0.75×/1×/1.25×/1.5×, to be confirmed in Phase 6). Both audio channels follow. |
| **Original volume** | Slider 0–100 %, own mute toggle, independent of Somali slider. |
| **Somali volume** | Slider 0–100 %, own mute toggle, independent of original slider. |
| Somali captions | CC toggle; takes effect immediately; state preserved across fullscreen. |
| Original captions | Second toggle, shown only when original subtitles were supplied. |
| Fullscreen | Enters/exits without interrupting playback; captions and audio settings still available. |
| Audio settings | Opens as a panel while playing; shows both sliders, mute toggles, "reset to 100/100"; shows warning if Somali voice is still being prepared. |

Volume sliders must show the numeric percentage, be operable by touch (≥48 dp target), keyboard (arrow keys, Home/End) and screen reader (role=slider, value text "Codka asalka: 30 boqolkiiba" [draft]).

## 3. Player controls — Mode A (YouTube)
- Official player with its **own** controls; we add **no** controls over it and nothing in front of any part of it **[V F12]**.
- Our UI sits **outside** the player rectangle (title, notes, library actions).
- No audio controls of ours; no "Somali voice" control is rendered. A visible, explained note: *"Codka Soomaaliga looma isticmaali karo muuqaalada YouTube"* [draft] so users understand why.
- Somali captions: only via the official player's own menu. If G13 clears, a captions panel *beside/below* the player (never overlapping) may be added.

## 4. Subtitle display (Mode B)
- Rendered by our `SubtitleRenderer` inside the video container.
- Options: font size (≥ 4 steps), text colour, background (none / semi-opaque / solid), edge/outline, position (bottom default, raise when controls visible).
- Contrast: default combination must meet WCAG AA contrast against its background (checked in tests with computed colours).
- Long Somali lines wrap to max two lines where possible; overflow handled without covering controls.
- Fullscreen: the **container** (video + captions + controls) goes fullscreen, not the bare video element, so custom captions and the audio panel survive **[design intent; Android behavior [U]; iPhone non-video fullscreen unreliable [V F21]]**.

## 5. Layout and responsiveness
- Mobile-first: designed at 360 × 640 dp, verified at 360, 412, 768 widths and landscape.
- Safe areas / display cutouts respected; no horizontal scrolling.
- One-hand reach: primary controls in the lower half; settings as bottom sheets.
- Low-data mode: avoid auto-downloading models/assets; show sizes before downloads.

## 6. Accessibility
Keyboard operability for every control; visible focus; labels in Somali; live-region announcements for state changes (voice ready, error); reduced-motion support; scalable text; contrast; touch targets ≥ 48 dp; captions are themselves an accessibility feature and must not be the only way to find state.

## 7. Feedback and state rules
- Somali voice not ready → player is playable with original audio; Somali slider disabled **with an explanation**, not silently inert.
- Any control that is disabled explains why (e.g., YouTube mode, model not installed, licence restriction).
- Non-commercial models display their licence notice where the voice is chosen.
- Errors use the fixed error vocabulary (DECISIONS ADR-004) mapped to plain Somali messages; never show raw stack traces or tool output.

## 8. Voice selection
Only voices that are installed, passed QA, and have a complete registry entry (G17) are listed. Each shows its licence tag. No invented voice names or personas.

## 9. Voice-preparation states *(added in reconciliation 1; D-13, ADR-022; tests AT-PR-01…10)*
All Somali strings are **draft working labels needing native review.** Progress is shown only where it is measurable; no time-remaining estimate before enough cues have been measured.

| State | What the user sees | Actions | Notes |
|---|---|---|---|
| **Idle / not prepared** | "Codka Soomaaliga weli lama diyaarin" [draft] + estimate of storage needed (marked *estimate*) | Prepare, choose voice | Disabled if no backend/voice available, with the reason. |
| **Storage warning** | Warning when estimated size exceeds free space or the user's budget (Q14) | Continue anyway · Free space · Cancel | Never silently proceeds past a failed space check. |
| **Preparing translation** | Stage label + determinate bar by cues done/total | Cancel | Skipped if translated text already exists. |
| **Preparing Somali voice** | Stage label + determinate bar by cues done/total (and seconds generated when known); current cue index | Cancel; "play with original audio meanwhile" | Playback of original audio stays available; Somali slider disabled with explanation. |
| **Paused / interrupted** | Reason (connection lost · app backgrounded · storage full · PC went to sleep) | Resume · Cancel | "Resume" continues from cached cues; if resume is **not** supported for the reason, say so plainly. |
| **Cancelled** | What was kept (finished cues) and its size | Resume later · Discard cached · Keep | — |
| **Failed (partial)** | Count of failed cues and error category in plain Somali (fixed vocabulary); finished cues kept | Retry failed cues · Retry all · Edit text of failed cue · Cancel | Never shows raw stack traces or tool output. |
| **Cached / ready from cache** | "Diyaar ka ahaa kaydka" [draft]: cached size and date | Use · Regenerate · Delete cache | Cache key: text + voice + revision + parameters, so changed text invalidates only the changed cues. |
| **Ready to play** | Ready indicator; Somali slider enabled | Play · Audio settings | Announced via live region. |
| **Error (blocking)** | Explanation + what can be done (e.g., re-pair, free space, check PC) | Retry · Details (non-sensitive) · Help | Maps to the error vocabulary in DECISIONS ADR-004. |

Accessibility: every state change is announced; progress bars have accessible names and values; cancel/retry reachable by keyboard and screen reader; touch targets ≥ 48 dp.

## 10. Backend pairing and connection status *(added in reconciliation 1; G23, ADR-020; tests AT-NET-*)*
- **Pairing screen:** explains in plain Somali that the PC shows a QR code; instructs to scan it with the phone's camera app (which opens the app); offers a manual code entry fallback; shows success with the PC's name; failed/expired code gives a clear message and a way to request a new code. No raw tokens or secrets are ever displayed.
- **Connection indicator** (always visible in Settings, and as a small badge on screens that need the PC): *Not paired · Connecting · Connected · Reconnecting · PC unreachable · Access revoked (pair again)*. Colour is never the only signal (icon + text).
- **Reconnection:** automatic with backoff; "Try now" button; after repeated failure, show likely causes (PC asleep, different Wi-Fi, LAN mode off) without jargon.
- **Offline:** Library, player, captions and already-prepared voice work with no PC; actions needing the PC are disabled with an explanation (not hidden).
- **Forget this PC / unpair:** removes the stored credential on the phone and tells the user how to revoke it on the PC.
- **Privacy note shown at pairing:** "Qoraalka oo keliya ayaa loo diraa kombuyuutarka; muuqaalka ma baxo taleefanka" [draft; *only the text is sent to the computer; the video never leaves the phone*].
