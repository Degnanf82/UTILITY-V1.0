# Vista de montaje sobre placa perforada (componentes arriba, cables de colores).
import sys, math
OUT = sys.argv[1]
P = 22               # paso de la rejilla (2.54 mm)
OX, OY = 60, 175     # origen de la rejilla
COLS, ROWS = 30, 43
F = "font-family:Inter,DejaVu Sans,Arial,sans-serif"

def xy(c, r):
    return OX + c * P, OY + r * P

pads = []      # (c, r, net)
draw = []      # elementos de componentes
labels = []

def pad(c, r, net):
    pads.append((c, r, net))

def text(x, y, t, size=12, weight=600, color="#17201c", anchor="middle", rot=0):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    labels.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{F};font-size:{size}px;font-weight:{weight}" fill="{color}"{tr}>{t}</text>')

BANDS = {"k": "#1a1a1a", "n": "#7b4a1e", "r": "#c62828", "o": "#ef6c00", "y": "#f2cc1b", "g": "#2e7d32", "u": "#c9a227"}

def resistor(c1, r1, c2, r2, n1, n2, bands, label, big=False):
    pad(c1, r1, n1); pad(c2, r2, n2)
    x1, y1 = xy(c1, r1); x2, y2 = xy(c2, r2)
    draw.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#9aa0a6" stroke-width="2.5"/>')
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    L = 46 if not big else 64
    h = 14 if not big else 20
    g = f'<g transform="translate({cx} {cy}) rotate({ang})">'
    if big:
        g += f'<rect x="{-L/2}" y="{-h/2}" width="{L}" height="{h}" rx="2" fill="#f2f1ec" stroke="#9c9a92"/>'
        g += f'<text x="0" y="4" text-anchor="middle" style="{F};font-size:10px;font-weight:700" fill="#3a3a36">1Ω 1W</text>'
    else:
        g += f'<rect x="{-L/2}" y="{-h/2}" width="{L}" height="{h}" rx="7" fill="#e7cf9f" stroke="#a88b55"/>'
        for i, b in enumerate(bands[:3]):
            g += f'<rect x="{-L/2+8+i*7}" y="{-h/2}" width="4" height="{h}" fill="{BANDS[b]}"/>'
        g += f'<rect x="{L/2-12}" y="{-h/2}" width="4" height="{h}" fill="{BANDS[bands[3]]}"/>'
    g += "</g>"
    draw.append(g)
    if abs(ang) < 45 or abs(ang) > 135:
        text(cx, cy - 12, label, 11)
    else:
        text(cx + 14, cy + 4, label, 11, anchor="start")

def diode(ca, ra, ck, rk, na, nk, label, glass=False):
    pad(ca, ra, na); pad(ck, rk, nk)
    x1, y1 = xy(ca, ra); x2, y2 = xy(ck, rk)
    draw.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#9aa0a6" stroke-width="2.5"/>')
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    body = "#e07b39" if glass else "#202326"
    band = "#202326" if glass else "#d8dbe0"
    draw.append(f'<g transform="translate({cx} {cy}) rotate({ang})"><rect x="-16" y="-6" width="32" height="12" rx="2" fill="{body}"/>'
                f'<rect x="9" y="-6" width="5" height="12" fill="{band}"/></g>')
    if abs(ang) < 45 or abs(ang) > 135:
        text(cx, cy - 11, label, 10)
    else:
        text(cx + 12, cy + 4, label, 10, anchor="start")

def to92(c, r, nets, label):
    for i, n in enumerate(nets):
        pad(c + i, r, n)
    x, y = xy(c + 1, r)
    draw.append(f'<path d="M{x-26},{y-6} L{x-26},{y-26} A26,20 0 0 1 {x+26},{y-26} L{x+26},{y-6} Z" fill="#1e2023"/>')
    text(x, y - 13, label, 9, 700, "#ffffff")
    for i, l in enumerate("EBC"):
        text(xy(c + i, r)[0], y + 18, l, 9, 700, "#56635d")

