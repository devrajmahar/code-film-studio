"""Shot 5 (9:16 Shorts): Monsoon Flood — Dramatic storm, lightning, clogged drain, submerged auto."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[4][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    flash = 0.0
    if 0.12 < t < 0.16 or 0.64 < t < 0.67:
        flash = 0.48

    top = kit.lerp_rgb((24, 32, 42), (168, 182, 202), flash)
    mid = kit.lerp_rgb((48, 56, 64), (192, 202, 216), flash)
    bot = kit.lerp_rgb((74, 78, 80), (170, 178, 184), flash)
    img = kit.make_sky_gradient(top, mid, bot, mid_pos=0.45)
    img = kit.add_painted_clouds_layer(img, sec * 1.8, y_top=60, y_bot=660, tint=(82, 90, 102), shadow=(36, 42, 52), density=0.62)
    d = ImageDraw.Draw(img)

    # Wet dark concrete buildings
    for i in range(6):
        bx = -35 + i * 215
        bh = 520 + ((i * 71) % 240)
        kit.draw_chaotic_building_25d(d, bx, 1060, 210, bh, (64, 62, 60), seed=500 + i)

    # Flooded muddy brown street water
    water_y = 1060
    d.rectangle((0, water_y, kit.W, kit.H), fill=(76, 62, 46))
    for r in range(44):
        ry = water_y + 18 + r * 18
        rx = ((r * 213 + sec * 44) % (kit.W + 120)) - 60
        d.line([(rx, ry), (rx + 78, ry)], fill=(108, 92, 72), width=2)

    # Clogged storm drain overflowing with plastic debris
    d.rectangle((90, 1110, 390, 1156), fill=(44, 40, 36), outline=kit.SMOG_INK, width=3)
    for g in range(7):
        d.line([(115 + g * 40, 1110), (115 + g * 40, 1156)], fill=(24, 22, 20), width=5)

    # Floating bottles & debris
    rng = np.random.default_rng(505)
    bcols = [(212, 210, 202), (188, 74, 60), (72, 138, 182), (218, 184, 64)]
    for i in range(28):
        bx = (rng.uniform(40, 1020) + sec * rng.uniform(18, 45)) % kit.W
        by = rng.uniform(1120, 1520) + math.sin(sec * 4.2 + i) * 6
        d.rounded_rectangle((bx, by, bx + 28, by + 11), radius=4, fill=bcols[i % len(bcols)], outline=kit.SMOG_INK, width=1)

    # Stalled auto-rickshaw half-submerged + golden headlight reflection on water
    kit.draw_detailed_auto(d, 740, 1280, scale=1.65, facing=-1, bob=math.sin(sec * 4) * 2)
    d.polygon([(640, 1228), (180, 1295), (180, 1395), (640, 1272)], fill=(196, 170, 108))
    for r in range(9):
        ry = 1270 + r * 14
        d.line([(200 + (r % 2) * 32, ry), (600, ry)], fill=(86, 72, 54), width=3)

    # Slanted heavy monsoon rain streaks
    rain_rng = np.random.default_rng(5000 + frame_idx * 31)
    for _ in range(380):
        rx = rain_rng.uniform(0, kit.W + 140)
        ry = rain_rng.uniform(-40, kit.H)
        length = rain_rng.uniform(42, 88)
        d.line([(rx, ry), (rx - length * 0.28, ry + length)], fill=(192, 208, 222), width=2)

    # Impact rings on water
    for k in range(22):
        phase = (sec * 2.4 + k * 0.17) % 1.0
        cx = ((k * 263) % (kit.W - 100)) + 50
        cy = 1140 + ((k * 173) % 520)
        rr = 6 + phase * 42
        d.ellipse((cx - rr, cy - rr * 0.35, cx + rr, cy + rr * 0.35), outline=(168, 162, 148), width=2)

    img = kit.draw_shorts_badge(img, "INDIA  ·  CLOGGED DRAINS & FLOODS", y=148, accent=(212, 134, 58), bg=(24, 28, 34))
    img = kit.finish_frame(img, global_idx, vignette=0.34, warmth=-0.10, bloom=0.14)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
