"""Shot 9: Outro — Illuminated bullet train gliding across twilight bridge under stars."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import rail_kit


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((14, 26, 58), (44, 78, 128), (222, 166, 124), mid_pos=0.60)
    d = ImageDraw.Draw(img)

    rng = np.random.default_rng(919)
    for i in range(85):
        sx = rng.uniform(40, kit.W - 40)
        sy = rng.uniform(70, 720)
        r = rng.uniform(1.3, 3.0) * (0.55 + 0.45 * math.sin(sec * 3.5 + i))
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(252, 248, 232))

    # Elevated bridge silhouette & glowing train streaking across
    rail_kit.draw_viaduct(d, 1460, col=(24, 30, 44), shade=(16, 20, 32))
    rail_kit.draw_shinkansen(d, 220 + t * 1180, 1450, length=820, height=84, stripe_col=(58, 176, 244), facing=1, lit_windows=True)

    fade = kit.ease_out(min(1.0, t * 2.8)) * (1.0 - kit.ease_in_out((t - 0.84) / 0.16))
    ov = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    f_main = kit.get_font(62, bold=True, serif=True)
    f_sub = kit.get_font(28, bold=True)

    for txt, font, y_pos, col in [
        ("GREAT TRANSIT", f_main, 635, (252, 248, 240)),
        ("BUILDS GREAT NATIONS.", f_main, 725, (248, 204, 108)),
        ("JAPAN vs INDIA  ·  CODE FILM STUDIO", f_sub, 860, (198, 214, 232)),
    ]:
        bb = od.textbbox((0, 0), txt, font=font)
        od.text((kit.W / 2 - (bb[2] - bb[0]) / 2, y_pos), txt, font=font, fill=(*col, int(255 * fade)))

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    img = kit.finish_frame(img, global_idx, vignette=0.28, bloom=0.20)
    if t > 0.88:
        k = kit.clamp(1.0 - (t - 0.88) / 0.12)
        img = Image.fromarray((np.array(img, dtype=np.float32) * k).astype(np.uint8), mode="RGB")
    return img
