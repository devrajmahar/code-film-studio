"""Film definition: INDIA vs EUROPE — 36s Vertical YouTube Shorts / Reels (1080x1920, 30fps)."""

WIDTH = 1080
HEIGHT = 1920
FPS = 30

VOICE = "en-GB-RyanNeural"
VOICE_RATE = "+15%"
AUDIO_BPM = 120

# Each shot: (id, module, start_sec, duration_sec, narration_text, caption_lines)
SHOTS = [
    ("s01_title", "shots.s01_title", 0.0, 3.2,
     "India versus Europe. Same century. Two completely different worlds.",
     ["India vs. Europe.", "Two completely different worlds."]),
    ("s02_air", "shots.s02_air", 3.2, 4.6,
     "In Indian cities, the air itself has a color. In Europe, you can see mountains fifty kilometers away.",
     ["In India, the air has a color.", "In Europe, 50 km visibility."]),
    ("s03_streets", "shots.s03_streets", 7.8, 4.6,
     "Walk down an Indian street: trash everywhere, broken footpaths, tangled wires—and zero waste management.",
     ["India: trash & tangled wires.", "Zero municipal management."]),
    ("s04_europe_street", "shots.s04_europe_street", 12.4, 4.6,
     "Now step into Europe. Underground bins, buried cables, and trams on time. Cleanliness isn't magic—it's design.",
     ["Europe: underground bins & trams.", "Cleanliness isn't magic—it's design."]),
    ("s05_monsoon_drain", "shots.s05_monsoon_drain", 17.0, 4.0,
     "In India, one hour of rain exposes decades of bad management: clogged drains and flooded roads.",
     ["India: one hour of rain,", "and roads turn into rivers."]),
    ("s06_transit_grid", "shots.s06_transit_grid", 21.0, 4.6,
     "Europe builds underground first—utility tunnels, strict zoning, and accountability. India still patches over chaos.",
     ["Europe builds underground first.", "India patches over chaos."]),
    ("s07_green_space", "shots.s07_green_space", 25.6, 3.8,
     "European cities protect clean air and walkable parks. That isn't a luxury—it's basic dignity.",
     ["Europe: clean air & green parks.", "Not a luxury—basic dignity."]),
    ("s08_choice", "shots.s08_choice", 29.4, 3.8,
     "Europe wasn't always clean either. It enforced standards and planning. India can make that same choice.",
     ["Europe chose strict standards.", "India can make that choice."]),
    ("s09_outro", "shots.s09_outro", 33.2, 2.8,
     "Clean cities aren't a miracle. They are a decision.",
     ["Clean cities aren't a miracle.", "They are a decision."]),
]

# Declarative soundtrack chord progression: [start_s, end_s, [midi_notes], hold_only?]
AUDIO_PROGRESSION = [
    [0.0, 3.2, [62, 65, 69]],
    [3.2, 5.4, [62, 65, 69]],
    [5.4, 7.8, [60, 64, 67]],
    [7.8, 12.4, [60, 63, 67]],
    [12.4, 17.0, [67, 71, 74]],
    [17.0, 21.0, [62, 65, 69]],
    [21.0, 25.6, [60, 64, 67]],
    [25.6, 29.4, [65, 69, 72]],
    [29.4, 33.2, [67, 71, 74]],
    [33.2, 36.0, [60, 64, 67, 72], True],
]

# Declarative spot SFX cues
AUDIO_SFX = [
    {"type": "bird", "t": 6.0, "hz": 2800, "pan": 0.45},
    {"type": "bird", "t": 6.7, "hz": 3200, "pan": -0.35},
    {"type": "horn", "t": 8.6, "dur": 0.16, "f1": 440, "f2": 540, "pan": -0.45},
    {"type": "horn", "t": 10.5, "dur": 0.20, "f1": 395, "f2": 490, "pan": 0.4},
    {"type": "tram_bell", "t": 13.1, "pan": -0.3},
    {"type": "bird", "t": 15.2, "hz": 2900, "pan": 0.4},
    {"type": "rain", "t": 17.0, "dur": 4.0},
    {"type": "bird", "t": 26.4, "hz": 2950, "pan": 0.45},
    {"type": "tram_bell", "t": 31.2, "pan": 0.3},
]

TOTAL_DURATION = sum(s[3] for s in SHOTS)
TOTAL_FRAMES = int(round(TOTAL_DURATION * FPS))


def shot_frame_range(shot):
    return int(round(shot[2] * FPS)), int(round(shot[3] * FPS))
