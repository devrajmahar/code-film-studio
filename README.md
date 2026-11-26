# Code Film Studio

A reusable, code-driven **procedural animated documentary & Shorts studio** (Python + Node.js + FFmpeg).
Create 9:16 vertical Shorts/Reels (or 16:9 films) entirely in code—with painterly 2.5D visuals, volumetric lighting, auto-synced narration, and a zero-dependency procedural soundtrack.

## Repository Architecture

```text
code-film-studio/
├── engine/                     # Reusable studio engine (shared across all films)
│   ├── kit.py                  # 2D gouache renderer, 2.5D buildings, volumetric skies, bloom, Shorts captions
│   ├── narration.py            # Per-shot edge-tts narrator (auto tempo-fit + Windows SAPI fallback)
│   ├── audio_engine.mjs        # Zero-dependency, zero-hum procedural soundtrack & Foley mixer
│   └── render.py               # Unified CLI: stills, audio, multiprocess frame render & FFmpeg MP4
└── films/                      # Individual films live here (one folder per video)
    └── india-vs-europe/        # Example 36s vertical Short (1080x1920 @ 30fps)
        ├── film.py             # Timeline, shots, narration script, captions, chords & SFX cues
        └── shots/              # Self-contained animated shot modules (s01..s09)
```

## Quick Start

### 1. Setup Environment (Once)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\pip install -r requirements.txt
# macOS / Linux:
.venv/bin/pip install -r requirements.txt
```
*(Requires Python 3.11+, Node.js 20+, and `ffmpeg`/`ffprobe` on PATH.)*

### 2. Build Any Film in One Command
```bash
# Preview 1 mid-frame still per shot:
.venv/Scripts/python engine/render.py india-vs-europe --stills

# Full pipeline (narration + soundtrack + frames + MP4):
.venv/Scripts/python engine/render.py india-vs-europe --all
```
Output MP4 is written to `films/<slug>/dist/<slug>.mp4`.

## Creating a New Film
1. Create a new folder `films/<your-film-slug>/` with a `film.py` and `shots/` folder (copy `films/india-vs-europe/` as a template).
2. Define `SHOTS`, `AUDIO_PROGRESSION`, and `AUDIO_SFX` inside `films/<your-film-slug>/film.py`.
3. Write each shot's `render(frame_idx, n_frames, global_idx)` function using helpers from `kit.py`.
4. Run `.venv/Scripts/python engine/render.py <your-film-slug> --all`.
