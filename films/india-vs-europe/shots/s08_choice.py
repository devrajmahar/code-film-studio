"""Shot 8 (9:16 Shorts): The Turning Point — Sweeping transformation wipe from chaos to clean boulevard."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[7][5]


def _render_before(sec):
    img = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.45)
    d = ImageDraw.Draw(img)
    for i in range(6):
        kit.draw_chaotic_building_25d(d, -40 + i * 225, 1110, 218, 560 + ((i * 77) % 190), (124, 106, 92), seed=800 + i)
    d.rectangle((0, 1110, kit.W, 1215), fill=(128, 116, 102))
    d.rectangle((0, 1215, kit.W, kit.H), fill=(78, 72, 64))
    kit.draw_gritty_trash_dump(d, 310, 1212, w=340, h=140, seed=81)
    kit.draw_gritty_trash_dump(d, 840, 1212, w=350, h=145, seed=82)
    for px in (150, 560, 960):
        d.line([(px, 1225), (px + 16, 360)], fill=kit.SMOG_INK, width=10)
    for w_i in range(8):
        kit.draw_catenary(d, 166, 395 + w_i * 12, 576, 405 + w_i * 10, sag=52 + w_i * 16, width=2)
        kit.draw_catenary(d, 576, 405 + w_i * 10, 976, 396 + w_i * 12, sag=48 + w_i * 16, width=2)
    kit.draw_detailed_auto(d, 740 - sec * 52, 1345, scale=1.5, facing=-1, bob=math.sin(sec * 20) * 2)
    img = kit.add_smog_veil(img, sec, y_start=200, y_end=1180, strength=0.32, speed=26)
    return img


def _render_after(sec):
    img = kit.make_sky_gradient((26, 96, 178), (98, 172, 228), (216, 240, 250), mid_pos=0.40)
    img = kit.add_sun_and_rays(img, 820, 310, 60, (255, 254, 236), (255, 242, 198), rays=True, ray_alpha=0.18)
    img = kit.add_painted_clouds_layer(img, sec, y_top=120, y_bot=600, density=0.44)
    d = ImageDraw.Draw(img)

    cols = [kit.CREAM_WALL, kit.OCHRE_WALL, kit.SAGE_WALL, kit.BLUSH_WALL]
    for i in range(6):
        kit.draw_euro_building_25d(d, -40 + i * 225, 1110, 218, 540 + ((i * 77) % 160), cols[i % len(cols)], kit.TERRACOTTA, stories=5, café=(i % 2 == 0))

    d.rectangle((0, 1110, kit.W, 1220), fill=(218, 212, 198), outline=kit.EURO_INK, width=2)
    for tx in (140, 540, 940):
        kit.draw_painterly_tree(d, tx, 1170, scale=1.05, sway=math.sin(sec * 1.5 + tx) * 0.3)

    d.rectangle((0, 1220, kit.W, 1300), fill=kit.BIKE_BRICK, outline=kit.EURO_INK, width=2)
    d.rectangle((0, 1300, kit.W, kit.H), fill=(112, 120, 128))
    for dash in range(10):
        d.line([(dash * 130 + 20, 1392), (dash * 130 + 82, 1392)], fill=(244, 242, 234), width=4)

    kit.draw_cyclist(d, 560 + sec * 105, 1282, scale=1.02, phase=sec * 8.0, coat_col=(44, 116, 92))
    kit.draw_detailed_tram(d, 110 + sec * 110, 1396, length=520, height=132)
    for i in range(5):
        kit.draw_bird(d, ((sec * 56 + i * 240) % (kit.W + 80)) - 40, 320 + i * 42, size=12, phase=sec * 7 + i)
    return img


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    wipe = kit.ease_in_out((t - 0.14) / 0.68)
    before = np.array(_render_before(sec))
    after = np.array(_render_after(sec))

    wx = int(kit.W * wipe)
    if wx <= 0:
        img = Image.fromarray(before, mode="RGB")
    elif wx >= kit.W:
        img = Image.fromarray(after, mode="RGB")
    else:
        comp = np.concatenate([after[:, :wx], before[:, wx:]], axis=1)
        img = Image.fromarray(comp, mode="RGB")
        d = ImageDraw.Draw(img)
        d.line([(wx, 0), (wx, kit.H)], fill=(255, 252, 232), width=8)

    img = kit.draw_shorts_badge(img, "THE CHOICE  ·  INDIA CAN BUILD THIS TOO", y=148, accent=(246, 198, 76), bg=(18, 42, 58))
    img = kit.finish_frame(img, global_idx, vignette=0.20, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
