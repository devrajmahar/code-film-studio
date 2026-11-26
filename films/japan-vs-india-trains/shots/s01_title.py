"""Shot 1: JAPAN vs INDIA — Top Shinkansen + Mt Fuji vs Bottom Indian Express."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import rail_kit

CAPS = film.SHOTS[0][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    split_y = kit.H // 2

    # --- TOP: Shinkansen gliding past Mount Fuji & cherry blossoms ---
    top = kit.make_sky_gradient((24, 86, 164), (92, 166, 226), (218, 238, 250), mid_pos=0.35)
    top = kit.add_sun_and_rays(top, 840, 240, 54, (255, 253, 238), (255, 240, 198), rays=True, ray_alpha=0.16)
    top = kit.add_painted_clouds_layer(top, sec, y_top=90, y_bot=460, density=0.44)
    dt = ImageDraw.Draw(top)

    rail_kit.draw_mt_fuji(dt, 540, split_y - 120, width=880, height=380)
    # Green foothills
    dt.rectangle((0, split_y - 145, kit.W, split_y), fill=(76, 126, 86))
    for tx in (120, 340, 780, 990):
        rail_kit.draw_sakura_tree(dt, tx, split_y - 90, scale=0.85, sway=math.sin(sec * 2 + tx) * 0.35)

    # Clean elevated viaduct + bullet train streaking right
    rail_kit.draw_viaduct(dt, split_y - 95)
    nose_x = 120 + t * 1450
    rail_kit.draw_shinkansen(dt, nose_x, split_y - 105, length=820, height=92, facing=1)

    # --- BOTTOM: Crowded Indian express rumbling through hazy clutter ---
    bot = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.72)
    db = ImageDraw.Draw(bot)
    for i in range(6):
        kit.draw_chaotic_building_25d(db, -30 + i * 215, split_y + 520, 205, 340 + ((i * 79) % 160), (112, 96, 82), seed=101 + i)

    # Ballast & cluttered rail bed
    db.rectangle((0, split_y + 520, kit.W, kit.H), fill=(78, 70, 62))
    db.line([(0, split_y + 592), (kit.W, split_y + 592)], fill=(44, 38, 34), width=6)
    kit.draw_gritty_trash_dump(db, 210, split_y + 685, w=280, h=95, seed=19)
    kit.draw_gritty_trash_dump(db, 860, split_y + 695, w=300, h=100, seed=27)

    # Slow chugging blue Indian express
    front_x = 920 - t * 240
    rail_kit.draw_indian_express(db, front_x, split_y + 592, length=820, height=122, facing=-1)
    bot = kit.add_smog_veil(bot, sec, y_start=split_y, y_end=kit.H, strength=0.32, speed=26)

    # Composite
    comp = np.concatenate([np.array(top)[:split_y], np.array(bot)[split_y:]], axis=0)
    img = Image.fromarray(comp, mode="RGB")
    d = ImageDraw.Draw(img)
    d.line([(0, split_y), (kit.W, split_y)], fill=(252, 248, 238), width=6)

    # Centerpiece title banner
    ta = kit.ease_out(min(1.0, t * 3.0))
    ov = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    by = split_y - 118
    od.rectangle((0, by, kit.W, by + 236), fill=(14, 17, 22, int(212 * ta)))
    f_big = kit.get_font(96, bold=True, serif=True)
    f_sub = kit.get_font(30, bold=True)
    t1 = "JAPAN vs INDIA"
    b1 = od.textbbox((0, 0), t1, font=f_big)
    od.text((kit.W / 2 - (b1[2] - b1[0]) / 2, by + 30), t1, font=f_big, fill=(252, 248, 240, int(255 * ta)))
    t2 = "TRAINS, SPEED & NATIONAL DISCIPLINE"
    b2 = od.textbbox((0, 0), t2, font=f_sub)
    od.text((kit.W / 2 - (b2[2] - b2[0]) / 2, by + 162), t2, font=f_sub, fill=(248, 204, 108, int(245 * ta)))

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    img = kit.finish_frame(img, global_idx, vignette=0.24, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
