"""Shot 9 (9:16 Shorts): Outro — Unified twilight skyline under one clear starry sky."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((16, 30, 64), (48, 86, 138), (228, 174, 126), mid_pos=0.60)
    img = kit.add_painted_clouds_layer(img, sec * 0.7, y_top=920, y_bot=1320, tint=(242, 196, 156), shadow=(138, 114, 122), density=0.42)
    d = ImageDraw.Draw(img)

    # Twinkling stars in clear upper twilight sky
    rng = np.random.default_rng(909)
    for i in range(85):
        sx = rng.uniform(40, kit.W - 40)
        sy = rng.uniform(70, 720)
        tw = 0.55 + 0.45 * math.sin(sec * 3.5 + i)
        r = rng.uniform(1.3, 3.0) * tw
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(252, 248, 232))

    # Unified clean skyline silhouette at bottom
    sil = (18, 24, 36)
    base = 1520
    d.rectangle((0, base, kit.W, kit.H), fill=sil)
    # Left: clean Indian dome + modern skyline
    d.rectangle((60, base - 160, 180, base), fill=sil)
    d.ellipse((70, base - 210, 170, base - 120), fill=sil)
    d.rectangle((205, base - 210, 325, base), fill=sil)
    # Center trees
    for tx in (430, 540, 650):
        d.ellipse((tx - 54, base - 95, tx + 54, base + 10), fill=sil)
    # Right: European gables + church spire
    d.rectangle((740, base - 155, 860, base), fill=sil)
    d.polygon([(735, base - 155), (800, base - 215), (865, base - 155)], fill=sil)
    d.rectangle((885, base - 185, 1005, base), fill=sil)
    d.polygon([(932, base - 185), (945, base - 320), (958, base - 185)], fill=sil)

    fade_in = kit.ease_out(min(1.0, t * 2.5))
    fade_out = 1.0 - kit.ease_in_out((t - 0.84) / 0.16)
    alpha = fade_in * fade_out

    overlay = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    f_main = kit.get_font(64, bold=True, serif=True)
    f_sub = kit.get_font(28, bold=True)

    lines = [
        ("CLEAN CITIES", f_main, 620, (252, 248, 240)),
        ("AREN'T A MIRACLE.", f_main, 705, (252, 248, 240)),
        ("THEY ARE A DECISION.", f_main, 815, (248, 204, 108)),
        ("INDIA vs EUROPE  ·  100% CODE-GENERATED", f_sub, 950, (198, 214, 232)),
    ]
    for txt, font, y_pos, col in lines:
        bb = od.textbbox((0, 0), txt, font=font)
        tw = bb[2] - bb[0]
        od.text((kit.W / 2 - tw / 2, y_pos), txt, font=font, fill=(*col, int(255 * alpha)))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = kit.finish_frame(img, global_idx, vignette=0.28, bloom=0.18)

    if t > 0.88:
        k = 1.0 - (t - 0.88) / 0.12
        arr = (np.array(img, dtype=np.float32) * kit.clamp(k)).astype(np.uint8)
        img = Image.fromarray(arr, mode="RGB")

    return img
