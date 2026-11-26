"""Shot 7: Safety Record — Golden sunset over Mount Fuji, lit Shinkansen & 60+ Years Zero Fatalities."""

import math
from PIL import Image, ImageDraw
import kit
import film
import rail_kit

CAPS = film.SHOTS[6][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    # Breathtaking golden-violet Japanese sunset
    img = kit.make_sky_gradient((34, 52, 98), (168, 102, 118), (248, 186, 126), mid_pos=0.52)
    img = kit.add_sun_and_rays(img, 540, 760, 88, (255, 244, 202), (252, 168, 104), rays=True, ray_alpha=0.22, halo_alpha=0.65)
    img = kit.add_painted_clouds_layer(img, sec * 0.8, y_top=220, y_bot=740, tint=(255, 214, 178), shadow=(142, 92, 112), density=0.45)
    d = ImageDraw.Draw(img)

    # Silhouetted purple-indigo Mount Fuji glowing in sunset
    rail_kit.draw_mt_fuji(d, 540, 1120, width=980, height=450, body_col=(54, 52, 86), snow_col=(252, 224, 202))

    # Calm reflecting lake
    d.rectangle((0, 1120, kit.W, kit.H), fill=(48, 56, 84))
    for r in range(24):
        ry = 1140 + r * 14
        rx = ((r * 211 + sec * 24) % (kit.W + 100)) - 50
        d.line([(rx, ry), (rx + 72, ry)], fill=(246, 182, 128), width=2)

    # Sleek elevated bridge + illuminated Shinkansen gliding silently
    rail_kit.draw_viaduct(d, 1085, col=(56, 64, 82), shade=(36, 42, 58))
    nose_x = 180 + t * 1280
    rail_kit.draw_shinkansen(d, nose_x, 1075, length=840, height=96, facing=1, lit_windows=True)

    # Big clean hero stat overlay in upper sky
    ov = Image.new("RGBA", (kit.W, kit.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    pop = kit.ease_out(min(1.0, t * 2.5))
    od.rounded_rectangle((96, 300, kit.W - 96, 565), radius=24, fill=(14, 20, 34, int(185 * pop)), outline=(252, 206, 104, int(230 * pop)), width=3)
    f_big = kit.get_font(92, bold=True)
    f_sub = kit.get_font(34, bold=True)
    t1 = "0 FATALITIES"
    b1 = od.textbbox((0, 0), t1, font=f_big)
    od.text((kit.W / 2 - (b1[2] - b1[0]) / 2, 326), t1, font=f_big, fill=(104, 248, 174, int(255 * pop)))
    t2 = "60+ YEARS  ·  10 BILLION PASSENGERS"
    b2 = od.textbbox((0, 0), t2, font=f_sub)
    od.text((kit.W / 2 - (b2[2] - b2[0]) / 2, 466), t2, font=f_sub, fill=(252, 244, 232, int(245 * pop)))

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    img = kit.draw_shorts_badge(img, "SAFETY  ·  60 YEARS WITHOUT A DERAILMENT", y=148, accent=(104, 248, 174), bg=(18, 28, 42))
    img = kit.finish_frame(img, global_idx, vignette=0.22, warmth=0.12, bloom=0.22)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