def relay(c, r, nets, label):
    # cuerpo de c..c+7, r..r+5 ; pads: COM, bobina A, bobina B, NC, NO
    x0, y0 = xy(c, r)
    draw.append(f'<rect x="{x0-10}" y="{y0-10}" width="{7*P+20}" height="{4*P+20}" rx="5" fill="#2557b0" stroke="#0d2a63"/>')
    text(x0 + 3.5 * P, y0 + 1.6 * P, label, 13, 700, "#ffffff")
    text(x0 + 3.5 * P, y0 + 2.4 * P, "SRD-05VDC", 10, 500, "#cfe0ff")
    pl = [(c, r + 2, "COM"), (c + 2, r, "bob"), (c + 2, r + 4, "bob"), (c + 7, r, "NC"), (c + 7, r + 4, "NO")]
    for (pc, pr, t), n in zip(pl, nets):
        pad(pc, pr, n)
        px, py = xy(pc, pr)
        text(px + (0 if pc != c else 18), py + (16 if pr == r else -9) if pc != c else py + 4, t, 9, 700, "#ffffff",
             anchor="middle" if pc != c else "start")

def button(c, r, n1, n2, label):
    pad(c, r, n1); pad(c + 2, r + 2, n2)
    x, y = xy(c + 1, r + 1)
    draw.append(f'<rect x="{x-24}" y="{y-24}" width="48" height="48" rx="4" fill="#2b2f33"/><circle cx="{x}" cy="{y}" r="12" fill="#d9dde2"/>')
    text(x, y + 40, label, 11, 700)

def hole_grid():
    s = []
    x0, y0 = xy(-1, -1)
    s.append(f'<rect x="{x0}" y="{y0}" width="{(COLS+1)*P}" height="{(ROWS+1)*P}" rx="10" fill="#c99a5b" stroke="#8a6431" stroke-width="2"/>')
    for c in range(COLS):
        for r in range(ROWS):
            x, y = xy(c, r)
            s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#d9b178"/><circle cx="{x}" cy="{y}" r="2.2" fill="#6b4a22"/>')
    return s

# ------------------------------------------------------------------ piezas
# Reles
relay(2, 3, ["PROBE_R", "+5V", "Q1C", "K2NC", "K2NO"], "K2 · mA")
relay(13, 3, ["K2NC", "+5V", "Q2C", "V_IN", "K1NO"], "K1 · Ω")
# Drivers
to92(3, 11, ["GND", "Q1B", "Q1C"], "Q1")
diode(7, 14, 7, 10, "Q1C", "+5V", "D1", glass=True)
resistor(4, 13, 4, 17, "Q1B", "K2_DRV", "nnrn", "R1 1k")
resistor(2, 13, 2, 17, "Q1B", "GND", "nnon", "R2 10k")
to92(14, 11, ["GND", "Q2B", "Q2C"], "Q2")
diode(18, 14, 18, 10, "Q2C", "+5V", "D2", glass=True)
resistor(15, 13, 15, 17, "Q2B", "K1_DRV", "nnrn", "R3 1k")
resistor(13, 13, 13, 17, "Q2B", "GND", "nnon", "R4 10k")
# Fusible y shunt
pad(23, 3, "K2NO"); pad(28, 3, "I_SHUNT")
x1, y1 = xy(23, 3); x2, y2 = xy(28, 3)
draw.append(f'<rect x="{x1-6}" y="{y1-12}" width="{x2-x1+12}" height="24" rx="5" fill="#1e2023"/>'
            f'<rect x="{x1+10}" y="{y1-8}" width="{x2-x1-20}" height="16" rx="3" fill="#dcedf5" stroke="#8fb3c4"/>'
            f'<rect x="{x1+10}" y="{y1-8}" width="14" height="16" fill="#b8bcc2"/><rect x="{x2-24}" y="{y1-8}" width="14" height="16" fill="#b8bcc2"/>')
