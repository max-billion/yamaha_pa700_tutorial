#!/usr/bin/env python3
"""Procedural from-scratch image asset generator for the Korg Pa700 Trainer UI.

Generates high-resolution PNG textures and 3D hardware sprites into ./assets/
using colors and proportions measured from upscaled_full_control_panel.png,
without copying any pixels from the reference photograph.
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def generate_panel_faceplate_bg() -> None:
    """Generates the brushed bronze-to-burgundy control panel + TouchView bezel."""
    w, h = 2400, 900
    # Coordinate grids [0..1]
    y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = x_grid / (w - 1)
    ny = y_grid / (h - 1)

    # Sampled palette from reference image:
    # Upper-left warm bronze highlight: (98, 76, 69) = #624c45
    # Mid-left rich mahogany:          (80, 54, 49) = #503631
    # Upper-right deep burgundy:       (65, 41, 36) = #412924
    # Lower deep burgundy:             (61, 33, 29) = #3d211d
    c_ul = np.array([102.0, 78.0, 70.0], dtype=np.float32)
    c_ur = np.array([68.0, 42.0, 37.0], dtype=np.float32)
    c_ll = np.array([64.0, 36.0, 32.0], dtype=np.float32)
    c_lr = np.array([56.0, 30.0, 26.0], dtype=np.float32)

    top = c_ul[None, None, :] * (1.0 - nx[:, :, None]) + c_ur[None, None, :] * nx[:, :, None]
    bot = c_ll[None, None, :] * (1.0 - nx[:, :, None]) + c_lr[None, None, :] * nx[:, :, None]
    base = top * (1.0 - ny[:, :, None] ** 0.85) + bot * (ny[:, :, None] ** 0.85)

    # Soft studio specular sheen on upper-left bronze region
    sheen = np.exp(-(((nx - 0.16) / 0.24) ** 2 + ((ny - 0.18) / 0.28) ** 2))
    base += sheen[:, :, None] * np.array([18.0, 15.0, 14.0], dtype=np.float32)

    # Subtle brushed horizontal metal grain
    rng = np.random.default_rng(700)
    grain = rng.normal(0.0, 1.8, size=(h, w // 8)).astype(np.float32)
    grain_img = Image.fromarray(np.clip(grain + 128, 0, 255).astype(np.uint8), mode="L")
    grain_img = grain_img.resize((w, h), resample=Image.Resampling.BILINEAR)
    grain_arr = (np.array(grain_img, dtype=np.float32) - 128.0) * 0.65
    base += grain_arr[:, :, None]

    arr = np.clip(base, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr, mode="RGB").convert("RGBA")

    # Outer dark chassis border & metallic bevel around faceplate
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Outer dark groove
    odraw.rounded_rectangle([2, 2, w - 3, h - 3], radius=22, outline=(18, 16, 16, 255), width=8)
    # Inner metallic highlight bevel
    odraw.rounded_rectangle([9, 9, w - 10, h - 10], radius=18, outline=(130, 96, 88, 135), width=3)
    odraw.rounded_rectangle([12, 12, w - 13, h - 13], radius=16, outline=(36, 18, 15, 160), width=2)

    # Top molded step ridge (characteristic Korg Pa700 upper panel contour)
    ridge_pts = [
        (16, 26),
        (int(w * 0.28), 26),
        (int(w * 0.315), 14),
        (int(w * 0.685), 14),
        (int(w * 0.72), 26),
        (w - 16, 26),
    ]
    odraw.line(ridge_pts, fill=(32, 16, 14, 190), width=4)
    odraw.line([(x, y + 3) for x, y in ridge_pts], fill=(135, 98, 90, 110), width=2)

    # Subtle horizontal divider groove above Row 3 and Row 4
    odraw.line([(18, int(h * 0.658)), (w - 18, int(h * 0.658))], fill=(34, 16, 14, 110), width=2)
    odraw.line([(18, int(h * 0.660)), (w - 18, int(h * 0.660))], fill=(118, 82, 74, 60), width=1)

    # TouchView Display Bezel (fx: 32.4%..67.2%, fy: 2.8%..63.2%)
    bx1, by1 = int(w * 0.324), int(h * 0.028)
    bx2, by2 = int(w * 0.672), int(h * 0.632)

    # Outer recessed shadow around bezel
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([bx1 - 6, by1 - 4, bx2 + 6, by2 + 8], radius=34, fill=(10, 6, 6, 185))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(im, shadow)

    # Bezel rim highlight + glossy black body (#131312)
    odraw.rounded_rectangle([bx1 - 2, by1 - 2, bx2 + 2, by2 + 2], radius=30, outline=(112, 76, 68, 150), width=3)
    odraw.rounded_rectangle([bx1, by1, bx2, by2], radius=28, fill=(19, 19, 18, 255), outline=(38, 38, 37, 255), width=2)

    # Subtle diagonal glass reflection across black bezel
    bezel_glass = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(bezel_glass)
    gdraw.polygon(
        [
            (bx1 + 18, by1 + 6),
            (bx1 + int((bx2 - bx1) * 0.56), by1 + 6),
            (bx1 + int((bx2 - bx1) * 0.34), by2 - 6),
            (bx1 + 18, by2 - 6),
        ],
        fill=(255, 255, 255, 9),
    )
    bezel_glass = bezel_glass.filter(ImageFilter.GaussianBlur(4))

    # Inner LCD frame recess (fx: 35.0%..64.6%, fy: 10.8%..55.8%)
    sx1, sy1 = int(w * 0.350), int(h * 0.108)
    sx2, sy2 = int(w * 0.646), int(h * 0.558)
    odraw.rectangle([sx1 - 3, sy1 - 3, sx2 + 3, sy2 + 3], fill=(8, 8, 8, 255), outline=(48, 48, 48, 200), width=1)

    # Recessed circular well for VALUE dial (center fx=0.824, fy=0.525)
    vx, vy = int(w * 0.824), int(h * 0.525)
    vr = 104
    dial_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ddraw = ImageDraw.Draw(dial_shadow)
    ddraw.ellipse([vx - vr - 8, vy - vr - 6, vx + vr + 8, vy + vr + 10], fill=(8, 4, 4, 210))
    dial_shadow = dial_shadow.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(im, dial_shadow)

    odraw.ellipse([vx - vr - 3, vy - vr - 3, vx + vr + 3, vy + vr + 3], fill=(16, 12, 12, 255), outline=(105, 70, 62, 140), width=3)
    odraw.ellipse([vx - vr + 4, vy - vr + 4, vx + vr - 4, vy + vr - 4], fill=(10, 9, 9, 255))

    im = Image.alpha_composite(im, overlay)
    im = Image.alpha_composite(im, bezel_glass)
    im.convert("RGB").save(os.path.join(ASSETS_DIR, "panel_faceplate_bg.png"), optimize=True)


def generate_speaker_grilles() -> None:
    """Generates from-scratch perforated metallic speaker grilles + dark chassis cheeks."""
    w, h = 540, 900
    for side in ("left", "right"):
        # Dark textured charcoal chassis (#2b2c28 .. #373833)
        rng = np.random.default_rng(101 if side == "left" else 202)
        noise = rng.normal(0.0, 2.2, size=(h, w)).astype(np.float32)
        y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)
        shade = 44.0 + 10.0 * (1.0 - y_grid / h) + noise
        chassis = np.stack([shade, shade + 1.0, shade - 2.0], axis=-1)
        im = Image.fromarray(np.clip(chassis, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")

        # Grille polygon mask with smooth rounded corners matching Pa700 speaker contour
        mask = Image.new("L", (w, h), 0)
        mdraw = ImageDraw.Draw(mask)
        if side == "left":
            pts = [(68, 68), (474, 68), (474, 608), (68, 514)]
        else:
            pts = [(66, 68), (472, 68), (472, 514), (66, 608)]
        mdraw.polygon(pts, fill=255)
        # Dilate with rounded circle brush (r=32) for true rounded polygon corners
        r_corner = 32
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            steps = max(abs(x1 - x0), abs(y1 - y0), 1)
            for s in range(0, steps + 1, 2):
                px = x0 + (x1 - x0) * s / steps
                py = y0 + (y1 - y0) * s / steps
                mdraw.ellipse([px - r_corner, py - r_corner, px + r_corner, py + r_corner], fill=255)
        clean_mask = mask

        # Outer dark bezel ring (r_corner + 9)
        outer_mask = Image.new("L", (w, h), 0)
        omdraw = ImageDraw.Draw(outer_mask)
        omdraw.polygon(pts, fill=255)
        r_outer = r_corner + 9
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            steps = max(abs(x1 - x0), abs(y1 - y0), 1)
            for s in range(0, steps + 1, 2):
                px = x0 + (x1 - x0) * s / steps
                py = y0 + (y1 - y0) * s / steps
                omdraw.ellipse([px - r_outer, py - r_outer, px + r_outer, py + r_outer], fill=255)

        # Underlying speaker cone silhouette + metallic mesh (#878682)
        mesh_rgb = np.zeros((h, w, 3), dtype=np.float32)
        mesh_rgb[:, :] = np.array([138.0, 137.0, 132.0], dtype=np.float32)

        cx = 285 if side == "left" else 255
        cy = 315
        dist = np.sqrt((x_grid - cx) ** 2 + (y_grid - cy) ** 2)
        # Lighter silver-white woofer cone behind mesh
        cone = np.clip(1.0 - np.abs(dist - 105.0) / 95.0, 0.0, 1.0) * 34.0
        dome = np.clip(1.0 - dist / 46.0, 0.0, 1.0) * (-18.0)
        grad = (1.0 - (y_grid / h) * 0.22) * 16.0
        mesh_rgb += (cone + dome + grad)[:, :, None]

        # Staggered micro-perforation holes
        holes = np.zeros((h, w), dtype=np.float32)
        spacing_x, spacing_y = 7, 6
        for ry in range(30, 650, spacing_y):
            offset = (spacing_x // 2) if ((ry // spacing_y) % 2 == 1) else 0
            for rx in range(28 + offset, 512, spacing_x):
                holes[ry - 1 : ry + 2, rx - 1 : rx + 2] = 1.0
        mesh_rgb = mesh_rgb * (1.0 - 0.62 * holes[:, :, None]) + np.array([22.0, 22.0, 20.0]) * (0.62 * holes[:, :, None])

        mesh_im = Image.fromarray(np.clip(mesh_rgb, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")

        # Recessed dark rounded bezel around speaker grille
        dark_bezel = Image.new("RGBA", (w, h), (13, 13, 12, 255))
        im.paste(dark_bezel, (0, 0), outer_mask)
        im.paste(mesh_im, (0, 0), clean_mask)
        im.convert("RGB").save(os.path.join(ASSETS_DIR, f"speaker_grille_{side}.png"), optimize=True)


def generate_oriental_subscale_bg() -> None:
    """Generates the Pa700 Oriental Quarter-Tone Sub-Scale recessed tray graphic."""
    w, h = 680, 210
    im = Image.new("RGBA", (w, h), (34, 35, 32, 255))
    draw = ImageDraw.Draw(im)

    # Recessed rounded tray
    draw.rounded_rectangle([6, 6, w - 7, h - 7], radius=18, fill=(24, 25, 23, 255), outline=(62, 63, 58, 255), width=3)
    draw.rounded_rectangle([10, 10, w - 11, h - 11], radius=15, outline=(12, 12, 11, 255), width=2)

    # 7 white piano keys silkscreen background (x: 26..495, y: 20..190)
    kx1, ky1, ky2 = 26, 20, 190
    key_w = 66
    gap = 3
    for i in range(7):
        x0 = kx1 + i * (key_w + gap)
        x1 = x0 + key_w
        draw.rounded_rectangle([x0, ky1, x1, ky2], radius=4, fill=(238, 239, 236, 255))

    # Carve dark upper cutouts for the 5 black keys (C#, D#, F#, G#, A#)
    black_positions = [0, 1, 3, 4, 5]
    for pos in black_positions:
        cx = kx1 + (pos + 1) * (key_w + gap) - gap // 2
        bx0 = cx - 26
        bx1 = cx + 26
        draw.rectangle([bx0, ky1 - 2, bx1, ky1 + 92], fill=(24, 25, 23, 255))

    # PRESET SC1-SC4 white bracket box on the right (x: 512..656)
    px0, py0, px1, py1 = 514, 24, 656, 188
    draw.rounded_rectangle([px0, py0, px1, py1], radius=8, outline=(232, 232, 230, 255), width=3)
    # Mask top center gap for "PRESET" text
    draw.rectangle([552, py0 - 4, 618, py0 + 6], fill=(24, 25, 23, 255))

    im.save(os.path.join(ASSETS_DIR, "oriental_subscale_bg.png"), optimize=True)


def make_rect_button(
    filename: str,
    w: int,
    h: int,
    base_rgb: tuple[int, int, int],
    tall_ridge: bool = False,
    pressed: bool = False,
) -> None:
    """Renders a 3D beveled rectangular/tall matte button sprite."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Outer recessed socket on faceplate
    draw.rounded_rectangle([1, 1, w - 2, h - 2], radius=8, fill=(10, 8, 8, 235), outline=(72, 48, 44, 110), width=1)

    pad = 5
    y_off = 2 if pressed else 0
    r, g, b = base_rgb
    if pressed:
        r, g, b = max(0, r - 6), max(0, g - 6), max(0, b - 6)

    # Subtle vertical gradient across button face
    face = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f_arr = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(pad + y_off, h - pad):
        t = (y - (pad + y_off)) / max(1, (h - 2 * pad - y_off))
        shade = 1.14 - 0.24 * t
        if tall_ridge and 0.26 <= t <= 0.31:
            # Characteristic Korg Pa700 horizontal tactile ridge on tall buttons
            shade = 1.28 if t < 0.285 else 0.82
        cr = int(np.clip(r * shade, 0, 255))
        cg = int(np.clip(g * shade, 0, 255))
        cb = int(np.clip(b * shade, 0, 255))
        f_arr[y, pad : w - pad] = [cr, cg, cb, 255]

    face_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(face_mask).rounded_rectangle([pad, pad + y_off, w - pad - 1, h - pad - 1], radius=5, fill=255)
    face = Image.fromarray(f_arr, mode="RGBA")
    im.paste(face, (0, 0), face_mask)

    # Top highlight & bottom shadow bevels
    top_hl = (min(255, r + 38), min(255, g + 38), min(255, b + 40), 130 if not pressed else 65)
    bot_sh = (max(0, r - 14), max(0, g - 14), max(0, b - 14), 210)
    draw.line([(pad + 3, pad + y_off + 1), (w - pad - 4, pad + y_off + 1)], fill=top_hl, width=2)
    draw.line([(pad + 3, h - pad - 2), (w - pad - 4, h - pad - 2)], fill=bot_sh, width=2)

    im.save(os.path.join(ASSETS_DIR, filename), optimize=True)


