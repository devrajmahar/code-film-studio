"""Shot 7: The 10-Year Singapore River Cleanup — 1977 Sludge wiping to Sparkling Marina Bay."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import sg_kit

CAPS = film.SHOTS[6][5]


def _render_dirty(sec):
    img = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.48)
    d = ImageDraw.Draw(img)
    for i in range(6):
        sg_kit.draw_kampong_shack(d, -20 + i * 195, 1040, w=185, h=155 + ((i * 31) % 45), seed=700 + i)
    d.rectangle((0, 1030, kit.W, kit.H), fill=(74, 58, 42))
    kit.draw_gritty_trash_dump(d, 280, 1065, w=340, h=125, seed=71)
    kit.draw_gritty_trash_dump(d, 820, 1075, w=340, h=130, seed=72)
    return kit.add_smog_veil(img, sec, y_start=200, y_end=1100, strength=0.30, speed=22)


def _render_clean(sec):
    img = kit.make_sky_gradient((20, 92, 174), (92, 172, 228), (214, 240, 250), mid_pos=0.40)
    img = kit.add_sun_and_rays(img, 810, 280, 58, (255, 254, 238), (255, 242, 198), rays=True, ray_alpha=0.18)
    img = kit.add_painted_clouds_layer(img, sec, y_top=110, y_bot=540, density=0.44)
    d = ImageDraw.Draw(img)

    # Restored pastel shophouses along Clarke Quay / Boat Quay + modern towers behind
    for bx, bh in [(80, 520), (310, 580), (620, 560), (850, 510)]:
        d.rectangle((bx, 1010 - bh, bx + 150, 1010), fill=(126, 172, 208), outline=(74, 114, 152), width=2)

    cols = [kit.CREAM_WALL, kit.OCHRE_WALL, kit.SAGE_WALL, kit.BLUSH_WALL]
    for i in range(6):
        kit.draw_euro_building_25d(d, -20 + i * 190, 1020, 182, 260 + ((i * 41) % 60), cols[i % len(cols)], kit.TERRACOTTA, stories=3, café=True)

    # Clean stone river promenade + trees
    d.rectangle((0, 1020, kit.W, 1085), fill=(224, 218, 204), outline=kit.EURO_INK, width=2)
    for tx in (130, 440, 740, 980):
        kit.draw_painterly_tree(d, tx, 1055, scale=0.78, sway=math.sin(sec * 1.6 + tx) * 0.3)

    # Sparkling turquoise Singapore River
    d.rectangle((0, 1085, kit.W, kit.H), fill=(42, 138, 184))
    for r in range(28):
        ry = 1108 + r * 14
        rx = ((r * 211 + sec * 32) % (kit.W + 100)) - 50
        d.line([(rx, ry), (rx + 64, ry)], fill=(182, 232, 250), width=2)
    return img


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    wipe = kit.ease_in_out((t - 0.12) / 0.66)
    dirty = np.array(_render_dirty(sec))
    clean = np.array(_render_clean(sec))

    wx = int(kit.W * wipe)
    if wx <= 0:
        img = Image.fromarray(dirty, mode="RGB")
    elif wx >= kit.W:
        img = Image.fromarray(clean, mode="RGB")
    else:
        comp = np.concatenate([clean[:, :wx], dirty[:, wx:]], axis=1)
        img = Image.fromarray(comp, mode="RGB")
        ImageDraw.Draw(img).line([(wx, 0), (wx, kit.H)], fill=(255, 252, 232), width=8)

    img = kit.draw_shorts_badge(img, "SINGAPORE RIVER  ·  10-YEAR CLEANUP REVIVAL", y=148, accent=(58, 206, 174), bg=(16, 40, 54))
    img = kit.finish_frame(img, global_idx, vignette=0.18, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
