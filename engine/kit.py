"""High-craft 9:16 painterly gouache & cinematic lighting toolkit for TWO SKIES Shorts."""

import math
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = 1080
H = 1920

# ---------------------------------------------------------------------------
# Math & easing
# ---------------------------------------------------------------------------

def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_rgb(c1, c2, t):
    t = clamp(t)
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def ease_out(t):
    t = clamp(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out(t):
    t = clamp(t)
    return 3 * t * t - 2 * t * t * t


# ---------------------------------------------------------------------------
# Rich Cinematic Color Palettes
# ---------------------------------------------------------------------------

SMOG_TOP = (86, 70, 56)
SMOG_MID = (154, 122, 88)
SMOG_BOT = (196, 158, 114)
SMOG_INK = (32, 24, 20)
RUST_RED = (168, 62, 46)
HAZARD_PURPLE = (148, 34, 88)

EURO_TOP = (24, 84, 158)
EURO_MID = (86, 158, 218)
EURO_BOT = (204, 232, 248)
EURO_INK = (24, 34, 48)
TERRACOTTA = (192, 88, 56)
SLATE_ROOF = (64, 78, 94)
CREAM_WALL = (242, 232, 212)
OCHRE_WALL = (232, 196, 132)
SAGE_WALL = (188, 208, 192)
BLUSH_WALL = (228, 198, 182)
TRAM_RED = (206, 48, 48)
BIKE_BRICK = (172, 82, 66)
RIVER_BLUE = (48, 122, 174)

# ---------------------------------------------------------------------------
# Cached procedural textures & fonts
# ---------------------------------------------------------------------------

_PAPER_TEX = None
_FBM_CLOUD = None
_VIGNETTE_MAP = None
_FONT_CACHE = {}


def get_paper_texture():
    global _PAPER_TEX
    if _PAPER_TEX is None:
        rng = np.random.default_rng(777)
        c1 = cv2.resize(rng.normal(1.0, 0.025, (H // 8, W // 8)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
        c2 = cv2.resize(rng.normal(0.0, 0.018, (H // 2, W // 2)).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
        _PAPER_TEX = np.clip((c1 + c2)[..., None], 0.92, 1.08)
    return _PAPER_TEX


def get_fbm_noise():
    """Tileable multi-octave soft cloud/smog noise (H x W float32 in 0..1)."""
    global _FBM_CLOUD
    if _FBM_CLOUD is None:
        rng = np.random.default_rng(1234)
        acc = np.zeros((H, W), dtype=np.float32)
        amp = 0.55
        for div in (32, 16, 8, 4):
            g = rng.uniform(0.0, 1.0, (max(4, H // div), max(4, W // div))).astype(np.float32)
            up = cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC)
            acc += up * amp
            amp *= 0.5
        acc = (acc - acc.min()) / (acc.max() - acc.min() + 1e-6)
        _FBM_CLOUD = acc
    return _FBM_CLOUD


def get_vignette_map():
    global _VIGNETTE_MAP
    if _VIGNETTE_MAP is None:
        yy = np.linspace(-1.0, 1.0, H, dtype=np.float32)[:, None]
        xx = np.linspace(-1.0, 1.0, W, dtype=np.float32)[None, :]
        r2 = xx * xx * 0.72 + yy * yy * 0.95
        _VIGNETTE_MAP = np.clip(r2 - 0.32, 0.0, 1.3)[..., None]
    return _VIGNETTE_MAP


def get_font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    if serif:
        candidates = [
            "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
            "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/bahnschrift.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        ]
    font = None
    for p in candidates:
        if os.path.exists(p):
            try:
                font = ImageFont.truetype(p, size)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()
    _FONT_CACHE[key] = font
    return font


# ---------------------------------------------------------------------------
# Sky, volumetric sunbeams & fBm smog/cloud layers
# ---------------------------------------------------------------------------

def make_sky_gradient(top_rgb, mid_rgb, bot_rgb, mid_pos=0.52, w=W, h=H):
    y = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    t1 = np.clip(y / max(mid_pos, 1e-5), 0.0, 1.0)
    t2 = np.clip((y - mid_pos) / max(1.0 - mid_pos, 1e-5), 0.0, 1.0)
    top = np.array(top_rgb, dtype=np.float32)
    mid = np.array(mid_rgb, dtype=np.float32)
    bot = np.array(bot_rgb, dtype=np.float32)
    col = np.where(y < mid_pos, top * (1.0 - t1) + mid * t1, mid * (1.0 - t2) + bot * t2)
    arr = np.broadcast_to(col[:, None, :], (h, w, 3)).astype(np.uint8).copy()
    return Image.fromarray(arr, mode="RGB")


def add_sun_and_rays(img, cx, cy, radius, core_rgb, halo_rgb, rays=True, ray_alpha=0.14, halo_alpha=0.55):
    arr = np.array(img, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = xx - cx
    dy = yy - cy
    dist = np.sqrt(dx * dx + dy * dy)

    # Atmospheric radial halo
    halo = np.exp(-((dist / (radius * 2.8)) ** 1.6)) * halo_alpha
    core = np.clip(1.0 - (dist - radius * 0.85) / (radius * 0.35 + 1e-5), 0.0, 1.0)

    hcol = np.array(halo_rgb, dtype=np.float32)
    ccol = np.array(core_rgb, dtype=np.float32)
    arr = arr * (1.0 - halo[..., None]) + hcol * halo[..., None]

    if rays:
        angle = np.arctan2(dy, dx)
        ray_pat = (0.5 + 0.5 * np.sin(angle * 7.0 + 0.6)) ** 3
        ray_falloff = np.exp(-dist / 980.0) * ray_pat * ray_alpha
        arr = arr + hcol * ray_falloff[..., None]

    arr = arr * (1.0 - core[..., None]) + ccol * core[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")


def add_smog_veil(img, sec, y_start=0, y_end=H, color=(184, 152, 114), strength=0.35, speed=26):
    """Layered drifting volumetric fBm smog/haze."""
    arr = np.array(img, dtype=np.float32)
    fbm = get_fbm_noise()
    shift = int(sec * speed) % W
    shifted = np.roll(fbm, shift, axis=1)
    y_mask = np.zeros((H, 1), dtype=np.float32)
    if y_end > y_start:
        ramp = np.linspace(0.25, 1.0, y_end - y_start, dtype=np.float32)
        y_mask[y_start:y_end, 0] = ramp
    alpha = np.clip(shifted * y_mask * strength, 0.0, 0.85)[..., None]
    col = np.array(color, dtype=np.float32)
    arr = arr * (1.0 - alpha) + col * alpha
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")


def add_painted_clouds_layer(img, sec, y_top=90, y_bot=700, tint=(252, 252, 250), shadow=(186, 208, 228), density=0.45):
    """Soft volumetric painterly cumulus clouds using thresholded fBm + top-down lighting."""
    arr = np.array(img, dtype=np.float32)
    fbm = get_fbm_noise()
    s1 = np.roll(fbm, int(sec * 16) % W, axis=1)
    s2 = np.roll(fbm, -int(sec * 7) % W, axis=1)
    n = 0.65 * s1 + 0.35 * s2

    # Vertical envelope so clouds float naturally in sky band
    yy = np.arange(H, dtype=np.float32)[:, None]
    mid_y = (y_top + y_bot) * 0.5
    half_y = max(1.0, (y_bot - y_top) * 0.5)
    env = np.clip(1.0 - ((yy - mid_y) / half_y) ** 2, 0.0, 1.0)

    cloud_mask = np.clip((n * env - (1.0 - density)) / 0.24, 0.0, 1.0)
    # Fake top-lit shading by shifting mask slightly downward
    lit_shift = np.roll(cloud_mask, 14, axis=0)
    shade = np.clip(cloud_mask - lit_shift * 0.55, 0.0, 1.0)

    c_lit = np.array(tint, dtype=np.float32)
    c_shd = np.array(shadow, dtype=np.float32)
    cloud_col = c_shd * (1.0 - shade[..., None]) + c_lit * shade[..., None]
    a = (cloud_mask * 0.88)[..., None]
    arr = arr * (1.0 - a) + cloud_col * a
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")


# ---------------------------------------------------------------------------
# Anti-aliased 2.5D Architecture, Trees, Vehicles & Gritty Street Props
# ---------------------------------------------------------------------------

def draw_euro_building_25d(draw, x, ground_y, w, h, wall_col, roof_col=TERRACOTTA, stories=5, spire=False, café=False, ink=EURO_INK):
    """2.5D sunlit European townhouse with shaded side return, balconies, roof dormers, warm glow."""
    y_top = ground_y - h
    side_w = max(14, int(w * 0.14))
    shade_col = tuple(max(0, int(c * 0.78)) for c in wall_col)
    roof_shade = tuple(max(0, int(c * 0.76)) for c in roof_col)

    # Shaded right side face (2.5D depth)
    draw.rectangle((x + w - side_w, y_top, x + w, ground_y), fill=shade_col, outline=ink, width=2)
    # Lit main facade
    fw = w - side_w
    draw.rectangle((x, y_top, x + fw, ground_y), fill=wall_col, outline=ink, width=2)

    # Subtle ground-floor stone plinth
    plinth_h = min(68, int(h * 0.16))
    plinth_col = tuple(max(0, int(c * 0.88)) for c in wall_col)
    draw.rectangle((x, ground_y - plinth_h, x + fw, ground_y), fill=plinth_col, outline=ink, width=2)

    # Mansard / gabled terracotta or slate roof
    roof_h = min(84, int(fw * 0.38))
    draw.polygon(
        [(x - 8, y_top), (x + 14, y_top - roof_h), (x + fw - 14, y_top - roof_h), (x + fw + 4, y_top)],
        fill=roof_col,
        outline=ink,
    )
    draw.polygon(
        [(x + fw - 14, y_top - roof_h), (x + w - 4, y_top - roof_h + 10), (x + w + 6, y_top), (x + fw + 4, y_top)],
        fill=roof_shade,
        outline=ink,
    )
    # Decorative cornice
    draw.rectangle((x - 6, y_top - 4, x + fw + 4, y_top + 10), fill=(248, 244, 234), outline=ink, width=2)

    if spire:
        sx = x + fw * 0.5
        draw.polygon(
            [(sx - 18, y_top - roof_h), (sx, y_top - roof_h - 135), (sx + 18, y_top - roof_h)],
            fill=(62, 118, 108),
            outline=ink,
        )
        draw.line([(sx, y_top - roof_h - 135), (sx, y_top - roof_h - 165)], fill=ink, width=3)

    # Arched / mullioned windows with cast shadow & sky reflection
    cols = max(2, int(fw // 54))
    pad_x = fw / (cols + 1)
    usable_h = h - plinth_h - 26
    story_h = usable_h / max(1, stories)
    for r in range(stories):
        wy = y_top + 22 + r * story_h
        for c in range(cols):
            wx = x + (c + 1) * pad_x
            ww = min(24, pad_x * 0.46)
            wh = min(38, story_h * 0.58)
            # Window frame shadow
            draw.rectangle((wx - ww / 2 - 2, wy - 2, wx + ww / 2 + 2, wy + wh + 2), fill=(60, 74, 92))
            # Glass with diagonal sky sheen
            draw.rectangle((wx - ww / 2, wy, wx + ww / 2, wy + wh), fill=(68, 104, 138), outline=ink, width=1)
            draw.polygon(
                [(wx - ww / 2 + 2, wy + 2), (wx + ww / 2 - 2, wy + 2), (wx - ww / 2 + 2, wy + wh * 0.6)],
                fill=(128, 174, 208),
            )
            # Mullion cross
            draw.line([(wx, wy), (wx, wy + wh)], fill=(238, 234, 224), width=2)
            draw.line([(wx - ww / 2, wy + wh * 0.45), (wx + ww / 2, wy + wh * 0.45)], fill=(238, 234, 224), width=2)
            # Wrought-iron balcony rail on alternate floors
            if r % 2 == 1:
                draw.rectangle((wx - ww * 0.72, wy + wh - 8, wx + ww * 0.72, wy + wh + 5), outline=ink, width=2)

    # Warm café awning at street level
    if café and plinth_h > 36:
        ay = ground_y - plinth_h + 6
        draw.polygon([(x + 12, ay), (x + fw - 12, ay), (x + fw - 4, ay + 22), (x + 4, ay + 22)], fill=TRAM_RED, outline=ink)
        draw.rectangle((x + 18, ay + 22, x + fw - 18, ground_y - 4), fill=(248, 224, 158), outline=ink, width=2)


def draw_chaotic_building_25d(draw, x, ground_y, w, h, wall_col, seed=0, ink=SMOG_INK):
    """2.5D weathered concrete block with grime stains, AC units, water tank, rebar, billboards."""
    rng = np.random.default_rng(seed)
    y_top = ground_y - h
    side_w = max(14, int(w * 0.14))
    shade_col = tuple(max(0, int(c * 0.72)) for c in wall_col)
    fw = w - side_w

    draw.rectangle((x + fw, y_top, x + w, ground_y), fill=shade_col, outline=ink, width=2)
    draw.rectangle((x, y_top, x + fw, ground_y), fill=wall_col, outline=ink, width=2)

    # Damp rainwater grime streaks from parapet
    grime_col = tuple(max(0, int(c * 0.78)) for c in wall_col)
    for g in range(5):
        gx = x + rng.uniform(10, fw - 18)
        gh = rng.uniform(35, min(160, h * 0.45))
        draw.rectangle((gx, y_top, gx + rng.uniform(8, 22), y_top + gh), fill=grime_col)

    # Black plastic rooftop water tank & exposed rust rebar
    tx = x + fw * 0.22
    draw.rounded_rectangle((tx, y_top - 34, tx + 38, y_top), radius=5, fill=(38, 42, 48), outline=ink, width=2)
    for i in range(5):
        rx = x + fw * 0.62 + i * 9
        draw.line([(rx, y_top), (rx + rng.uniform(-4, 4), y_top - rng.uniform(18, 36))], fill=ink, width=2)

    # Irregular concrete balconies & mismatched windows + AC boxes
    rows = max(2, int(h // 64))
    cols = max(2, int(fw // 52))
    for r in range(rows):
        for c in range(cols):
            wx = x + 14 + c * ((fw - 28) / max(1, cols))
            wy = y_top + 28 + r * ((h - 62) / max(1, rows))
            ww, wh = 24, 30
            lit = rng.random() < 0.22
            wcol = (218, 174, 96) if lit else (46, 40, 38)
            # Concrete chajja (sunshade)
            draw.polygon([(wx - 4, wy - 4), (wx + ww + 4, wy - 4), (wx + ww + 8, wy + 2), (wx - 2, wy + 2)], fill=shade_col, outline=ink)
            draw.rectangle((wx, wy + 2, wx + ww, wy + wh), fill=wcol, outline=ink, width=2)
            if rng.random() < 0.42:
                # Hanging rusty AC unit + drip pipe
                draw.rectangle((wx + ww + 2, wy + 12, wx + ww + 20, wy + 26), fill=(148, 142, 132), outline=ink, width=1)
                draw.ellipse((wx + ww + 5, wy + 15, wx + ww + 14, wy + 24), fill=(68, 64, 60))

    # Faded cluttered rooftop/wall hoarding
    if rng.random() < 0.65:
        bcol = RUST_RED if rng.random() < 0.5 else (188, 144, 48)
        draw.rectangle((x + 8, y_top + 8, x + fw - 8, y_top + 42), fill=bcol, outline=ink, width=2)
        draw.line([(x + 20, y_top + 24), (x + fw - 26, y_top + 24)], fill=(238, 228, 208), width=4)


def draw_painterly_tree(draw, x, ground_y, scale=1.0, sway=0.0, golden=False, ink=EURO_INK):
    """Organic multi-clustered painterly tree with branches, shadow pockets & sunlit rim."""
    s = scale
    th = 165 * s
    top_x = x + sway * 16 * s
    top_y = ground_y - th

    # Cast ground shadow
    draw.ellipse((x - 58 * s, ground_y - 10 * s, x + 78 * s, ground_y + 12 * s), fill=(64, 82, 66))

    # Tapered trunk + Y-branches
    draw.polygon(
        [(x - 13 * s, ground_y), (x + 13 * s, ground_y), (top_x + 5 * s, top_y), (top_x - 5 * s, top_y)],
        fill=(76, 54, 38),
        outline=ink,
    )
    draw.line([(top_x, top_y + 38 * s), (top_x - 32 * s, top_y - 6 * s)], fill=(76, 54, 38), width=max(2, int(7 * s)))
    draw.line([(top_x, top_y + 34 * s), (top_x + 34 * s, top_y - 4 * s)], fill=(76, 54, 38), width=max(2, int(7 * s)))

    # Deep shadow foliage -> mid foliage -> sunlit leaf clusters
    c_dark = (36, 78, 48) if not golden else (46, 86, 48)
    c_mid = (64, 126, 62) if not golden else (84, 144, 62)
    c_lit = (118, 178, 84) if not golden else (164, 198, 88)
    c_rim = (176, 214, 118) if not golden else (232, 224, 122)

    clusters = [
        (-48, 8, 42, c_dark), (48, 10, 40, c_dark), (0, -4, 48, c_dark),
        (-54, -22, 38, c_mid), (52, -20, 36, c_mid), (-22, -48, 44, c_mid), (26, -46, 42, c_mid),
        (-30, -64, 34, c_lit), (12, -74, 38, c_lit), (42, -48, 28, c_lit),
        (16, -86, 22, c_rim), (-18, -78, 20, c_rim),
    ]
    for dx, dy, r, col in clusters:
        bx = top_x + dx * s + sway * 5 * s
        by = top_y + dy * s
        rr = r * s
        draw.ellipse((bx - rr, by - rr * 0.85, bx + rr, by + rr * 0.85), fill=col)


def draw_gritty_trash_dump(draw, cx, ground_y, w=320, h=125, seed=1, ink=SMOG_INK):
    """Realistic jagged waste heap with rusted overflowing bin, crumpled bags, boxes & leachate stain."""
    rng = np.random.default_rng(seed)
    # Dark wet leachate puddle stain around base
    draw.ellipse((cx - w * 0.58, ground_y - 12, cx + w * 0.58, ground_y + 18), fill=(52, 46, 38))

    # Rusted tilted municipal dumpster behind pile
    bx = cx - w * 0.34
    draw.polygon(
        [(bx, ground_y - 10), (bx + 115, ground_y - 10), (bx + 124, ground_y - 96), (bx - 8, ground_y - 92)],
        fill=(78, 92, 82),
        outline=ink,
    )
    # Rust patches on dumpster
    draw.rectangle((bx + 12, ground_y - 68, bx + 54, ground_y - 32), fill=(116, 68, 46))

    # Jagged polygonal mound (shaded back + front)
    pts = [(cx - w * 0.52, ground_y)]
    for i in range(13):
        u = i / 12.0
        px = cx - w * 0.48 + w * 0.96 * u
        arch = math.sin(u * math.pi)
        py = ground_y - h * arch * rng.uniform(0.62, 1.15)
        pts.append((px, py))
    pts.append((cx + w * 0.52, ground_y))
    draw.polygon(pts, fill=(76, 68, 58), outline=ink)

    # Crumpled angular trash polygons (cardboard, black/white/blue torn bags, bottles)
    cols = [(164, 134, 96), (52, 54, 58), (206, 202, 190), (84, 126, 152), (168, 76, 60), (132, 124, 110)]
    for _ in range(38):
        ox = rng.uniform(-w * 0.44, w * 0.44)
        arch = math.sqrt(max(0.04, 1.0 - (ox / (w * 0.5)) ** 2))
        oy = rng.uniform(6, h * arch * 0.94)
        sz = rng.uniform(12, 28)
        ang = rng.uniform(0, 6.28)
        poly = []
        for k in range(5):
            a = ang + k * (6.28 / 5) + rng.uniform(-0.3, 0.3)
            rr = sz * rng.uniform(0.55, 1.05)
            poly.append((cx + ox + math.cos(a) * rr, ground_y - oy + math.sin(a) * rr * 0.72))
        col = cols[int(rng.integers(0, len(cols)))]
        draw.polygon(poly, fill=col, outline=ink)


def draw_detailed_auto(draw, cx, ground_y, scale=1.0, facing=1, bob=0.0, ink=SMOG_INK):
    """Detailed shaded auto-rickshaw with ground shadow, driver silhouette, headlight & spoked wheels."""
    s = scale
    f = facing
    y = ground_y + bob
    # Ground shadow
    draw.ellipse((cx - 64 * s, ground_y - 8 * s, cx + 64 * s, ground_y + 10 * s), fill=(48, 44, 38))
    # Lower green chassis + darker underside
    body = [
        (cx - 58 * s * f, y - 16 * s),
        (cx + 50 * s * f, y - 16 * s),
        (cx + 60 * s * f, y - 50 * s),
        (cx + 30 * s * f, y - 88 * s),
        (cx - 50 * s * f, y - 88 * s),
        (cx - 60 * s * f, y - 46 * s),
    ]
    draw.polygon(body, fill=(32, 118, 66), outline=ink)
    # Yellow canvas roof with highlight
    top = [
        (cx - 52 * s * f, y - 58 * s),
        (cx + 42 * s * f, y - 58 * s),
        (cx + 30 * s * f, y - 90 * s),
        (cx - 50 * s * f, y - 90 * s),
    ]
    draw.polygon(top, fill=(236, 188, 42), outline=ink)
    # Interior cabin shadow & driver silhouette
    draw.rectangle((min(cx - 42 * s * f, cx + 14 * s * f), y - 58 * s, max(cx - 42 * s * f, cx + 14 * s * f), y - 30 * s), fill=(26, 30, 32))
    draw.ellipse((cx + 2 * s * f - 8 * s, y - 56 * s, cx + 2 * s * f + 8 * s, y - 40 * s), fill=(52, 46, 44))
    # Slanted glass windshield with glare
    draw.polygon(
        [(cx + 26 * s * f, y - 56 * s), (cx + 52 * s * f, y - 52 * s), (cx + 36 * s * f, y - 84 * s), (cx + 20 * s * f, y - 84 * s)],
        fill=(174, 198, 208),
        outline=ink,
    )
    # Warm headlight
    draw.ellipse((cx + 52 * s * f - 6 * s, y - 44 * s, cx + 52 * s * f + 6 * s, y - 32 * s), fill=(252, 232, 146), outline=ink)
    # Wheels with hubcaps
    for wx in (-36, 36):
        draw.ellipse((cx + wx * s - 15 * s, y - 26 * s, cx + wx * s + 15 * s, y + 4 * s), fill=(28, 26, 26), outline=ink, width=2)
        draw.ellipse((cx + wx * s - 6 * s, y - 17 * s, cx + wx * s + 6 * s, y - 5 * s), fill=(154, 152, 146))


def draw_detailed_tram(draw, x, ground_y, length=520, height=136, ink=EURO_INK):
    """Sleek European tram with cast shadow, sky glass reflections, LED display & pantograph."""
    y_top = ground_y - height - 14
    # Cast shadow on tracks
    draw.rectangle((x + 12, ground_y - 8, x + length - 12, ground_y + 8), fill=(72, 78, 84))
    # White/silver aerodynamic body
    draw.rounded_rectangle((x, y_top, x + length, ground_y - 12), radius=22, fill=(246, 246, 242), outline=ink, width=3)
    # Lower grey skirt & crimson transit stripe
    draw.rectangle((x + 8, ground_y - 30, x + length - 8, ground_y - 14), fill=(74, 80, 88))
    draw.rectangle((x + 6, ground_y - 54, x + length - 6, ground_y - 30), fill=TRAM_RED)
    # Panoramic windows with diagonal specular highlights
    n_win = 6
    margin = 28
    ww = (length - margin * 2 - (n_win - 1) * 10) / n_win
    for i in range(n_win):
        wx = x + margin + i * (ww + 10)
        draw.rounded_rectangle((wx, y_top + 20, wx + ww, y_top + 76), radius=7, fill=(56, 94, 126), outline=ink, width=2)
        draw.polygon([(wx + 4, y_top + 22), (wx + ww * 0.65, y_top + 22), (wx + 4, y_top + 68)], fill=(116, 166, 202))
    # Glowing amber LED route strip on front
    draw.rectangle((x + length - 88, y_top + 8, x + length - 26, y_top + 18), fill=(248, 194, 62))
    # Pantograph reaching up to overhead wire
    px = x + length * 0.5
    draw.line([(px - 24, y_top), (px + 14, y_top - 30), (px - 18, y_top - 58)], fill=ink, width=3)
    draw.line([(px - 42, y_top - 58), (px + 14, y_top - 58)], fill=ink, width=4)


def draw_cyclist(draw, cx, ground_y, scale=1.0, phase=0.0, coat_col=(46, 88, 138), ink=EURO_INK):
    s = scale
    y = ground_y
    r = 22 * s
    draw.ellipse((cx - 46 * s, y - 5 * s, cx + 46 * s, y + 6 * s), fill=(116, 62, 52))
    draw.ellipse((cx - 34 * s - r, y - 2 * r, cx - 34 * s + r, y), outline=ink, width=max(2, int(3 * s)))
    draw.ellipse((cx + 34 * s - r, y - 2 * r, cx + 34 * s + r, y), outline=ink, width=max(2, int(3 * s)))
    draw.line([(cx - 34 * s, y - r), (cx - 4 * s, y - 46 * s), (cx + 26 * s, y - 46 * s), (cx + 34 * s, y - r)], fill=(232, 72, 62), width=max(2, int(3 * s)))
    draw.line([(cx - 4 * s, y - 46 * s), (cx, y - r)], fill=(232, 72, 62), width=max(2, int(3 * s)))
    bob = math.sin(phase) * 2.2 * s
    draw.line([(cx - 6 * s, y - 50 * s + bob), (cx + 8 * s, y - 84 * s + bob)], fill=coat_col, width=max(4, int(11 * s)))
    draw.ellipse((cx + 2 * s, y - 104 * s + bob, cx + 22 * s, y - 84 * s + bob), fill=(234, 198, 174), outline=ink, width=2)
    draw.line([(cx + 6 * s, y - 78 * s + bob), (cx + 26 * s, y - 54 * s)], fill=coat_col, width=max(2, int(5 * s)))


def draw_catenary(draw, x1, y1, x2, y2, sag=44, color=(28, 22, 20), width=2, steps=20):
    pts = []
    for i in range(steps + 1):
        u = i / steps
        x = x1 + (x2 - x1) * u
        y = y1 + (y2 - y1) * u + sag * 4.0 * u * (1.0 - u)
        pts.append((x, y))
    draw.line(pts, fill=color, width=width)


def draw_bird(draw, x, y, size=12, phase=0.0, color=(34, 46, 62), width=2):
    wing = math.sin(phase) * size * 0.75
    pts = [
        (x - size, y - wing),
        (x - size * 0.35, y - wing * 0.45 - size * 0.2),
        (x, y),
        (x + size * 0.35, y - wing * 0.45 - size * 0.2),
        (x + size, y - wing),
    ]
    draw.line(pts, fill=color, width=width, joint="curve")


# ---------------------------------------------------------------------------
# Shorts-safe Kinetic Captions, Badges & Cinematic Finishing Pass
# ---------------------------------------------------------------------------

def draw_shorts_badge(img, text, y=148, accent=TRAM_RED, bg=(18, 22, 28), alpha=1.0):
    """Top-safe editorial pill badge centered for 9:16 Shorts."""
    if alpha <= 0.02:
        return img
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    font = get_font(28, bold=True)
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    px, py = 28, 12
    x0 = W / 2 - tw / 2 - px
    y0 = y
    a = int(235 * clamp(alpha))
    d.rounded_rectangle((x0, y0, x0 + tw + px * 2, y0 + th + py * 2), radius=12, fill=(*bg, int(205 * clamp(alpha))), outline=(*accent, a), width=3)
    d.text((W / 2 - tw / 2, y0 + py - 3), text, font=font, fill=(250, 248, 242, a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def draw_shorts_caption(img, lines, t_shot=0.5, highlight_accent=(252, 206, 86)):
    """Bold, crisp, YouTube-Shorts-safe 2-line kinetic captions in lower-safe zone (y ~ 1420-1560)."""
    if not lines:
        return img
    pop = ease_out(min(1.0, t_shot * 6.5))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    font = get_font(50, bold=True)
    y_base = 1430 + int((1.0 - pop) * 24)
    a = int(255 * pop)

    for idx, line in enumerate(lines):
        bb = d.textbbox((0, 0), line, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        tx = W / 2 - tw / 2
        ty = y_base + idx * 74
        # Soft dark backing pill for 100% readability on any mobile screen
        d.rounded_rectangle(
            (tx - 24, ty - 10, tx + tw + 24, ty + th + 16),
            radius=14,
            fill=(12, 15, 20, int(185 * pop)),
        )
        # Drop shadow + main text (line 2 accented in warm gold)
        col = highlight_accent if idx == 1 else (252, 250, 246)
        d.text((tx + 2, ty + 3), line, font=font, fill=(0, 0, 0, int(200 * pop)))
        d.text((tx, ty), line, font=font, fill=(*col, a))

    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def finish_frame(img, frame_idx=0, vignette=0.26, warmth=0.0, bloom=0.14):
    """Cinematic post-processing: subtle highlight bloom, gouache paper texture, film grain & vignette."""
    arr = np.array(img, dtype=np.float32)

    # Soft cinematic bloom on highlights
    if bloom > 0.01:
        hi = np.clip(arr - 185.0, 0.0, 70.0) * (255.0 / 70.0)
        glow = cv2.GaussianBlur(hi, (0, 0), sigmaX=18, sigmaY=18)
        arr += glow * bloom

    # Cold-press paper grain (static texture — silky smooth H.264 playback, no noisy bitrate bloat)
    arr *= get_paper_texture()

    # Cinematic color grade warmth/coolness
    if abs(warmth) > 0.001:
        arr[..., 0] += warmth * 15.0
        arr[..., 2] -= warmth * 13.0

    # Vignette
    if vignette > 0.001:
        arr *= (1.0 - vignette * get_vignette_map())

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")
