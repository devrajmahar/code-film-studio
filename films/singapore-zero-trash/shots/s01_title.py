"""Shot 1: SINGAPORE 1965 vs TODAY — Top Marina Bay Sands & Supertrees vs Bottom 1965 River Slums."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import sg_kit

CAPS = film.SHOTS[0][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    split_y = kit.H // 2

    # --- TOP: Futuristic Singapore Garden City ---
    top = kit.make_sky_gradient((18, 86, 168), (82, 166, 228), (208, 238, 250), mid_pos=0.36)
    top = kit.add_sun_and_rays(top, 840, 230, 56, (255, 253, 238), (255, 240, 196), rays=True, ray_alpha=0.18)
    top = kit.add_painted_clouds_layer(top, sec, y_top=80, y_bot=460, density=0.44)
    dt = ImageDraw.Draw(top)

    pan = 24 * t
    # Background financial towers
    for bx, bh, bw in [(70, 320, 110), (200, 380, 120), (780, 360, 115), (915, 310, 110)]:
        dt.rectangle((bx - pan * 0.4, split_y - 90 - bh, bx + bw - pan * 0.4, split_y - 90), fill=(122, 166, 204), outline=(74, 112, 148), width=2)

    # Iconic Marina Bay Sands centerpiece
    sg_kit.draw_marina_bay_sands(dt, 520 - pan * 0.6, split_y - 85, scale=1.05)

    # Supertree Grove & lush green waterfront
    dt.rectangle((0, split_y - 90, kit.W, split_y), fill=(52, 134, 178))
    for sx, sc in [(160, 0.78), (310, 0.92), (760, 0.90), (920, 0.76)]:
        sg_kit.draw_supertree(dt, sx + pan * 0.8, split_y - 75, scale=sc)
    for tx in (80, 240, 680, 840, 1000):
        kit.draw_painterly_tree(dt, tx + pan * 0.8, split_y - 68, scale=0.62, sway=math.sin(sec * 1.8 + tx) * 0.3)

    # --- BOTTOM: 1965 Kampong Slums & Trash-Choked River ---
    bot = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.72)
    db = ImageDraw.Draw(bot)
    for i in range(6):
        sg_kit.draw_kampong_shack(db, -20 + i * 190 - pan * 0.7, split_y + 520, w=182, h=150 + ((i * 37) % 45), seed=10 + i)

    # Murky polluted brown 1965 river + floating trash heaps
    db.rectangle((0, split_y + 505, kit.W, kit.H), fill=(76, 62, 44))
    kit.draw_gritty_trash_dump(db, 250 - pan * 0.8, split_y + 545, w=330, h=110, seed=11)
    kit.draw_gritty_trash_dump(db, 830 - pan * 0.8, split_y + 555, w=340, h=115, seed=12)
    bot = kit.add_smog_veil(bot, sec, y_start=split_y, y_end=kit.H, strength=0.32, speed=24)

    comp = np.concatenate([np.array(top)[:split_y], np.array(bot)[split_y:]], axis=0)
    img = Image.fromarray(comp, mode="RGB")
    ImageDraw.Draw(img).line([(0, split_y), (kit.W, split_y)], fill=(252, 248, 238), width=6)

    # Centerpiece title banner
    ta = kit.ease_out(min(1.0, t * 3.0))
    ov = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    by = split_y - 118
    od.rectangle((0, by, kit.W, by + 236), fill=(14, 17, 22, int(214 * ta)))
    f_big = kit.get_font(90, bold=True, serif=True)
    f_sub = kit.get_font(30, bold=True)
    t1 = "1965 vs TODAY"
    b1 = od.textbbox((0, 0), t1, font=f_big)
    od.text((kit.W / 2 - (b1[2] - b1[0]) / 2, by + 32), t1, font=f_big, fill=(252, 248, 240, int(255 * ta)))
    t2 = "HOW SINGAPORE ERASED ITS SLUMS & TRASH"
    b2 = od.textbbox((0, 0), t2, font=f_sub)
    od.text((kit.W / 2 - (b2[2] - b2[0]) / 2, by + 162), t2, font=f_sub, fill=(102, 242, 168, int(245 * ta)))

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    img = kit.finish_frame(img, global_idx, vignette=0.24, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
