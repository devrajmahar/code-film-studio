"""Shot 2: 320 km/h Shinkansen vs 55 km/h Indian Express — Split speed comparison."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import rail_kit

CAPS = film.SHOTS[1][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    split_y = kit.H // 2

    # --- TOP: Shinkansen streaking at 320 km/h with speed lines ---
    top = kit.make_sky_gradient((20, 78, 152), (76, 154, 218), (206, 234, 248), mid_pos=0.38)
    dt = ImageDraw.Draw(top)
    # Fast horizontal motion speed lines
    for i in range(28):
        ly = 220 + i * 24
        lx = ((i * 231 - sec * 1950) % (kit.W + 300)) - 150
        dt.line([(lx, ly), (lx + 160, ly)], fill=(224, 242, 255), width=2)

    rail_kit.draw_viaduct(dt, split_y - 120)
    # Fast streaking Shinkansen passing across center
    sx = 380 + math.sin(t * 3.14) * 380
    rail_kit.draw_shinkansen(dt, sx + 360, split_y - 130, length=880, height=106, facing=1)

    # Big glowing cyan speed readout on top (properly sized so text never overflows!)
    f_num = kit.get_font(78, bold=True)
    f_lbl = kit.get_font(28, bold=True)
    spd_j = int(kit.lerp(180, 320, kit.ease_out(min(1.0, t * 2.2))))
    dt.rounded_rectangle((68, 245, 530, 415), radius=18, fill=(14, 28, 46), outline=(56, 210, 248), width=4)
    dt.text((100, 260), f"{spd_j} km/h", font=f_num, fill=(92, 232, 255))
    dt.text((104, 360), "JAPAN · SHINKANSEN", font=f_lbl, fill=(226, 240, 250))

    # --- BOTTOM: Indian express crawling at 55 km/h ---
    bot = kit.make_sky_gradient((106, 86, 66), (168, 136, 98), (206, 174, 130), mid_pos=0.72)
    db = ImageDraw.Draw(bot)
    # Slow moving telegraph poles
    for i in range(5):
        px = ((i * 290 + sec * 95) % (kit.W + 200)) - 100
        db.line([(px, split_y + 120), (px, kit.H)], fill=kit.SMOG_INK, width=7)
    db.rectangle((0, split_y + 420, kit.W, kit.H), fill=(82, 74, 64))
    db.line([(0, split_y + 465), (kit.W, split_y + 465)], fill=(46, 40, 34), width=6)

    # Gently rocking slow Indian train
    bob = math.sin(sec * 16) * 2.5
    rail_kit.draw_indian_express(db, 890 - t * 140, split_y + 465 + bob, length=860, height=126, facing=-1)

    # Amber/red speed readout (properly sized so text never overflows!)
    spd_i = int(kit.lerp(30, 55, kit.ease_out(min(1.0, t * 2.2))))
    db.rounded_rectangle((68, split_y + 75, 530, split_y + 245), radius=18, fill=(42, 22, 20), outline=(228, 92, 68), width=4)
    db.text((100, split_y + 90), f"{spd_i} km/h", font=f_num, fill=(252, 136, 102))
    db.text((104, split_y + 190), "INDIA · AVG EXPRESS", font=f_lbl, fill=(244, 224, 210))

    comp = np.concatenate([np.array(top)[:split_y], np.array(bot)[split_y:]], axis=0)
    img = Image.fromarray(comp, mode="RGB")
    ImageDraw.Draw(img).line([(0, split_y), (kit.W, split_y)], fill=(252, 248, 238), width=6)

    img = kit.draw_shorts_badge(img, "SPEED  ·  320 KM/H vs 55 KM/H", y=148, accent=(56, 210, 248), bg=(16, 28, 44))
    img = kit.finish_frame(img, global_idx, vignette=0.22, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
