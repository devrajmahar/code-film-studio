"""Shot 1 (9:16 Shorts): Top-vs-Bottom Split Horizon — Clean European Sky vs Smoggy Skyline."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[0][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    split_y = kit.H // 2

    # --- TOP HALF: Crisp Alpine-lit European skyline ---
    top = kit.make_sky_gradient(kit.EURO_TOP, kit.EURO_MID, kit.EURO_BOT, mid_pos=0.35)
    top = kit.add_sun_and_rays(top, 820, 260, 56, (255, 253, 236), (255, 240, 194), rays=True, ray_alpha=0.16)
    top = kit.add_painted_clouds_layer(top, sec, y_top=90, y_bot=520, density=0.46)
    dt = ImageDraw.Draw(top)

    pan_r = 22 * t
    # Distant snow-capped Alps
    alps = [
        (-40, 740), (160 + pan_r * 0.3, 520), (350 + pan_r * 0.3, 620),
        (560 + pan_r * 0.3, 470), (770 + pan_r * 0.3, 595), (960 + pan_r * 0.3, 505),
        (kit.W + 40, 650), (kit.W + 40, split_y), (-40, split_y),
    ]
    dt.polygon(alps, fill=(130, 168, 206), outline=(92, 132, 172))
    for px, py in [(160, 520), (560, 470), (960, 505)]:
        sx = px + pan_r * 0.3
        dt.polygon([(sx, py), (sx - 44, py + 58), (sx + 48, py + 54)], fill=(248, 250, 255))

    # 2.5D European townhouses
    euro_b = [
        (-20, 270, 190, kit.CREAM_WALL, kit.TERRACOTTA, False),
        (165, 325, 205, kit.OCHRE_WALL, kit.SLATE_ROOF, False),
        (365, 290, 195, kit.SAGE_WALL, kit.TERRACOTTA, True),
        (555, 315, 210, kit.CREAM_WALL, kit.TERRACOTTA, False),
        (760, 280, 195, kit.BLUSH_WALL, kit.SLATE_ROOF, False),
        (950, 310, 195, kit.OCHRE_WALL, kit.TERRACOTTA, False),
    ]
    for bx, bh, bw, wcol, rcol, sp in euro_b:
        kit.draw_euro_building_25d(dt, bx - pan_r, split_y - 24, bw, bh, wcol, rcol, stories=4, spire=sp)

    for tx in (110, 440, 790, 1020):
        kit.draw_painterly_tree(dt, tx - pan_r * 1.1, split_y - 16, scale=0.68, sway=math.sin(sec * 1.7 + tx) * 0.3)

    for i in range(5):
        kit.draw_bird(dt, ((sec * 58 + i * 230) % (kit.W + 80)) - 40, 240 + i * 32, size=11, phase=sec * 7.5 + i)

    dt.rectangle((0, split_y - 24, kit.W, split_y), fill=(68, 114, 84))

    # --- BOTTOM HALF: Dense smoggy urban skyline + tangled poles ---
    bot = kit.make_sky_gradient(kit.SMOG_TOP, kit.SMOG_MID, kit.SMOG_BOT, mid_pos=0.72)
    bot = kit.add_sun_and_rays(bot, 260, split_y + 210, 68, (238, 196, 134), (194, 146, 94), rays=False, halo_alpha=0.52)
    db = ImageDraw.Draw(bot)

    pan_l = -24 * t
    # Far hazy towers
    for i in range(8):
        bx = -30 + i * 160 + pan_l * 0.45
        bh = 330 + ((i * 83) % 210)
        db.rectangle((bx, kit.H - 180 - bh, bx + 135, kit.H - 180), fill=(122, 102, 84))

    # Mid 2.5D chaotic blocks
    for i in range(6):
        bx = -40 + i * 210 + pan_l * 0.9
        bh = 360 + ((i * 97) % 190)
        kit.draw_chaotic_building_25d(db, bx, kit.H - 140, 200, bh, (108, 92, 78), seed=10 + i)

    # Foreground tangled overhead wires
    poles = [120, 540, 960]
    for px in poles:
        x0 = px + pan_l * 1.3
        db.line([(x0, kit.H), (x0 + 16, split_y + 220)], fill=kit.SMOG_INK, width=10)
        db.line([(x0 - 38, split_y + 260), (x0 + 62, split_y + 252)], fill=kit.SMOG_INK, width=5)
    for w_i in range(7):
        sag = 38 + w_i * 16 + math.sin(sec * 2.2 + w_i) * 4
        kit.draw_catenary(db, -30, split_y + 258 + w_i * 9, 556 + pan_l * 1.3, split_y + 255 + w_i * 7, sag=sag, width=2)
        kit.draw_catenary(db, 556 + pan_l * 1.3, split_y + 255 + w_i * 7, kit.W + 30, split_y + 266 + w_i * 9, sag=sag * 0.95, width=2)

    db.rectangle((0, kit.H - 140, kit.W, kit.H), fill=(48, 42, 36))
    bot = kit.add_smog_veil(bot, sec, y_start=split_y, y_end=kit.H, strength=0.38, speed=32)

    # Composite Top + Bottom
    comp = np.concatenate([np.array(top)[:split_y], np.array(bot)[split_y:]], axis=0)
    img = Image.fromarray(comp, mode="RGB")

    # Crisp divider & editorial title centerpiece
    d = ImageDraw.Draw(img)
    d.line([(0, split_y), (kit.W, split_y)], fill=(252, 248, 238), width=6)

    title_a = kit.ease_out(min(1.0, t * 2.8))
    overlay = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    band_h = 240
    by = split_y - band_h // 2
    od.rectangle((0, by, kit.W, by + band_h), fill=(14, 17, 22, int(205 * title_a)))
    f_big = kit.get_font(96, bold=True, serif=True)
    f_sub = kit.get_font(30, bold=True)

    t1 = "INDIA vs EUROPE"
    b1 = od.textbbox((0, 0), t1, font=f_big)
    od.text((kit.W / 2 - (b1[2] - b1[0]) / 2, by + 34 + int((1 - title_a) * 20)), t1, font=f_big, fill=(252, 248, 240, int(255 * title_a)))
    t2 = "WHY EUROPE BREATHES — AND INDIA CHOKES"
    b2 = od.textbbox((0, 0), t2, font=f_sub)
    od.text((kit.W / 2 - (b2[2] - b2[0]) / 2, by + 168 + int((1 - title_a) * 20)), t2, font=f_sub, fill=(248, 204, 108, int(245 * title_a)))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = kit.finish_frame(img, global_idx, vignette=0.26, bloom=0.14)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