text((x1 + x2) / 2, y1 - 18, "F1 fusible 315 mA", 11)
resistor(28, 5, 28, 9, "I_SHUNT", "GND", None, "R_SH", big=True)
# PTC
pad(23, 7, "K1NO"); pad(25, 7, "NODO_X")
x, y = xy(24, 7)
draw.append(f'<line x1="{x-P}" y1="{y}" x2="{x+P}" y2="{y}" stroke="#9aa0a6" stroke-width="2.5"/><circle cx="{x}" cy="{y}" r="12" fill="#e8b100" stroke="#8a6a00"/>')
text(x, y - 17, "RT1 PTC", 11)
# Divisor + frecuencia
resistor(21, 12, 26, 12, "V_IN", "V_ADC", "nngn", "R5 1M")
resistor(28, 12, 28, 16, "V_ADC", "GND", "nnyn", "R6 100k")
diode(22, 14, 26, 14, "V_ADC", "+3V3", "D3 BAT85")
diode(22, 16, 26, 16, "GND", "V_ADC", "D4 BAT85")
resistor(21, 18, 26, 18, "V_IN", "FREQ", "nnyn", "R7 100k")
diode(22, 20, 26, 20, "FREQ", "+3V3", "D5 BAT85")
diode(22, 22, 26, 22, "GND", "FREQ", "D6 BAT85")
# Zener y C1
diode(10, 22, 10, 19, "GND", "+3V3", "DZ1 3.6V")
pad(11, 30, "+3V3"); pad(11, 32, "GND")
x, y = xy(11, 31)
draw.append(f'<rect x="{x-8}" y="{y-10}" width="16" height="20" rx="4" fill="#e0a33a"/>')
text(x + 14, y + 4, "C1", 10, anchor="start")
# ESP32-C3 (USB abajo)
L = ["REF_100K", "SENSE", "SDA", "SCL", "DESC", "K1_DRV", "REF_1M", "K2_DRV"]
R = ["REF_1K", "REF_10K", None, "FREQ", "BUZ", "+3V3", "GND", "+5V"]
xa, ya = xy(2, 26); xb, yb = xy(9, 33)
draw.append(f'<rect x="{xa-14}" y="{ya-48}" width="{xb-xa+28}" height="{yb-ya+80}" rx="8" fill="#3b1f63" stroke="#24113f" stroke-width="1.5"/>')
draw.append(f'<rect x="{xa+30}" y="{ya-8}" width="{xb-xa-60}" height="{3*P}" rx="3" fill="#0d1030" stroke="#9aa0a6" stroke-width="2"/>')
text((xa + xb) / 2, ya + 28, "OLED", 11, 700, "#8fb8ff")
draw.append(f'<rect x="{(xa+xb)/2-26}" y="{yb+14}" width="52" height="30" rx="6" fill="#b9bec4"/>')
text((xa + xb) / 2, ya + 5.2 * P, "ESP32-C3", 13, 700, "#ffffff")
for i, n in enumerate(L):
    pad(2, 26 + i, n)
    text(xy(2, 26 + i)[0] + 12, xy(2, 26 + i)[1] + 4, ["3", "4", "5", "6", "7", "8", "9", "10"][i], 9, 700, "#ffffff", "start")
for i, n in enumerate(R):
    pad(9, 26 + i, n or "NC")
    text(xy(9, 26 + i)[0] - 12, xy(9, 26 + i)[1] + 4, ["0", "1", "2", "TX", "RX", "V3", "GD", "V5"][i], 9, 700, "#ffffff", "end")
# ADS1115 (cabecera de 10 pines en la fila 31)
xa, ya = xy(13, 26)
draw.append(f'<rect x="{xa-14}" y="{ya-12}" width="{9*P+28}" height="{5*P+24}" rx="6" fill="#1c5aa6" stroke="#0f3a72"/>')
text(xa + 4.5 * P, ya + 1.2 * P, "ADS1115", 14, 700, "#ffffff")
for i, (nm, n) in enumerate(zip(["VDD", "GND", "SCL", "SDA", "ADDR", "ALRT", "A0", "A1", "A2", "A3"],
                                ["+3V3", "GND", "SCL", "SDA", "GND", "NC", "V_ADC", "X_ADC", "I_SHUNT", "BTN"])):
    pad(13 + i, 31, n)
    x, y = xy(13 + i, 31)
    text(x + 4, y - 12, nm, 9, 700, "#ffffff", "start", rot=-90)
