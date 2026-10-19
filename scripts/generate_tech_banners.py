#!/usr/bin/env python3
"""
Generates ultra-techy, futuristic Cyber / Dev-HUD Header and Footer SVGs for GitHub Profile:
1. assets/tech_header_banner.svg (1200 x 320)
2. assets/tech_footer_banner.svg (1200 x 200)
"""

import os
import math

def generate_header_svg(out_path):
    W, H = 1200, 320
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto">',
        '  <defs>',
        '    <linearGradient id="hdrBg" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#020a14" />',
        '      <stop offset="40%" stop-color="#041426" />',
        '      <stop offset="80%" stop-color="#061c36" />',
        '      <stop offset="100%" stop-color="#020a14" />',
        '    </linearGradient>',
        '    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#00f5ff" />',
        '      <stop offset="50%" stop-color="#ffffff" />',
        '      <stop offset="100%" stop-color="#39ff14" />',
        '    </linearGradient>',
        '    <linearGradient id="laserGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#00f5ff" stop-opacity="0" />',
        '      <stop offset="30%" stop-color="#00f5ff" stop-opacity="0.8" />',
        '      <stop offset="50%" stop-color="#ffffff" stop-opacity="1" />',
        '      <stop offset="70%" stop-color="#39ff14" stop-opacity="0.8" />',
        '      <stop offset="100%" stop-color="#39ff14" stop-opacity="0" />',
        '    </linearGradient>',
        '    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="3" result="blur" />',
        '      <feMerge>',
        '        <feMergeNode in="blur" />',
        '        <feMergeNode in="SourceGraphic" />',
        '      </feMerge>',
        '    </filter>',
        '  </defs>',
        '',
        '  <!-- Background Canvas -->',
        f'  <rect width="{W}" height="{H}" rx="16" fill="url(#hdrBg)" stroke="#00f5ff" stroke-opacity="0.35" stroke-width="2" />',
        '',
        '  <!-- Cyber Dot Matrix Grid -->',
        '  <g fill="#00f5ff" opacity="0.15">'
    ]

    # Grid dots
    for gx in range(40, W - 40, 28):
        for gy in range(40, H - 40, 28):
            svg.append(f'    <circle cx="{gx}" cy="{gy}" r="1" />')

    svg.extend([
        '  </g>',
        '',
        '  <!-- Chamfered Inner Frame -->',
        f'  <path d="M 30 50 L 50 30 L {W - 50} 30 L {W - 30} 50 L {W - 30} {H - 50} L {W - 50} {H - 30} L 50 {H - 30} L 30 {H - 50} Z" '
        'fill="none" stroke="#00f5ff" stroke-opacity="0.4" stroke-width="1.2" stroke-dasharray="8 6" />',
        '',
        '  <!-- Corner Brackets -->',
        '  <path d="M 22 60 L 22 22 L 60 22" fill="none" stroke="#00f5ff" stroke-width="3" />',
        f'  <path d="M {W - 60} 22 L {W - 22} 22 L {W - 22} 60" fill="none" stroke="#00f5ff" stroke-width="3" />',
        f'  <path d="M 22 {H - 60} L 22 {H - 22} L 60 {H - 22}" fill="none" stroke="#00f5ff" stroke-width="3" />',
        f'  <path d="M {W - 60} {H - 22} L {W - 22} {H - 22} L {W - 22} {H - 60}" fill="none" stroke="#00f5ff" stroke-width="3" />',
        '',
        '  <!-- Tech Circuit Traces Left -->',
        '  <path d="M 30 160 L 90 160 L 120 130 L 180 130" fill="none" stroke="#00f5ff" stroke-opacity="0.5" stroke-width="1.5" />',
        '  <circle cx="180" cy="130" r="3" fill="#00f5ff" />',
        '  <path d="M 30 190 L 110 190 L 140 220 L 200 220" fill="none" stroke="#39ff14" stroke-opacity="0.5" stroke-width="1.5" />',
        '  <circle cx="200" cy="220" r="3" fill="#39ff14" />',
        '',
        '  <!-- Tech Circuit Traces Right -->',
        f'  <path d="M {W - 30} 160 L {W - 90} 160 L {W - 120} 130 L {W - 180} 130" fill="none" stroke="#00f5ff" stroke-opacity="0.5" stroke-width="1.5" />',
        f'  <circle cx="{W - 180}" cy="130" r="3" fill="#00f5ff" />',
        f'  <path d="M {W - 30} 190 L {W - 110} 190 L {W - 140} 220 L {W - 200} 220" fill="none" stroke="#39ff14" stroke-opacity="0.5" stroke-width="1.5" />',
        f'  <circle cx="{W - 200}" cy="220" r="3" fill="#39ff14" />',
        '',
        '  <!-- Top Telemetry Header Bar -->',
        '  <rect x="70" y="44" width="220" height="24" rx="4" fill="#051828" stroke="#00f5ff" stroke-opacity="0.4" />',
        '  <circle cx="84" cy="56" r="4" fill="#39ff14" filter="url(#glow)" />',
        '  <text x="96" y="60" fill="#39ff14" font-family="Consolas, monospace" font-size="11" font-weight="bold">SYSTEM STATUS: 200 OK</text>',
        '',
        f'  <text x="{W // 2}" y="60" text-anchor="middle" fill="#00f5ff" opacity="0.8" font-family="Consolas, monospace" font-size="11" font-weight="bold">'
        '◈ OPERATOR PROTOCOL AK-OS v6.0 // APPLIED AI &amp; DISTRIBUTED SYSTEMS ◈</text>',
        '',
        f'  <rect x="{W - 280}" y="44" width="210" height="24" rx="4" fill="#051828" stroke="#00f5ff" stroke-opacity="0.4" />',
        f'  <text x="{W - 175}" y="60" text-anchor="middle" fill="#00f5ff" font-family="Consolas, monospace" font-size="11">NODE: ASIA-SOUTH-1 // INDIA 🇮🇳</text>',
        '',
        '  <!-- Central Laser Divider Line -->',
        f'  <line x1="80" y1="80" x2="{W - 80}" y2="80" stroke="url(#laserGrad)" stroke-width="2" />',
        '',
        '  <!-- Main Hero Title -->',
        f'  <text x="{W // 2}" y="152" text-anchor="middle" fill="url(#textGrad)" filter="url(#glow)" '
        'font-family="system-ui, -apple-system, \'Segoe UI\', sans-serif" font-size="64" font-weight="900" letter-spacing="6">ADITYA KUMAR</text>',
        '',
        '  <!-- Subtitle Tagline -->',
        f'  <text x="{W // 2}" y="196" text-anchor="middle" fill="#00f5ff" '
        'font-family="Consolas, Fira Code, monospace" font-size="16" font-weight="bold" letter-spacing="3">'
        '⚡ FULL-STACK DEVELOPER  ·  AI SYSTEMS ARCHITECT  ·  DESKTOP &amp; MOBILE BUILDER ⚡</text>',
        '',
        '  <!-- Terminal Command Prompt Box -->',
        f'  <rect x="{W // 2 - 380}" y="222" width="760" height="34" rx="6" fill="#020a14" stroke="#00f5ff" stroke-opacity="0.5" stroke-width="1.2" />',
        f'  <text x="{W // 2}" y="244" text-anchor="middle" fill="#39ff14" font-family="Consolas, monospace" font-size="12">'
        '<tspan fill="#00f5ff">aditya@workstation:~$</tspan> ./deploy --stack="React • Django • TypeScript • Kotlin • Gemini AI • AES-256" --status=READY</text>',
        '',
        '  <!-- Bottom Telemetry Ticks Bar -->',
        f'  <line x1="80" y1="278" x2="{W - 80}" y2="278" stroke="#00f5ff" stroke-opacity="0.3" stroke-width="1" />'
    ])

    # Ticks along bottom line
    for tx in range(100, W - 80, 50):
        svg.append(f'  <line x1="{tx}" y1="274" x2="{tx}" y2="282" stroke="#00f5ff" stroke-opacity="0.5" stroke-width="1" />')

    svg.extend([
        f'  <text x="80" y="296" fill="#00f5ff" opacity="0.7" font-family="Consolas, monospace" font-size="10">UPTIME: 99.98%</text>',
        f'  <text x="{W // 2}" y="296" text-anchor="middle" fill="#39ff14" opacity="0.9" font-family="Consolas, monospace" font-size="10">● ALL REPOSITORIES ACTIVE &amp; PASSING CI/CD</text>',
        f'  <text x="{W - 80}" y="296" text-anchor="end" fill="#00f5ff" opacity="0.7" font-family="Consolas, monospace" font-size="10">CLEARANCE: LEVEL 5 ROOT</text>',
        '</svg>'
    ])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Generated: {out_path}")

