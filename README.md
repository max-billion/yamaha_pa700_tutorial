# Korg Pa700 Interactive Control Panel & Auto-Arranger Trainer

Interactive browser-based hardware panel emulator, SoundFont + Web Audio synthesizer, Auto-Arranger groove engine, and live-performance crash course for the **Korg Pa700 / Pa700 ORIENTAL (OS v1.5)**.

## What's Inside (Complete OS v1.5 Manual Catalog)

Extracted directly from `Pa700_User_Manual_v15_E.pdf` (`scripts/extract_manual_resources.py`):
- **379 Factory Styles** across 12 categories (`Pop` through `World`) with paginated `P1–P5` Style Select, bespoke 8-track instrument lineups (`DRUM`, `PERC`, `BASS`, `ACC1–ACC5`), and individually composed multi-bar MIDI arrangements across 7 meters (`4/4`, `2/4`, `3/4`, `6/8`, `12/8`, `6/4`, `9/8`).
- **298 Factory Keyboard Sets** across all 9 `KEYBOARD SET LIBRARY` category buttons (`Piano & EP` through `Ethnic`), plus Style-linked Keyboard Sets `1–4` and `MY SETTING`.
- **1,845 Sounds** (**1,727 melodic Sounds + 118 Drum Kits**) organized across `Factory`, `Legacy`, and `GM/XG` tabs in TouchView **Sound Select**.
- **52 DNC (Defined Nuance Control) Sounds** mapped to `SW 1`, `SW 2`, Joystick `Y+ / Y-`, Legato, and AfterTouch (`DNC` badge in the Audio HUD and Sound Select footer).
- **415 Factory Pads** (`HIT` One-Shots & `SEQ` Loops) across 20 Pad groups via TouchView **Pad Select**.
- **Real-Time Search (`🔍 SEARCH`)** filtering all 379 Styles, 298 Keyboard Sets, 1,845 Sounds, and 415 Pads.

## SoundFont Audio Engine

Powered by vendored **SpessaSynth** ([`vendor/spessasynth/`](./vendor/spessasynth/)) + streaming SoundFont support + zero-network Procedural Web Audio fallback ([`pa700_audio.js`](./pa700_audio.js)):
- **Supported SoundFont Libraries**:
  - **FluidR3 GM (Stream)** — default on launch; fetches per-instrument samples on demand over CORS-enabled jsDelivr CDN with zero multi-megabyte upfront download and caches decoded patches in memory.
  - **GeneralUser GS** (`.sf3` 8MB compact or `.sf2` 31MB full), **FluidR3 Mono** (`.sf3` 23MB), **MuseScore General** (`MS Basic .sf3` 49MB) via CORS mirrors & IndexedDB caching.
  - **FreePats GM (`.sf2` Stack)** — upload or drag-and-drop local `.sf2`/`.sf3` files via the **`+ .sf2`** button (persisted in IndexedDB).
  - **Procedural WebAudio (Offline)** — instant zero-network fallback synthesizer.
- **Ghost-Note Protection on Key Release**: Remote per-instrument patches finish downloading and caching in the background regardless of connection speed, while keys released before a download completes cleanly suppress delayed ghost notes.

## Quick Start & Static Hosting (`*.github.io`)

The app is 100% static (HTML/CSS/ES+classic JS + PNG sprites + IndexedDB) and deploys directly to **GitHub Pages (`*.github.io`)** or any static web server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/index.html
```

Or open [`pa700_standalone.html`](./pa700_standalone.html) directly via `file://` (uses FluidR3 Streaming + Procedural Web Audio offline; serve via HTTP/`*.github.io` for full `.sf2`/`.sf3` SpessaSynth AudioWorklet synthesis).

See [`CRASH_COURSE.md`](./CRASH_COURSE.md) for the live-gig cheat sheet (or click **Guided Gig Crash Course (3 Drills)** inside the top toolbar).

## Maintenance Scripts

```bash
# Re-extract all 379 Styles, 298 Kbd Sets, 1,845 Sounds, 52 DNC maps & 415 Pads from manual PDF
python3 scripts/extract_manual_resources.py

# Regenerate single-file pa700_standalone.html
python3 scripts/build_standalone.py

# Optional: download full .sf2/.sf3 SoundFonts locally under ./soundfonts/ (gitignored)
python3 scripts/download_soundfonts.py --libs compact

# Regenerate panel & button PNG sprites in ./assets/
python3 generate_assets.py
```