# Nodo X: referencias y protecciones (fila 35 = tira comun)
for i, (n, b, lab) in enumerate([("REF_1K", "nnrn", "R8 1k"), ("REF_10K", "nnon", "R9 10k"), ("REF_100K", "nnyn", "R10 100k"),
                                 ("REF_1M", "nngn", "R11 1M"), ("DESC", "rrnu", "R12 220")]):
    resistor(13 + 2 * i, 35, 13 + 2 * i, 39, "NODO_X", n, b, "")
    text(xy(13 + 2 * i, 41)[0], xy(13 + 2 * i, 41)[1] - 4, lab, 10, 700, "#17201c", "middle")
resistor(23, 35, 23, 39, "NODO_X", "X_ADC", "nnrn", "")
text(xy(23, 41)[0], xy(23, 41)[1] - 4, "R13 1k", 10)
resistor(25, 35, 25, 39, "NODO_X", "SENSE", "nnrn", "")
text(xy(25, 41)[0] + 6, xy(25, 41)[1] + 12, "R14 1k", 10)
diode(27, 35, 27, 39, "NODO_X", "+3V3", "")
diode(29, 39, 29, 35, "GND", "NODO_X", "")
text(xy(27, 41)[0], xy(27, 41)[1] - 4, "D7", 10); text(xy(29, 41)[0], xy(29, 41)[1] - 4, "D8", 10)
text(xy(21, 33.6)[0], xy(21, 33.6)[1], "tira común = NODO X", 11, 700, "#138a55")
# Botones (A3)
resistor(1, 36, 4, 36, "+3V3", "BTN", "nnon", "R15 10k")
button(1, 38, "BTN", "GND", "MODO")
resistor(6, 36, 6, 39, "BTN", "BTN_H", "nnon", "R16")
button(6, 39, "BTN_H", "GND", "HOLD")
resistor(10, 36, 10, 39, "BTN", "BTN_R", "ooon", "R17")
button(10, 39, "BTN_R", "GND", "REL")
# Buzzer y Q3
x, y = xy(25.5, 27.5)
draw.append(f'<circle cx="{x}" cy="{y}" r="34" fill="#1e2023"/><circle cx="{x}" cy="{y}" r="6" fill="#55595e"/>')
text(x, y - 40, "BZ1", 11)
pad(24, 26, "BZ_N"); pad(27, 26, "+5V")
text(xy(27, 26)[0] + 8, xy(27, 26)[1] - 8, "+", 14, 700, "#ffffff", "start")
to92(23, 30, ["GND", "Q3B", "BZ_N"], "Q3")
resistor(27, 30, 27, 33, "Q3B", "BUZ", "nnrn", "R18 1k")
# Jacks (fuera de la placa)
pad(1, 0, "PROBE_R"); pad(5, 0, "GND")

# ------------------------------------------------------------------ cables
COL = {"+5V": "#e8590c", "+3V3": "#d22a3f", "GND": "#1d2421", "SDA": "#e0a100", "SCL": "#1d64c8",
       "PROBE_R": "#c62828", "K2NC": "#c62828", "K2NO": "#c62828", "I_SHUNT": "#c62828", "V_IN": "#c62828", "K1NO": "#c62828",
       "K1_DRV": "#7b3fbf", "K2_DRV": "#7b3fbf", "BUZ": "#7b3fbf", "BTN": "#7b3fbf"}
nets = {}
for c, r, n in pads:
    if n in ("NC",):
        continue
    nets.setdefault(n, []).append((c, r))
