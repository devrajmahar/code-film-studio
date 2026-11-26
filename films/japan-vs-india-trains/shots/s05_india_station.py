"""Shot 5: The Indian Platform — Crowded platform, open train doors, litter on tracks, tin roof."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import rail_kit

CAPS = film.SHOTS[4][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((118, 98, 78), (174, 146, 112), (206, 176, 136), mid_pos=0.45)
    d = ImageDraw.Draw(img)

    # Rusted corrugated iron platform roof + steel trusses
    d.polygon([(0, 0), (kit.W, 0), (kit.W, 470), (0, 440)], fill=(78, 66, 58))
    for rx in range(0, kit.W, 54):
        d.line([(rx, 0), (rx, 460)], fill=(58, 48, 42), width=3)
    # Classic yellow Indian railway station board
    d.rectangle((260, 485, 820, 585), fill=(238, 192, 42), outline=kit.SMOG_INK, width=4)
    f_sgn = kit.get_font(40, bold=True)
    d.text((345, 512), "PLATFORM  04  ·  JN", font=f_sgn, fill=(28, 24, 22))

    # Tangled overhead wires & rust pillars
    for px in (120, 960):
        d.rectangle((px, 440, px + 26, 1120), fill=(92, 74, 62), outline=kit.SMOG_INK, width=2)
    for w_i in range(6):
        kit.draw_catenary(d, 0, 595 + w_i * 12, kit.W, 608 + w_i * 10, sag=36 + w_i * 14, width=2)

    # Track bed littered with bottles & wrappers
    d.rectangle((0, 960, kit.W, 1100), fill=(72, 64, 56))
    rng = np.random.default_rng(515)
    tcols = [(216, 212, 202), (186, 76, 60), (76, 136, 176), (220, 186, 62)]
    for i in range(42):
        lx = rng.uniform(20, kit.W - 20)
        ly = rng.uniform(1005, 1085)
        d.polygon([(lx, ly), (lx + 18, ly - 5), (lx + 24, ly + 8), (lx + 4, ly + 10)], fill=tcols[i % len(tcols)], outline=kit.SMOG_INK)

    # Boxy blue Indian express pulling in slowly with open doors
    front_x = 980 - t * 220
    rail_kit.draw_indian_express(d, front_x, 1020, length=940, height=168, facing=-1)

    # Cracked concrete crowded platform in foreground
    d.rectangle((0, 1085, kit.W, kit.H), fill=(134, 122, 108), outline=kit.SMOG_INK, width=3)
    # Dense jostling crowd silhouettes rushing toward train doors
    crowd_cols = [(164, 72, 56), (52, 84, 122), (188, 138, 52), (76, 98, 72), (124, 66, 88), (64, 60, 58)]
    rng_c = np.random.default_rng(525)
    for i in range(28):
        cx = rng_c.uniform(60, kit.W - 60) + math.sin(sec * 4.5 + i) * 10
        cy = rng_c.uniform(1180, 1360)
        bob = abs(math.sin(sec * 7.0 + i * 1.3)) * 5
        col = crowd_cols[i % len(crowd_cols)]
        d.ellipse((cx - 14, cy - 92 - bob, cx + 14, cy - 64 - bob), fill=(116, 86, 68), outline=kit.SMOG_INK, width=2)
        d.rounded_rectangle((cx - 19, cy - 62 - bob, cx + 19, cy - 6 - bob), radius=6, fill=col, outline=kit.SMOG_INK, width=2)

    img = kit.add_smog_veil(img, sec, y_start=350, y_end=1150, strength=0.22, speed=22)
    img = kit.draw_shorts_badge(img, "INDIA  ·  PACKED PLATFORMS & OPEN DOORS", y=148, accent=kit.RUST_RED, bg=(38, 22, 18))
    img = kit.finish_frame(img, global_idx, vignette=0.30, warmth=0.26, bloom=0.08)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
