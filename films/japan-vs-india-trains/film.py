"""Film 02: JAPAN vs INDIA — Trains & Transit (Audio-synced vertical Short, 1080x1920 @ 30fps)."""

WIDTH = 1080
HEIGHT = 1920
FPS = 30

VOICE = "en-GB-RyanNeural"
VOICE_RATE = "+18%"
AUDIO_BPM = 124

SHOTS = [
    ("s01_title", "shots.s01_title", 0.0, 4.0,
     "Japan versus India. Two rail giants living in different centuries.",
     ["Japan vs. India: Trains.", "Two completely different centuries."]),
    ("s02_speed", "shots.s02_speed", 4.0, 5.0,
     "Japan's Shinkansen flies at three hundred twenty kilometers per hour. Indian express trains average fifty-five.",
     ["Shinkansen: 320 km/h.", "Indian Express: 55 km/h."]),
    ("s03_punctuality", "shots.s03_punctuality", 9.0, 5.0,
     "Shinkansen's average yearly delay? Twenty-four seconds. In India, four hours late is normal.",
     ["Japan avg delay: 24 seconds.", "India: 4 hours late is normal."]),
    ("s04_japan_station", "shots.s04_japan_station", 14.0, 5.0,
     "Japanese platforms have automatic safety doors, spotless floors, and seven-minute turnarounds.",
     ["Japan: safety doors & spotless floors.", "Cleaned in 7 minutes flat."]),
    ("s05_india_station", "shots.s05_india_station", 19.0, 5.0,
     "Indian stations? Packed platforms, open doors, and trash scattered across the tracks.",
     ["India: packed platforms & open doors.", "Trash scattered on the tracks."]),
    ("s06_engineering", "shots.s06_engineering", 24.0, 5.5,
     "Why? Japan built dedicated elevated tracks. India forces freight, locals, and express trains onto one shared rail.",
     ["Japan: dedicated elevated rails.", "India: everything shares one track."]),
    ("s07_safety", "shots.s07_safety", 29.5, 4.5,
     "Sixty years and ten billion riders later, the Shinkansen has zero fatal derailments.",
     ["60+ years. 10 billion riders.", "Zero fatal derailments."]),
    ("s08_future", "shots.s08_future", 34.0, 5.0,
     "India is finally building dedicated corridors and high-speed rail. Great transit isn't luck—it's discipline.",
     ["High-speed rail isn't luck.", "It's discipline & investment."]),
    ("s09_outro", "shots.s09_outro", 39.0, 3.5,
     "Great transit doesn't just move people. It builds great nations.",
     ["Great transit doesn't just move people.", "It builds great nations."]),
]

AUDIO_PROGRESSION = [
    [0.0, 4.0, [64, 67, 71]],
    [4.0, 9.0, [60, 64, 67]],
    [9.0, 14.0, [62, 66, 69]],
    [14.0, 19.0, [67, 71, 74]],
    [19.0, 24.0, [62, 65, 69]],
    [24.0, 29.5, [60, 64, 67]],
    [29.5, 34.0, [65, 69, 72]],
    [34.0, 39.0, [67, 71, 74]],
    [39.0, 42.5, [60, 64, 67, 72], True],
]

AUDIO_SFX = [
    {"type": "whoosh", "shot": 0, "offset": 0.35, "dur": 0.75, "pan": 0.1},
    {"type": "whoosh", "shot": 1, "offset": 0.35, "dur": 0.75, "pan": 0.0},
    {"type": "station_chime", "shot": 3, "offset": 0.20, "pan": 0.0},
    {"type": "horn", "shot": 4, "offset": 0.50, "dur": 0.22, "f1": 310, "f2": 390, "pan": -0.35},
    {"type": "whoosh", "shot": 6, "offset": 0.75, "dur": 0.80, "pan": 0.15},
    {"type": "station_chime", "shot": 7, "offset": 1.4, "pan": 0.0},
]

TOTAL_DURATION = sum(s[3] for s in SHOTS)
TOTAL_FRAMES = int(round(TOTAL_DURATION * FPS))


def shot_frame_range(shot):
    return int(round(shot[2] * FPS)), int(round(shot[3] * FPS))