def generate_footer_svg(out_path):
    W, H = 1200, 200
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto">',
        '  <defs>',
        '    <linearGradient id="ftrBg" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#020a14" />',
        '      <stop offset="60%" stop-color="#051828" />',
        '      <stop offset="100%" stop-color="#020a14" />',
        '    </linearGradient>',
        '    <linearGradient id="eqGrad" x1="0%" y1="100%" x2="0%" y2="0%">',
        '      <stop offset="0%" stop-color="#00f5ff" />',
        '      <stop offset="100%" stop-color="#39ff14" />',
        '    </linearGradient>',
        '    <filter id="ftrGlow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="2" result="blur" />',
        '      <feMerge>',
        '        <feMergeNode in="blur" />',
        '        <feMergeNode in="SourceGraphic" />',
        '      </feMerge>',
        '    </filter>',
        '  </defs>',
        '',
        f'  <rect width="{W}" height="{H}" rx="14" fill="url(#ftrBg)" stroke="#00f5ff" stroke-opacity="0.35" stroke-width="1.8" />',
        '',
        '  <!-- Corner Brackets -->',
        '  <path d="M 20 40 L 20 20 L 40 20" fill="none" stroke="#00f5ff" stroke-width="2.5" />',
        f'  <path d="M {W - 40} 20 L {W - 20} 20 L {W - 20} 40" fill="none" stroke="#00f5ff" stroke-width="2.5" />',
        f'  <path d="M 20 {H - 40} L 20 {H - 20} L 40 {H - 20}" fill="none" stroke="#00f5ff" stroke-width="2.5" />',
        f'  <path d="M {W - 40} {H - 20} L {W - 20} {H - 20} L {W - 20} {H - 40}" fill="none" stroke="#00f5ff" stroke-width="2.5" />',
        '',
        '  <!-- Equalizer Visualizer Bars Left -->',
        '  <g transform="translate(60, 40)">'
    ]

    # Equalizer heights
    eq_left = [18, 28, 42, 60, 48, 35, 55, 68, 40, 22, 35, 50, 30]
    for i, eh in enumerate(eq_left):
        svg.append(f'    <rect x="{i * 12}" y="{80 - eh}" width="6" height="{eh}" rx="2" fill="url(#eqGrad)" opacity="0.75" />')

    svg.extend([
        '  </g>',
        '',
        '  <!-- Equalizer Visualizer Bars Right -->',
        f'  <g transform="translate({W - 210}, 40)">'
    ])

    eq_right = [30, 50, 35, 22, 40, 68, 55, 35, 48, 60, 42, 28, 18]
    for i, eh in enumerate(eq_right):
        svg.append(f'    <rect x="{i * 12}" y="{80 - eh}" width="6" height="{eh}" rx="2" fill="url(#eqGrad)" opacity="0.75" />')

    svg.extend([
        '  </g>',
        '',
        '  <!-- Central Telemetry Text -->',
        f'  <text x="{W // 2}" y="52" text-anchor="middle" fill="#00f5ff" font-family="Consolas, monospace" font-size="12" font-weight="bold" letter-spacing="2">'
        '// END OF TRANSMISSION // TERMINAL PROTOCOL AK-OS 6.0 //</text>',
        '',
        f'  <text x="{W // 2}" y="95" text-anchor="middle" fill="#39ff14" filter="url(#ftrGlow)" '
        'font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" letter-spacing="3">'
        '⚡ SYSTEM STATUS: ALL NODES ONLINE &amp; READY TO DEPLOY ⚡</text>',
        '',
        f'  <line x1="280" y1="120" x2="{W - 280}" y2="120" stroke="#00f5ff" stroke-opacity="0.3" stroke-width="1" />',
        '',
        f'  <text x="{W // 2}" y="145" text-anchor="middle" fill="#a0c4df" font-family="Consolas, monospace" font-size="12">'
        'ENCRYPTION: AES-256 (FERNET)  •  INTEGRITY: SHA-256 VERIFIED  •  BASE: MORADABAD, INDIA [IN]</text>',
        '',
        f'  <text x="{W // 2}" y="172" text-anchor="middle" fill="#00f5ff" opacity="0.8" font-family="Consolas, monospace" font-size="11">'
        '&copy; 2026 ADITYA KUMAR (@Aditya-tmu) · BUILT WITH CODE, RESILIENCE &amp; PASSION</text>',
        '</svg>'
    ])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Generated: {out_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    assets_dir = os.path.join(repo_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    header_path = os.path.join(assets_dir, "tech_header_banner.svg")
    footer_path = os.path.join(assets_dir, "tech_footer_banner.svg")

    print("[*] Generating Ultra-Techy Header SVG...")
    generate_header_svg(header_path)

    print("[*] Generating Ultra-Techy Footer SVG...")
    generate_footer_svg(footer_path)

    print("\n[SUCCESS] Tech header & footer banners generated successfully!")

if __name__ == "__main__":
    main()
