#!/usr/bin/env python3
"""
Aditya Kumar — GitHub Profile Asset Generator
----------------------------------------------
Generates custom-branded developer profile graphics from source portrait:
1. assets/aditya_profile_card.png   -> Futuristic Cyber / Developer ID Card (1060x490)
2. assets/aditya_avatar_hud.png     -> Circular Neon HUD Avatar with dark backdrop (500x500)
3. assets/aditya_code_art.svg       -> Vector Code-Matrix Portrait rendered purely with code tokens
4. assets/aditya_ascii_art.txt      -> Terminal ASCII Art Portrait

Usage:
    python scripts/generate_profile_assets.py
    python scripts/generate_profile_assets.py --input "path/to/image.jpg" --outdir "assets"
"""

import os
import sys
import math
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def find_font(font_names, size):
    """Attempt to load one of the specified system fonts or fall back to default."""
    font_dirs = [
        "C:/Windows/Fonts",
        os.path.expanduser("~/.fonts"),
        "/usr/share/fonts/truetype",
        "/System/Library/Fonts"
    ]
    for name in font_names:
        for fdir in font_dirs:
            fpath = os.path.join(fdir, name)
            if os.path.exists(fpath):
                try:
                    return ImageFont.truetype(fpath, size)
                except Exception:
                    pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def crop_smart_portrait(img_path):
    """Intelligently detects face center and crops a balanced square portrait."""
    pil_img = Image.open(img_path).convert("RGB")
    width, height = pil_img.size

    cx = width / 2.0
    cy = height / 2.0
    face_size = min(width, height) * 0.72

    if HAS_CV2:
        try:
            cv_img = cv2.imread(img_path)
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) > 0:
                best_face = max(faces, key=lambda f: f[2] * f[3])
                fx, fy, fw, fh = best_face
                cx = fx + fw / 2.0
                cy = fy + fh / 2.0 + fh * 0.16
                face_size = fh * 2.15
        except Exception as e:
            print(f"Face detection fallback: {e}")

    box_size = int(face_size)
    box_size = min(box_size, width, height)
    
    x0 = int(cx - box_size / 2.0)
    y0 = int(cy - box_size / 2.0)

    if x0 < 0:
        x0 = 0
    if y0 < 0:
        y0 = 0
    if x0 + box_size > width:
        x0 = width - box_size
    if y0 + box_size > height:
        y0 = height - box_size

    cropped = pil_img.crop((x0, y0, x0 + box_size, y0 + box_size))
    
    # Polish clarity & contrast
    enhancer = ImageEnhance.Sharpness(cropped)
    cropped = enhancer.enhance(1.22)
    enhancer = ImageEnhance.Contrast(cropped)
    cropped = enhancer.enhance(1.08)

    return cropped

def draw_chamfer_box(draw, xy, chamfer, outline=None, fill=None, width=1):
    """Draw a rectangle with diagonal chamfered corners."""
    x0, y0, x1, y1 = xy
    c = chamfer
    pts = [
        (x0 + c, y0),
        (x1 - c, y0),
        (x1, y0 + c),
        (x1, y1 - c),
        (x1 - c, y1),
        (x0 + c, y1),
        (x0, y1 - c),
        (x0, y0 + c)
    ]
    if fill:
        draw.polygon(pts, fill=fill)
    if outline:
        draw.polygon(pts, outline=outline, width=width)

