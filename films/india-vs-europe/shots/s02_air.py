"""Shot 2 (9:16 Shorts): The Air — AQI 438 Hazardous Smog wiping vertically to AQI 18 Alpine Riverfront."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[1][5]


def _render_smog(t, sec):
    img = kit.make_sky_gradient((96, 76, 58), (168, 134, 96), (208, 172, 126), mid_pos=0.52)
    img = kit.add_sun_and_rays(img, 760 - 25 * t, 460, 78, (242, 202, 140), (198, 150, 96), rays=False, halo_alpha=0.62)
    d = ImageDraw.Draw(img)

    pan = -65 * t
    # Far hazy skyline
    for i in range(9):
        bx = -40 + i * 145 + pan * 0.4
        bh = 440 + ((i * 73) % 260)
        d.rectangle((bx, 1380 - bh, bx + 122, 1380), fill=(138, 114, 92))

    # Mid buildings + belching industrial chimney
    for i in range(6):
        bx = -50 + i * 215 + pan * 0.85
        bh = 420 + ((i * 97) % 240)
        kit.draw_chaotic_building_25d(d, bx, 1460, 202, bh, (104, 88, 76), seed=200 + i)

    sx = 180 + pan * 0.85
    d.polygon([(sx, 1460), (sx + 68, 1460), (sx + 50, 740), (sx + 18, 740)], fill=(64, 56, 50), outline=kit.SMOG_INK)
    for k in range(12):
        u = (sec * 0.42 + k * 0.083) % 1.0
        px = sx + 34 + u * 480 + math.sin(u * 5 + k) * 22
        py = 735 - u * 310
        pr = 26 + u * 78
        d.ellipse((px - pr, py - pr * 0.72, px + pr, py + pr * 0.72), fill=(122, 104, 88))

    d.rectangle((0, 1455, kit.W, kit.H), fill=(52, 44, 38))
    img = kit.add_smog_veil(img, sec, y_start=260, y_end=1550, color=(188, 154, 112), strength=0.45, speed=38)

    # Floating PM2.5 particles
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(202)
    for _ in range(110):
        mx = (rng.uniform(0, kit.W) + sec * rng.uniform(22, 56)) % kit.W
        my = rng.uniform(240, 1460) + math.sin(sec * 1.5 + mx * 0.01) * 10
        r = rng.uniform(2.0, 4.8)
        d.ellipse((mx - r, my - r, mx + r, my + r), fill=(224, 196, 152))

    aqi_val = int(kit.lerp(190, 438, kit.ease_out(min(1.0, t * 2.2))))
    img = kit.draw_shorts_badge(img, f"INDIA  ·  AQI {aqi_val} HAZARDOUS", y=148, accent=kit.HAZARD_PURPLE, bg=(38, 18, 28))
    return img


def _render_clean(t, sec):
    img = kit.make_sky_gradient((22, 86, 164), (84, 158, 222), (206, 236, 250), mid_pos=0.46)
    img = kit.add_sun_and_rays(img, 810, 390, 62, (255, 254, 240), (255, 242, 200), rays=True, ray_alpha=0.18)
    img = kit.add_painted_clouds_layer(img, sec, y_top=160, y_bot=780, density=0.48)
    d = ImageDraw.Draw(img)

    pan = 45 * t
    # Crisp snow-capped Alps
    alps = [
        (-40, 1180), (140 + pan * 0.3, 740), (340 + pan * 0.3, 890),
        (560 + pan * 0.3, 660), (790 + pan * 0.3, 850), (980 + pan * 0.3, 710),
        (kit.W + 40, 920), (kit.W + 40, 1320), (-40, 1320),
    ]
    d.polygon(alps, fill=(122, 164, 204), outline=(82, 124, 166))
    for px, py in [(140, 740), (560, 660), (980, 710)]:
        sx = px + pan * 0.3
        d.polygon([(sx, py), (sx - 56, py + 78), (sx + 62, py + 72)], fill=(248, 252, 255))

    # Sunlit European lakeside town
    b_specs = [
        (-20, 290, 185, kit.CREAM_WALL, kit.TERRACOTTA, False),
        (165, 345, 205, kit.OCHRE_WALL, kit.SLATE_ROOF, False),
        (370, 315, 195, kit.SAGE_WALL, kit.TERRACOTTA, True),
        (565, 330, 210, kit.CREAM_WALL, kit.TERRACOTTA, False),
        (775, 295, 190, kit.BLUSH_WALL, kit.SLATE_ROOF, False),
        (965, 335, 195, kit.OCHRE_WALL, kit.TERRACOTTA, False),
    ]
    for bx, bh, bw, wcol, rcol, sp in b_specs:
        kit.draw_euro_building_25d(d, bx - pan * 0.65, 1230, bw, bh, wcol, rcol, stories=4, spire=sp)

    # Shimmering Alpine river/lake
    d.rectangle((0, 1230, kit.W, kit.H), fill=kit.RIVER_BLUE)
    for r in range(36):
        ry = 1255 + r * 16
        rx = ((r * 197 + sec * (32 + (r % 4) * 10)) % (kit.W + 120)) - 60
        d.line([(rx, ry), (rx + 56, ry)], fill=(182, 226, 248), width=3)

    for i in range(6):
        kit.draw_bird(d, ((sec * 64 + i * 210) % (kit.W + 80)) - 40, 420 + (i % 3) * 52, size=13, phase=sec * 7.5 + i)

    img = kit.draw_shorts_badge(img, "EUROPE  ·  AQI 18 CLEAR AIR", y=148, accent=(58, 196, 132), bg=(16, 42, 56))
    return img


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    wipe = kit.ease_in_out((t - 0.45) / 0.14)
    if wipe <= 0.001:
        img = _render_smog(t, sec)
        img = kit.finish_frame(img, global_idx, vignette=0.28, warmth=0.32, bloom=0.10)
    elif wipe >= 0.999:
        img = _render_clean(t, sec)
        img = kit.finish_frame(img, global_idx, vignette=0.18, warmth=-0.06, bloom=0.18)
    else:
        smog = np.array(_render_smog(t, sec))
        clean = np.array(_render_clean(t, sec))
        wy = int(kit.H * wipe)
        comp = np.concatenate([clean[:wy], smog[wy:]], axis=0)
        img = Image.fromarray(comp, mode="RGB")
        d = ImageDraw.Draw(img)
        d.line([(0, wy), (kit.W, wy)], fill=(252, 250, 242), width=7)
        img = kit.finish_frame(img, global_idx, vignette=0.22, bloom=0.15)

    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
