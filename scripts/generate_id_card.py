#!/usr/bin/env python3
"""
Aditya Kumar — High-Contrast Smart ID Badge, Flip Animation & Achievement Nodes
---------------------------------------------------------------------------------
Features:
- Exact mathematical horizontal centering for all university, name, and credential text.
- Large, high-contrast, crystal-clear typography readable without zoom.
- 100% valid XML compliance for SVG achievement nodes.
- High-visibility color scheme (Deep Obsidian #06101e, Neon Cyan #00f5ff, Matrix Green #39ff14, Gold #ffd700, Pure White #ffffff).
- Smooth 3D flip-and-pause animation GIF (aditya_id_card_flip_pause.gif).
"""

import os
import sys
import math
import random
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

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

def center_text(draw, y, text, font, fill, width=640):
    """Draws text centered horizontally on the canvas with sub-pixel precision."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, fill=fill, font=font)
    return x, tw

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
    
    cropped = ImageEnhance.Sharpness(cropped).enhance(1.25)
    cropped = ImageEnhance.Contrast(cropped).enhance(1.10)
    return cropped

def draw_lanyard_punch(draw, cx, cy, w=130, h=28):
    x0, y0, x1, y1 = cx - w//2, cy - h//2, cx + w//2, cy + h//2
    draw.rounded_rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], radius=14, outline=(80, 105, 135, 255), width=2)
    draw.rounded_rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + 1], radius=13, outline=(190, 220, 255, 240), width=1)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=(3, 7, 14, 255))
    draw.line([(x0 + 10, y0 + 3), (x1 - 10, y0 + 3)], fill=(1, 3, 6, 255), width=2)

def draw_emv_chip(draw, x, y, w=88, h=68):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(225, 185, 55, 255), outline=(160, 125, 20, 255), width=2)
    draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + h - 3], radius=6, outline=(255, 230, 120, 255), width=1)
    mid_y = y + h // 2
    draw.line([(x + 6, mid_y), (x + w - 6, mid_y)], fill=(120, 90, 15, 255), width=2)
    draw.line([(x + w // 3, y + 6), (x + w // 3, mid_y)], fill=(120, 90, 15, 255), width=2)
    draw.line([(x + 2 * w // 3, y + 6), (x + 2 * w // 3, mid_y)], fill=(120, 90, 15, 255), width=2)
    draw.line([(x + w // 3, mid_y), (x + w // 3, y + h - 6)], fill=(120, 90, 15, 255), width=2)
    draw.line([(x + 2 * w // 3, mid_y), (x + 2 * w // 3, y + h - 6)], fill=(120, 90, 15, 255), width=2)
    cw, ch = 30, 22
    draw.ellipse([x + w//2 - cw//2, y + h//2 - ch//2, x + w//2 + cw//2, y + h//2 + ch//2], outline=(120, 90, 15, 255), fill=(245, 210, 85, 255), width=1)

def draw_rfid_wave(draw, x, y, color=(0, 245, 255, 240)):
    for r in [9, 16, 23]:
        draw.arc([x - r, y - r, x + r, y + r], start=-45, end=45, fill=color, width=2)

def draw_hologram_seal(draw, x, y, r=40):
    colors = [
        (255, 100, 150, 210),
        (255, 210, 50, 210),
        (50, 255, 150, 210),
        (0, 245, 255, 230),
        (160, 110, 255, 210)
    ]
    for i, col in enumerate(colors):
        cr = r - i * 6
        if cr > 4:
            draw.ellipse([x - cr, y - cr, x + cr, y + cr], outline=col, width=2)
    
    star_pts = []
    for step in range(10):
        sr = 12 if step % 2 == 0 else 5
        ang = step * (math.pi / 5) - math.pi / 2
        star_pts.append((x + int(sr * math.cos(ang)), y + int(sr * math.sin(ang))))
    draw.polygon(star_pts, fill=(255, 255, 255, 250))

def draw_barcode(draw, x, y, w, h, code_str="TMU-052974-2023"):
    random.seed(42)
    curr_x = x
    while curr_x < x + w - 4:
        bar_w = random.choice([2, 3, 4, 5])
        if curr_x + bar_w > x + w - 4:
            break
        draw.rectangle([curr_x, y, curr_x + bar_w, y + h], fill=(255, 255, 255, 255))
        space_w = random.choice([2, 3, 4])
        curr_x += bar_w + space_w

def generate_id_card_front(portrait, out_path):
    W, H = 640, 980
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    card_bounds = (16, 16, W - 17, H - 17)
    corner_r = 28

    # 1. 3D Drop shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([20, 22, W - 14, H - 12], radius=corner_r, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    card.paste(shadow, (0, 0), shadow)

    # 2. Rich Deep Obsidian Base with Cyan Border
    draw.rounded_rectangle(card_bounds, radius=corner_r, fill=(8, 18, 34, 255), outline=(0, 245, 255, 220), width=3)
    draw.rounded_rectangle([19, 19, W - 20, H - 20], radius=corner_r - 2, outline=(50, 110, 175, 90), width=1)

    # Fonts (Scaled larger for immediate high-contrast legibility)
    font_univ = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 20)
    font_dept = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 14)
    font_name = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 32)
    font_role = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 15)
    font_bold = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 15)
    font_small = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 13)
    font_micro = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 11)

    # 3. Lanyard Punch Slot
    draw_lanyard_punch(draw, W // 2, 44, w=130, h=28)

    # 4. University Header Box (Mathematical exact center alignment)
    head_y = 80
    draw.rounded_rectangle([30, head_y, W - 30, head_y + 80], radius=12, fill=(4, 24, 48, 255), outline=(0, 245, 255, 200), width=2)
    center_text(draw, head_y + 10, "TEERTHANKER MAHAVEER UNIVERSITY", font_univ, (0, 245, 255, 255), width=W)
    center_text(draw, head_y + 35, "FACULTY OF ENGINEERING & COMPUTING SCIENCES", font_dept, (255, 255, 255, 255), width=W)
    center_text(draw, head_y + 55, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", font_small, (200, 235, 255, 240), width=W)

    # 5. Smartcard Chip & RFID
    draw_emv_chip(draw, 48, 176, w=88, h=68)
    draw_rfid_wave(draw, 160, 210, color=(0, 245, 255, 250))
    draw.text((188, 202), "RFID // SECURE CHIP", fill=(0, 245, 255, 240), font=font_small)

    # Holographic Seal Top Right
    draw_hologram_seal(draw, W - 80, 210, r=40)

    # 6. Framed Portrait Photo (Exact Center)
    pw, ph = 240, 260
    px = (W - pw) // 2
    py = 258
    resized_p = portrait.resize((pw, ph), Image.Resampling.LANCZOS)
    
    draw.rounded_rectangle([px - 4, py - 4, px + pw + 4, py + ph + 4], radius=10, fill=(3, 14, 28, 255), outline=(0, 245, 255, 255), width=3)
    card.paste(resized_p, (px, py))

    # Corner brackets on photo
    b_len = 18
    draw.line([(px, py), (px + b_len, py)], fill=(57, 255, 20, 255), width=3)
    draw.line([(px, py), (px, py + b_len)], fill=(57, 255, 20, 255), width=3)
    draw.line([(px + pw, py), (px + pw - b_len, py)], fill=(57, 255, 20, 255), width=3)
    draw.line([(px + pw, py), (px + pw, py + b_len)], fill=(57, 255, 20, 255), width=3)

    # 7. Identity & Role (Exact Center Alignment)
    name_y = 538
    center_text(draw, name_y, "ADITYA KUMAR", font_name, (255, 255, 255, 255), width=W)
    center_text(draw, name_y + 40, "FULL-STACK DEVELOPER & AI SYSTEMS ARCHITECT", font_role, (0, 245, 255, 255), width=W)

    # 8. High-Contrast Metadata Grid Box
    grid_y = 612
    draw.rounded_rectangle([32, grid_y, W - 32, grid_y + 190], radius=12, fill=(4, 18, 36, 255), outline=(0, 245, 255, 150), width=2)

    fields = [
        ("ENROLLMENT NO :", "052974 // TMU CSE (IBM)"),
        ("STATUS / ROLE :", "SYSTEM OPERATOR [VERIFIED]"),
        ("CLEARANCE     :", "LEVEL 5 // ROOT ACCESS"),
        ("CORE STACK    :", "REACT • DJANGO • KOTLIN • GEMINI AI"),
        ("SECURITY SPEC :", "AES-256 • PBKDF2 • SHA-256 • MONGODB"),
        ("VALIDITY      :", "2023 - 2027 // CONTINUOUS"),
    ]

    fy = grid_y + 15
    for label, val in fields:
        draw.text((50, fy), label, fill=(57, 255, 20, 255), font=font_bold)
        val_color = (255, 215, 0, 255) if "LEVEL 5" in val else (255, 255, 255, 255)
        draw.text((224, fy), val, fill=val_color, font=font_bold)
        fy += 28

    # 9. Holographic Rainbow Security Foil
    holo_y = 812
    for hx in range(32, W - 32):
        h_ratio = (hx - 32) / (W - 64)
        hr = int(127 + 127 * math.sin(h_ratio * math.pi * 3))
        hg = int(127 + 127 * math.sin(h_ratio * math.pi * 3 + 2))
        hb = int(127 + 127 * math.sin(h_ratio * math.pi * 3 + 4))
        draw.line([(hx, holo_y), (hx, holo_y + 22)], fill=(hr, hg, hb, 220))
    center_text(draw, holo_y + 4, "◈ TMU OFFICIAL SMART CARD  •  SECURE CREDENTIAL  •  AUTHORIZED ACCESS ONLY ◈", font_micro, (10, 15, 25, 255), width=W)

    # 10. High-Density Barcode (Exact Center)
    bw = W - 100
    bx = (W - bw) // 2
    draw_barcode(draw, bx, 846, bw, 48, code_str="TMU-052974-2023-ADITYA")
    center_text(draw, 904, "* TMU-CSE-2023-052974-ROOT *", font_small, (0, 245, 255, 240), width=W)
    center_text(draw, 936, "PROPERTY OF TMU // IF FOUND RETURN IMMEDIATELY", font_micro, (190, 220, 255, 220), width=W)

    card.save(out_path, format="PNG")
    print(f"[OK] Generated: {out_path}")

def generate_id_card_back(sign_path, qr_data, out_path):
    W, H = 640, 980
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    card_bounds = (16, 16, W - 17, H - 17)
    corner_r = 28

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([20, 22, W - 14, H - 12], radius=corner_r, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    card.paste(shadow, (0, 0), shadow)

    draw.rounded_rectangle(card_bounds, radius=corner_r, fill=(8, 18, 34, 255), outline=(0, 245, 255, 220), width=3)
    draw.rounded_rectangle([19, 19, W - 20, H - 20], radius=corner_r - 2, outline=(50, 110, 175, 90), width=1)

    font_title = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 16)
    font_bold = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 14)
    font_sub = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 13)
    font_small = find_font(["CascadiaMono.ttf", "consola.ttf", "segoeui.ttf", "arial.ttf"], 12)
    font_micro = find_font(["CascadiaCode.ttf", "consolab.ttf", "segoeuib.ttf", "arialbd.ttf"], 11)

    # 1. Lanyard Slot
    draw_lanyard_punch(draw, W // 2, 44, w=130, h=28)

    # 2. Magnetic Stripe
    mag_y = 84
    draw.rectangle([16, mag_y, W - 16, mag_y + 88], fill=(16, 18, 24, 255))
    draw.line([(16, mag_y + 2), (W - 16, mag_y + 2)], fill=(50, 55, 65, 255), width=2)
    draw.line([(16, mag_y + 86), (W - 16, mag_y + 86)], fill=(5, 8, 12, 255), width=2)
    center_text(draw, mag_y + 36, "MAGNETIC STRIPE  •  ENCODED TRACKS 1, 2, 3  •  DO NOT EXPOSE TO MAGNETS", font_micro, (140, 165, 195, 220), width=W)

    # 3. Signature Panel
    sig_y = 192
    draw.rounded_rectangle([32, sig_y, W - 32, sig_y + 76], radius=6, fill=(245, 247, 252, 255), outline=(190, 200, 220, 255), width=2)
    
    for lx in range(40, W - 40, 14):
        draw.line([(lx, sig_y + 5), (lx + 20, sig_y + 71)], fill=(225, 230, 242, 255), width=1)

    if sign_path and os.path.exists(sign_path):
        try:
            sign_img = Image.open(sign_path).convert("RGBA")
            sw, sh = 220, 68
            sign_resized = sign_img.resize((sw, sh), Image.Resampling.LANCZOS)
            card.paste(sign_resized, ((W - sw) // 2, sig_y + 4), sign_resized)
        except Exception:
            center_text(draw, sig_y + 24, "Aditya Kumar", font_title, (20, 30, 60, 255), width=W)
    else:
        center_text(draw, sig_y + 24, "Aditya Kumar", font_title, (20, 30, 60, 255), width=W)

    center_text(draw, sig_y + 82, "AUTHORIZED OPERATOR SIGNATURE // NOT VALID UNLESS SIGNED", font_micro, (0, 245, 255, 240), width=W)

    # 4. Production Clearances Box
    proj_y = 290
    draw.rounded_rectangle([32, proj_y, W - 32, proj_y + 195], radius=12, fill=(4, 18, 36, 255), outline=(0, 245, 255, 150), width=2)
    center_text(draw, proj_y + 10, "◈ PRODUCTION DEPLOYMENTS & SYSTEM CLEARANCE ◈", font_title, (57, 255, 20, 255), width=W)
    draw.line([(50, proj_y + 34), (W - 50, proj_y + 34)], fill=(0, 245, 255, 80), width=1)

    projs = [
        ("SKILLNEST", "AI Student Marketplace · Gemini AI Verification · WebSockets"),
        ("VINDYWASHINI", "Modern Desktop Billing · Electron · React · GST Invoicing"),
        ("FILE VAULT", "Encrypted Desktop Storage · AES-256 (Fernet) · PBKDF2"),
        ("INVOICE PRO", "Production Billing Engine · Dynamic UPI QR · Live PDF"),
        ("VANASPATI", "Native Android App · Kotlin · Botanical Care · Bilingual"),
    ]

    py = proj_y + 45
    for title, desc in projs:
        draw.text((48, py), f"[✓] {title}", fill=(0, 245, 255, 255), font=font_bold)
        draw.text((180, py), f":: {desc}", fill=(255, 255, 255, 250), font=font_sub)
        py += 28

    # 5. Direct Uplink Contacts Box
    con_y = 502
    draw.rounded_rectangle([32, con_y, W - 32, con_y + 185], radius=12, fill=(4, 18, 36, 255), outline=(0, 245, 255, 150), width=2)
    center_text(draw, con_y + 10, "◈ DIRECT UPLINK & SECURE COMMUNICATIONS ◈", font_title, (57, 255, 20, 255), width=W)
    draw.line([(50, con_y + 34), (W - 50, con_y + 34)], fill=(0, 245, 255, 80), width=1)

    contacts = [
        ("PRIMARY EMAIL :", "hpaditya87857.contact@gmail.com"),
        ("ACADEMIC EMAIL:", "aditya.052974@tmu.ac.in"),
        ("PHONE / WA   :", "+91 7505762707"),
        ("GITHUB PROFILE:", "https://github.com/Aditya-tmu"),
        ("LINKEDIN     :", "linkedin.com/in/aditya-kumar-835068277"),
    ]

    cy = con_y + 45
    for c_title, c_val in contacts:
        draw.text((48, cy), c_title, fill=(0, 245, 255, 255), font=font_bold)
        draw.text((188, cy), c_val, fill=(255, 255, 255, 255), font=font_sub)
        cy += 26

    # 6. Scannable QR Code Box (Exact Center)
    qr_y = 705
    qr_size = 145
    qr_x = (W - qr_size) // 2

    if HAS_QR:
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#020a14", back_color="#ffffff").convert("RGBA")
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)
        draw.rounded_rectangle([qr_x - 4, qr_y - 4, qr_x + qr_size + 4, qr_y + qr_size + 4], radius=6, fill=(255, 255, 255, 255))
        card.paste(qr_img, (qr_x, qr_y))

    center_text(draw, qr_y + qr_size + 10, "SCAN TO VISIT GITHUB & REPOSITORIES", font_bold, (0, 245, 255, 255), width=W)
    center_text(draw, 895, "TERMS: Official smart credential issued by TMU FOECS.", font_small, (200, 230, 255, 220), width=W)
    center_text(draw, 915, "Unauthorized reproduction is strictly prohibited under IT Act.", font_small, (200, 230, 255, 220), width=W)
    center_text(draw, 940, "SERIAL NO: TMU-2023-CSE-052974-V6", font_micro, (0, 245, 255, 240), width=W)

    card.save(out_path, format="PNG")
    print(f"[OK] Generated: {out_path}")

def generate_flip_pause_gif(front_path, back_path, out_path):
    """Generates a smooth 3D flip-and-pause animation GIF (holds front and back so user can read)."""
    front = Image.open(front_path).convert("RGBA")
    back = Image.open(back_path).convert("RGBA")
    
    target_w, target_h = 380, 580
    front_s = front.resize((target_w, target_h), Image.Resampling.LANCZOS)
    back_s = back.resize((target_w, target_h), Image.Resampling.LANCZOS)

    canvas_w, canvas_h = 440, 610

    # Frames sequence:
    # 1. Front hold (e.g., 20 frames * 150ms = 3.0s)
    # 2. Flip from Front to Back (12 frames transition)
    # 3. Back hold (20 frames * 150ms = 3.0s)
    # 4. Flip from Back to Front (12 frames transition)
    
    frames = []
    durations = []

    # Front static frame
    f_canvas = Image.new("RGBA", (canvas_w, canvas_h), (2, 10, 20, 0))
    f_canvas.paste(front_s, ((canvas_w - target_w) // 2, (canvas_h - target_h) // 2))

    # Back static frame
    b_canvas = Image.new("RGBA", (canvas_w, canvas_h), (2, 10, 20, 0))
    b_canvas.paste(back_s, ((canvas_w - target_w) // 2, (canvas_h - target_h) // 2))

    # Add front hold
    frames.append(f_canvas)
    durations.append(3200)  # 3.2 seconds static front

    # Flip front to back (angle 0 to 180)
    flip_steps = 10
    for s in range(1, flip_steps):
        angle_deg = (s / float(flip_steps)) * 180.0
        rad = math.radians(angle_deg)
        cos_val = math.cos(rad)
        
        frame = Image.new("RGBA", (canvas_w, canvas_h), (2, 10, 20, 0))
        is_front = (cos_val >= 0)
        source_card = front_s if is_front else back_s
        proj_w = max(4, int(target_w * abs(cos_val)))
        rotated = source_card.resize((proj_w, target_h), Image.Resampling.BILINEAR)
        
        paste_x = (canvas_w - proj_w) // 2
        paste_y = (canvas_h - target_h) // 2
        
        edge_thickness = int(6 * (1.0 - abs(cos_val)))
        if edge_thickness > 0:
            edge_x = paste_x + (proj_w if is_front else 0)
            f_draw = ImageDraw.Draw(frame)
            f_draw.rectangle([edge_x - 1, paste_y + 10, edge_x + edge_thickness, paste_y + target_h - 10], fill=(0, 200, 220, 200))
            
        frame.paste(rotated, (paste_x, paste_y), rotated)
        frames.append(frame)
        durations.append(50)

    # Add back hold
    frames.append(b_canvas)
    durations.append(3400)  # 3.4 seconds static back

    # Flip back to front (angle 180 to 360)
    for s in range(1, flip_steps):
        angle_deg = 180.0 + (s / float(flip_steps)) * 180.0
        rad = math.radians(angle_deg)
        cos_val = math.cos(rad)
        
        frame = Image.new("RGBA", (canvas_w, canvas_h), (2, 10, 20, 0))
        is_front = (cos_val >= 0)
        source_card = front_s if is_front else back_s
        proj_w = max(4, int(target_w * abs(cos_val)))
        rotated = source_card.resize((proj_w, target_h), Image.Resampling.BILINEAR)
        
        paste_x = (canvas_w - proj_w) // 2
        paste_y = (canvas_h - target_h) // 2
        
        edge_thickness = int(6 * (1.0 - abs(cos_val)))
        if edge_thickness > 0:
            edge_x = paste_x + (proj_w if is_front else 0)
            f_draw = ImageDraw.Draw(frame)
            f_draw.rectangle([edge_x - 1, paste_y + 10, edge_x + edge_thickness, paste_y + target_h - 10], fill=(0, 200, 220, 200))
            
        frame.paste(rotated, (paste_x, paste_y), rotated)
        frames.append(frame)
        durations.append(50)

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2
    )
    print(f"[OK] Generated Flip & Pause GIF: {out_path}")

def generate_achievements_svg(out_path):
    """Generates a 100% compliant XML SVG for verified achievement nodes."""
    achievements = [
        {
            "icon": "🏆",
            "title": "FULL-STACK MAESTRO",
            "tier": "TIER S // DIAMOND",
            "desc1": "Architected &amp; shipped 4+ production systems",
            "desc2": "across React, Django, Node &amp; Electron",
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
            "desc2": "with AES-256 Fernet, PBKDF2 &amp; SHA-256",
            "color": "#ff007f",
            "stat": "AES-256 - PBKDF2"
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
            "desc2": "with Django Channels, Redis &amp; pub/sub",
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
            "stat": "GST &amp; DYNAMIC UPI"
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
        '  <text x="28" y="32" fill="#39ff14" font-family="Consolas, monospace" font-size="13" font-weight="bold">◈ OPERATOR ACHIEVEMENT NODES // VERIFIED MILESTONES</text>',
        f'  <text x="{W - 28}" y="32" text-anchor="end" fill="#00f5ff" font-family="Consolas, monospace" font-size="12">ENGINEERING TIERS: DIAMOND &amp; GOLD</text>',
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
        svg.append(f'    <text x="14" y="32" font-size="20">{ach["icon"]}</text>')
        svg.append(f'    <text x="44" y="24" fill="{col}" font-family="Consolas, monospace" font-size="11.5" font-weight="bold">{ach["title"]}</text>')
        svg.append(f'    <text x="44" y="38" fill="#ffffff" opacity="0.65" font-family="Consolas, monospace" font-size="9">{ach["tier"]}</text>')
        svg.append(f'    <text x="14" y="62" fill="#cceeff" font-family="Consolas, monospace" font-size="10">{ach["desc1"]}</text>')
        svg.append(f'    <text x="14" y="78" fill="#cceeff" font-family="Consolas, monospace" font-size="10">{ach["desc2"]}</text>')
        svg.append(f'    <rect x="14" y="98" width="{card_w - 28}" height="22" rx="4" fill="#020a14" stroke="{col}" stroke-opacity="0.35" />')
        svg.append(f'    <text x="{card_w // 2}" y="113" text-anchor="middle" fill="{col}" font-family="Consolas, monospace" font-size="9.5" font-weight="bold">{ach["stat"]}</text>')
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
    print("[*] Generating High-Contrast ID Badge (Front)...")
    generate_id_card_front(portrait, front_path)

    back_path = os.path.join(assets_dir, "aditya_id_card_back.png")
    print("[*] Generating High-Contrast ID Badge (Back)...")
    generate_id_card_back(sign_path, "https://github.com/Aditya-tmu", back_path)

    gif_path = os.path.join(assets_dir, "aditya_id_card_flip_pause.gif")
    print("[*] Generating Smooth 3D Flip & Pause Animation (GIF)...")
    generate_flip_pause_gif(front_path, back_path, gif_path)

    ach_path = os.path.join(assets_dir, "aditya_achievements.svg")
    print("[*] Generating High-Contrast Achievement Nodes SVG...")
    generate_achievements_svg(ach_path)

    # Validate XML
    ET.parse(ach_path)
    print(f"[XML VALIDATED] {ach_path}")

    print("\n[SUCCESS] All high-contrast ID card & achievement assets generated successfully!")

if __name__ == "__main__":
    main()
