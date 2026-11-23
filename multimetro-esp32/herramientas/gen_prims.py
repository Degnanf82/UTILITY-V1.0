# Genera la version pictorica del diagrama del multimetro.
import re, sys

SRC = sys.argv[1] if len(sys.argv)>1 else None   # html anterior (para reusar estilos, tabla, pasos y materiales)
OUT = sys.argv[2]


# ------------------------------------------------------------------ primitivas
BAND = {"k": "#1a1a1a", "n": "#7b4a1e", "r": "#c62828", "o": "#ef6c00", "y": "#f2cc1b", "g": "#2e7d32", "u": "#c9a227"}

def wire(pts, cls="w-ana"):
    return f'<polyline class="w {cls}" points="{" ".join(f"{x},{y}" for x, y in pts)}"/>'

def dot(x, y, cls="d-ana"):
    return f'<circle class="dot {cls}" cx="{x}" cy="{y}" r="5.5"/>'

def chip(x, y, text, kind, anchor="start", w=None):
    """Etiqueta redondeada centrada verticalmente en y."""
    cw = w or int(len(text) * 6.9 + 16)
    x0 = x if anchor == "start" else (x - cw if anchor == "end" else x - cw / 2)
    return (f'<g class="chip c-{kind}"><rect x="{x0:.0f}" y="{y-12}" width="{cw}" height="24" rx="12"/>'
            f'<text x="{x0 + cw/2:.0f}" y="{y+4}" text-anchor="middle">{text}</text></g>')

def res_h(x1, x2, y, bands, label, big=False):
    bw, bh = (70, 22) if big else (54, 16)
    cx = (x1 + x2) / 2
    s = wire([(x1, y), (x2, y)], "w-lead")
    s += f'<rect class="{"rbig" if big else "rbody"}" x="{cx-bw/2}" y="{y-bh/2}" width="{bw}" height="{bh}" rx="{bh/2 if not big else 3}"/>'
    if bands:
        for i, b in enumerate(bands[:3]):
            s += f'<rect x="{cx-bw/2+10+i*8}" y="{y-bh/2}" width="4.5" height="{bh}" fill="{BAND[b]}"/>'
        s += f'<rect x="{cx+bw/2-14}" y="{y-bh/2}" width="4.5" height="{bh}" fill="{BAND[bands[3]]}"/>'
    s += f'<text class="lbl" x="{cx}" y="{y-bh/2-7}" text-anchor="middle">{label}</text>'
    return s

def res_v(x, y1, y2, bands, label, side="right", big=False):
    bw, bh = (22, 70) if big else (16, 54)
    cy = (y1 + y2) / 2
    s = wire([(x, y1), (x, y2)], "w-lead")
    s += f'<rect class="{"rbig" if big else "rbody"}" x="{x-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" rx="{bw/2 if not big else 3}"/>'
    if bands:
        for i, b in enumerate(bands[:3]):
            s += f'<rect x="{x-bw/2}" y="{cy-bh/2+10+i*8}" width="{bw}" height="4.5" fill="{BAND[b]}"/>'
        s += f'<rect x="{x-bw/2}" y="{cy+bh/2-14}" width="{bw}" height="4.5" fill="{BAND[bands[3]]}"/>'
    if big:
        s += f'<text class="rbig-t" x="{x}" y="{cy+4}" text-anchor="middle" transform="rotate(-90 {x} {cy})">R10</text>'
    lines = label.split("|")
    for i, l in enumerate(lines):
        yy = cy + 4 + (i - (len(lines) - 1) / 2) * 15
        if side == "right":
            s += f'<text class="lbl" x="{x+bw/2+8}" y="{yy}">{l}</text>'
        else:
            s += f'<text class="lbl" x="{x-bw/2-8}" y="{yy}" text-anchor="end">{l}</text>'
    return s

def diode_h(x1, x2, y, cathode="left", label="BAT85"):
    cx = (x1 + x2) / 2
    s = wire([(x1, y), (x2, y)], "w-lead")
    s += f'<rect class="dbody" x="{cx-18}" y="{y-6}" width="36" height="12" rx="2"/>'
    bx = cx - 18 + 3 if cathode == "left" else cx + 18 - 8
    s += f'<rect class="dband" x="{bx}" y="{y-6}" width="5" height="12"/>'
    s += f'<text class="lbl-m" x="{cx}" y="{y-11}" text-anchor="middle">{label}</text>'
    return s

def diode_v(x, y1, y2, cathode="top", label="BAT85"):
    cy = (y1 + y2) / 2
    s = wire([(x, y1), (x, y2)], "w-lead")
    s += f'<rect class="dbody" x="{x-6}" y="{cy-18}" width="12" height="36" rx="2"/>'
    by = cy - 18 + 3 if cathode == "top" else cy + 18 - 8
    s += f'<rect class="dband" x="{x-6}" y="{by}" width="12" height="5"/>'
    s += f'<text class="lbl-m" x="{x+12}" y="{cy+4}">{label}</text>'
    return s

def jack(x, y, kind, label, lx=None, anchor="end"):
    s = f'<circle class="jack-{kind}" cx="{x}" cy="{y}" r="13"/><circle class="jack-hole" cx="{x}" cy="{y}" r="4.5"/>'
    s += f'<text class="lbl-b" x="{lx if lx is not None else x-22}" y="{y+5}" text-anchor="{anchor}">{label}</text>'
    return s

def svg(w, h, body, label):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{body}</svg>'

