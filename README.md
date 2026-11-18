# Korg Pa700 Interactive Control Panel & Auto-Arranger Trainer

Interactive browser-based hardware panel emulator, Web Audio polyphonic synthesizer, Auto-Arranger groove engine, and live-performance crash course for the **Korg Pa700 / Pa700 ORIENTAL**.

## Quick Start

Open [`index.html`](./index.html) (or the self-contained single-file [`pa700_standalone.html`](./pa700_standalone.html)) directly in any modern browser, or serve locally:

```bash
python3 -m http.server 8000
```

See [`CRASH_COURSE.md`](./CRASH_COURSE.md) for the live-gig cheat sheet (or click **Guided Gig Crash Course (3 Drills)** inside the top toolbar of the app).

## Regenerating Panel & Sprite Assets

All panel, speaker grille, knob, `VALUE` dial, button, and LED images in [`assets/`](./assets/) are generated procedurally from scratch via Pillow + NumPy:

```bash
python3 generate_assets.py
```
