"""Film 03: How Singapore Went From Slums to Zero Trash (1080x1920 @ 30fps)."""

WIDTH = 1080
HEIGHT = 1920
FPS = 30

VOICE = "en-GB-RyanNeural"
VOICE_RATE = "+28%"
AUDIO_BPM = 134

SHOTS = [
    ("s01_title", "shots.s01_title", 0.0, 3.6,
     "In nineteen sixty-five, Singapore was choked with slums and trash. Today, it's the cleanest city on Earth.",
     ["Singapore: 1965 vs. Today.", "From slums to zero trash."]),
    ("s02_1965_river", "shots.s02_1965_river", 3.6, 4.0,
     "Sixty years ago, most citizens lived in crowded shanties—and the Singapore River was biologically dead.",
     ["1965: overcrowded wooden shacks.", "A biologically dead river."]),
    ("s03_hdb_housing", "shots.s03_hdb_housing", 7.6, 4.0,
     "So Singapore cleared the slums and built clean high-rise public housing for eighty percent of its people.",
     ["Slums replaced by clean housing", "for 80% of the population."]),
    ("s04_strict_laws", "shots.s04_strict_laws", 11.6, 3.8,
     "Then came ruthless enforcement. Heavy fines for littering and dumping turned cleanliness into a national habit.",
     ["Strict fines & zero tolerance.", "Cleanliness became a habit."]),
    ("s05_waste_to_energy", "shots.s05_waste_to_energy", 15.4, 4.2,
     "Where does the trash go? Thousand-degree plants burn it—shrinking waste by ninety percent and powering the grid.",
     ["1,000°C waste-to-energy plants", "shrink trash by 90% & make power."]),
    ("s06_semakau_island", "shots.s06_semakau_island", 19.6, 3.8,
     "The clean ash builds an offshore island—so pure that coral reefs and mangroves thrive right beside it.",
     ["Clean ash builds a green island", "surrounded by living coral reefs."]),
    ("s07_river_cleanup", "shots.s07_river_cleanup", 23.4, 3.8,
     "A ten-year cleanup dredged the dead river, moved street hawkers indoors, and brought marine life back.",
     ["10-year cleanup revived the river", "and moved hawkers into clean halls."]),
    ("s08_garden_city", "shots.s08_garden_city", 27.2, 3.8,
     "By planting millions of trees and vertical sky-gardens, Singapore became a futuristic city inside a forest.",
     ["Millions of trees & sky-gardens.", "A city built inside a forest."]),
    ("s09_outro", "shots.s09_outro", 31.0, 3.0,
     "Singapore proves poverty isn't destiny. Clean cities are built by fearless leadership.",
     ["Poverty isn't destiny.", "Clean cities take leadership."]),
]

AUDIO_PROGRESSION = [
    [0.0, 3.6, [62, 65, 69]],
    [3.6, 7.6, [60, 63, 67]],
    [7.6, 11.6, [60, 64, 67]],
    [11.6, 15.4, [65, 69, 72]],
    [15.4, 19.6, [62, 66, 69]],
    [19.6, 23.4, [67, 71, 74]],
    [23.4, 27.2, [60, 64, 67]],
    [27.2, 31.0, [67, 71, 74]],
    [31.0, 34.0, [60, 64, 67, 72], True],
]

AUDIO_SFX = [
    {"type": "whoosh", "shot": 0, "offset": 0.25, "dur": 0.55, "pan": 0.1},
    {"type": "bird", "shot": 2, "offset": 0.6, "hz": 2850, "pan": 0.4},
    {"type": "station_chime", "shot": 3, "offset": 0.25, "pan": 0.0},
    {"type": "whoosh", "shot": 4, "offset": 0.4, "dur": 0.6, "pan": -0.2},
    {"type": "bird", "shot": 5, "offset": 0.5, "hz": 3000, "pan": 0.35},
    {"type": "bird", "shot": 7, "offset": 0.4, "hz": 2900, "pan": -0.35},
]

TOTAL_DURATION = sum(s[3] for s in SHOTS)
TOTAL_FRAMES = int(round(TOTAL_DURATION * FPS))


def shot_frame_range(shot):
    return int(round(shot[2] * FPS)), int(round(shot[3] * FPS))
