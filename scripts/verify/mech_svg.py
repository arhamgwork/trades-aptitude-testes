# -*- coding: utf-8 -*-
"""Small SVG builders for mechanical items. Each takes the same numbers the
stem quotes, so the drawing and the question cannot drift apart."""

INK, LINE, FILL = "#22323A", "#6B7C83", "#FBFCFA"


def _open(w, h, label):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">')


def gear_pair(t1, t2, label_a="A", label_b="B"):
    r1, r2 = 44, 44 * t2 / t1
    r2 = max(18, min(r2, 58))
    cx1, cy = 70, 82
    cx2 = cx1 + r1 + r2 + 6
    w = cx2 + r2 + 20
    s = [_open(w, 164, f"two meshed gears, {t1} teeth and {t2} teeth")]
    for cx, r, t, lab in ((cx1, r1, t1, label_a), (cx2, r2, t2, label_b)):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>')
        n = max(8, min(t, 24))
        import math
        for i in range(n):
            a = 2 * math.pi * i / n
            x1 = cx + (r - 5) * math.cos(a)
            y1 = cy + (r - 5) * math.sin(a)
            x2 = cx + (r + 5) * math.cos(a)
            y2 = cy + (r + 5) * math.sin(a)
            s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="13" fill="{INK}">{lab}</text>')
        s.append(f'<text x="{cx}" y="{cy + r + 18:.0f}" text-anchor="middle" font-size="11" fill="{LINE}">{t} teeth</text>')
    s.append('</svg>')
    return "".join(s)


def pulley_block(lines, load):
    w, h = 220, 200
    s = [_open(w, h, f"block and tackle with {lines} supporting lines")]
    s.append(f'<rect x="20" y="16" width="180" height="7" fill="{INK}"/>')
    top_y, bot_y = 46, 132
    for i in range(lines):
        x = 60 + i * (100 / max(1, lines - 1) if lines > 1 else 0)
        s.append(f'<line x1="{x:.1f}" y1="{top_y}" x2="{x:.1f}" y2="{bot_y}" stroke="{LINE}" stroke-width="2"/>')
    s.append(f'<circle cx="70" cy="{top_y}" r="16" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<circle cx="150" cy="{top_y}" r="16" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<circle cx="110" cy="{bot_y}" r="16" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="86" y="152" width="48" height="30" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<text x="110" y="172" text-anchor="middle" font-size="12" fill="{INK}">{load} lb</text>')
    s.append(f'<text x="196" y="{top_y - 6}" text-anchor="end" font-size="11" fill="{LINE}">{lines} supporting lines</text>')
    s.append('</svg>')
    return "".join(s)


def lever(d_effort, d_load, load):
    w, h = 300, 130
    total = d_effort + d_load
    fx = 30 + (d_effort / total) * 240
    s = [_open(w, h, "lever on a fulcrum")]
    s.append(f'<line x1="30" y1="60" x2="270" y2="60" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<polygon points="{fx:.0f},64 {fx-14:.0f},94 {fx+14:.0f},94" fill="{INK}"/>')
    s.append(f'<line x1="30" y1="30" x2="30" y2="56" stroke="{LINE}" stroke-width="2"/>')
    s.append(f'<polygon points="30,26 25,38 35,38" fill="{INK}"/>')
    s.append(f'<text x="30" y="20" text-anchor="middle" font-size="11" fill="{INK}">effort</text>')
    s.append(f'<rect x="252" y="28" width="34" height="26" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<text x="269" y="46" text-anchor="middle" font-size="11" fill="{INK}">{load} lb</text>')
    s.append(f'<text x="{(30 + fx)/2:.0f}" y="112" text-anchor="middle" font-size="11" fill="{LINE}">{d_effort} ft</text>')
    s.append(f'<text x="{(fx + 270)/2:.0f}" y="112" text-anchor="middle" font-size="11" fill="{LINE}">{d_load} ft</text>')
    s.append(f'<line x1="30" y1="104" x2="{fx:.0f}" y2="104" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<line x1="{fx:.0f}" y1="104" x2="270" y2="104" stroke="{LINE}" stroke-width="1"/>')
    s.append('</svg>')
    return "".join(s)


def pistons(a_small, a_big, force_in):
    w, h = 300, 150
    s = [_open(w, h, "two connected hydraulic pistons")]
    s.append(f'<rect x="30" y="70" width="240" height="34" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="40" y="40" width="40" height="34" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="200" y="24" width="64" height="50" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<text x="60" y="20" text-anchor="middle" font-size="11" fill="{INK}">{force_in} lb</text>')
    s.append(f'<polygon points="60,24 54,36 66,36" fill="{INK}"/>')
    s.append(f'<text x="60" y="122" text-anchor="middle" font-size="11" fill="{LINE}">{a_small} sq in</text>')
    s.append(f'<text x="232" y="122" text-anchor="middle" font-size="11" fill="{LINE}">{a_big} sq in</text>')
    s.append('</svg>')
    return "".join(s)


def circuit(resistors, volts, kind="series"):
    w, h = 300, 150
    s = [_open(w, h, f"{kind} circuit with {len(resistors)} resistors")]
    s.append(f'<rect x="24" y="30" width="252" height="86" fill="none" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="14" y="58" width="20" height="30" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<text x="24" y="132" text-anchor="middle" font-size="11" fill="{INK}">{volts} V</text>')
    if kind == "series":
        for i, r in enumerate(resistors):
            x = 80 + i * 90
            s.append(f'<rect x="{x}" y="20" width="46" height="20" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
            s.append(f'<text x="{x+23}" y="35" text-anchor="middle" font-size="11" fill="{INK}">{r} Ω</text>')
    else:
        for i, r in enumerate(resistors):
            y = 44 + i * 40
            s.append(f'<rect x="130" y="{y}" width="46" height="20" fill="{FILL}" stroke="{INK}" stroke-width="2"/>')
            s.append(f'<text x="153" y="{y+15}" text-anchor="middle" font-size="11" fill="{INK}">{r} Ω</text>')
            s.append(f'<line x1="90" y1="{y+10}" x2="130" y2="{y+10}" stroke="{INK}" stroke-width="2"/>')
            s.append(f'<line x1="176" y1="{y+10}" x2="216" y2="{y+10}" stroke="{INK}" stroke-width="2"/>')
    s.append('</svg>')
    return "".join(s)
