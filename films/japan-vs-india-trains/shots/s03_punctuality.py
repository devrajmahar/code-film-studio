"""Shot 3: Punctuality — 24 Seconds Average Delay vs 4 Hours Late LED Departure Boards."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[2][5]


def _draw_clock(d, cx, cy, r, minute_angle, sec_angle, accent):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(246, 246, 242), outline=(34, 42, 54), width=6)
    for h in range(12):
        a = h * math.pi / 6
        d.line([(cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78),
                (cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)], fill=(34, 42, 54), width=4)
    # Minute & hour hands
    d.line([(cx, cy), (cx + math.cos(minute_angle) * r * 0.68, cy + math.sin(minute_angle) * r * 0.68)], fill=(24, 30, 38), width=6)
    d.line([(cx, cy), (cx + math.cos(sec_angle) * r * 0.76, cy + math.sin(sec_angle) * r * 0.76)], fill=accent, width=3)
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=accent)


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((16, 24, 36), (22, 32, 46), (14, 18, 26), mid_pos=0.5)
    d = ImageDraw.Draw(img)

    # Subtle station grid background
    for gx in range(0, kit.W, 64):
        d.line([(gx, 0), (gx, kit.H)], fill=(24, 36, 52), width=1)
    for gy in range(0, kit.H, 64):
        d.line([(0, gy), (kit.W, gy)], fill=(24, 36, 52), width=1)

    f_hdr = kit.get_font(34, bold=True)
    f_big = kit.get_font(86, bold=True)
    f_row = kit.get_font(32, bold=True)

    # --- TOP CARD: JAPAN SHINKANSEN BOARD ---
    d.rounded_rectangle((64, 270, kit.W - 64, 780), radius=24, fill=(14, 30, 38), outline=(58, 212, 146), width=4)
    d.text((104, 305), "JAPAN · JR TOKAI SHINKANSEN", font=f_hdr, fill=(104, 236, 176))
    d.line([(100, 358), (kit.W - 100, 358)], fill=(44, 88, 76), width=2)
    d.text((104, 390), "NOZOMI 24   TOKYO", font=f_row, fill=(242, 248, 246))
    d.text((104, 444), "STATUS:  ON TIME", font=f_row, fill=(84, 238, 158))
    d.text((104, 545), "24 SEC", font=f_big, fill=(92, 248, 172))
    d.text((104, 650), "AVERAGE ANNUAL DELAY", font=f_row, fill=(182, 214, 202))
    _draw_clock(d, 845, 555, 118, -math.pi / 2 + 0.04, -math.pi / 2 + sec * 0.6, (58, 212, 146))

    # --- BOTTOM CARD: INDIA DELAY BOARD ---
    d.rounded_rectangle((64, 845, kit.W - 64, 1355), radius=24, fill=(38, 18, 20), outline=(236, 82, 66), width=4)
    d.text((104, 880), "INDIA · NORTHERN RAILWAYS", font=f_hdr, fill=(248, 128, 112))
    d.line([(100, 933), (kit.W - 100, 933)], fill=(96, 46, 44), width=2)
    d.text((104, 965), "12302 EXP   NEW DELHI", font=f_row, fill=(248, 236, 228))
    blink = (int(sec * 3) % 2) == 0
    d.text((104, 1019), "STATUS:  DELAYED", font=f_row, fill=(255, 92, 76) if blink else (180, 62, 52))
    hrs = kit.lerp(1.0, 4.25, kit.ease_out(min(1.0, t * 2.0)))
    d.text((104, 1120), f"{int(hrs)}H {int((hrs % 1) * 60):02d}M", font=f_big, fill=(255, 118, 92))
    d.text((104, 1225), "LATE ARRIVAL", font=f_row, fill=(224, 186, 174))
    # Rapidly spinning delay clock!
    _draw_clock(d, 845, 1130, 118, -math.pi / 2 + t * 18.0, -math.pi / 2 + t * 72.0, (236, 82, 66))

    img = kit.draw_shorts_badge(img, "PUNCTUALITY  ·  24 SEC vs 4 HOURS", y=148, accent=(248, 204, 108), bg=(20, 26, 36))
    img = kit.finish_frame(img, global_idx, vignette=0.26, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
