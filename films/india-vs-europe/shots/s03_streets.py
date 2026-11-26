"""Shot 3 (9:16 Shorts): Street Level — Gritty waste dump, rusted bin, tangled cables, autos."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[2][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    pan = -75 * t

    img = kit.make_sky_gradient((104, 86, 68), (168, 138, 102), (206, 174, 130), mid_pos=0.45)
    d = ImageDraw.Draw(img)

    # Tall dense 2.5D weathered concrete buildings towering in 9:16 frame
    bcols = [(142, 122, 104), (126, 108, 94), (150, 128, 108), (118, 104, 94), (138, 118, 100)]
    for i in range(6):
        bx = -60 + i * 225 + pan * 0.55
        bh = 620 + ((i * 89) % 240)
        kit.draw_chaotic_building_25d(d, bx, 1110, 220, bh, bcols[i % len(bcols)], seed=300 + i)

    # Cracked broken concrete sidewalk
    d.rectangle((0, 1105, kit.W, 1215), fill=(130, 118, 104), outline=kit.SMOG_INK, width=2)
    for c in range(9):
        cx = c * 155 + pan * 0.85
        d.line([(cx, 1108), (cx + 18, 1152), (cx - 12, 1212)], fill=(66, 58, 50), width=2)

    # Dusty potholed asphalt road
    d.rectangle((0, 1215, kit.W, kit.H), fill=(82, 76, 68))
    for px, py, rw, rh in [(260, 1340, 88, 28), (780, 1460, 105, 32), (480, 1650, 92, 26)]:
        d.ellipse((px + pan - rw, py - rh, px + pan + rw, py + rh), fill=(52, 46, 42), outline=kit.SMOG_INK, width=2)

    # Realistic gritty trash dumps with rusted municipal dumpster
    kit.draw_gritty_trash_dump(d, 310 + pan * 0.85, 1212, w=360, h=148, seed=11)
    kit.draw_gritty_trash_dump(d, 870 + pan * 0.85, 1212, w=380, h=156, seed=22)

    # Fluttering plastic bags blowing across street
    for i in range(6):
        bx = ((sec * (92 + i * 16) + i * 210) % (kit.W + 100)) - 50
        by = 1040 + math.sin(sec * 3.2 + i * 1.7) * 65 + (i % 3) * 45
        bcol = (224, 220, 210) if i % 2 == 0 else (188, 86, 72)
        d.polygon([(bx, by), (bx + 24, by - 12), (bx + 32, by + 12), (bx + 8, by + 20)], fill=bcol, outline=kit.SMOG_INK)

    # Detailed auto-rickshaws jostling with exhaust puffs
    auto_x1 = 1060 - sec * 115
    auto_x2 = 160 + sec * 95
    kit.draw_detailed_auto(d, auto_x1, 1320, scale=1.45, facing=-1, bob=math.sin(sec * 24) * 2.4)
    kit.draw_detailed_auto(d, auto_x2, 1390, scale=1.6, facing=1, bob=math.sin(sec * 28 + 1) * 2.8)

    for k in range(6):
        u = (sec * 2.2 + k * 0.16) % 1.0
        ex = auto_x2 - 92 - u * 125
        ey = 1368 - u * 42
        er = 12 + u * 32
        d.ellipse((ex - er, ey - er, ex + er, ey + er), fill=(108, 100, 90))

    # Crooked utility poles & heavy spiderweb of sagging overhead cables
    poles = [130, 560, 990]
    for idx, px in enumerate(poles):
        x0 = px + pan * 1.15
        lean = 20 if idx % 2 == 0 else -16
        d.line([(x0, 1230), (x0 + lean, 340)], fill=kit.SMOG_INK, width=11)
        d.line([(x0 + lean - 48, 390), (x0 + lean + 48, 382)], fill=kit.SMOG_INK, width=6)
        d.line([(x0 + lean - 40, 445), (x0 + lean + 44, 452)], fill=kit.SMOG_INK, width=5)

    for j in range(len(poles) - 1):
        x1 = poles[j] + pan * 1.15 + (20 if j % 2 == 0 else -16)
        x2 = poles[j + 1] + pan * 1.15 + (20 if (j + 1) % 2 == 0 else -16)
        for w_i in range(10):
            sag = 45 + w_i * 22 + math.sin(sec * 2.5 + w_i + j) * 5
            kit.draw_catenary(d, x1, 385 + w_i * 11, x2, 392 + ((w_i * 9) % 72), sag=sag, width=2)

    img = kit.add_smog_veil(img, sec, y_start=200, y_end=1200, color=(184, 152, 114), strength=0.25, speed=24)
    img = kit.draw_shorts_badge(img, "INDIA  ·  TRASH & TANGLED WIRES", y=148, accent=kit.RUST_RED, bg=(38, 24, 20))
    img = kit.finish_frame(img, global_idx, vignette=0.30, warmth=0.28, bloom=0.08)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