def generate_profile_card(portrait, out_path):
    """Generates a high-resolution 1060x490 futuristic Operator ID / Profile Card."""
    W, H = 1060, 490
    card = Image.new("RGBA", (W, H), (2, 10, 20, 255))
    draw = ImageDraw.Draw(card)

    # 1. Background gradient and tech grid
    for y in range(H):
        ratio = y / float(H)
        r = int(2 + ratio * 5)
        g = int(10 + ratio * 14)
        b = int(20 + ratio * 20)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Dot grid matrix
    grid_gap = 24
    for gx in range(24, W - 24, grid_gap):
        for gy in range(24, H - 24, grid_gap):
            draw.point((gx, gy), fill=(0, 245, 255, 30))

    # Tech circuit accent lines
    draw.line([(0, 44), (W, 44)], fill=(0, 245, 255, 60), width=1)
    draw.line([(0, H - 42), (W, H - 42)], fill=(0, 245, 255, 60), width=1)
    draw.line([(325, 44), (325, H - 42)], fill=(0, 245, 255, 45), width=1)

    # Outer borders with chamfered corners
    draw_chamfer_box(draw, (8, 8, W - 9, H - 9), chamfer=16, outline=(0, 245, 255, 130), width=2)
    draw_chamfer_box(draw, (14, 14, W - 15, H - 15), chamfer=12, outline=(0, 245, 255, 40), width=1)

    # Corner bracket accents
    bracket_len = 26
    c_color = (0, 245, 255, 240)
    # TL
    draw.line([(18, 18), (18 + bracket_len, 18)], fill=c_color, width=3)
    draw.line([(18, 18), (18, 18 + bracket_len)], fill=c_color, width=3)
    # TR
    draw.line([(W - 19 - bracket_len, 18), (W - 19, 18)], fill=c_color, width=3)
    draw.line([(W - 19, 18), (W - 19, 18 + bracket_len)], fill=c_color, width=3)
    # BL
    draw.line([(18, H - 19), (18 + bracket_len, H - 19)], fill=c_color, width=3)
    draw.line([(18, H - 19 - bracket_len), (18, H - 19)], fill=c_color, width=3)
    # BR
    draw.line([(W - 19 - bracket_len, H - 19), (W - 19, H - 19)], fill=c_color, width=3)
    draw.line([(W - 19, H - 19 - bracket_len), (W - 19, H - 19)], fill=c_color, width=3)

    # Fonts
    font_title = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 30)
    font_sub = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 15)
    font_bold = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 12)
    font_code = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 12)
    font_small = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 11)

    # 2. Top Header Bar
    draw.ellipse([(28, 20), (38, 30)], fill=(57, 255, 20, 255))
    draw.ellipse([(25, 17), (41, 33)], outline=(57, 255, 20, 90), width=1)
    draw.text((46, 17), "SYS: AK-OS // v4.2  [ ACTIVE ]", fill=(57, 255, 20, 235), font=font_small)
    draw.text((345, 17), "SECURITY: PBKDF2 + AES-256 (FERNET) // ENCRYPTED", fill=(0, 245, 255, 180), font=font_small)
    draw.text((W - 275, 17), "TMU CSE (IBM) // MORADABAD [IN]", fill=(0, 245, 255, 210), font=font_small)

    # 3. Left Section: Circular HUD Avatar
    avatar_center = (168, 215)
    avatar_radius = 112
    
    p_size = avatar_radius * 2
    resized_portrait = portrait.resize((p_size, p_size), Image.Resampling.LANCZOS)

    # Circular mask with soft edge
    mask = Image.new("L", (p_size, p_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([(0, 0), (p_size - 1, p_size - 1)], fill=255)

    card.paste(resized_portrait, (avatar_center[0] - avatar_radius, avatar_center[1] - avatar_radius), mask)

    # Inner cyber border
    draw.ellipse([
        (avatar_center[0] - avatar_radius - 2, avatar_center[1] - avatar_radius - 2),
        (avatar_center[0] + avatar_radius + 2, avatar_center[1] + avatar_radius + 2)
    ], outline=(0, 245, 255, 230), width=2)
    
    # Outer dashed ring
    outer_r = avatar_radius + 14
    draw.ellipse([
        (avatar_center[0] - outer_r, avatar_center[1] - outer_r),
        (avatar_center[0] + outer_r, avatar_center[1] + outer_r)
    ], outline=(0, 245, 255, 75), width=1)

    # Radar tick marks
    for angle_deg in range(0, 360, 30):
        rad = math.radians(angle_deg)
        r1 = outer_r + 2
        r2 = outer_r + (8 if angle_deg % 90 == 0 else 4)
        x1 = avatar_center[0] + int(r1 * math.cos(rad))
        y1 = avatar_center[1] + int(r1 * math.sin(rad))
        x2 = avatar_center[0] + int(r2 * math.cos(rad))
        y2 = avatar_center[1] + int(r2 * math.sin(rad))
        color = (57, 255, 20, 240) if angle_deg % 90 == 0 else (0, 245, 255, 130)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)

    # Operator Verified Badge under avatar
    badge_y = 358
    draw_chamfer_box(draw, (44, badge_y, 292, badge_y + 32), chamfer=6, fill=(5, 24, 40, 230), outline=(0, 245, 255, 190), width=1)
    draw.text((64, badge_y + 7), "◈ SYSTEM OPERATOR · VERIFIED ◈", fill=(0, 245, 255, 245), font=font_small)

    draw.text((62, 403), "HANDLE: @Aditya-tmu", fill=(56, 217, 245, 210), font=font_small)
    draw.text((62, 421), "COORDS: 28.8386 N, 78.7733 E", fill=(0, 245, 255, 140), font=font_small)

    # 4. Right Section: Profile & Telemetry Data
    rx = 350
    # Name
    draw.text((rx, 58), "ADITYA KUMAR", fill=(0, 245, 255, 255), font=font_title)
    # Role Title
    draw.text((rx, 98), "Full-Stack Developer  •  AI & Scalable Systems Engineer", fill=(56, 217, 245, 240), font=font_sub)

    # Divider bar
    draw.line([(rx, 126), (W - 35, 126)], fill=(0, 245, 255, 75), width=1)

    # Specs table
    specs = [
        ("EDUCATION", "B.Tech in Computer Science & Eng. (IBM) @ TMU Moradabad"),
        ("FLAGSHIPS", "SkillNest (Gemini AI Marketplace) · Vindywashini Books · File Vault"),
        ("FULL-STACK", "React · Django · TypeScript · Node.js · Express · WebSockets · Vite"),
        ("DESK/APP  ", "Electron Desktop Billing Suite · Native Android App (Kotlin)"),
        ("SECURITY ", "AES-256 (Fernet) · PBKDF2 (390k iters) · SHA-256 · MongoDB Atlas"),
        ("AI / ML   ", "Google Gemini AI API · TFLite Mobile ML · Regression Models"),
        ("DATABASES", "PostgreSQL · MongoDB Atlas · MySQL · Redis"),
        ("CREED    ", "\"Building scalable software that solves actual real-world problems.\""),
    ]

    sy = 138
    line_h = 24
    for key, val in specs:
        draw.text((rx, sy), key, fill=(57, 255, 20, 235), font=font_bold)
        draw.text((rx + 90, sy), "::", fill=(0, 245, 255, 150), font=font_code)
        val_color = (255, 215, 0, 240) if "CREED" in key else (215, 245, 255, 235)
        draw.text((rx + 116, sy), val, fill=val_color, font=font_code)
        sy += line_h

    # 5. Bottom Footer Bar
    draw.text((28, H - 33), "HOSTED: GITHUB PAGES // VERCEL", fill=(0, 245, 255, 150), font=font_small)
    draw.text((350, H - 33), "LATENCY: 8ms  •  INTEGRITY: SHA-256 VERIFIED  •  STATUS: HTTP 200 OK", fill=(57, 255, 20, 210), font=font_small)
    draw.text((W - 200, H - 33), "NODE: ASIA-SOUTH-1 ✓", fill=(0, 245, 255, 150), font=font_small)

    card.save(out_path, format="PNG")
    print(f"[OK] Generated: {out_path}")

def generate_avatar_hud(portrait, out_path):
    """Generates a standalone circular HUD Avatar with dark obsidian backdrop (500x500)."""
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = (S // 2, S // 2)

    # Dark background circle with cyber gradient
    bg_radius = 242
    draw.ellipse([
        (center[0] - bg_radius, center[1] - bg_radius),
        (center[0] + bg_radius, center[1] + bg_radius)
    ], fill=(2, 10, 20, 250), outline=(0, 245, 255, 90), width=2)

    # Outer HUD Ring
    outer_r = 228
    draw.ellipse([
        (center[0] - outer_r, center[1] - outer_r),
        (center[0] + outer_r, center[1] + outer_r)
    ], outline=(0, 245, 255, 80), width=1)

    # Ticks on outer ring
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        is_cardinal = (deg % 90 == 0)
        is_major = (deg % 30 == 0)
        t_len = 16 if is_cardinal else (10 if is_major else 5)
        color = (57, 255, 20, 240) if is_cardinal else ((0, 245, 255, 190) if is_major else (0, 245, 255, 70))
        
        x1 = center[0] + int(outer_r * math.cos(rad))
        y1 = center[1] + int(outer_r * math.sin(rad))
        x2 = center[0] + int((outer_r - t_len) * math.cos(rad))
        y2 = center[1] + int((outer_r - t_len) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2 if is_cardinal else 1)

    # Second inner ring
    mid_r = 200
    draw.ellipse([
        (center[0] - mid_r, center[1] - mid_r),
        (center[0] + mid_r, center[1] + mid_r)
    ], outline=(0, 245, 255, 130), width=1)

    # Portrait Circle
    port_r = 184
    p_size = port_r * 2
    resized_portrait = portrait.resize((p_size, p_size), Image.Resampling.LANCZOS)

    p_mask = Image.new("L", (p_size, p_size), 0)
    p_mask_draw = ImageDraw.Draw(p_mask)
    p_mask_draw.ellipse([(0, 0), (p_size - 1, p_size - 1)], fill=255)

    img.paste(resized_portrait, (center[0] - port_r, center[1] - port_r), p_mask)

    # Border around portrait
    draw.ellipse([
        (center[0] - port_r, center[1] - port_r),
        (center[0] + port_r, center[1] + port_r)
    ], outline=(0, 245, 255, 255), width=3)
    draw.ellipse([
        (center[0] - port_r - 4, center[1] - port_r - 4),
        (center[0] + port_r + 4, center[1] + port_r + 4)
    ], outline=(57, 255, 20, 170), width=1)

    # Cardinal labels
    font_hud = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 12)
    draw.text((center[0] - 6, 10), "N", fill=(57, 255, 20, 240), font=font_hud)
    draw.text((center[0] - 6, S - 26), "S", fill=(57, 255, 20, 240), font=font_hud)
    draw.text((12, center[1] - 8), "W", fill=(57, 255, 20, 240), font=font_hud)
    draw.text((S - 22, center[1] - 8), "E", fill=(57, 255, 20, 240), font=font_hud)

    # Bottom badge
    draw_chamfer_box(draw, (115, S - 58, S - 115, S - 22), chamfer=6, fill=(2, 10, 20, 245), outline=(0, 245, 255, 210), width=1)
    font_badge = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 11)
    draw.text((136, S - 46), "◈ ADITYA KUMAR · OPERATOR ◈", fill=(0, 245, 255, 245), font=font_badge)

    img.save(out_path, format="PNG")
    print(f"[OK] Generated: {out_path}")

