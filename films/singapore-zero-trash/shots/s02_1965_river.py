"""Shot 2: 1965 Dead Singapore River — Wooden shanties, garbage barges, polluted brown sludge."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import sg_kit

CAPS = film.SHOTS[1][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    pan = -60 * t

    img = kit.make_sky_gradient((98, 82, 64), (162, 134, 98), (198, 166, 124), mid_pos=0.45)
    d = ImageDraw.Draw(img)

    # Stacked ramshackle wooden kampong slums along riverfront
    for row_y, sc, seed_base in [(880, 0.95, 200), (1050, 1.1, 220)]:
        for i in range(7):
            sg_kit.draw_kampong_shack(
                d,
                -40 + i * 185 + pan * sc,
                row_y,
                w=int(180 * sc),
                h=int((135 + ((i * 41) % 45)) * sc),
                seed=seed_base + i,
            )

    # Murky polluted brown river
    water_y = 1040
    d.rectangle((0, water_y, kit.W, kit.H), fill=(72, 58, 42))
    for r in range(36):
        ry = water_y + 18 + r * 20
        rx = ((r * 213 + sec * 32) % (kit.W + 120)) - 60
        d.line([(rx, ry), (rx + 80, ry)], fill=(96, 80, 58), width=2)

    # Riverbank trash mounds & floating garbage
    kit.draw_gritty_trash_dump(d, 260 + pan * 0.9, water_y + 20, w=360, h=135, seed=21)
    kit.draw_gritty_trash_dump(d, 860 + pan * 0.9, water_y + 25, w=360, h=140, seed=22)

    # Old wooden bumboats jammed in the filthy water
    for bx, by in [(240, 1220), (640, 1310)]:
        ux = bx + pan * 1.1
        uy = by + math.sin(sec * 3.5 + bx) * 4
        d.polygon([(ux - 110, uy - 28), (ux + 110, uy - 28), (ux + 82, uy + 14), (ux - 82, uy + 14)], fill=(86, 56, 36), outline=kit.SMOG_INK)
        d.rectangle((ux - 54, uy - 54, ux + 44, uy - 28), fill=(116, 86, 62), outline=kit.SMOG_INK, width=2)

    # Floating plastic & debris in river
    rng = np.random.default_rng(209)
    cols = [(210, 206, 196), (178, 74, 58), (82, 128, 156), (144, 122, 88)]
    for i in range(34):
        fx = (rng.uniform(30, 1040) + sec * rng.uniform(16, 38)) % kit.W
        fy = rng.uniform(1120, 1520)
        d.rounded_rectangle((fx, fy, fx + 24, fy + 10), radius=3, fill=cols[i % len(cols)], outline=kit.SMOG_INK, width=1)

    img = kit.add_smog_veil(img, sec, y_start=200, y_end=1150, strength=0.34, speed=24)
    img = kit.draw_shorts_badge(img, "SINGAPORE 1965  ·  SLUMS & DEAD RIVER", y=148, accent=kit.RUST_RED, bg=(38, 22, 18))
    img = kit.finish_frame(img, global_idx, vignette=0.30, warmth=0.28, bloom=0.08)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
