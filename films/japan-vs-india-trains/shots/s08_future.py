"""Shot 8: The Transformation Wipe — Old congested tracks transforming into modern Indian high-speed rail."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import rail_kit

CAPS = film.SHOTS[7][5]


def _render_before(sec):
    img = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.45)
    d = ImageDraw.Draw(img)
    for i in range(6):
        kit.draw_chaotic_building_25d(d, -40 + i * 225, 1080, 218, 520 + ((i * 77) % 180), (118, 100, 88), seed=808 + i)
    d.rectangle((0, 1080, kit.W, kit.H), fill=(76, 68, 60))
    kit.draw_gritty_trash_dump(d, 260, 1260, w=320, h=110, seed=85)
    kit.draw_gritty_trash_dump(d, 840, 1270, w=320, h=115, seed=86)
    rail_kit.draw_indian_express(d, 860 - sec * 60, 1140, length=820, height=130, facing=-1)
    return kit.add_smog_veil(img, sec, y_start=200, y_end=1150, strength=0.30, speed=24)


def _render_after(sec):
    img = kit.make_sky_gradient((24, 92, 172), (96, 170, 228), (218, 240, 250), mid_pos=0.40)
    img = kit.add_sun_and_rays(img, 810, 290, 58, (255, 254, 238), (255, 242, 198), rays=True, ray_alpha=0.18)
    img = kit.add_painted_clouds_layer(img, sec, y_top=120, y_bot=580, density=0.44)
    d = ImageDraw.Draw(img)

    # Clean modern Indian skyline + lush boulevard trees below viaduct
    cols = [kit.CREAM_WALL, kit.OCHRE_WALL, kit.SAGE_WALL, kit.BLUSH_WALL]
    for i in range(6):
        kit.draw_euro_building_25d(d, -30 + i * 220, 1120, 212, 470 + ((i * 67) % 150), cols[i % len(cols)], kit.TERRACOTTA, stories=4)
    d.rectangle((0, 1120, kit.W, kit.H), fill=(88, 140, 82))
    for tx in (140, 480, 860):
        kit.draw_painterly_tree(d, tx, 1210, scale=0.95, sway=math.sin(sec * 1.6 + tx) * 0.3)

    # Modern elevated viaduct + sleek white-and-saffron Indian high-speed bullet train!
    rail_kit.draw_viaduct(d, 1085)
    rail_kit.draw_shinkansen(d, 340 + sec * 320, 1075, length=820, height=102, stripe_col=(234, 118, 34), facing=1)
    return img


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    wipe = kit.ease_in_out((t - 0.12) / 0.70)
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
        ImageDraw.Draw(img).line([(wx, 0), (wx, kit.H)], fill=(255, 252, 232), width=8)

    img = kit.draw_shorts_badge(img, "THE FUTURE  ·  HIGH-SPEED RAIL & DISCIPLINE", y=148, accent=(246, 178, 56), bg=(18, 42, 58))
    img = kit.finish_frame(img, global_idx, vignette=0.20, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
