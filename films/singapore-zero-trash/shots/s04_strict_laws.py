"""Shot 4: Strict Civic Enforcement — Fines, CWO cleanup enforcement & spotless underground bins."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[3][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((16, 26, 40), (22, 36, 54), (14, 20, 32), mid_pos=0.5)
    d = ImageDraw.Draw(img)
    for gx in range(0, kit.W, 60):
        d.line([(gx, 0), (gx, kit.H)], fill=(26, 42, 62), width=1)
    for gy in range(0, kit.H, 60):
        d.line([(0, gy), (kit.W, gy)], fill=(26, 42, 62), width=1)

    f_hdr = kit.get_font(32, bold=True)
    f_big = kit.get_font(68, bold=True)
    f_row = kit.get_font(28, bold=True)

    # Three punchy animated enforcement cards popping in sequentially
    cards = [
        (275, "FIRST-TIME LITTERING", "$300 FINE", "ON-THE-SPOT NEA ENFORCEMENT", (64, 214, 152)),
        (640, "REPEAT OFFENDERS", "$2,000 + CWO", "MANDATORY PUBLIC STREET CLEANING", (248, 196, 72)),
        (1005, "ILLEGAL DUMPING & SPITTING", "ZERO TOLERANCE", "CAMERAS + STRICT MUNICIPAL AUDITS", (244, 96, 82)),
    ]

    for idx, (y0, title, hero, sub, accent) in enumerate(cards):
        pop = kit.ease_out((t - idx * 0.14) / 0.28)
        if pop <= 0.01:
            continue
        dy = int((1.0 - pop) * 28)
        d.rounded_rectangle((68, y0 + dy, kit.W - 68, y0 + 310 + dy), radius=22, fill=(18, 30, 46), outline=accent, width=4)
        d.text((108, y0 + 28 + dy), title, font=f_hdr, fill=accent)
        d.line([(104, y0 + 78 + dy), (kit.W - 104, y0 + 78 + dy)], fill=(44, 68, 92), width=2)
        d.text((108, y0 + 104 + dy), hero, font=f_big, fill=(252, 250, 244))
        d.text((108, y0 + 224 + dy), sub, font=f_row, fill=(186, 210, 228))

    img = kit.draw_shorts_badge(img, "ENFORCEMENT  ·  STRICT LAWS & ACCOUNTABILITY", y=148, accent=(248, 196, 72), bg=(18, 28, 42))
    img = kit.finish_frame(img, global_idx, vignette=0.24, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
