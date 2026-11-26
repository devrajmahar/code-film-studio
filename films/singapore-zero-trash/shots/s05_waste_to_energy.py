"""Shot 5: The Secret Machine — 1,000°C Waste-to-Energy Incineration & 90% Volume Reduction Blueprint."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[4][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((14, 24, 38), (20, 32, 48), (12, 18, 28), mid_pos=0.5)
    d = ImageDraw.Draw(img)
    for gx in range(0, kit.W, 60):
        d.line([(gx, 0), (gx, kit.H)], fill=(24, 38, 56), width=1)
    for gy in range(0, kit.H, 60):
        d.line([(0, gy), (kit.W, gy)], fill=(24, 38, 56), width=1)

    f_hdr = kit.get_font(30, bold=True)
    f_big = kit.get_font(62, bold=True)
    f_lbl = kit.get_font(24, bold=True)

    # Stage 1 (Top): Sealed Waste Intake -> 1,000°C Furnace
    d.rounded_rectangle((64, 265, kit.W - 64, 765), radius=22, fill=(24, 34, 48), outline=(248, 134, 62), width=4)
    d.text((100, 292), "24/7 WASTE-TO-ENERGY PLANT (TUAS NEXUS)", font=f_hdr, fill=(252, 166, 92))
    d.text((100, 340), "BURNS TRASH AT 1,000°C  ·  SCRUBS 99.9% OF FLUE GAS", font=f_lbl, fill=(208, 222, 236))

    # Animated glowing furnace core
    fx0, fy0, fx1, fy1 = 104, 415, 560, 715
    d.rounded_rectangle((fx0, fy0, fx1, fy1), radius=16, fill=(44, 22, 20), outline=(252, 146, 68), width=3)
    for k in range(7):
        flame_h = 85 + math.sin(sec * 12 + k * 1.4) * 32
        cx = fx0 + 48 + k * 62
        d.polygon([(cx - 28, fy1 - 12), (cx, fy1 - 12 - flame_h), (cx + 28, fy1 - 12)], fill=(252, 132, 48))
        d.polygon([(cx - 14, fy1 - 12), (cx, fy1 - 12 - flame_h * 0.65), (cx + 14, fy1 - 12)], fill=(255, 224, 96))
    d.text((fx0 + 36, fy0 + 24), "1,000°C FURNACE", font=f_hdr, fill=(255, 232, 164))

    # Volume reduction bar chart on right of card 1 (100% Trash -> 10% Ash!)
    d.rectangle((635, 445, 735, 685), fill=(156, 134, 114), outline=(236, 232, 224), width=2)
    d.text((626, 405), "100% TRASH", font=f_lbl, fill=(224, 216, 206))
    d.text((765, 550), "→", font=f_big, fill=(252, 186, 82))
    ash_h = int(240 * 0.12)
    d.rectangle((835, 685 - ash_h, 935, 685), fill=(82, 224, 152), outline=(236, 248, 240), width=2)
    d.text((828, 610), "10% ASH", font=f_lbl, fill=(104, 246, 172))

    # Stage 2 (Bottom): Clean Electricity Grid Output + 90% Reduction Stat
    d.rounded_rectangle((64, 830, kit.W - 64, 1345), radius=22, fill=(16, 36, 44), outline=(64, 224, 156), width=4)
    d.text((100, 862), "RESULT:  -90% WASTE VOLUME  +  CLEAN POWER", font=f_hdr, fill=(96, 242, 172))

    # Animated power conduit feeding city buildings
    py = 1045
    d.rounded_rectangle((100, py - 24, kit.W - 100, py + 24), radius=12, fill=(26, 54, 66), outline=(82, 212, 168), width=2)
    d.line([(120, py), (kit.W - 120, py)], fill=(86, 246, 174), width=10)
    for p in range(6):
        px = 125 + ((sec * 260 + p * 140) % (kit.W - 260))
        d.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(255, 255, 240))

    d.text((104, 1135), "-90% VOLUME", font=f_big, fill=(102, 248, 176))
    d.text((104, 1235), "POWERS THOUSANDS OF HDB HOMES DAILY", font=f_lbl, fill=(198, 228, 216))

    img = kit.draw_shorts_badge(img, "WASTE-TO-ENERGY  ·  1,000°C INCINERATION", y=148, accent=(252, 152, 72), bg=(20, 28, 40))
    img = kit.finish_frame(img, global_idx, vignette=0.24, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
