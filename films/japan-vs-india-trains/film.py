"""Film 02: JAPAN vs INDIA — Trains & Transit (36s, 1080x1920 @ 30fps)."""

WIDTH = 1080
HEIGHT = 1920
FPS = 30

VOICE = "en-GB-RyanNeural"
VOICE_RATE = "+15%"
AUDIO_BPM = 124

SHOTS = [
    ("s01_title", "shots.s01_title", 0.0, 3.2,
     "Japan versus India. Both move millions by rail every day. Yet they live in different centuries.",
     ["Japan vs. India: Trains.", "Two completely different centuries."]),
    ("s02_speed", "shots.s02_speed", 3.2, 4.4,
     "Japan's Shinkansen glides at three hundred twenty kilometers per hour. Most Indian express trains still average fifty-five.",
     ["Shinkansen: 320 km/h.", "Indian Express: 55 km/h."]),
    ("s03_punctuality", "shots.s03_punctuality", 7.6, 4.2,
     "Average yearly delay on the Shinkansen? Twenty-four seconds. In India, a four-hour delay is just another Tuesday.",
     ["Japan avg delay: 24 seconds.", "India: 4 hours late is normal."]),
    ("s04_japan_station", "shots.s04_japan_station", 11.8, 4.4,
     "Step onto a Japanese platform. Automatic safety doors, spotless floors, painted queues, and a seven-minute cleaning miracle.",
     ["Japan: safety doors & spotless floors.", "Cleaned in 7 minutes flat."]),
    ("s05_india_station", "shots.s05_india_station", 16.2, 4.4,
     "Now look at an Indian station. Packed platforms, open doors, trash on the tracks, and millions fighting just to board.",
     ["India: packed platforms & open doors.", "Trash scattered on the tracks."]),
    ("s06_engineering", "shots.s06_engineering", 20.6, 4.4,
     "Here's why. Japan built dedicated elevated tracks with zero road crossings. India runs freight, locals, and express trains on the same rails.",
     ["Japan: dedicated elevated rails.", "India: everything shares one track."]),
    ("s07_safety", "shots.s07_safety", 25.0, 4.0,
     "In over sixty years and ten billion passengers, the Shinkansen has never had a single fatal derailment.",
     ["60+ years. 10 billion riders.", "Zero fatal derailments."]),
    ("s08_future", "shots.s08_future", 29.0, 4.0,
     "India is finally building freight corridors and high-speed rail. World-class transit isn't luck—it's discipline and investment.",
     ["High-speed rail isn't luck.", "It's discipline & investment."]),
    ("s09_outro", "shots.s09_outro", 33.0, 3.0,
     "Great transit doesn't just move people. It builds great nations.",
     ["Great transit doesn't just move people.", "It builds great nations."]),
]

AUDIO_PROGRESSION = [
    [0.0, 3.2, [64, 67, 71]],         # Em
    [3.2, 7.6, [60, 64, 67]],         # C
    [7.6, 11.8, [62, 66, 69]],        # D
    [11.8, 16.2, [67, 71, 74]],       # G (clean Japan station)
    [16.2, 20.6, [62, 65, 69]],       # Dm (chaotic India station)
    [20.6, 25.0, [60, 64, 67]],       # C (blueprint)
    [25.0, 29.0, [65, 69, 72]],       # F (sunset safety)
    [29.0, 33.0, [67, 71, 74]],       # G (transformation)
    [33.0, 36.0, [60, 64, 67, 72], True],  # C resolve
]

AUDIO_SFX = [
    {"type": "whoosh", "t": 0.6, "dur": 0.9, "pan": 0.1},
    {"type": "whoosh", "t": 3.8, "dur": 0.85, "pan": 0.0},
    {"type": "station_chime", "t": 12.2, "pan": 0.0},
    {"type": "horn", "t": 17.0, "dur": 0.25, "f1": 310, "f2": 390, "pan": -0.35},
    {"type": "whoosh", "t": 26.2, "dur": 0.95, "pan": 0.15},
    {"type": "station_chime", "t": 31.0, "pan": 0.0},
]

TOTAL_DURATION = sum(s[3] for s in SHOTS)  # 36.0s
TOTAL_FRAMES = int(round(TOTAL_DURATION * FPS))  # 1080 frames


def shot_frame_range(shot):
    return int(round(shot[2] * FPS)), int(round(shot[3] * FPS))
