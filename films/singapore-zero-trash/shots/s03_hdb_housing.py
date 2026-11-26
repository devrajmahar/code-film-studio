"""Shot 3: The Public Housing Revolution — Slums transforming into clean green HDB high-rises."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import sg_kit

CAPS = film.SHOTS[2][5]


def _render_slums(sec):
    img = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.50)
    d = ImageDraw.Draw(img)
    for i in range(6):
        sg_kit.draw_kampong_shack(d, -20 + i * 195, 1210, w=188, h=165 + ((i * 39) % 50), seed=300 + i)
    d.rectangle((0, 1210, kit.W, kit.H), fill=(82, 70, 56))
    kit.draw_gritty_trash_dump(d, 310, 1235, w=350, h=130, seed=31)
    kit.draw_gritty_trash_dump(d, 820, 1245, w=350, h=135, seed=32)
    return kit.add_smog_veil(img, sec, y_start=200, y_end=1250, strength=0.30, speed=22)


def _render_hdb(sec):
    img = kit.make_sky_gradient((22, 92, 174), (92, 172, 228), (214, 240, 250), mid_pos=0.40)
    img = kit.add_sun_and_rays(img, 820, 280, 58, (255, 254, 238), (255, 242, 198), rays=True, ray_alpha=0.18)
    img = kit.add_painted_clouds_layer(img, sec, y_top=120, y_bot=580, density=0.45)
    d = ImageDraw.Draw(img)

    accents = [(224, 108, 74), (64, 158, 138), (232, 174, 68), (78, 138, 194)]
    for i in range(5):
        bx = 35 + i * 210
        bh = 620 + ((i * 65) % 140)
        sg_kit.draw_hdb_tower(d, bx, 1180, w=192, h=bh, accent_col=accents[i % len(accents)])

    # Clean landscaped park courtyard & shaded walkways
    d.rectangle((0, 1180, kit.W, kit.H), fill=(84, 146, 82))
    d.polygon([(0, 1270), (kit.W, 1250), (kit.W, 1370), (0, 1395)], fill=(224, 218, 204), outline=kit.EURO_INK)
    for tx in (130, 390, 680, 950):
        kit.draw_painterly_tree(d, tx, 1245, scale=0.95, sway=math.sin(sec * 1.6 + tx) * 0.3)
    return img


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    # Vertical upward wipe: clean HDB towers rise up from bottom to top!
    wipe = kit.ease_in_out((t - 0.10) / 0.62)
    slums = np.array(_render_slums(sec))
    hdb = np.array(_render_hdb(sec))

    wy = int(kit.H * (1.0 - wipe))
    if wy >= kit.H:
        img = Image.fromarray(slums, mode="RGB")
    elif wy <= 0:
        img = Image.fromarray(hdb, mode="RGB")
    else:
        comp = np.concatenate([slums[:wy], hdb[wy:]], axis=0)
        img = Image.fromarray(comp, mode="RGB")
        ImageDraw.Draw(img).line([(0, wy), (kit.W, wy)], fill=(255, 252, 232), width=8)

    img = kit.draw_shorts_badge(img, "PUBLIC HOUSING  ·  80% IN CLEAN HDB TOWERS", y=148, accent=(62, 204, 136), bg=(18, 42, 56))
    img = kit.finish_frame(img, global_idx, vignette=0.20, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
