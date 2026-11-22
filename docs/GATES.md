# TubeSomali — Gate Register

**Revision 2 · reconciliation pass 1 · 2026-11-20** · Single source of truth for blockers and release gates. Updated at the end of every phase.
G1–G10 come from Phase 0 rev 1. **G11–G18 are the owner's (rev 2 brief).** **G19–G22 are added by the architect** and need approval. **G23 (backend connection security) was requested by the owner in the Final Reconciliation brief; G24 (dual-audio feasibility checkpoint) formalises the owner's "mandatory checkpoint"** — gate numbers 23–24 are the architect's labelling and need approval.

Status vocabulary: **OPEN** (unresolved) · **BLOCKED** (cannot progress or produce evidence until a named external prerequisite exists) · **CLOSED-BY-DESIGN** (feature will not be built) · **PASSED** (evidence attached) · **FAILED** (evidence attached).
At the end of Phase 0 nothing has been tested, so **no gate is PASSED**.

### Revision history
| Date | Change | Reason |
|---|---|---|
| 2026-11-20 rev 2 | Created; G1–G22. | Owner rev-2 brief. |
| 2026-11-20 rev 2 / reconciliation 1 | Added **G23**, **G24**; added status **BLOCKED**; G8 set to BLOCKED (this sandbox); G11 phase text updated (spike is now **mandatory Phase 1b**, not "earlier/optional"); G19 phase list now 2, 3, 6; G22 phase list now 1b, 2, 6, 10; G2/G3/G9 given explicit cross-references; release rule extended to G23/G24. No gate removed; no closing condition weakened. | Owner Final Reconciliation brief; consistency audit (CONSISTENCY_AUDIT.md). |
| 2026-11-21 rev 2 / reconciliation 2 | **G15 test reference corrected** (AT-DA-10 → AT-DA-07). No other gate text changed; no gate status changed (24 gates: G1 CLOSED-BY-DESIGN, G8 BLOCKED in this sandbox, 22 OPEN, **0 PASSED**). | Pass-2 consistency audit (CONSISTENCY_AUDIT.md, finding C-01). |