def generate_code_art_svg(portrait, out_path):
    """Generates an SVG vector graphic of the portrait composed of code tokens."""
    COLS = 85
    ROWS = 55
    
    small_img = portrait.resize((COLS, ROWS), Image.Resampling.BILINEAR)
    gray_img = small_img.convert("L")
    rgb_img = small_img.convert("RGB")

    code_tokens = [
        "const", "let", "def", "class", "return", "async", "await", "import",
        "React", "Django", "Kotlin", "Gemini", "Node", "Vite", "Vault", "GST",
        "if", "else", "for", "while", "lambda", "try", "catch", "Aditya",
        "1", "0", "{", "}", "[", "]", "<", ">", "=>", "==", "!=", "&&", "||"
    ]

    cell_w = 8.5
    cell_h = 12.0
    svg_w = int(COLS * cell_w + 40)
    svg_h = int(ROWS * cell_h + 80)

    token_idx = 0

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="auto">',
        '  <defs>',
        '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#020a14" />',
        '      <stop offset="50%" stop-color="#051828" />',
        '      <stop offset="100%" stop-color="#020a14" />',
        '    </linearGradient>',
        '  </defs>',
        f'  <rect width="{svg_w}" height="{svg_h}" rx="14" fill="url(#bgGrad)" stroke="#00f5ff" stroke-opacity="0.35" stroke-width="1.5" />',
        '  <!-- Header Banner -->',
        f'  <text x="24" y="28" fill="#39ff14" font-family="Consolas, Fira Code, monospace" font-size="12" font-weight="bold">◈ CODE-SYNTHESIZED OPERATOR PORTRAIT // ADITYA KUMAR (@Aditya-tmu)</text>',
        f'  <text x="{svg_w - 24}" y="28" text-anchor="end" fill="#00f5ff" font-family="Consolas, Fira Code, monospace" font-size="11">SYNTAX ENGINE: PYTHON • REACT • KOTLIN</text>',
        f'  <line x1="20" y1="38" x2="{svg_w - 20}" y2="38" stroke="#00f5ff" stroke-opacity="0.25" stroke-width="1" />',
        '  <!-- Code Characters Grid -->'
    ]

    offset_x = 20
    offset_y = 52

    for r in range(ROWS):
        c = 0
        while c < COLS:
            token = code_tokens[token_idx % len(code_tokens)]
            token_idx += 1
            for ch in token:
                if c >= COLS:
                    break
                lum = gray_img.getpixel((c, r))
                norm = lum / 255.0
                
                if norm < 0.15:
                    fill_color = "#072033"
                    opacity = "0.35"
                    weight = "normal"
                elif norm < 0.40:
                    fill_color = "#007a8a"
                    opacity = "0.7"
                    weight = "normal"
                elif norm < 0.65:
                    fill_color = "#00d4e6"
                    opacity = "0.9"
                    weight = "600"
                elif norm < 0.85:
                    fill_color = "#00f5ff"
                    opacity = "1.0"
                    weight = "bold"
                else:
                    fill_color = "#e0ffff" if (c + r) % 3 != 0 else "#39ff14"
                    opacity = "1.0"
                    weight = "bold"

                px = offset_x + c * cell_w
                py = offset_y + r * cell_h

                ch_esc = "&lt;" if ch == "<" else ("&gt;" if ch == ">" else ("&amp;" if ch == "&" else ch))
                svg_lines.append(
                    f'  <text x="{px:.1f}" y="{py:.1f}" fill="{fill_color}" opacity="{opacity}" '
                    f'font-family="Consolas, Fira Code, monospace" font-size="9" font-weight="{weight}">{ch_esc}</text>'
                )
                c += 1

    svg_lines.extend([
        f'  <line x1="20" y1="{svg_h - 26}" x2="{svg_w - 20}" y2="{svg_h - 26}" stroke="#00f5ff" stroke-opacity="0.25" stroke-width="1" />',
        f'  <text x="24" y="{svg_h - 10}" fill="#00f5ff" opacity="0.8" font-family="Consolas, Fira Code, monospace" font-size="10">STATUS: 200 OK  •  SOURCE: "C:\\Users\\adity\\Desktop\\Aditya.jpeg"  •  GENERATED AUTOMATICALLY VIA CODE</text>',
        f'  <text x="{svg_w - 24}" y="{svg_h - 10}" text-anchor="end" fill="#39ff14" opacity="0.9" font-family="Consolas, Fira Code, monospace" font-size="10">RUNTIME: Python 3.12 + Pillow + OpenCV ✓</text>',
        '</svg>'
    ])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"[OK] Generated: {out_path}")

