"""Custom painterly rail, Shinkansen, Mount Fuji & Indian Express drawing kit."""

import math
from PIL import ImageDraw
import kit


def draw_mt_fuji(draw, cx, base_y, width=780, height=340, body_col=(82, 114, 158), snow_col=(248, 251, 255)):
    """Iconic symmetrical Mount Fuji silhouette with jagged snow cap."""
    pts = [
        (cx - width * 0.5, base_y),
        (cx - width * 0.18, base_y - height * 0.68),
        (cx - width * 0.06, base_y - height),
        (cx + width * 0.06, base_y - height),
        (cx + width * 0.18, base_y - height * 0.68),
        (cx + width * 0.5, base_y),
    ]
    draw.polygon(pts, fill=body_col)
    # Jagged snow cap
    sy = base_y - height * 0.65
    snow = [
        (cx - width * 0.06, base_y - height),
        (cx + width * 0.06, base_y - height),
        (cx + width * 0.16, sy),
        (cx + width * 0.09, sy + 28),
        (cx + width * 0.02, sy - 6),
        (cx - width * 0.05, sy + 24),
        (cx - width * 0.11, sy - 4),
        (cx - width * 0.16, sy + 14),
    ]
    draw.polygon(snow, fill=snow_col)


def draw_sakura_tree(draw, x, ground_y, scale=1.0, sway=0.0):
    """Painterly Japanese cherry blossom tree."""
    s = scale
    th = 145 * s
    tx = x + sway * 12 * s
    ty = ground_y - th
    draw.polygon([(x - 10 * s, ground_y), (x + 10 * s, ground_y), (tx + 4 * s, ty), (tx - 4 * s, ty)], fill=(78, 52, 46))
    clusters = [
        (-42, 6, 38, (218, 134, 156)), (42, 8, 36, (218, 134, 156)),
        (-22, -32, 42, (242, 174, 192)), (24, -30, 40, (242, 174, 192)),
        (0, -58, 38, (254, 212, 224)), (-28, -50, 28, (254, 212, 224)), (26, -48, 26, (254, 212, 224)),
    ]
    for dx, dy, r, col in clusters:
        bx, by = tx + dx * s + sway * 4 * s, ty + dy * s
        rr = r * s
        draw.ellipse((bx - rr, by - rr * 0.82, bx + rr, by + rr * 0.82), fill=col)


