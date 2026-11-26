"""Shot 4: The Japanese Platform — Spotless floors, safety doors, painted queues & Shinkansen."""

import math
from PIL import Image, ImageDraw
import kit
import film
import rail_kit

CAPS = film.SHOTS[3][5]


def render(frame_idx, n_frames, global_idx):
    t = frame_idx / max(1, n_frames - 1)
    sec = frame_idx / float(film.FPS)

    # Bright modern Tokyo station concourse
    img = kit.make_sky_gradient((196, 212, 226), (228, 236, 242), (240, 244, 248), mid_pos=0.45)
    d = ImageDraw.Draw(img)

    # Sleek steel canopy roof + warm recessed LED strips
    d.polygon([(0, 0), (kit.W, 0), (kit.W, 470), (0, 470)], fill=(48, 58, 72))
    for i in range(4):
        ly = 230 + i * 58
        d.rectangle((70, ly, kit.W - 70, ly + 14), fill=(246, 250, 255))

    # Hanging crisp JR station sign
    d.rounded_rectangle((310, 495, 770, 610), radius=10, fill=(248, 250, 252), outline=(36, 48, 62), width=3)
    d.rectangle((310, 565, 770, 584), fill=(24, 118, 194))
    f_sgn = kit.get_font(38, bold=True)
    d.text((390, 510), "TOKYO  ·  TRACK 14", font=f_sgn, fill=(24, 34, 46))

    # Shinkansen gliding smoothly to a gentle stop behind glass doors
    ease_stop = 1.0 - (1.0 - kit.clamp(t * 1.4)) ** 3
    nose_x = 120 + ease_stop * 860
    rail_kit.draw_shinkansen(d, nose_x, 1020, length=940, height=138, facing=1)

    # Automatic glass platform screen doors (clean silver frames + blue accent)
    door_open = kit.ease_in_out((t - 0.62) / 0.16) * 44
    for i in range(4):
        bx = 40 + i * 260
        # Fixed glass panel
        d.rectangle((bx, 860, bx + 90, 1085), fill=(196, 220, 236), outline=(56, 68, 82), width=3)
        # Sliding glass door
        d.rectangle((bx + 90 + door_open, 860, bx + 235 + door_open, 1085), fill=(214, 232, 244), outline=(56, 68, 82), width=3)
        d.rectangle((bx, 955, bx + 235, 972), fill=(26, 114, 192))

    # Spotless polished stone platform floor + yellow tactile safety strip
    d.rectangle((0, 1085, kit.W, kit.H), fill=(228, 226, 220))
    d.rectangle((0, 1110, kit.W, 1142), fill=(244, 198, 42), outline=(186, 148, 28), width=2)

    # Painted neat queuing lines + calm lined-up commuters
    for qx in (200, 720):
        d.rectangle((qx - 52, 1158, qx + 52, 1340), outline=(44, 118, 186), width=4)
        for row in range(2):
            for col_i in (-24, 24):
                px = qx + col_i
                py = 1220 + row * 68
                coat = (42, 58, 84) if (row + col_i) % 2 == 0 else (68, 76, 88)
                d.ellipse((px - 14, py - 92, px + 14, py - 64), fill=(236, 204, 182), outline=kit.EURO_INK, width=2)
                d.rounded_rectangle((px - 18, py - 62, px + 18, py - 6), radius=6, fill=coat, outline=kit.EURO_INK, width=2)

    img = kit.draw_shorts_badge(img, "JAPAN  ·  ORDER, SAFETY DOORS & CLEANLINESS", y=148, accent=(58, 196, 132), bg=(18, 42, 56))
    img = kit.finish_frame(img, global_idx, vignette=0.18, bloom=0.16)
    img = kit.draw_shorts_caption(img, CAPS, t)
    return img
