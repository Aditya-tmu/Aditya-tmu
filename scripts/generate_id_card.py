#!/usr/bin/env python3
"""
Aditya Kumar — Realistic ID Badge & 3D Flip Generator
------------------------------------------------------
Generates:
1. assets/aditya_id_card_front.png   -> Realistic Physical Smart ID Badge (Front, 600x950)
2. assets/aditya_id_card_back.png    -> Realistic Physical Smart ID Badge (Back, 600x950)
3. assets/aditya_id_card_3d_flip.gif -> Smooth 3D Spinning / Flipping Animation
4. assets/aditya_achievements.svg    -> High-Contrast Glowing Achievement Nodes Grid (GitHub SVG Compatible)
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def find_font(font_names, size):
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
    pil_img = Image.open(img_path).convert("RGB")
    width, height = pil_img.size
    cx, cy = width / 2.0, height / 2.0
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
        except Exception:
            pass

    box_size = int(min(face_size, width, height))
    x0 = max(0, min(int(cx - box_size / 2.0), width - box_size))
    y0 = max(0, min(int(cy - box_size / 2.0), height - box_size))
    cropped = pil_img.crop((x0, y0, x0 + box_size, y0 + box_size))
    
    # Mild enhance
    cropped = ImageEnhance.Sharpness(cropped).enhance(1.22)
    cropped = ImageEnhance.Contrast(cropped).enhance(1.08)
    return cropped

def draw_lanyard_punch(draw, cx, cy, w=120, h=26):
    """Draws a realistic lanyard punch hole slot with metallic bezel."""
    x0, y0, x1, y1 = cx - w//2, cy - h//2, cx + w//2, cy + h//2
    draw.rounded_rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], radius=14, outline=(70, 90, 115, 255), width=2)
    draw.rounded_rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + 1], radius=13, outline=(170, 205, 235, 220), width=1)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=(4, 8, 14, 255))
    draw.line([(x0 + 8, y0 + 3), (x1 - 8, y0 + 3)], fill=(2, 4, 8, 255), width=2)

def draw_emv_chip(draw, x, y, w=84, h=66):
    """Draws a realistic gold smartcard EMV chip with contact pins."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(212, 175, 55, 255), outline=(170, 135, 30, 255), width=2)
    draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + h - 3], radius=6, outline=(245, 215, 110, 255), width=1)
    mid_y = y + h // 2
    draw.line([(x + 6, mid_y), (x + w - 6, mid_y)], fill=(130, 100, 20, 255), width=2)
    draw.line([(x + w // 3, y + 6), (x + w // 3, mid_y)], fill=(130, 100, 20, 255), width=2)
    draw.line([(x + 2 * w // 3, y + 6), (x + 2 * w // 3, mid_y)], fill=(130, 100, 20, 255), width=2)
    draw.line([(x + w // 3, mid_y), (x + w // 3, y + h - 6)], fill=(130, 100, 20, 255), width=2)
    draw.line([(x + 2 * w // 3, mid_y), (x + 2 * w // 3, y + h - 6)], fill=(130, 100, 20, 255), width=2)
    cw, ch = 28, 20
    draw.ellipse([x + w//2 - cw//2, y + h//2 - ch//2, x + w//2 + cw//2, y + h//2 + ch//2], outline=(130, 100, 20, 255), fill=(230, 195, 75, 255), width=1)

def draw_rfid_wave(draw, x, y, color=(0, 245, 255, 220)):
    for r in [8, 14, 20]:
        draw.arc([x - r, y - r, x + r, y + r], start=-45, end=45, fill=color, width=2)

def draw_hologram_seal(draw, x, y, r=38):
    colors = [
        (255, 100, 150, 190),
        (255, 200, 50, 190),
        (50, 255, 150, 190),
        (0, 245, 255, 210),
        (150, 100, 255, 190)
    ]
    for i, col in enumerate(colors):
        cr = r - i * 6
        if cr > 4:
            draw.ellipse([x - cr, y - cr, x + cr, y + cr], outline=col, width=2)
    star_pts = []
    for step in range(10):
        sr = 11 if step % 2 == 0 else 5
        ang = step * (math.pi / 5) - math.pi / 2
        star_pts.append((x + int(sr * math.cos(ang)), y + int(sr * math.sin(ang))))
    draw.polygon(star_pts, fill=(255, 255, 255, 240))

def draw_barcode(draw, x, y, w, h, code_str="TMU-052974-2023"):
    random.seed(42)
    curr_x = x
    while curr_x < x + w - 4:
        bar_w = random.choice([1, 2, 3, 4])
        if curr_x + bar_w > x + w - 4:
            break
        draw.rectangle([curr_x, y, curr_x + bar_w, y + h], fill=(240, 245, 255, 240))
        space_w = random.choice([2, 3, 4])
        curr_x += bar_w + space_w

def generate_id_card_front(portrait, out_path):
    W, H = 600, 950
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    card_bounds = (15, 15, W - 16, H - 16)
    corner_r = 26

    # 1. Drop shadow behind the physical card
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([18, 20, W - 13, H - 11], radius=corner_r, fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    card.paste(shadow, (0, 0), shadow)

    # 2. Solid dark titanium / obsidian card base
    draw.rounded_rectangle(card_bounds, radius=corner_r, fill=(10, 18, 32, 255), outline=(0, 245, 255, 180), width=2)
    draw.rounded_rectangle([17, 17, W - 18, H - 18], radius=corner_r - 2, outline=(60, 120, 180, 70), width=1)

    # Subtle tech dot matrix
    for gx in range(28, W - 28, 20):
        for gy in range(80, H - 80, 20):
            draw.point((gx, gy), fill=(0, 245, 255, 22))

    # Fonts
    font_title = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 25)
    font_bold = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 12)
    font_sub = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 12)
    font_univ = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 14)
    font_dept = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 11)
    font_small = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 10)
    font_hologram = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 9)

    # 3. Lanyard Slot at top
    draw_lanyard_punch(draw, W // 2, 42, w=120, h=26)

    # 4. University / Organization Header Bar
    head_y = 76
    draw.rounded_rectangle([35, head_y, W - 35, head_y + 60], radius=8, fill=(5, 24, 45, 240), outline=(0, 245, 255, 140), width=1)
    draw.text((W // 2 - 180, head_y + 8), "TEERTHANKER MAHAVEER UNIVERSITY", fill=(0, 245, 255, 255), font=font_univ)
    draw.text((W // 2 - 170, head_y + 28), "FACULTY OF ENGINEERING & COMPUTING SCIENCES", fill=(56, 217, 245, 220), font=font_dept)
    draw.text((W // 2 - 130, head_y + 44), "DEPARTMENT OF COMPUTER SCIENCE & ENG.", fill=(180, 225, 255, 200), font=font_small)

    # 5. Chip & RFID Section
    draw_emv_chip(draw, 50, 155, w=82, h=64)
    draw_rfid_wave(draw, 155, 187, color=(0, 245, 255, 230))
    draw.text((180, 180), "RFID // SECURE CHIP", fill=(0, 245, 255, 180), font=font_small)

    # Holographic stamp top right
    draw_hologram_seal(draw, W - 85, 187, r=36)

    # 6. Official Photo with Frame & Tick Marks
    pw, ph = 240, 260
    px, py = W // 2 - pw // 2, 238
    resized_p = portrait.resize((pw, ph), Image.Resampling.LANCZOS)
    
    draw.rounded_rectangle([px - 4, py - 4, px + pw + 4, py + ph + 4], radius=10, fill=(3, 15, 30, 255), outline=(0, 245, 255, 220), width=2)
    card.paste(resized_p, (px, py))

    # Corner photo tick brackets
    b_len = 16
    draw.line([(px, py), (px + b_len, py)], fill=(57, 255, 20, 255), width=2)
    draw.line([(px, py), (px, py + b_len)], fill=(57, 255, 20, 255), width=2)
    draw.line([(px + pw, py), (px + pw - b_len, py)], fill=(57, 255, 20, 255), width=2)
    draw.line([(px + pw, py), (px + pw, py + b_len)], fill=(57, 255, 20, 255), width=2)

    # 7. Identity Details
    name_y = 516
    draw.text((W // 2 - 110, name_y), "ADITYA KUMAR", fill=(0, 245, 255, 255), font=font_title)
    draw.text((W // 2 - 165, name_y + 34), "FULL-STACK DEVELOPER & AI SYSTEMS ARCHITECT", fill=(56, 217, 245, 230), font=font_sub)

    # Metadata Grid Box
    grid_y = 585
    draw.rounded_rectangle([40, grid_y, W - 40, grid_y + 170], radius=10, fill=(4, 18, 35, 230), outline=(0, 245, 255, 90), width=1)

    fields = [
        ("ENROLLMENT NO :", "052974 // TMU CSE (IBM)"),
        ("STATUS / ROLE :", "SYSTEM OPERATOR [VERIFIED]"),
        ("CLEARANCE     :", "LEVEL 5 // ROOT ACCESS"),
        ("COGNITIVE STACK:", "REACT • DJANGO • KOTLIN • GEMINI AI"),
        ("SECURITY SPEC :", "AES-256 • PBKDF2 • SHA-256 • MONGODB"),
        ("VALIDITY      :", "2023 - 2027 // CONTINUOUS"),
    ]

    fy = grid_y + 12
    for label, val in fields:
        draw.text((55, fy), label, fill=(57, 255, 20, 230), font=font_bold)
        val_color = (255, 215, 0, 245) if "LEVEL 5" in val else (225, 245, 255, 235)
        draw.text((205, fy), val, fill=val_color, font=font_bold)
        fy += 25

    # 8. Holographic Foil Security Strip
    holo_y = 770
    for hx in range(40, W - 40):
        h_ratio = (hx - 40) / (W - 80)
        hr = int(127 + 127 * math.sin(h_ratio * math.pi * 3))
        hg = int(127 + 127 * math.sin(h_ratio * math.pi * 3 + 2))
        hb = int(127 + 127 * math.sin(h_ratio * math.pi * 3 + 4))
        draw.line([(hx, holo_y), (hx, holo_y + 22)], fill=(hr, hg, hb, 210))
    draw.text((55, holo_y + 5), "◈ TMU SECURE SMART CARD  •  OFFICIAL CREDENTIAL  •  AUTHORIZED ACCESS ONLY ◈", fill=(10, 15, 25, 240), font=font_hologram)

    # 9. Barcode at bottom
    draw_barcode(draw, 50, 806, W - 100, 48, code_str="TMU-052974-2023-ADITYA")
    draw.text((W // 2 - 130, 864), "* TMU-CSE-2023-052974-ROOT *", fill=(0, 245, 255, 200), font=font_dept)

    # Bottom notice
    draw.text((W // 2 - 145, 904), "PROPERTY OF TMU // IF FOUND RETURN IMMEDIATELY", fill=(150, 180, 210, 160), font=font_small)

    card.save(out_path, format="PNG")
    print(f"[OK] Generated: {out_path}")

def generate_id_card_back(sign_path, qr_data, out_path):
    W, H = 600, 950
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    card_bounds = (15, 15, W - 16, H - 16)
    corner_r = 26

    # Drop shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([18, 20, W - 13, H - 11], radius=corner_r, fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    card.paste(shadow, (0, 0), shadow)

    # Solid dark titanium card base matching front
    draw.rounded_rectangle(card_bounds, radius=corner_r, fill=(10, 18, 32, 255), outline=(0, 245, 255, 180), width=2)
    draw.rounded_rectangle([17, 17, W - 18, H - 18], radius=corner_r - 2, outline=(60, 120, 180, 70), width=1)

    # Fonts
    font_bold = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 12)
    font_title = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 15)
    font_sub = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 11)
    font_small = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 10)
    font_tiny = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 9)

    # 1. Lanyard Slot at top
    draw_lanyard_punch(draw, W // 2, 42, w=120, h=26)

    # 2. Magnetic Stripe
    mag_y = 78
    draw.rectangle([15, mag_y, W - 15, mag_y + 85], fill=(15, 17, 22, 255))
    draw.line([(15, mag_y + 2), (W - 15, mag_y + 2)], fill=(45, 50, 60, 255), width=2)
    draw.line([(15, mag_y + 83), (W - 15, mag_y + 83)], fill=(5, 7, 10, 255), width=2)
    draw.text((35, mag_y + 34), "MAGNETIC STRIPE  •  ENCODED TRACKS 1, 2, 3  •  DO NOT EXPOSE TO MAGNETIC FIELD", fill=(100, 115, 135, 180), font=font_tiny)

    # 3. Authorized Signature Panel
    sig_y = 182
    draw.rounded_rectangle([35, sig_y, W - 35, sig_y + 75], radius=6, fill=(245, 247, 250, 255), outline=(180, 190, 205, 255), width=1)
    
    for lx in range(40, W - 40, 12):
        draw.line([(lx, sig_y + 5), (lx + 20, sig_y + 70)], fill=(225, 230, 240, 255), width=1)

    if sign_path and os.path.exists(sign_path):
        try:
            sign_img = Image.open(sign_path).convert("RGBA")
            sw, sh = 200, 65
            sign_resized = sign_img.resize((sw, sh), Image.Resampling.LANCZOS)
            card.paste(sign_resized, (W // 2 - sw // 2, sig_y + 5), sign_resized)
        except Exception:
            draw.text((W // 2 - 60, sig_y + 25), "Aditya Kumar", fill=(20, 30, 60, 255), font=font_title)
    else:
        draw.text((W // 2 - 60, sig_y + 25), "Aditya Kumar", fill=(20, 30, 60, 255), font=font_title)

    draw.text((38, sig_y + 78), "AUTHORIZED OPERATOR SIGNATURE // NOT VALID UNLESS SIGNED", fill=(0, 245, 255, 180), font=font_tiny)

    # 4. Production Systems & Authorizations Box
    proj_y = 280
    draw.rounded_rectangle([35, proj_y, W - 35, proj_y + 185], radius=10, fill=(4, 18, 35, 230), outline=(0, 245, 255, 90), width=1)
    draw.text((50, proj_y + 10), "◈ PRODUCTION DEPLOYMENTS & SYSTEM CLEARANCE ◈", fill=(57, 255, 20, 255), font=font_title)
    draw.line([(50, proj_y + 32), (W - 50, proj_y + 32)], fill=(0, 245, 255, 50), width=1)

    projs = [
        ("SKILLNEST", "AI Student Marketplace · Gemini AI Verification · WebSockets"),
        ("VINDYWASHINI", "Modern Desktop Billing · Electron · React · GST Invoicing"),
        ("FILE VAULT", "Encrypted Desktop Storage · AES-256 (Fernet) · PBKDF2"),
        ("INVOICE PRO", "Production Billing Engine · Dynamic UPI QR · Live PDF"),
        ("VANASPATI", "Native Android App · Kotlin · Botanical Care · Bilingual"),
    ]

    py = proj_y + 42
    for title, desc in projs:
        draw.text((50, py), f"[✓] {title}", fill=(0, 245, 255, 240), font=font_bold)
        draw.text((165, py), f":: {desc}", fill=(215, 235, 255, 220), font=font_sub)
        py += 26

    # 5. Direct Uplink & Emergency Contacts Box
    con_y = 480
    draw.rounded_rectangle([35, con_y, W - 35, con_y + 175], radius=10, fill=(4, 18, 35, 230), outline=(0, 245, 255, 90), width=1)
    draw.text((50, con_y + 10), "◈ DIRECT UPLINK & SECURE COMMUNICATIONS ◈", fill=(57, 255, 20, 255), font=font_title)
    draw.line([(50, con_y + 32), (W - 50, con_y + 32)], fill=(0, 245, 255, 50), width=1)

    contacts = [
        ("PRIMARY EMAIL :", "hpaditya87857.contact@gmail.com"),
        ("ACADEMIC EMAIL:", "aditya.052974@tmu.ac.in"),
        ("PHONE / WA   :", "+91 7505762707"),
        ("GITHUB PROFILE:", "https://github.com/Aditya-tmu"),
        ("LINKEDIN     :", "linkedin.com/in/aditya-kumar-835068277"),
    ]

    cy = con_y + 42
    for c_title, c_val in contacts:
        draw.text((50, cy), c_title, fill=(0, 245, 255, 230), font=font_bold)
        draw.text((170, cy), c_val, fill=(225, 245, 255, 230), font=font_sub)
        cy += 24

    # 6. QR Code Box (Bottom Section)
    qr_y = 672
    qr_size = 145
    qr_x = W // 2 - qr_size // 2

    if HAS_QR:
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#020a14", back_color="#ffffff").convert("RGBA")
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)
        draw.rounded_rectangle([qr_x - 4, qr_y - 4, qr_x + qr_size + 4, qr_y + qr_size + 4], radius=6, fill=(255, 255, 255, 255))
        card.paste(qr_img, (qr_x, qr_y))
    else:
        draw.rounded_rectangle([qr_x, qr_y, qr_x + qr_size, qr_y + qr_size], radius=6, fill=(255, 255, 255, 255))
        draw.text((qr_x + 30, qr_y + 60), "QR CODE", fill=(0, 0, 0, 255), font=font_bold)

    draw.text((W // 2 - 120, qr_y + qr_size + 10), "SCAN TO VISIT GITHUB & REPOSITORIES", fill=(0, 245, 255, 210), font=font_sub)

    # 7. Cardholder Disclaimer
    draw.text((W // 2 - 180, 860), "TERMS: Official smart credential issued by TMU FOECS.", fill=(160, 185, 215, 170), font=font_small)
    draw.text((W // 2 - 215, 878), "Unauthorized reproduction or tampering is strictly prohibited under IT Act.", fill=(160, 185, 215, 170), font=font_small)
    draw.text((W // 2 - 145, 908), "SERIAL NO: TMU-2023-CSE-052974-V4", fill=(0, 245, 255, 170), font=font_small)

    card.save(out_path, format="PNG")
    print(f"[OK] Generated: {out_path}")

def generate_3d_flip_gif(front_path, back_path, out_path, num_frames=36):
    front = Image.open(front_path).convert("RGBA")
    back = Image.open(back_path).convert("RGBA")
    
    target_w, target_h = 360, 570
    front_s = front.resize((target_w, target_h), Image.Resampling.LANCZOS)
    back_s = back.resize((target_w, target_h), Image.Resampling.LANCZOS)

    canvas_w, canvas_h = 440, 600
    frames = []

    for i in range(num_frames):
        angle_deg = (i / float(num_frames)) * 360.0
        rad = math.radians(angle_deg)
        cos_val = math.cos(rad)

        frame = Image.new("RGBA", (canvas_w, canvas_h), (2, 10, 20, 0))
        
        is_front = (cos_val >= 0)
        source_card = front_s if is_front else back_s

        proj_w = max(4, int(target_w * abs(cos_val)))
        rotated_side = source_card.resize((proj_w, target_h), Image.Resampling.BILINEAR)

        # Dynamic perspective edge shadow
        paste_x = (canvas_w - proj_w) // 2
        paste_y = (canvas_h - target_h) // 2

        edge_thickness = int(6 * (1.0 - abs(cos_val)))
        if edge_thickness > 0:
            edge_x = paste_x + (proj_w if cos_val >= 0 else 0)
            f_draw = ImageDraw.Draw(frame)
            f_draw.rectangle([edge_x - 1, paste_y + 10, edge_x + edge_thickness, paste_y + target_h - 10], fill=(0, 200, 220, 200))

        frame.paste(rotated_side, (paste_x, paste_y), rotated_side)
        frames.append(frame)

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=65,
        loop=0,
        disposal=2
    )
    print(f"[OK] Generated 3D Flip GIF: {out_path}")

def generate_achievements_svg(out_path):
    """Generates a high-contrast, glowing, self-contained SVG for achievement nodes with 100% native SVG text."""
    achievements = [
        {
            "icon": "🏆",
            "title": "FULL-STACK MAESTRO",
            "tier": "TIER S // DIAMOND",
            "desc1": "Architected & shipped 4+ production systems",
            "desc2": "across React, Django, Node & Electron",
            "color": "#00f5ff",
            "stat": "4+ APPS DEPLOYED"
        },
        {
            "icon": "🤖",
            "title": "AI SYSTEMS PIONEER",
            "tier": "TIER S // DIAMOND",
            "desc1": "Integrated Google Gemini AI verification",
            "desc2": "and mobile on-device TFLite ML models",
            "color": "#39ff14",
            "stat": "GEMINI + TFLITE"
        },
        {
            "icon": "🛡️",
            "title": "CRYPTO GUARDIAN",
            "tier": "TIER A // GOLD",
            "desc1": "Built military-grade encrypted storage vault",
            "desc2": "with AES-256 Fernet, PBKDF2 & SHA-256",
            "color": "#ff007f",
            "stat": "AES-256 • PBKDF2"
        },
        {
            "icon": "📱",
            "title": "NATIVE ARCHITECT",
            "tier": "TIER A // GOLD",
            "desc1": "Shipped bilingual Android Kotlin application",
            "desc2": "with real-time camera photo identification",
            "color": "#ffd700",
            "stat": "KOTLIN ANDROID"
        },
        {
            "icon": "⚡",
            "title": "REALTIME SPECIALIST",
            "tier": "TIER A // GOLD",
            "desc1": "Engineered zero-latency WebSocket channels",
            "desc2": "with Django Channels, Redis & pub/sub",
            "color": "#00f5ff",
            "stat": "WEBSOCKETS CHANNELS"
        },
        {
            "icon": "🧾",
            "title": "FINTECH BUILDER",
            "tier": "TIER A // GOLD",
            "desc1": "Automated GST compliance, GSTR-1/3B filing",
            "desc2": "and dynamic UPI payment settlement",
            "color": "#39ff14",
            "stat": "GST & DYNAMIC UPI"
        }
    ]

    W = 900
    H = 350
    card_w = 270
    card_h = 138
    cols = 3
    spacing_x = 24
    spacing_y = 18
    start_x = 24
    start_y = 52

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto">',
        '  <defs>',
        '    <linearGradient id="bgG" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#020a14" />',
        '      <stop offset="100%" stop-color="#051828" />',
        '    </linearGradient>',
        '  </defs>',
        f'  <rect width="{W}" height="{H}" rx="14" fill="url(#bgG)" stroke="#00f5ff" stroke-opacity="0.35" stroke-width="1.5" />',
        '  <!-- Header -->',
        '  <text x="28" y="32" fill="#39ff14" font-family="Consolas, Fira Code, monospace" font-size="13" font-weight="bold">◈ OPERATOR ACHIEVEMENT NODES // VERIFIED MILESTONES</text>',
        f'  <text x="{W - 28}" y="32" text-anchor="end" fill="#00f5ff" font-family="Consolas, Fira Code, monospace" font-size="12">ENGINEERING TIERS: DIAMOND &amp; GOLD</text>',
        f'  <line x1="24" y1="40" x2="{W - 24}" y2="40" stroke="#00f5ff" stroke-opacity="0.25" stroke-width="1" />'
    ]

    for idx, ach in enumerate(achievements):
        r = idx // cols
        c = idx % cols
        x = start_x + c * (card_w + spacing_x)
        y = start_y + r * (card_h + spacing_y)
        col = ach["color"]

        svg.append(f'  <!-- Card {idx + 1} -->')
        svg.append(f'  <g transform="translate({x}, {y})">')
        svg.append(f'    <rect width="{card_w}" height="{card_h}" rx="10" fill="#041220" stroke="{col}" stroke-opacity="0.45" stroke-width="1.2" />')
        svg.append(f'    <rect x="1" y="1" width="{card_w - 2}" height="3" fill="{col}" opacity="0.85" rx="2" />')
        # Icon
        svg.append(f'    <text x="14" y="32" font-size="20">{ach["icon"]}</text>')
        # Title
        svg.append(f'    <text x="44" y="24" fill="{col}" font-family="Consolas, Fira Code, monospace" font-size="11.5" font-weight="bold">{ach["title"]}</text>')
        # Tier
        svg.append(f'    <text x="44" y="38" fill="#ffffff" opacity="0.65" font-family="Consolas, Fira Code, monospace" font-size="9">{ach["tier"]}</text>')
        # Desc lines
        svg.append(f'    <text x="14" y="62" fill="#cceeff" font-family="Consolas, Fira Code, monospace" font-size="10">{ach["desc1"]}</text>')
        svg.append(f'    <text x="14" y="78" fill="#cceeff" font-family="Consolas, Fira Code, monospace" font-size="10">{ach["desc2"]}</text>')
        # Stat badge
        svg.append(f'    <rect x="14" y="98" width="{card_w - 28}" height="22" rx="4" fill="#020a14" stroke="{col}" stroke-opacity="0.35" />')
        svg.append(f'    <text x="{card_w // 2}" y="113" text-anchor="middle" fill="{col}" font-family="Consolas, Fira Code, monospace" font-size="9.5" font-weight="bold">{ach["stat"]}</text>')
        svg.append('  </g>')

    svg.append('</svg>')

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Generated: {out_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    assets_dir = os.path.join(repo_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    portrait_path = os.path.join(assets_dir, "Aditya.jpeg")
    if not os.path.exists(portrait_path):
        portrait_path = r"C:\Users\adity\Desktop\Aditya.jpeg"

    sign_path = os.path.join(assets_dir, "Aditya_Sign.png")
    if not os.path.exists(sign_path):
        sign_path = r"C:\Users\adity\Desktop\Aditya_Sign.png"

    print(f"[*] Processing portrait: {portrait_path}")
    portrait = crop_smart_portrait(portrait_path)

    front_path = os.path.join(assets_dir, "aditya_id_card_front.png")
    print("[*] Generating Realistic ID Badge (Front)...")
    generate_id_card_front(portrait, front_path)

    back_path = os.path.join(assets_dir, "aditya_id_card_back.png")
    print("[*] Generating Realistic ID Badge (Back with Signature & Contacts)...")
    generate_id_card_back(sign_path, "https://github.com/Aditya-tmu", back_path)

    gif_path = os.path.join(assets_dir, "aditya_id_card_3d_flip.gif")
    print("[*] Generating Smooth 3D Spinning Animation (GIF)...")
    generate_3d_flip_gif(front_path, back_path, gif_path, num_frames=36)

    ach_path = os.path.join(assets_dir, "aditya_achievements.svg")
    print("[*] Generating High-Contrast Achievement Nodes SVG...")
    generate_achievements_svg(ach_path)

    print("\n[SUCCESS] All realistic ID card and achievement assets generated successfully!")

if __name__ == "__main__":
    main()
