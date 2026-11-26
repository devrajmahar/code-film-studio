"""Film 02: JAPAN vs INDIA — High-Retention 32s Vertical Short (1080x1920 @ 30fps)."""

WIDTH = 1080
HEIGHT = 1920
FPS = 30

VOICE = "en-GB-RyanNeural"
VOICE_RATE = "+28%"
AUDIO_BPM = 134

SHOTS = [
    ("s01_title", "shots.s01_title", 0.0, 3.0,
     "Japan versus India. Same rails, two different centuries.",
     ["Japan vs. India: Trains.", "Two different centuries."]),
    ("s02_speed", "shots.s02_speed", 3.0, 3.8,
     "Japan's Shinkansen hits three-twenty kilometers an hour. Indian expresses average fifty-five.",
     ["Shinkansen: 320 km/h.", "Indian Express: 55 km/h."]),
    ("s03_punctuality", "shots.s03_punctuality", 6.8, 3.8,
     "Japan's average yearly delay? Twenty-four seconds. In India, four hours late is normal.",
     ["Japan avg delay: 24 seconds.", "India: 4 hours late is normal."]),
    ("s04_japan_station", "shots.s04_japan_station", 10.6, 3.6,
     "Japanese platforms: safety doors, spotless floors, cleaned in seven minutes.",
     ["Japan: safety doors & spotless floors.", "Cleaned in 7 minutes flat."]),
    ("s05_india_station", "shots.s05_india_station", 14.2, 3.6,
     "Indian stations: packed crowds, open doors, and trash across the tracks.",
     ["India: packed platforms & open doors.", "Trash across the tracks."]),
    ("s06_engineering", "shots.s06_engineering", 17.8, 4.2,
     "Why? Japan built dedicated elevated rails. India jams freight, locals, and expresses on one track.",
     ["Japan: dedicated elevated rails.", "India: everything shares one track."]),
    ("s07_safety", "shots.s07_safety", 22.0, 3.4,
     "Sixty years. Ten billion riders. Zero fatal derailments.",
     ["60+ years. 10 billion riders.", "Zero fatal derailments."]),
    ("s08_future", "shots.s08_future", 25.4, 3.8,
     "India is finally building high-speed rail. Because world-class transit is pure discipline.",
     ["High-speed rail isn't luck.", "It's pure discipline."]),
    ("s09_outro", "shots.s09_outro", 29.2, 2.8,
     "Great transit doesn't just move people. It builds great nations.",
     ["Great transit moves people.", "It builds great nations."]),
]

AUDIO_PROGRESSION = [
    [0.0, 3.0, [64, 67, 71]],
    [3.0, 6.8, [60, 64, 67]],
    [6.8, 10.6, [62, 66, 69]],
    [10.6, 14.2, [67, 71, 74]],
    [14.2, 17.8, [62, 65, 69]],
    [17.8, 22.0, [60, 64, 67]],
    [22.0, 25.4, [65, 69, 72]],
    [25.4, 29.2, [67, 71, 74]],
    [29.2, 32.0, [60, 64, 67, 72], True],
]

AUDIO_SFX = [
    {"type": "whoosh", "shot": 0, "offset": 0.25, "dur": 0.55, "pan": 0.1},
    {"type": "whoosh", "shot": 1, "offset": 0.25, "dur": 0.55, "pan": 0.0},
    {"type": "station_chime", "shot": 3, "offset": 0.15, "pan": 0.0},
    {"type": "horn", "shot": 4, "offset": 0.40, "dur": 0.18, "f1": 310, "f2": 390, "pan": -0.35},
    {"type": "whoosh", "shot": 6, "offset": 0.50, "dur": 0.60, "pan": 0.15},
    {"type": "station_chime", "shot": 7, "offset": 1.1, "pan": 0.0},
]

TOTAL_DURATION = sum(s[3] for s in SHOTS)
TOTAL_FRAMES = int(round(TOTAL_DURATION * FPS))


def shot_frame_range(shot):
    return int(round(shot[2] * FPS)), int(round(shot[3] * FPS))
