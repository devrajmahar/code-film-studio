"""Shot 9: Outro — Illuminated Night Marina Bay Sands & Supertrees under starry sky."""

import math
import numpy as np
from PIL import Image, ImageDraw
import kit
import film
import sg_kit


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    img = kit.make_sky_gradient((12, 22, 52), (38, 68, 118), (196, 138, 122), mid_pos=0.62)
    d = ImageDraw.Draw(img)

    rng = np.random.default_rng(939)
    for i in range(85):
        sx = rng.uniform(40, kit.W - 40)
        sy = rng.uniform(70, 680)
        r = rng.uniform(1.3, 3.0) * (0.55 + 0.45 * math.sin(sec * 3.5 + i))
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(252, 248, 232))

    # Illuminated Marina Bay Sands & glowing night Supertrees at bottom
    base_y = 1540
    d.rectangle((0, base_y, kit.W, kit.H), fill=(18, 30, 52))
    sg_kit.draw_marina_bay_sands(d, 540, base_y, scale=1.15, night=True)
    for sx, sc in [(180, 0.95), (890, 0.95)]:
        sg_kit.draw_supertree(d, sx, base_y + 10, scale=sc, night=True)

    fade = kit.ease_out(min(1.0, t * 2.8)) * (1.0 - kit.ease_in_out((t - 0.84) / 0.16))
    ov = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    f_main = kit.get_font(60, bold=True, serif=True)
    f_sub = kit.get_font(28, bold=True)

    for txt, font, y_pos, col in [
        ("POVERTY ISN'T DESTINY.", f_main, 560, (252, 248, 240)),
        ("LEADERSHIP IS.", f_main, 650, (104, 248, 174)),
        ("SINGAPORE  ·  CODE FILM STUDIO", f_sub, 780, (198, 214, 232)),
    ]:
        bb = od.textbbox((0, 0), txt, font=font)
        od.text((kit.W / 2 - (bb[2] - bb[0]) / 2, y_pos), txt, font=font, fill=(*col, int(255 * fade)))

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    img = kit.finish_frame(img, global_idx, vignette=0.28, bloom=0.22)
    if t > 0.88:
        k = kit.clamp(1.0 - (t - 0.88) / 0.12)
        img = Image.fromarray((np.array(img, dtype=np.float32) * k).astype(np.uint8), mode="RGB")
    return img
