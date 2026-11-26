"""Shot 6: Pulau Semakau — Offshore eco-landfill island surrounded by turquoise water, mangroves & coral."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[5][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    # Tropical cerulean sky + turquoise South China Sea
    img = kit.make_sky_gradient((18, 86, 168), (82, 168, 226), (176, 232, 246), mid_pos=0.35)
    img = kit.add_sun_and_rays(img, 830, 260, 58, (255, 254, 238), (255, 242, 198), rays=True, ray_alpha=0.18)
    img = kit.add_painted_clouds_layer(img, sec, y_top=100, y_bot=460, density=0.42)
    d = ImageDraw.Draw(img)

    # Shimmering turquoise ocean below horizon
    sea_y = 660
    d.rectangle((0, sea_y, kit.W, kit.H), fill=(26, 134, 168))
    for r in range(38):
        ry = sea_y + 18 + r * 32
        rx = ((r * 211 + sec * 28) % (kit.W + 120)) - 60
        d.line([(rx, ry), (rx + 74, ry)], fill=(116, 214, 232), width=2)

    # Pulau Semakau engineered ring island in center
    cx, cy = 540, 1020
    # Outer coral & turquoise reef halo
    d.ellipse((cx - 450, cy - 230, cx + 450, cy + 230), fill=(52, 184, 194))
    # Engineered rock bund seawall ring (impermeable membrane)
    d.ellipse((cx - 390, cy - 190, cx + 390, cy + 190), fill=(214, 206, 188), outline=(44, 62, 76), width=4)
    # Lush green mangrove & tropical forest ring + clean inner ash cells
    d.ellipse((cx - 340, cy - 155, cx + 340, cy + 155), fill=(72, 156, 86), outline=(36, 88, 52), width=3)
    d.ellipse((cx - 210, cy - 90, cx + 210, cy + 90), fill=(44, 148, 174), outline=(214, 206, 188), width=4)

    # Mangrove trees around the island perimeter
    for ang_deg in range(0, 360, 24):
        a = math.radians(ang_deg)
        tx = cx + math.cos(a) * 285
        ty = cy + math.sin(a) * 125
        d.ellipse((tx - 32, ty - 26, tx + 32, ty + 26), fill=(52, 132, 68))
        d.ellipse((tx - 20, ty - 30, tx + 20, ty + 14), fill=(112, 184, 88))

    # Label callout on island
    f_lbl = kit.get_font(28, bold=True)
    d.rounded_rectangle((cx - 230, cy - 32, cx + 230, cy + 32), radius=12, fill=(14, 32, 44), outline=(88, 238, 172), width=3)
    d.text((cx - 200, cy - 18), "PULAU SEMAKAU ECO-ISLAND", font=f_lbl, fill=(116, 248, 184))

    for i in range(5):
        kit.draw_bird(d, ((sec * 58 + i * 240) % (kit.W + 80)) - 40, 340 + i * 38, size=12, phase=sec * 7.5 + i)

    img = kit.draw_shorts_badge(img, "PULAU SEMAKAU  ·  ASH ISLAND & CORAL REEFS", y=148, accent=(64, 218, 168), bg=(16, 38, 52))
    img = kit.finish_frame(img, global_idx, vignette=0.18, bloom=0.18)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
