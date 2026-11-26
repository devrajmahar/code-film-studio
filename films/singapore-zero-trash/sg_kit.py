"""Custom drawing helpers for Singapore: Marina Bay Sands, Supertree Grove, 1965 Kampong shacks & HDB towers."""

import math
import numpy as np
import kit


def draw_marina_bay_sands(draw, cx, base_y, scale=1.0, night=False):
    """Iconic 3-tower Marina Bay Sands with cantilevered SkyPark boat on top."""
    s = scale
    ink = (22, 34, 48)
    th = int(380 * s)
    tw = int(68 * s)
    spacing = int(108 * s)
    top_y = base_y - th

    glass_lit = (54, 108, 152) if not night else (36, 62, 96)
    glass_shd = (36, 76, 114) if not night else (22, 38, 64)

    for idx in (-1, 0, 1):
        tx = cx + idx * spacing - tw // 2
        # Slight inward taper like real MBS towers
        poly = [
            (tx - int(8 * s), base_y),
            (tx + tw + int(6 * s), base_y),
            (tx + tw, top_y),
            (tx + int(6 * s), top_y),
        ]
        draw.polygon(poly, fill=glass_lit, outline=ink)
        # Shaded side edge
        draw.polygon(
            [(tx + tw - int(14 * s), top_y), (tx + tw, top_y), (tx + tw + int(6 * s), base_y), (tx + tw - int(10 * s), base_y)],
            fill=glass_shd,
            outline=ink,
        )
        # Horizontal floor bands
        for r in range(1, 14):
            fy = top_y + int(r * (th / 14.0))
            col = (248, 224, 154) if (night and (r + idx) % 2 == 0) else (136, 188, 224)
            draw.line([(tx + int(4 * s), fy), (tx + tw - int(14 * s), fy)], fill=col, width=max(1, int(2 * s)))

    # SkyPark cantilevered ship platform spanning across all 3 towers
    ship_w = int(340 * s)
    ship_h = int(28 * s)
    sx0 = cx - int(155 * s)
    sx1 = sx0 + ship_w
    hull = [
        (sx0, top_y - ship_h),
        (sx1 + int(34 * s), top_y - ship_h),
        (sx1 + int(8 * s), top_y + int(4 * s)),
        (sx0 + int(16 * s), top_y + int(4 * s)),
    ]
    draw.polygon(hull, fill=(238, 242, 246) if not night else (218, 198, 146), outline=ink)
    # Rooftop trees on SkyPark
    for gx in range(int(sx0 + 25 * s), int(sx1 + 10 * s), int(38 * s)):
        r = int(12 * s)
        draw.ellipse((gx - r, top_y - ship_h - r, gx + r, top_y - ship_h + int(4 * s)), fill=(68, 156, 86))


def draw_supertree(draw, cx, base_y, scale=1.0, night=False):
    """Gardens by the Bay Supertree canopy tower with glowing magenta/violet lattice."""
    s = scale
    h = int(230 * s)
    top_y = base_y - h
    trunk_col = (146, 74, 128) if not night else (218, 88, 184)
    vine_col = (54, 134, 76) if not night else (68, 174, 112)

    # Flared hourglass lattice trunk + living green core
    trunk = [
        (cx - int(32 * s), base_y),
        (cx + int(32 * s), base_y),
        (cx + int(14 * s), base_y - int(h * 0.52)),
        (cx + int(56 * s), top_y),
        (cx - int(56 * s), top_y),
        (cx - int(14 * s), base_y - int(h * 0.52)),
    ]
    draw.polygon(trunk, fill=vine_col, outline=trunk_col)

    # Flared canopy crown
    cw = int(92 * s)
    ch = int(24 * s)
    draw.ellipse((cx - cw, top_y - ch, cx + cw, top_y + ch), fill=trunk_col, outline=(36, 24, 44), width=2)
    # Lattice ribs
    for k in (-42, -20, 0, 20, 42):
        draw.line([(cx + int(k * 0.35 * s), base_y - int(h * 0.45)), (cx + int(k * 1.8 * s), top_y)], fill=(244, 176, 224), width=max(1, int(2 * s)))


def draw_kampong_shack(draw, x, base_y, w=185, h=140, seed=1):
    """1965 dilapidated wooden stilt kampong shack with rusted tin roof."""
    rng = np.random.default_rng(seed)
    ink = (34, 26, 20)
    y_top = base_y - h
    # Wooden stilts in mud/water
    for sx in (x + 18, x + w // 2, x + w - 18):
        draw.line([(sx, base_y - 24), (sx, base_y + 32)], fill=(64, 46, 32), width=6)
    # Weathered timber plank walls
    wcol = (118 + int(rng.integers(-12, 12)), 92 + int(rng.integers(-10, 10)), 68)
    draw.rectangle((x, y_top + 28, x + w, base_y - 22), fill=wcol, outline=ink, width=2)
    for py in range(int(y_top + 44), int(base_y - 24), 18):
        draw.line([(x, py), (x + w, py)], fill=(78, 58, 42), width=1)
    # Crooked dark window
    draw.rectangle((x + 28, y_top + 52, x + 64, y_top + 84), fill=(38, 32, 28), outline=ink, width=2)
    draw.rectangle((x + w - 68, y_top + 48, x + w - 26, base_y - 22), fill=(48, 38, 30), outline=ink, width=2)
    # Patched rusted corrugated tin roof
    rcol = (138, 74, 52) if rng.random() < 0.5 else (106, 86, 72)
    draw.polygon([(x - 14, y_top + 32), (x + w * 0.5, y_top), (x + w + 14, y_top + 32)], fill=rcol, outline=ink)


def draw_hdb_tower(draw, x, base_y, w=205, h=580, accent_col=(224, 112, 78)):
    """Modern clean Singapore HDB public housing tower with vertical sky-garden balconies."""
    ink = (28, 38, 50)
    y_top = base_y - h
    side_w = int(w * 0.14)
    fw = w - side_w
    # Shaded side return + clean bright white/cream main facade
    draw.rectangle((x + fw, y_top, x + w, base_y), fill=(198, 204, 210), outline=ink, width=2)
    draw.rectangle((x, y_top, x + fw, base_y), fill=(244, 246, 248), outline=ink, width=2)
    # Signature vertical color accent band & rooftop solar canopy
    draw.rectangle((x + 12, y_top, x + 36, base_y), fill=accent_col)
    draw.rectangle((x - 6, y_top - 16, x + w + 4, y_top), fill=(52, 74, 98), outline=ink, width=2)

    # Neat grid of recessed windows + lush sky-garden planter ledges every 3rd floor
    rows = max(4, int(h // 52))
    for r in range(rows):
        wy = y_top + 22 + r * 50
        for c in range(3):
            wx = x + 52 + c * 42
            draw.rectangle((wx, wy, wx + 28, wy + 28), fill=(64, 104, 138), outline=ink, width=1)
        if r % 3 == 1:
            # Hanging green planter balcony
            for gx in range(x + 48, x + fw - 18, 22):
                draw.ellipse((gx - 12, wy + 22, gx + 12, wy + 38), fill=(72, 162, 86))
