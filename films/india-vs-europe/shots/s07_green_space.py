"""Shot 7 (9:16 Shorts): Public Space & Dignity — Golden-hour European riverside park."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[6][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((38, 102, 174), (144, 188, 224), (248, 214, 158), mid_pos=0.48)
    img = kit.add_sun_and_rays(img, 760, 480, 74, (255, 248, 212), (254, 202, 126), rays=True, ray_alpha=0.22, halo_alpha=0.62)
    img = kit.add_painted_clouds_layer(img, sec, y_top=140, y_bot=680, tint=(255, 242, 220), shadow=(210, 194, 184), density=0.45)
    d = ImageDraw.Draw(img)

    pan = 38 * t
    # Sunlit European skyline across river
    for i, (bx, bh, bw, wcol, rcol) in enumerate([
        (-20, 210, 185, kit.CREAM_WALL, kit.TERRACOTTA),
        (165, 260, 195, kit.OCHRE_WALL, kit.SLATE_ROOF),
        (360, 230, 185, kit.SAGE_WALL, kit.TERRACOTTA),
        (545, 250, 200, kit.CREAM_WALL, kit.TERRACOTTA),
        (745, 215, 190, kit.BLUSH_WALL, kit.SLATE_ROOF),
        (935, 245, 195, kit.OCHRE_WALL, kit.TERRACOTTA),
    ]):
        kit.draw_euro_building_25d(d, bx - pan * 0.4, 920, bw, bh, wcol, rcol, stories=3, spire=(i == 2))

    # Golden-lit shimmering river
    d.rectangle((0, 920, kit.W, 1110), fill=(64, 138, 186))
    for r in range(24):
        ry = 936 + r * 7
        rx = ((r * 211 + sec * 30) % (kit.W + 100)) - 50
        d.line([(rx, ry), (rx + 62, ry)], fill=(252, 228, 176), width=2)

    # Lush sunlit green embankment & warm stone promenade
    d.polygon([(0, 1095), (kit.W, 1068), (kit.W, kit.H), (0, kit.H)], fill=(86, 144, 76))
    d.polygon([(0, 1215), (kit.W, 1185), (kit.W, 1355), (0, 1390)], fill=(222, 212, 190), outline=kit.EURO_INK)

    # Wooden benches
    for bx in (220, 760):
        ux = bx - pan * 0.65
        d.rectangle((ux, 1164, ux + 96, 1178), fill=(142, 92, 54), outline=kit.EURO_INK, width=2)
        d.rectangle((ux, 1182, ux + 96, 1196), fill=(162, 108, 66), outline=kit.EURO_INK, width=2)
        d.line([(ux + 12, 1196), (ux + 12, 1218)], fill=kit.EURO_INK, width=4)
        d.line([(ux + 84, 1196), (ux + 84, 1218)], fill=kit.EURO_INK, width=4)

    # Golden-hour painterly trees
    for tx, sc in [(110, 1.25), (490, 1.05), (950, 1.2)]:
        kit.draw_painterly_tree(d, tx - pan * 0.65, 1185, scale=sc, sway=math.sin(sec * 1.4 + tx * 0.01) * 0.32, golden=True)

    # People strolling peacefully
    walkers = [(180 + sec * 44, 1285, (46, 86, 136)), (240 + sec * 44, 1292, (194, 88, 68)), (880 - sec * 38, 1260, (58, 118, 84))]
    for wx, wy, col in walkers:
        bob = abs(math.sin(sec * 6.0 + wx * 0.05)) * 4
        d.ellipse((wx - 10, wy - 84 - bob, wx + 10, wy - 64 - bob), fill=(234, 198, 174), outline=kit.EURO_INK, width=2)
        d.rounded_rectangle((wx - 12, wy - 62 - bob, wx + 12, wy - 22 - bob), radius=5, fill=col, outline=kit.EURO_INK, width=2)
        stride = math.sin(sec * 6.0 + wx * 0.05) * 10
        d.line([(wx - 4, wy - 22 - bob), (wx - 4 + stride, wy)], fill=kit.EURO_INK, width=4)
        d.line([(wx + 4, wy - 22 - bob), (wx + 4 - stride, wy)], fill=kit.EURO_INK, width=4)

    for i in range(6):
        kit.draw_bird(d, ((sec * 52 + i * 210) % (kit.W + 80)) - 40, 340 + (i % 3) * 48, size=12, phase=sec * 7 + i)

    img = kit.draw_shorts_badge(img, "EUROPE  ·  CLEAN AIR & WALKABLE PARKS", y=148, accent=(118, 194, 96), bg=(22, 46, 36))
    img = kit.finish_frame(img, global_idx, vignette=0.18, warmth=0.16, bloom=0.22)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
