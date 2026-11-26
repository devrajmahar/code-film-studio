"""Shot 4 (9:16 Shorts): European Boulevard — 2.5D townhouses, cafés, underground bins, bike lane & tram."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[3][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)
    pan = 68 * t

    img = kit.make_sky_gradient((26, 92, 172), (96, 168, 226), (214, 238, 250), mid_pos=0.40)
    img = kit.add_sun_and_rays(img, 240, 290, 56, (255, 254, 238), (255, 242, 198), rays=True, ray_alpha=0.16)
    img = kit.add_painted_clouds_layer(img, sec, y_top=120, y_bot=620, density=0.45)
    d = ImageDraw.Draw(img)

    # Tall sunlit 2.5D European facades with café awnings & balconies
    facades = [
        (-40, 520, 230, kit.CREAM_WALL, kit.TERRACOTTA, False, True),
        (190, 590, 240, kit.OCHRE_WALL, kit.SLATE_ROOF, False, False),
        (430, 545, 230, kit.SAGE_WALL, kit.TERRACOTTA, True, True),
        (660, 575, 245, kit.CREAM_WALL, kit.TERRACOTTA, False, True),
        (905, 535, 235, kit.BLUSH_WALL, kit.SLATE_ROOF, False, False),
    ]
    for bx, bh, bw, wcol, rcol, sp, cf in facades:
        kit.draw_euro_building_25d(d, bx - pan * 0.45, 1085, bw, bh, wcol, rcol, stories=5, spire=sp, café=cf)

    # Wide clean cobblestone pedestrian promenade
    d.rectangle((0, 1085, kit.W, 1215), fill=(216, 210, 198), outline=kit.EURO_INK, width=2)
    for i in range(18):
        lx = ((i * 75) - pan * 0.7) % (kit.W + 75) - 35
        d.line([(lx, 1085), (lx - 20, 1215)], fill=(186, 180, 168), width=1)

    # Sleek underground recessed waste bins
    for bx in (260, 810):
        ux = bx - pan * 0.7
        d.rounded_rectangle((ux, 1126, ux + 44, 1184), radius=6, fill=(178, 186, 194), outline=kit.EURO_INK, width=2)
        d.rectangle((ux + 8, 1138, ux + 36, 1148), fill=(44, 52, 60))
        d.rounded_rectangle((ux + 52, 1126, ux + 96, 1184), radius=6, fill=(178, 186, 194), outline=kit.EURO_INK, width=2)
        d.rectangle((ux + 60, 1138, ux + 88, 1148), fill=(48, 152, 92))

    # Lush painterly boulevard trees
    for tx in (120, 560, 990):
        kit.draw_painterly_tree(d, tx - pan * 0.7, 1132, scale=1.0, sway=math.sin(sec * 1.5 + tx) * 0.3)

    # Dedicated red-brick bike lane
    d.rectangle((0, 1215, kit.W, 1300), fill=kit.BIKE_BRICK, outline=kit.EURO_INK, width=2)
    for dash in range(12):
        dx = ((dash * 130) - pan * 0.9) % (kit.W + 130) - 65
        d.line([(dx, 1258), (dx + 56, 1258)], fill=(246, 242, 234), width=4)

    # Clean granite transit road & tram rails
    d.rectangle((0, 1300, kit.W, kit.H), fill=(112, 118, 126))
    d.line([(0, 1378), (kit.W, 1378)], fill=(58, 64, 70), width=4)
    d.line([(0, 1404), (kit.W, 1404)], fill=(58, 64, 70), width=4)

    # Overhead single sleek tram catenary wire
    d.line([(0, 1202), (kit.W, 1202)], fill=(46, 54, 64), width=2)

    # Cyclists gliding smoothly (drawn behind tram since bike lane is further back)
    kit.draw_cyclist(d, (140 + sec * 135) % (kit.W + 160) - 80, 1280, scale=1.08, phase=sec * 8.0, coat_col=(42, 86, 136))
    kit.draw_cyclist(d, (680 + sec * 115) % (kit.W + 160) - 80, 1284, scale=1.02, phase=sec * 7.5 + 2.0, coat_col=(188, 84, 62))

    # Gliding modern European tram in foreground
    tram_x = -540 + t * 1850
    kit.draw_detailed_tram(d, tram_x, 1396, length=560, height=138)

    for i in range(4):
        kit.draw_bird(d, ((sec * 56 + i * 280) % (kit.W + 80)) - 40, 320 + i * 44, size=12, phase=sec * 7 + i)

    img = kit.draw_shorts_badge(img, "EUROPE  ·  CLEAN STREETS & DESIGN", y=148, accent=(58, 186, 124), bg=(18, 44, 58))
    img = kit.finish_frame(img, global_idx, vignette=0.18, warmth=0.05, bloom=0.18)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