def make_round_button(filename: str, size: int, pressed: bool = False) -> None:
    """Renders a 3D beveled circular matte-black button sprite."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Recessed circular socket
    draw.ellipse([2, 2, size - 3, size - 3], fill=(10, 8, 8, 235), outline=(76, 50, 46, 120), width=2)

    pad = 7
    y_off = 2 if pressed else 0
    # Radial/vertical shaded cap
    cap = np.zeros((size, size, 4), dtype=np.uint8)
    cx, cy = size / 2.0, size / 2.0 + y_off
    rad = size / 2.0 - pad
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            if d <= rad:
                light = 28.0 - 10.0 * (dy / rad) - 4.0 * (d / rad) ** 2
                if pressed:
                    light -= 4.0
                v = int(np.clip(light, 12, 52))
                cap[y, x] = [v, v + 1, v + 2, 255]

    cap_im = Image.fromarray(cap, mode="RGBA")
    im = Image.alpha_composite(im, cap_im)
    draw = ImageDraw.Draw(im)
    draw.arc(
        [pad + 1, pad + y_off + 1, size - pad - 2, size - pad + y_off - 2],
        start=200,
        end=340,
        fill=(72, 74, 78, 120 if not pressed else 60),
        width=2,
    )
    im.save(os.path.join(ASSETS_DIR, filename), optimize=True)


def make_led_sprites() -> None:
    """Renders unlit, glowing red-amber, and glowing green LED lens sprites."""
    w, h = 72, 42

    # 1. Unlit smoked translucent lens
    off = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(off)
    odraw.rounded_rectangle([24, 14, 48, 26], radius=4, fill=(46, 44, 44, 235), outline=(20, 19, 19, 255), width=1)
    odraw.line([(27, 16), (45, 16)], fill=(86, 84, 84, 120), width=1)
    off.save(os.path.join(ASSETS_DIR, "led_off.png"), optimize=True)

    # 2. Lit Red/Amber LED (matches photo warm red-orange halo + hot core)
    # 3. Lit Green LED (matches START/STOP emerald-mint halo + hot core)
    configs = [
        ("led_red.png", (255, 62, 34), (255, 238, 224)),
        ("led_green.png", (62, 232, 136), (234, 255, 242)),
        ("led_amber.png", (255, 164, 36), (255, 248, 225)),
    ]
    y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2.0, h / 2.0 - 1.0
    for fname, halo_rgb, core_rgb in configs:
        # Elliptical distance for horizontal LED lens
        dx = (x_grid - cx) / 14.5
        dy = (y_grid - cy) / 9.5
        d = np.sqrt(dx * dx + dy * dy)

        glow = np.exp(-(d ** 1.65) * 1.45)
        alpha = np.clip(glow * 245.0, 0, 255)

        arr = np.zeros((h, w, 4), dtype=np.uint8)
        for c in range(3):
            arr[:, :, c] = np.clip(halo_rgb[c] * 0.9 + glow * 45.0, 0, 255).astype(np.uint8)
        arr[:, :, 3] = alpha.astype(np.uint8)

        im = Image.fromarray(arr, mode="RGBA")
        draw = ImageDraw.Draw(im)
        draw.rounded_rectangle([24, 14, 48, 26], radius=4, fill=(*halo_rgb, 255))
        draw.rounded_rectangle([27, 16, 45, 24], radius=3, fill=(*core_rgb, 255))
        im = im.filter(ImageFilter.GaussianBlur(0.5))
        im.save(os.path.join(ASSETS_DIR, fname), optimize=True)


def make_rotary_knob_sprites() -> None:
    """Renders rotary knob base shadow + rotatable knob cap with white pointer."""
    size = 128
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(base)

    # Drop shadow + outer skirt
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([20, 24, size - 20, size - 14], fill=(6, 4, 4, 210))
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))
    base = Image.alpha_composite(base, shadow)

    bdraw = ImageDraw.Draw(base)
    bdraw.ellipse([22, 22, size - 23, size - 23], fill=(20, 20, 21, 255), outline=(66, 66, 68, 190), width=2)
    bdraw.ellipse([28, 28, size - 29, size - 29], fill=(32, 33, 35, 255), outline=(14, 14, 15, 255), width=2)
    base.save(os.path.join(ASSETS_DIR, "knob_base.png"), optimize=True)

    # Rotatable cap with fluted grip ticks & bright white pointer at 12 o'clock
    cap = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cap)
    cx, cy = size // 2, size // 2
    r_outer = 31
    for deg in range(0, 360, 18):
        ang = math.radians(deg)
        x0 = cx + (r_outer - 3) * math.sin(ang)
        y0 = cy - (r_outer - 3) * math.cos(ang)
        x1 = cx + (r_outer + 1) * math.sin(ang)
        y1 = cy - (r_outer + 1) * math.cos(ang)
        cdraw.line([(x0, y0), (x1, y1)], fill=(54, 55, 58, 200), width=2)

    cdraw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(28, 29, 31, 255), outline=(74, 76, 80, 180), width=2)
    # White pointer line at top (0 deg = 12 o'clock)
    cdraw.rounded_rectangle([cx - 3, cy - 27, cx + 3, cy - 8], radius=2, fill=(246, 246, 244, 255))
    cap.save(os.path.join(ASSETS_DIR, "knob_cap.png"), optimize=True)


def make_value_dial_sprite() -> None:
    """Renders the brushed champagne-silver VALUE dial with 5 radial slots & finger dimple."""
    size = 240
    y_grid, x_grid = np.mgrid[0:size, 0:size].astype(np.float32)
    cx, cy = size / 2.0, size / 2.0
    dx, dy = x_grid - cx, y_grid - cy
    dist = np.sqrt(dx * dx + dy * dy)
    angle = np.arctan2(dy, dx)

    rad = 104.0
    # Conical brushed metallic reflection matching reference (#fdf8ec highlight -> #c8c2b6)
    conical = 0.5 + 0.5 * np.cos(2.0 * (angle + 0.65))
    radial_falloff = 1.0 - 0.14 * (dist / rad) ** 2
    lum = (212.0 + 40.0 * conical) * radial_falloff

    arr = np.zeros((size, size, 4), dtype=np.uint8)
    inside = dist <= rad
    arr[:, :, 0] = np.clip(lum * 1.01, 0, 255).astype(np.uint8)
    arr[:, :, 1] = np.clip(lum * 0.99, 0, 255).astype(np.uint8)
    arr[:, :, 2] = np.clip(lum * 0.94, 0, 255).astype(np.uint8)
    arr[:, :, 3] = np.where(inside, 255, 0).astype(np.uint8)

    im = Image.fromarray(arr, mode="RGBA")
    draw = ImageDraw.Draw(im)

    # Beveled metallic outer edge
    draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(255, 252, 244, 220), width=3)
    draw.ellipse([cx - rad + 3, cy - rad + 3, cx + rad - 3, cy + rad - 3], outline=(138, 133, 124, 180), width=2)

    # 5 dark radial tick slots (at 60, 120, 180, 240, 300 degrees from top, matching photo!)
    for deg in (60, 120, 180, 240, 300):
        ang = math.radians(deg)
        x0 = cx + 56 * math.sin(ang)
        y0 = cy - 56 * math.cos(ang)
        x1 = cx + 92 * math.sin(ang)
        y1 = cy - 92 * math.cos(ang)
        draw.line([(x0, y0), (x1, y1)], fill=(26, 25, 24, 245), width=6)

    # Concave glossy black/chrome finger dimple at 0 degrees (12 o'clock)
    dimple_cx, dimple_cy, dimple_r = cx, cy - 60, 25
    draw.ellipse(
        [dimple_cx - dimple_r, dimple_cy - dimple_r, dimple_cx + dimple_r, dimple_cy + dimple_r],
        fill=(22, 22, 23, 255),
        outline=(150, 146, 138, 220),
        width=2,
    )
    # Specular crescent inside dimple
    draw.arc(
        [dimple_cx - dimple_r + 5, dimple_cy - dimple_r + 5, dimple_cx + dimple_r - 5, dimple_cy + dimple_r - 5],
        start=200,
        end=340,
        fill=(215, 215, 215, 175),
        width=3,
    )

    im.save(os.path.join(ASSETS_DIR, "value_dial.png"), optimize=True)


def main() -> None:
    ensure_dir(ASSETS_DIR)
    print("Generating from-scratch Pa700 panel & control sprites...")
    generate_panel_faceplate_bg()
    generate_speaker_grilles()
    generate_oriental_subscale_bg()

    # Tall performance buttons (black & START/STOP crimson red #851d1c)
    make_rect_button("btn_tall_black.png", 88, 124, (27, 28, 30), tall_ridge=True, pressed=False)
    make_rect_button("btn_tall_black_pressed.png", 88, 124, (27, 28, 30), tall_ridge=True, pressed=True)
    make_rect_button("btn_tall_red.png", 96, 124, (138, 30, 29), tall_ridge=True, pressed=False)
    make_rect_button("btn_tall_red_pressed.png", 96, 124, (138, 30, 29), tall_ridge=True, pressed=True)

    # Rectangular & square buttons
    make_rect_button("btn_rect_black.png", 94, 68, (27, 28, 30), tall_ridge=False, pressed=False)
    make_rect_button("btn_rect_black_pressed.png", 94, 68, (27, 28, 30), tall_ridge=False, pressed=True)
    make_rect_button("btn_square_black.png", 74, 68, (27, 28, 30), tall_ridge=False, pressed=False)
    make_rect_button("btn_square_black_pressed.png", 74, 68, (27, 28, 30), tall_ridge=False, pressed=True)

    # Round buttons
    make_round_button("btn_round_black.png", 76, pressed=False)
    make_round_button("btn_round_black_pressed.png", 76, pressed=True)

    # LEDs, Rotary Knobs & Value Dial
    make_led_sprites()
    make_rotary_knob_sprites()
    make_value_dial_sprite()
    print(f"Done! Generated {len(os.listdir(ASSETS_DIR))} assets in {ASSETS_DIR}")


if __name__ == "__main__":
    main()
