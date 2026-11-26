"""Shot 8: City in a Garden — Golden-hour Marina Bay Sands & glowing Supertree Grove."""

import math
from PIL import Image, ImageDraw
import kit
import film
import sg_kit

CAPS = film.SHOTS[7][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    pan = 36 * t

    img = kit.make_sky_gradient((34, 96, 168), (148, 184, 218), (250, 208, 148), mid_pos=0.48)
    img = kit.add_sun_and_rays(img, 780, 440, 76, (255, 248, 212), (254, 198, 122), rays=True, ray_alpha=0.22, halo_alpha=0.62)
    img = kit.add_painted_clouds_layer(img, sec, y_top=140, y_bot=640, tint=(255, 240, 216), shadow=(206, 188, 178), density=0.45)
    d = ImageDraw.Draw(img)

    # Marina Bay Sands towering in golden light
    sg_kit.draw_marina_bay_sands(d, 540 - pan * 0.4, 1020, scale=1.45)

    # Shimmering Marina Bay water
    d.rectangle((0, 1020, kit.W, 1185), fill=(58, 134, 182))
    for r in range(22):
        ry = 1035 + r * 7
        rx = ((r * 211 + sec * 28) % (kit.W + 100)) - 50
        d.line([(rx, ry), (rx + 64, ry)], fill=(252, 224, 168), width=2)

    # Lush green Gardens by the Bay foreground + Supertrees + OCBC Skyway bridge
    d.polygon([(0, 1175), (kit.W, 1155), (kit.W, kit.H), (0, kit.H)], fill=(76, 142, 74))

    # Suspended golden skywalk bridge connecting the Supertrees
    kit.draw_catenary(d, 210 + pan * 0.6, 865, 860 + pan * 0.6, 865, sag=42, color=(246, 204, 112), width=5)

    for sx, sc in [(210, 1.35), (535, 1.15), (860, 1.35)]:
        sg_kit.draw_supertree(d, sx + pan * 0.6, 1235, scale=sc)

    for tx, sc in [(90, 1.0), (370, 0.92), (700, 0.95), (990, 1.05)]:
        kit.draw_painterly_tree(d, tx + pan * 0.7, 1265, scale=sc, sway=math.sin(sec * 1.5 + tx) * 0.3, golden=True)

    for i in range(6):
        kit.draw_bird(d, ((sec * 56 + i * 210) % (kit.W + 80)) - 40, 320 + (i % 3) * 48, size=12, phase=sec * 7 + i)

    img = kit.draw_shorts_badge(img, "CITY IN A GARDEN  ·  SKYPARK & SUPERTREES", y=148, accent=(108, 224, 138), bg=(20, 44, 36))
    img = kit.finish_frame(img, global_idx, vignette=0.18, warmth=0.16, bloom=0.22)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
