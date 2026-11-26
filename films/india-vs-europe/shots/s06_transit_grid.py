"""Shot 6 (9:16 Shorts): The Hidden Machine — Underground European utility tunnels vs unplanned sprawl."""

import math
from PIL import Image, ImageDraw
import kit
import film

CAPS = film.SHOTS[5][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((34, 102, 178), (112, 178, 228), (216, 238, 250), mid_pos=0.25)
    img = kit.add_painted_clouds_layer(img, sec, y_top=100, y_bot=420, density=0.42)
    d = ImageDraw.Draw(img)

    ground_y = 640
    # Clean sunlit European surface above ground
    for bx, bh, bw, wcol, rcol in [
        (20, 270, 210, kit.CREAM_WALL, kit.TERRACOTTA),
        (235, 315, 220, kit.OCHRE_WALL, kit.SLATE_ROOF),
        (650, 295, 210, kit.SAGE_WALL, kit.TERRACOTTA),
        (865, 275, 210, kit.CREAM_WALL, kit.TERRACOTTA),
    ]:
        kit.draw_euro_building_25d(d, bx, ground_y, bw, bh, wcol, rcol, stories=4)
    kit.draw_painterly_tree(d, 515, ground_y, scale=0.82, sway=math.sin(sec * 1.5) * 0.25)
    kit.draw_detailed_tram(d, 310 + math.sin(sec * 0.85) * 160, ground_y, length=420, height=106)

    # Architectural blueprint subsurface
    d.rectangle((0, ground_y, kit.W, kit.H), fill=(20, 30, 42))
    for gx in range(0, kit.W, 60):
        d.line([(gx, ground_y), (gx, kit.H)], fill=(28, 42, 58), width=1)
    for gy in range(ground_y, kit.H, 60):
        d.line([(0, gy), (kit.W, gy)], fill=(28, 42, 58), width=1)
    d.line([(0, ground_y), (kit.W, ground_y)], fill=(244, 248, 252), width=6)

    # TOP subsurface band: Organized European utility corridors
    reveal = kit.ease_out(min(1.0, t * 2.2))
    pipes = [
        (735, (242, 194, 66), "POWER & FIBER CONDUIT"),
        (835, (64, 184, 232), "PRESSURIZED CLEAN WATER"),
        (935, (62, 198, 128), "VACUUM WASTE SUCTION"),
        (1035, (116, 152, 226), "STORMWATER DRAINAGE TUNNEL"),
    ]
    font_lbl = kit.get_font(24, bold=True)
    for idx, (py, col, label) in enumerate(pipes):
        end_x = int(76 + (kit.W - 152) * reveal)
        d.rounded_rectangle((66, py - 24, max(92, end_x), py + 24), radius=12, fill=(32, 46, 62), outline=(136, 166, 194), width=2)
        d.line([(86, py), (max(92, end_x - 20), py)], fill=col, width=10)
        for p in range(6):
            fx = 92 + ((sec * 180 + p * 170 + idx * 42) % max(40, end_x - 115))
            d.ellipse((fx - 7, py - 7, fx + 7, py + 7), fill=(252, 252, 248))
        d.text((82, py - 50), label, font=font_lbl, fill=(224, 236, 248))

    # LOWER subsurface band (reveals at t=0.40): Unplanned tangled pipes & active leaks
    chaos_a = kit.ease_out((t - 0.40) / 0.18)
    if chaos_a > 0.02:
        div_y = 1105
        d.line([(60, div_y), (kit.W - 60, div_y)], fill=(224, 86, 68), width=4)
        d.text((76, div_y + 18), "VS INDIA · UNPLANNED SPRAWL & BAD MANAGEMENT", font=font_lbl, fill=(242, 132, 112))
        tangles = [
            [(76, 1200), (380, 1285), (690, 1175), (995, 1310)],
            [(70, 1335), (410, 1195), (720, 1355), (1000, 1225)],
            [(90, 1185), (510, 1370), (920, 1200)],
        ]
        tcols = [(194, 84, 62), (162, 132, 86), (174, 94, 110)]
        for pts, col in zip(tangles, tcols):
            d.line(pts, fill=col, width=12, joint="curve")
        for lx, ly in [(395, 1272), (710, 1340)]:
            pr = 14 + ((sec * 44) % 36)
            d.ellipse((lx - pr, ly - pr, lx + pr, ly + pr), outline=(242, 82, 64), width=3)
            d.ellipse((lx - 9, ly - 9, lx + 9, ly + 9), fill=(242, 82, 64))

    img = kit.draw_shorts_badge(img, "EUROPE vs INDIA  ·  UNDERGROUND FIRST", y=148, accent=(66, 184, 232), bg=(18, 32, 46))
    img = kit.finish_frame(img, global_idx, vignette=0.22, bloom=0.14)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