| ID | Gate | Mode | Phase | Status | Closes when (evidence required) |
|---|---|---|---|---|---|
| G1 | No audio replacement / alternate audio / mixing / mute-for-dubbing on a YouTube player | YouTube | all | **CLOSED-BY-DESIGN** | Enforced by code boundary (ADR-013) + automated test. Reopened only by written YouTube authorization + compliance review. Basis: API policy III.I.7 (F2). |
| G2 | YouTube ToS on automated access | YouTube | 3 | OPEN → **folded into G14** | See G14. |
| G3 | Cloud-IP blocking of caption retrieval | YouTube | 3, 9 | OPEN | Topology decided (Q2, Q13; ADR-005); no proxy/evasion. Moot while G14 keeps retrieval disabled. |
| G4 | Definition of "authorized media" + rights-declaration flow | Authorized | 2, 6 | OPEN | Owner answers Q3; flow specified in PRODUCT_SPEC §5 and implemented/tested. |
| G5 | Commercial eligibility of every model (MT + TTS) | Both | 4, 5 | OPEN | Owner answers Q1; licence matrix complete. |
| G6 | Translation quality and licence | Authorized | 4 | OPEN | Measured evaluation + native review (G7). |
| G7 | Native Somali reviewers identified | Both | 4, 5, 8 | OPEN | Owner answers Q4. |
| G8 | Build/test environment (installs, device access) | — | 1 | **BLOCKED** (this sandbox: installs disabled, no device, no YouTube reachability) | Installs enabled in a new chat (Q7), or tests run on owner's machine/CI; device access via Q9. |
| G9 | POC defects closed (findings P1–P12 in DECISIONS App. A) | YouTube (research) | 3 | OPEN | Refactor merged, tests green; each of P1–P10 closed or explicitly waived. |
| G10 | Free-hosting fit for backend | Both | 9 | OPEN | Measured RAM/CPU vs current free-tier docs. |
| **G11** | Dual-audio mixer + independent gain controls work **on Android** | Authorized | 1b (feasibility checkpoint, G24) → 6 (production) | OPEN | AT-DA-01…10 pass on ≥2 physical Android devices, results recorded. Phase 1b (AT-SP-*) gives an early signal only and is **not** G11 evidence. |
| **G12** | Somali TTS synchronization quality verified | Authorized | 6 | OPEN | AT-SY-* pass; native reviewer rates timing naturalness (not only numeric drift). |
| **G13** | Custom Somali subtitle display next to a YouTube player | YouTube | 7, 8 | OPEN — **default: not built** | Written policy review of the *exact* layout. Evidence so far: overlays in front of any part of the player are prohibited (F12); adjacent placement is not addressed by the text I read. Official player CC/auto-translate remains the default. |
| **G14** | YouTube caption retrieval method | YouTube | 3, 8 | OPEN — **retrieval disabled** | Policy clearance recorded by the owner. Until then: no unofficial retrieval in any shipped build; research-only flag, off by default everywhere. |
| **G15** | Independent original/Somali volume acceptance | Authorized | 6 | OPEN | AT-DA-01…05 (+AT-DA-07 sweep/click) pass on device. *(Pass 2 fix: previously cited AT-DA-10, which is the headphone/Bluetooth output-change test; the click/sweep test is AT-DA-07.)* |
| **G16** | Fullscreen, pause, seek, speed synchronization acceptance | Authorized | 6, 7 | OPEN | AT-SY-*, AT-FS-* pass on device. |
| **G17** | Per-voice TTS licence + provenance verified | Authorized | 5 | OPEN | Voice registry entry complete for each exposed voice; NC notices where applicable; speaker consent documented where a voice derives from a real person. |
| **G18** | Android/PWA performance and resource limits measured | Authorized | 9, 10 | OPEN | Measured RAM, storage, battery/thermal observations, latency on target devices; recorded, not estimated. |
| G19 *(added)* | Caption source for authorized media without subtitles (no-ASR consequence) | Authorized | 2, 3, 6 | OPEN | Owner confirms Q8: videos with no subtitles require user-supplied SRT/VTT or embedded subtitle tracks. |
| G20 *(added)* | Misuse mitigation: ripped/third-party media submitted as "authorized" | Authorized | 2, 8 | OPEN | Declaration UX + ToS text + no URL-to-file path; residual risk stated honestly (cannot be technically eliminated). |
| G21 *(added)* | TTS compute placement and pre-render latency | Authorized | 5, 6 | OPEN | Measured synthesis speed on the chosen host (device vs your PC/server); owner answers Q2. |
| G22 *(added)* | Media container/codec support on target Android browsers/WebView | Authorized | 1b, 2, 6, 10 | OPEN | Format matrix measured on devices (which files play); fallback policy decided. |
| **G23** *(owner-requested; numbering added)* | **Android ↔ PC/local backend connection security**: no unauthenticated backend reachable from the LAN; secure pairing; token protection; reconnection; offline behavior; data minimization; credential storage | Both (backend) | 1 (design + automated tests), 4 (first phone→backend feature use), 8 (audit) | OPEN | AT-NET-01…14 pass (automated over loopback **and** on a physical Android phone over a real LAN, including a failed attempt from a second, unpaired LAN device); transport decision recorded (Q11); no unauthenticated route other than the pairing endpoint and health; LAN mode off by default; logs contain no secrets. See ARCHITECTURE §11. |
| **G24** *(formalises owner's mandatory checkpoint)* | **Dual-audio feasibility checkpoint** (Phase 1b exit): measured findings on independent gains, headroom, click-free transitions, clock sync, pause/seek/speed/buffering, Bluetooth/headphones, backgrounding, stale-audio cancellation; approaches compared; recommendation + tolerances proposed | Authorized | 1b | OPEN | AT-SP-01…14 executed on the owner's available Android device with full environment records, report delivered, owner approves recommendation and tolerances (Q12). **Blocks the start of Phase 4 and Phase 5 implementation.** Passing on one device is recorded as *single-device feasibility* — multi-device validation is claimed only after two physical devices are tested (G11). |

## Release rule
Any gate that is OPEN, BLOCKED or FAILED and relevant to a deliverable prevents calling that deliverable "production-ready". Gates apply per mode: **Authorized Media** can release once G4–G7, G11, G12, G15–G24 pass (G8–G10 for build/hosting where applicable); **YouTube mode** can release a plain official-player experience independent of G12/G13/G14 (those gate only the *extra* features; G1 stays closed by design and G23 applies if any backend is used). G2, G3 and G9 concern research-only retrieval code and gate only that code.