def generate_ascii_art(portrait, out_path):
    """Generates a text ASCII art file of Aditya's portrait for terminal / pre blocks."""
    WIDTH = 68
    chars = "@%#*+=-:. "
    
    # Aspect ratio adjustment (characters are taller than wide, ~2:1)
    aspect = portrait.size[1] / portrait.size[0]
    height = int(WIDTH * aspect * 0.5)
    
    small = portrait.resize((WIDTH, height), Image.Resampling.BILINEAR).convert("L")
    
    ascii_rows = []
    ascii_rows.append("/*" + "═" * 70 + "*/")
    ascii_rows.append("/*  ADITYA KUMAR · CODE-SYNTHESIZED ASCII OPERATOR PORTRAIT           */")
    ascii_rows.append("/*  @Aditya-tmu  ·  B.Tech CSE (IBM)  ·  Full-Stack & AI Builder        */")
    ascii_rows.append("/*" + "═" * 70 + "*/\n")

    for y in range(height):
        row = ""
        for x in range(WIDTH):
            pixel = small.getpixel((x, y))
            char_idx = int((pixel / 255.0) * (len(chars) - 1))
            row += chars[char_idx]
        ascii_rows.append(row)

    ascii_rows.append("\n/* [END PORTRAIT] AUTOMATICALLY GENERATED FROM C:\\Users\\adity\\Desktop\\Aditya.jpeg */")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ascii_rows))
    print(f"[OK] Generated: {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate GitHub profile graphics from portrait.")
    parser.add_argument("--input", default=None, help="Input image path")
    parser.add_argument("--outdir", default=None, help="Output directory for generated assets")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    assets_dir = args.outdir or os.path.join(repo_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    candidates = [
        args.input,
        os.path.join(assets_dir, "Aditya.jpeg"),
        r"C:\Users\adity\Desktop\Aditya.jpeg",
        "Aditya.jpeg"
    ]
    input_path = None
    for c in candidates:
        if c and os.path.exists(c):
            input_path = c
            break

    if not input_path:
        print("[ERROR] Could not find input image at any expected location!")
        sys.exit(1)

    print(f"[*] Processing source image: {input_path}")
    portrait = crop_smart_portrait(input_path)

    card_path = os.path.join(assets_dir, "aditya_profile_card.png")
    avatar_path = os.path.join(assets_dir, "aditya_avatar_hud.png")
    svg_path = os.path.join(assets_dir, "aditya_code_art.svg")
    ascii_path = os.path.join(assets_dir, "aditya_ascii_art.txt")

    print("[*] Generating Futuristic Profile Card...")
    generate_profile_card(portrait, card_path)

    print("[*] Generating Neon HUD Avatar...")
    generate_avatar_hud(portrait, avatar_path)

    print("[*] Generating Synthesized Code Vector Art (SVG)...")
    generate_code_art_svg(portrait, svg_path)

    print("[*] Generating Terminal ASCII Portrait...")
    generate_ascii_art(portrait, ascii_path)

    print("\n[SUCCESS] All profile image assets generated successfully!")

if __name__ == "__main__":
    main()