def draw_shinkansen(draw, nose_x, rail_y, length=780, height=96, stripe_col=(24, 96, 186), facing=1, lit_windows=False):
    """Aerodynamic N700S Shinkansen bullet train with sleek duck-bill nose & blue stripes."""
    f = facing
    ink = (26, 36, 52)
    tail_x = nose_x - length * f
    top_y = rail_y - height - 10

    # Cast shadow on viaduct
    draw.rectangle((min(nose_x, tail_x), rail_y - 6, max(nose_x, tail_x), rail_y + 8), fill=(68, 76, 86))

    # Aerodynamic body polygon with long curved duck-bill nose
    body = [
        (tail_x, rail_y - 10),
        (nose_x - 12 * f, rail_y - 10),
        (nose_x, rail_y - 24),
        (nose_x - 24 * f, rail_y - 46),
        (nose_x - 86 * f, rail_y - 74),
        (nose_x - 155 * f, top_y),
        (tail_x, top_y),
    ]
    draw.polygon(body, fill=(248, 250, 252), outline=ink)

    # Signature dual royal blue Shinkansen stripes
    s1 = [(tail_x, rail_y - 34), (nose_x - 20 * f, rail_y - 34), (nose_x - 28 * f, rail_y - 44), (tail_x, rail_y - 44)]
    s2 = [(tail_x, rail_y - 22), (nose_x - 10 * f, rail_y - 22), (nose_x - 14 * f, rail_y - 28), (tail_x, rail_y - 28)]
    draw.polygon(s1, fill=stripe_col)
    draw.polygon(s2, fill=stripe_col)

    # Sleek cockpit canopy
    cockpit = [
        (nose_x - 74 * f, rail_y - 68),
        (nose_x - 132 * f, top_y + 8),
        (nose_x - 160 * f, top_y + 12),
        (nose_x - 104 * f, rail_y - 54),
    ]
    draw.polygon(cockpit, fill=(38, 62, 92), outline=ink)

    # Small aerodynamic passenger windows
    w_fill = (252, 228, 148) if lit_windows else (54, 86, 118)
    n_win = max(4, int((length - 200) // 48))
    for i in range(n_win):
        wx = nose_x - (185 + i * 48) * f
        x0, x1 = min(wx, wx - 28 * f), max(wx, wx - 28 * f)
        draw.rounded_rectangle((x0, top_y + 24, x1, top_y + 46), radius=5, fill=w_fill, outline=ink, width=1)

    # Glowing LED headlight
    draw.ellipse((nose_x - 36 * f - 6, rail_y - 48, nose_x - 36 * f + 6, rail_y - 36), fill=(255, 252, 224))


def draw_indian_express(draw, front_x, rail_y, length=740, height=118, facing=-1):
    """Classic boxy blue/red Indian express train with barred windows & crowded doorways."""
    f = facing
    ink = (32, 26, 22)
    tail_x = front_x - length * f
    x0, x1 = min(front_x, tail_x), max(front_x, tail_x)
    top_y = rail_y - height - 12

    # Ground shadow
    draw.rectangle((x0, rail_y - 6, x1, rail_y + 10), fill=(46, 40, 34))

    # Boxy weathered ICF blue body + grey roof
    draw.rectangle((x0, top_y, x1, rail_y - 12), fill=(52, 92, 142), outline=ink, width=3)
    draw.rectangle((x0, top_y, x1, top_y + 16), fill=(116, 112, 108), outline=ink, width=2)
    # Faded light-blue band + rust stains
    draw.rectangle((x0 + 2, top_y + 44, x1 - 2, top_y + 82), fill=(86, 134, 182))
    draw.rectangle((x0 + 2, rail_y - 24, x1 - 2, rail_y - 14), fill=(96, 66, 52))

    # Barred passenger windows + open crowded doors
    pos = x0 + 36
    idx = 0
    while pos < x1 - 54:
        if idx % 5 == 0:
            # Open doorway with dark interior & standing passenger silhouette
            draw.rectangle((pos, top_y + 26, pos + 44, rail_y - 14), fill=(28, 24, 22), outline=ink, width=2)
            draw.ellipse((pos + 14, top_y + 42, pos + 30, top_y + 58), fill=(54, 48, 46))
            draw.rectangle((pos + 10, top_y + 58, pos + 34, top_y + 98), fill=(168, 86, 62))
            pos += 64
        else:
            # Barred window
            draw.rectangle((pos, top_y + 34, pos + 36, top_y + 72), fill=(42, 46, 52), outline=ink, width=2)
            for b in (12, 24):
                draw.line([(pos, top_y + 34 + b), (pos + 36, top_y + 34 + b)], fill=(148, 152, 156), width=2)
            pos += 50
        idx += 1

    # Bogie wheels
    for bx in range(int(x0 + 70), int(x1 - 70), 170):
        draw.ellipse((bx - 16, rail_y - 22, bx + 16, rail_y + 4), fill=(36, 34, 34), outline=ink, width=2)
        draw.ellipse((bx + 28, rail_y - 22, bx + 60, rail_y + 4), fill=(36, 34, 34), outline=ink, width=2)


def draw_viaduct(draw, rail_y, col=(208, 214, 220), shade=(166, 174, 184), ink=(36, 46, 58)):
    """Clean Japanese concrete elevated Shinkansen viaduct with pillars."""
    draw.rectangle((0, rail_y, kit.W, rail_y + 44), fill=col, outline=ink, width=2)
    draw.rectangle((0, rail_y + 32, kit.W, rail_y + 52), fill=shade, outline=ink, width=2)
    # Noise barrier lip
    draw.rectangle((0, rail_y - 14, kit.W, rail_y), fill=(228, 232, 236), outline=ink, width=2)
    for px in (140, 520, 900):
        draw.rectangle((px, rail_y + 52, px + 68, kit.H), fill=col, outline=ink, width=2)
        draw.rectangle((px + 50, rail_y + 52, px + 68, kit.H), fill=shade)
