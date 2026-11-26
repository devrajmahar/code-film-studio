"""Shot 6: The Engineering Blueprint — Dedicated Elevated Tracks vs Shared Mixed-Traffic Rails."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[5][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((16, 26, 40), (22, 34, 52), (14, 20, 32), mid_pos=0.5)
    d = ImageDraw.Draw(img)
    for gx in range(0, kit.W, 60):
        d.line([(gx, 0), (gx, kit.H)], fill=(26, 40, 60), width=1)
    for gy in range(0, kit.H, 60):
        d.line([(0, gy), (kit.W, gy)], fill=(26, 40, 60), width=1)

    f_hdr = kit.get_font(30, bold=True)
    f_lbl = kit.get_font(23, bold=True)

    # --- TOP BLUEPRINT: JAPAN DEDICATED HIGH-SPEED CORRIDOR ---
    d.rounded_rectangle((56, 265, kit.W - 56, 770), radius=20, fill=(20, 36, 54), outline=(58, 206, 246), width=3)
    d.text((90, 292), "JAPAN · DEDICATED ELEVATED SLAB TRACK", font=f_hdr, fill=(96, 224, 255))
    d.text((90, 336), "ZERO ROAD CROSSINGS · AUTOMATED ATC BLOCKS", font=f_lbl, fill=(182, 214, 232))

    # Two sleek dedicated high-speed lines with fast cyan train pulses
    for idx, ry in enumerate((470, 615)):
        d.rounded_rectangle((90, ry - 26, kit.W - 90, ry + 26), radius=12, fill=(30, 50, 72), outline=(112, 162, 198), width=2)
        d.line([(110, ry), (kit.W - 110, ry)], fill=(58, 212, 248), width=6)
        # Fast Shinkansen capsule gliding smoothly
        tx = 120 + ((sec * 480 + idx * 380) % 720)
        d.rounded_rectangle((tx, ry - 14, tx + 135, ry + 14), radius=10, fill=(248, 250, 255), outline=(36, 98, 186), width=3)
        # Green ATC signal dots
        for sx in (260, 540, 820):
            d.ellipse((sx - 8, ry - 44, sx + 8, ry - 28), fill=(68, 236, 146))

    # --- BOTTOM BLUEPRINT: INDIA SHARED MIXED-TRAFFIC RAIL ---
    d.rounded_rectangle((56, 835, kit.W - 56, 1345), radius=20, fill=(40, 22, 24), outline=(236, 92, 72), width=3)
    d.text((90, 862), "INDIA · SHARED SINGLE MIXED-TRAFFIC LINE", font=f_hdr, fill=(250, 132, 112))
    d.text((90, 906), "FREIGHT + LOCALS + EXPRESS + ROAD CROSSINGS", font=f_lbl, fill=(224, 188, 178))

    # One congested track with 3 different conflicting train types jammed together
    ry = 1100
    d.rounded_rectangle((90, ry - 32, kit.W - 90, ry + 32), radius=12, fill=(56, 34, 34), outline=(186, 92, 78), width=2)
    d.line([(110, ry), (kit.W - 110, ry)], fill=(214, 108, 82), width=6)

    # Vertical road cutting right across the rail track!
    d.rectangle((500, 965, 580, 1290), fill=(72, 68, 66), outline=(216, 174, 72), width=3)
    d.text((462, 1296), "ROAD CROSSING", font=f_lbl, fill=(248, 198, 84))

    # Slow jammed freight, local, and express blocks stalling behind crossing
    shift = math.sin(sec * 3.0) * 14
    d.rounded_rectangle((130 + shift, ry - 18, 300 + shift, ry + 18), radius=6, fill=(142, 104, 72), outline=(250, 236, 220), width=2)
    d.text((156 + shift, ry - 12), "FREIGHT", font=kit.get_font(18, bold=True), fill=(252, 246, 238))
    d.rounded_rectangle((330 + shift, ry - 18, 470 + shift, ry + 18), radius=6, fill=(72, 124, 178), outline=(250, 236, 220), width=2)
    d.text((352 + shift, ry - 12), "EXPRESS", font=kit.get_font(18, bold=True), fill=(252, 246, 238))
    d.rounded_rectangle((615 - shift, ry - 18, 765 - shift, ry + 18), radius=6, fill=(196, 86, 68), outline=(250, 236, 220), width=2)
    d.text((648 - shift, ry - 12), "LOCAL", font=kit.get_font(18, bold=True), fill=(252, 246, 238))

    # Pulsing red bottleneck alert on crossing
    pr = 16 + ((sec * 46) % 36)
    d.ellipse((540 - pr, ry - pr, 540 + pr, ry + pr), outline=(255, 76, 62), width=4)
    d.ellipse((540 - 10, ry - 10, 540 + 10, ry + 10), fill=(255, 76, 62))

    img = kit.draw_shorts_badge(img, "ENGINEERING  ·  DEDICATED vs SHARED RAILS", y=148, accent=(58, 206, 246), bg=(18, 30, 44))
    img = kit.finish_frame(img, global_idx, vignette=0.24, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