wires = []
for n, pts in nets.items():
    if len(pts) < 2:
        continue
    # arbol de expansion minima (Prim): cada pad se une al mas cercano ya conectado
    pts = list(dict.fromkeys(pts))
    inside = [pts[0]]
    edges = []
    rest = pts[1:]
    while rest:
        a, b = min(((a, b) for a in inside for b in rest),
                   key=lambda e: (e[0][0] - e[1][0]) ** 2 + (e[0][1] - e[1][1]) ** 2)
        edges.append((a, b)); inside.append(b); rest.remove(b)
    col = COL.get(n, "#138a55")
    for a, b in edges:
        if (a[0] == b[0] and abs(a[1] - b[1]) <= 0) :
            continue
        x1, y1 = xy(*a); x2, y2 = xy(*b)
        dx, dy = x2 - x1, y2 - y1
        mx, my = (x1 + x2) / 2 - dy * 0.12, (y1 + y2) / 2 + dx * 0.12
        wires.append(f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="#00000055" stroke-width="7" stroke-linecap="round"/>'
                     f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{col}" stroke-width="4.2" stroke-linecap="round" opacity="0.93"/>')

padsvg = []
for c, r, n in pads:
    x, y = xy(c, r)
    padsvg.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#c9a227" stroke="#6b4a22" stroke-width="1"/>')

# Jacks
jx, jy = xy(1, 0); kx, ky = xy(5, 0)
jacks = [f'<circle cx="{jx}" cy="{jy-70}" r="18" fill="#c62828"/><circle cx="{jx}" cy="{jy-70}" r="6" fill="#111"/>',
         f'<line x1="{jx}" y1="{jy-52}" x2="{jx}" y2="{jy}" stroke="#c62828" stroke-width="5"/>',
         f'<circle cx="{kx}" cy="{ky-70}" r="18" fill="#1d2421"/><circle cx="{kx}" cy="{ky-70}" r="6" fill="#555"/>',
         f'<line x1="{kx}" y1="{ky-52}" x2="{kx}" y2="{ky}" stroke="#1d2421" stroke-width="5"/>']
text(jx, jy - 96, "Punta ROJA", 12, 700, "#c62828")
text(kx + 30, ky - 64, "Punta NEGRA (COM)", 12, 700, "#1d2421", "start")

W = OX * 2 + COLS * P + 260
H = OY + ROWS * P + 60
legend = []
lx = OX + COLS * P + 40
for i, (t, c) in enumerate([("+5V", "#e8590c"), ("+3.3V", "#d22a3f"), ("GND", "#1d2421"), ("SDA", "#e0a100"), ("SCL", "#1d64c8"),
                             ("punta roja / relés / shunt", "#c62828"), ("control (relés, buzzer, botones)", "#7b3fbf"), ("señales analógicas", "#138a55")]):
    y = OY + 20 + i * 30
    legend.append(f'<line x1="{lx}" y1="{y}" x2="{lx+34}" y2="{y}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>')
    legend.append(f'<text x="{lx+44}" y="{y+5}" style="{F};font-size:13px" fill="#17201c">{t}</text>')
notes = ["Vista desde arriba (lado de componentes).", "Placa perforada de 7 × 9 cm (rejilla 2.54 mm).",
         "Cables: usa cable aislado; los cruces", "no se tocan.", "Las tiras de la placa no se usan:", "cada unión es un cable o una soldadura.",
         "Los cables rojos gruesos llevan la", "corriente medida (hasta 300 mA)."]
for i, t in enumerate(notes):
    legend.append(f'<text x="{lx}" y="{OY + 300 + i*20}" style="{F};font-size:12.5px" fill="#40504a">{t}</text>')

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
       f'<text x="{OX-20}" y="40" style="{F};font-size:28px;font-weight:700" fill="#17201c">Montaje en placa perforada</text>',
       f'<text x="{OX-20}" y="64" style="{F};font-size:14px" fill="#56635d">Multímetro ESP32-C3 (OLED 0.42") · disposición sugerida de piezas y cables</text>']
svg += hole_grid() + draw + wires + padsvg + jacks + labels + legend + ["</svg>"]
open(OUT, "w", encoding="utf-8").write("\n".join(svg))
print("ok", W, H)
