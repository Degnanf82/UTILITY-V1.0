# Montaje en placa perforada v2: piezas junto a sus pines y cables trazados por un ruteador
# ortogonal sobre la rejilla (no pasan por debajo de los modulos, minimiza cruces).
import sys, math, heapq, json, os
OUT = sys.argv[1]

# Reutiliza las primitivas de dibujo de placa.py (todo lo anterior a "piezas").
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "placa.py"), encoding="utf-8").read()
exec(src[:src.index("# ------------------------------------------------------------------ piezas")].replace("OUT = sys.argv[1]", ""))

COLS, ROWS = 34, 46
OX, OY = 130, 190
KO = []   # celdas bloqueadas por cuerpos de piezas (c0, r0, c1, r1) inclusivo

def ko(c0, r0, c1, r1):
    KO.append((min(c0, c1), min(r0, r1), max(c0, c1), max(r0, r1)))

def R(c1, r1, c2, r2, n1, n2, bands, label, **kw):
    resistor(c1, r1, c2, r2, n1, n2, bands, label, **kw)
    if c1 == c2: ko(c1, min(r1, r2) + 1, c1, max(r1, r2) - 1)
    else: ko(min(c1, c2) + 1, r1, max(c1, c2) - 1, r1)

def D(ca, ra, ck, rk, na, nk, label, glass=False):
    diode(ca, ra, ck, rk, na, nk, label, glass)
    if ca == ck: ko(ca, min(ra, rk) + 1, ca, max(ra, rk) - 1)
    else: ko(min(ca, ck) + 1, ra, max(ca, ck) - 1, ra)

def Q(c, r, nets, label):
    to92(c, r, nets, label)
    ko(c, r - 1, c + 2, r - 1)

def K(c, r, nets, label):
    relay(c, r, nets, label)
    ko(c, r, c + 7, r + 4)

def SW(c, r, n1, n2, label):
    button(c, r, n1, n2, label)
    ko(c, r, c + 2, r + 2)

# ------------------------------------------------------------------ piezas
# Puntas (bornes) arriba a la izquierda
pad(0, 1, "PROBE_R", "punta ROJA"); pad(0, 9, "GND", "punta NEGRA")
# Reles
K(2, 2, ["PROBE_R", "+5V", "Q1C", "K2NC", "K2NO"], "K2 · mA")
K(14, 2, ["K2NC", "+5V", "Q2C", "V_IN", "K1NO"], "K1 · Ω")
# Driver de K2 (debajo de K2)
Q(3, 12, ["GND", "Q1B", "Q1C"], "Q1")
D(7, 12, 7, 9, "Q1C", "+5V", "D1", glass=True)
R(4, 14, 4, 18, "Q1B", "K2_DRV", "nnrn", "R1 1k")
R(2, 14, 2, 18, "Q1B", "GND", "nnon", "R2 10k", side="left")
# Driver de K1 (debajo de K1)
Q(15, 12, ["GND", "Q2B", "Q2C"], "Q2")
D(19, 12, 19, 9, "Q2C", "+5V", "D2", glass=True)
R(16, 14, 16, 18, "Q2B", "K1_DRV", "nnrn", "R3 1k")
R(14, 14, 14, 18, "Q2B", "GND", "nnon", "R4 10k", side="left")
# Fusible y shunt (entre los dos drivers)
pad(10, 8, "K2NO", "F1 arriba"); pad(10, 16, "I_SHUNT", "F1 abajo")
x1, y1 = xy(10, 8); x2, y2 = xy(10, 16)
draw.append(f'<rect x="{x1-12}" y="{y1-6}" width="24" height="{y2-y1+12}" rx="5" fill="#1e2023"/>'
            f'<rect x="{x1-8}" y="{y1+10}" width="16" height="{y2-y1-20}" rx="3" fill="#dcedf5" stroke="#8fb3c4"/>'
            f'<rect x="{x1-8}" y="{y1+10}" width="16" height="14" fill="#b8bcc2"/><rect x="{x1-8}" y="{y2-24}" width="16" height="14" fill="#b8bcc2"/>')
text(x1 + 18, (y1 + y2) / 2, "F1 315 mA", 11, anchor="start")
ko(10, 9, 10, 15)
R(10, 18, 10, 23, "I_SHUNT", "GND", None, "R_SH 1 Ω 1 W", big=True)
# Divisor de voltaje y frecuencia (arriba a la derecha)
R(23, 2, 27, 2, "V_IN", "V_ADC", "nngn", "R5 1M")
R(30, 2, 30, 6, "V_ADC", "GND", "nnyn", "R6 100k", side="left")
D(24, 4, 27, 4, "V_ADC", "+3V3", "D3")
D(24, 6, 27, 6, "GND", "V_ADC", "D4")
R(23, 8, 27, 8, "V_IN", "FREQ", "nnyn", "R7 100k")
D(24, 10, 27, 10, "FREQ", "+3V3", "D5")
D(24, 12, 27, 12, "GND", "FREQ", "D6")
D(25, 15, 29, 15, "GND", "+3V3", "DZ1 3.6V")
# PTC
pad(21, 9, "K1NO", "RT1 arriba"); pad(21, 11, "NODO_X", "RT1 abajo")
x, y = xy(21, 10)
draw.append(f'<line x1="{x}" y1="{y-P}" x2="{x}" y2="{y+P}" stroke="#9aa0a6" stroke-width="2.5"/><circle cx="{x}" cy="{y}" r="12" fill="#e8b100" stroke="#8a6a00"/>')
text(x + 16, y + 4, "RT1 PTC", 11, anchor="start")
ko(21, 10, 21, 10)
# Buzzer, Q3 y R18 (derecha, al medio)
x, y = xy(29.5, 20)
draw.append(f'<circle cx="{x}" cy="{y}" r="34" fill="#1e2023"/><circle cx="{x}" cy="{y}" r="6" fill="#55595e"/>')
text(x, y - 40, "BZ1", 11)
pad(28, 20, "BZ_N", "BZ1 −"); pad(31, 20, "+5V", "BZ1 +")
text(xy(31, 20)[0] + 8, xy(31, 20)[1] - 8, "+", 14, 700, "#ffffff", "start")
ko(29, 18, 30, 22); ko(28, 18, 28, 19); ko(31, 18, 31, 19)
Q(27, 25, ["GND", "Q3B", "BZ_N"], "Q3")
R(28, 27, 32, 27, "Q3B", "BUZ", "nnrn", "R18 1k")
# ESP32-C3 (USB hacia el borde inferior)
EL = ["REF_100K", "SENSE", "SDA", "SCL", "DESC", "K1_DRV", "REF_1M", "K2_DRV"]
ER = ["REF_1K", "REF_10K", None, "FREQ", "BUZ", "+3V3", "GND", "+5V"]
EC0, EC1, ER0 = 10, 17, 35
xa, ya = xy(EC0, ER0); xb, yb = xy(EC1, ER0 + 7)
draw.append(f'<rect x="{xa-14}" y="{ya-60}" width="{xb-xa+28}" height="{yb-ya+96}" rx="8" fill="#3b1f63" stroke="#24113f" stroke-width="1.5"/>')
draw.append(f'<rect x="{xa+32}" y="{ya-8}" width="{xb-xa-64}" height="{3*P}" rx="3" fill="#0d1030" stroke="#9aa0a6" stroke-width="2"/>')
text((xa + xb) / 2, ya + 28, "OLED", 11, 700, "#8fb8ff")
draw.append(f'<rect x="{(xa+xb)/2-26}" y="{yb+18}" width="52" height="34" rx="6" fill="#b9bec4"/>')
text((xa + xb) / 2, ya + 5.3 * P, "ESP32-C3", 13, 700, "#ffffff")
for i, n in enumerate(EL):
    pad(EC0, ER0 + i, n, "ESP pin " + ["3", "4", "5", "6", "7", "8", "9", "10"][i])
    text(xy(EC0, ER0 + i)[0] + 12, xy(EC0, ER0 + i)[1] + 4, ["3", "4", "5", "6", "7", "8", "9", "10"][i], 9, 700, "#ffffff", "start")
for i, n in enumerate(ER):
    pad(EC1, ER0 + i, n or "NC", "ESP pin " + ["0", "1", "2", "TX", "RX", "V3", "GD", "V5"][i])
    text(xy(EC1, ER0 + i)[0] - 12, xy(EC1, ER0 + i)[1] + 4, ["0", "1", "2", "TX", "RX", "V3", "GD", "V5"][i], 9, 700, "#ffffff", "end")
ko(EC0, ER0 - 3, EC1, ROWS - 1)
# Nodo X: referencias junto a los pines izquierdos; tira comun en la columna 1
R(3, 35, 7, 35, "NODO_X", "REF_100K", "nnyn", "R10 100k")
R(3, 36, 7, 36, "NODO_X", "SENSE", "nnrn", "R14 1k")
R(3, 39, 7, 39, "NODO_X", "DESC", "rrnu", "R12 220")
R(3, 41, 7, 41, "NODO_X", "REF_1M", "nngn", "R11 1M")
R(19, 35, 23, 35, "REF_1K", "NODO_X", "nnrn", "R8 1k")
R(19, 36, 23, 36, "REF_10K", "NODO_X", "nnon", "R9 10k")
R(3, 33, 7, 33, "NODO_X", "X_ADC", "nnrn", "R13 1k")
D(1, 44, 4, 44, "NODO_X", "+3V3", "D7")
D(5, 44, 8, 44, "GND", "NODO_X", "D8")
# ADS1115 con la cabecera hacia arriba (fila 25) y el cuerpo debajo
AC0, AR = 12, 25
xa, ya = xy(AC0, AR)
draw.append(f'<rect x="{xa-14}" y="{ya-12}" width="{9*P+28}" height="{5*P+24}" rx="6" fill="#1c5aa6" stroke="#0f3a72"/>')
text(xa + 4.5 * P, ya + 4.2 * P, "ADS1115", 14, 700, "#ffffff")
text(xa + 4.5 * P, ya + 4.9 * P, "(montado con los pines hacia arriba)", 9, 500, "#cfe0ff")
for i, (nm, n) in enumerate(zip(["VDD", "GND", "SCL", "SDA", "ADDR", "ALRT", "A0", "A1", "A2", "A3"],
                                ["+3V3", "GND", "SCL", "SDA", "GND", "NC", "V_ADC", "X_ADC", "I_SHUNT", "BTN"])):
    pad(AC0 + i, AR, n, "ADS " + nm)
    x, y = xy(AC0 + i, AR)
    text(x + 4, y + 12, nm, 9, 700, "#ffffff", "end", rot=-90)
ko(AC0, AR + 1, AC0 + 9, AR + 5)
# C1 104 encima de VDD/GND
pad(12, 23, "+3V3", "C1 izq."); pad(14, 23, "GND", "C1 der.")
x, y = xy(13, 23)
draw.append(f'<rect x="{x-10}" y="{y-8}" width="20" height="16" rx="5" fill="#e0a33a"/>')
text(x, y - 12, "C1 104", 10)
ko(13, 23, 13, 23)
# Botones (abajo a la derecha) con su escalera
R(24, 33, 28, 33, "+3V3", "BTN", "nnon", "R15 10k")
SW(21, 39, "BTN", "GND", "MODO")
R(26, 35, 26, 39, "BTN", "BTN_H", "nnon", "R16 10k", side="left")
SW(25, 40, "BTN_H", "GND", "HOLD")
R(30, 35, 30, 39, "BTN", "BTN_R", "ooon", "R17 33k", side="left")
SW(29, 40, "BTN_R", "GND", "REL")

# ------------------------------------------------------------------ ruteador
# Rejilla de medio paso: los pads estan en coordenadas pares; los cables pueden ir entre agujeros.
S = 2
GC, GR = COLS * S - 1, ROWS * S - 1
padnet = {}
paddesc = {}
for c, r, n, d in pads:
    padnet[(c * S, r * S)] = n
    paddesc[(c * S, r * S)] = d
blocked = set()
for c0, r0, c1, r1 in KO:
    for c in range(c0 * S - 1, c1 * S + 2):
        for r in range(r0 * S - 1, r1 * S + 2):
            if (c, r) not in padnet:
                blocked.add((c, r))
# salida libre: las celdas vecinas de cada pad solo las puede usar la red del pad
exitnet = {}
for (pc, pr), n in padnet.items():
    for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        cell = (pc + dc, pr + dr)
        if cell in padnet: continue
        exitnet.setdefault(cell, n)
        if exitnet[cell] != n: exitnet[cell] = None   # compartida por dos pads: libre para ambos
POWER = ("GND", "+5V", "+3V3")
LAYERS = {"top": ({}, {}, {}), "bot": ({}, {}, {})}
H, V, NODE = LAYERS["top"]
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def chan(d):
    return H if d[1] == 0 else V

BOTTOM = False
def enterable(cell, net):
    if cell in padnet: return padnet[cell] == net
    if cell in exitnet and exitnet[cell] not in (None, net): return False
    if not BOTTOM and cell in blocked and exitnet.get(cell, "#") not in (net, None): return False
    if cell in NODE and NODE[cell] != net: return False
    return True

def route_net(net, terms):
    terms = [(c * S, r * S) for c, r in terms]
    tree = {terms[0]}
    NODE[terms[0]] = net
    left = set(terms[1:])
    paths = []
    while left:
        pq = []
        best = {}
        for cell in tree:
            for d in DIRS:
                best[(cell, d)] = 0
                heapq.heappush(pq, (0, cell, d))
        prev = {}
        found = None
        while pq:
            cost, cell, d = heapq.heappop(pq)
            if best.get((cell, d), 1e9) < cost: continue
            if cell in left:
                found = (cell, d); break
            for nd in DIRS:
                if nd == (-d[0], -d[1]): continue
                nxt = (cell[0] + nd[0], cell[1] + nd[1])
                if not (0 <= nxt[0] <= GC and 0 <= nxt[1] <= GR): continue
                if cell not in tree:
                    if nd != d:
                        if H.get(cell, net) != net or V.get(cell, net) != net: continue
                    elif chan(nd).get(cell, net) != net: continue
                else:
                    if chan(nd).get(cell, net) != net: continue
                if not enterable(nxt, net): continue
                if chan(nd).get(nxt, net) != net: continue
                if nxt in padnet and nxt not in left and nxt not in tree: continue
                step = 1.0
                if cell not in tree and nd != d: step += 1.2
                other = V if nd[1] == 0 else H
                if nxt in other and other[nxt] != net: step += 10.0
                # preferir las lineas de agujeros (coordenadas pares) para que se vea ordenado
                if (nxt[0] % 2 and nd[1] != 0) or (nxt[1] % 2 and nd[0] != 0): step += 0.15
                nc = cost + step
                if nc < best.get((nxt, nd), 1e9):
                    best[(nxt, nd)] = nc
                    prev[(nxt, nd)] = (cell, d)
                    heapq.heappush(pq, (nc, nxt, nd))
        if not found:
            return paths, left
        path = [found]
        while path[-1] in prev:
            path.append(prev[path[-1]])
        path.reverse()
        cells = [p[0] for p in path]
        for i in range(len(cells) - 1):
            a2, b2 = cells[i], cells[i + 1]
            d = (b2[0] - a2[0], b2[1] - a2[1])
            ch = chan(d); ch[a2] = net; ch[b2] = net
        for i, cell in enumerate(cells):
            if i == 0 or i == len(cells) - 1:
                NODE[cell] = net
            else:
                a2, b2 = cells[i - 1], cells[i + 1]
                if a2[0] != b2[0] and a2[1] != b2[1]:
                    H[cell] = net; V[cell] = net
        paths.append(cells)
        tree.update(cells)
        left.discard(cells[-1])
    return paths, set()

nets = {}
for c, r, n, d in pads:
    if n == "NC": continue
    nets.setdefault(n, []).append((c, r))
def span(n):
    pts = nets[n]
    return (max(p[0] for p in pts) - min(p[0] for p in pts)) + (max(p[1] for p in pts) - min(p[1] for p in pts))
import random
def run(order):
    global H, V, NODE, BOTTOM
    for L in LAYERS.values():
        for d in L: d.clear()
    routes, failed = {}, {}
    for n in order:
        lay = "bot" if n in POWER else "top"
        H, V, NODE = LAYERS[lay]
        BOTTOM = lay == "bot"
        paths, left = route_net(n, nets[n])
        routes[n] = paths
        if left: failed[n] = left
    Ht, Vt, _ = LAYERS["top"]
    cross = sum(1 for c in Ht if c in Vt and Ht[c] != Vt[c])
    return routes, failed, cross, None
base = [n for n in nets if len(nets[n]) > 1]
PRIO = {"SDA": 0, "SCL": 0, "GND": 1, "+5V": 2, "+3V3": 3}
orders = [sorted(base, key=lambda n: (PRIO.get(n, 4), span(n))),
          sorted(base, key=lambda n: span(n)),
          sorted(base, key=lambda n: (PRIO.get(n, 4), -span(n)))]
rng = random.Random(7)
for _ in range(30):
    o = base[:]; rng.shuffle(o); o.sort(key=lambda n: PRIO.get(n, 4)); orders.append(o)
best = None
for i, o in enumerate(orders):
    routes, failed, cross, st = run(o)
    nf = sum(len(v) for v in failed.values())
    score = (nf, cross)
    if best is None or score < best[0]:
        best = (score, o, routes, failed, st)
    if nf == 0 and cross <= 25: break
(score, order, routes, failed, st) = best
print("mejor: faltan", score[0], "cruces", score[1], {k: len(v) for k, v in failed.items()})

# ------------------------------------------------------------------ dibujo de cables
COL = {"+5V": "#e8590c", "+3V3": "#d22a3f", "GND": "#1d2421", "SDA": "#e0a100", "SCL": "#1d64c8"}
PALETA = ["#2e7d32", "#7b1fa2", "#00838f", "#8d6e63", "#0d47a1", "#9e9d24", "#d81b60", "#004d40", "#e65100",
          "#5e35b1", "#827717", "#0288d1", "#ad1457", "#00bfa5", "#6d4c41", "#3949ab", "#c62828", "#f9a825",
          "#4e342e", "#26a69a", "#ab47bc", "#558b2f", "#1e88e5", "#ff7043", "#546e7a", "#7cb342"]
k = 0
for n in sorted(routes):
    if n not in COL:
        COL[n] = PALETA[k % len(PALETA)]; k += 1

def sxy(c):
    return OX + c[0] * P / S, OY + c[1] * P / S

def poly(cells):
    pts = [sxy(c) for c in cells]
    # simplificar puntos colineales
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = out[-1], pts[i], pts[i + 1]
        if (b[0] - a[0]) * (c[1] - b[1]) != (b[1] - a[1]) * (c[0] - b[0]):
            out.append(b)
    out.append(pts[-1])
    # esquinas redondeadas
    d = f"M{out[0][0]},{out[0][1]}"
    for i in range(1, len(out) - 1):
        a, b, c = out[i - 1], out[i], out[i + 1]
        r = 7
        ux, uy = (b[0] - a[0]), (b[1] - a[1]); L1 = math.hypot(ux, uy); ux, uy = ux / L1, uy / L1
        vx, vy = (c[0] - b[0]), (c[1] - b[1]); L2 = math.hypot(vx, vy); vx, vy = vx / L2, vy / L2
        d += f" L{b[0]-ux*r:.1f},{b[1]-uy*r:.1f} Q{b[0]},{b[1]} {b[0]+vx*r:.1f},{b[1]+vy*r:.1f}"
    d += f" L{out[-1][0]},{out[-1][1]}"
    return d

wires = []
junctions = []
CORTO = {"PROBE_R": "ROJA", "K2NC": "K2→K1", "K2NO": "K2→F1", "I_SHUNT": "A2", "V_IN": "VIN", "K1NO": "K1→PTC",
         "V_ADC": "A0", "FREQ": "TX", "NODO_X": "NODO X", "X_ADC": "A1", "SENSE": "IO4", "REF_1K": "IO0", "REF_10K": "IO1",
         "REF_100K": "IO3", "REF_1M": "IO9", "DESC": "IO7", "K1_DRV": "IO8", "K2_DRV": "IO10", "Q1B": "B·Q1", "Q2B": "B·Q2",
         "Q1C": "C·Q1", "Q2C": "C·Q2", "BUZ": "RX", "Q3B": "B·Q3", "BZ_N": "BZ−", "BTN": "A3", "BTN_H": "HOLD", "BTN_R": "REL",
         "SDA": "SDA", "SCL": "SCL"}
chips = []
def chip_on(cells, n):
    # tramo recto mas largo del camino
    best_seg, cur = None, [cells[0]]
    segs = []
    for i in range(1, len(cells)):
        if len(cur) >= 2 and (cells[i][0] - cur[-1][0], cells[i][1] - cur[-1][1]) != (cur[1][0] - cur[0][0], cur[1][1] - cur[0][1]):
            segs.append(cur); cur = [cur[-1]]
        cur.append(cells[i])
    segs.append(cur)
    seg = max(segs, key=len)
    if len(seg) < 6: return
    a, b = sxy(seg[0]), sxy(seg[-1])
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    t = CORTO.get(n, n)
    w = len(t) * 6.4 + 10
    chips.append(f'<rect x="{mx-w/2:.1f}" y="{my-8:.1f}" width="{w:.1f}" height="16" rx="8" fill="#ffffff" stroke="{COL[n]}" stroke-width="2"/>'
                 f'<text x="{mx:.1f}" y="{my+4:.1f}" text-anchor="middle" style="{F};font-size:10px;font-weight:800" fill="{COL[n]}">{t}</text>')
under = []
for n in order:
    for cells in routes.get(n, []):
        dpath = poly(cells)
        if n in POWER:
            under.append(f'<path d="{dpath}" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0.7"/>'
                         f'<path d="{dpath}" fill="none" stroke="{COL[n]}" stroke-width="3.4" stroke-dasharray="7 5" stroke-linecap="round" stroke-linejoin="round"/>')
            continue
        wires.append(f'<path d="{dpath}" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="{dpath}" fill="none" stroke="{COL[n]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
        chip_on(cells, n)
        if cells[0] not in padnet:
            x, y = sxy(cells[0])
            junctions.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{COL[n]}" stroke="#fff" stroke-width="1.5"/>')

padsvg = []
for c, r, n, _d in pads:
    x, y = xy(c, r)
    padsvg.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#c9a227" stroke="#6b4a22" stroke-width="1"/>')

# Puntas fuera de la placa
jx, jy = xy(0, 1); kx, ky = xy(0, 9)
jacks = [f'<line x1="{jx-56}" y1="{jy}" x2="{jx}" y2="{jy}" stroke="#c62828" stroke-width="5"/><circle cx="{jx-70}" cy="{jy}" r="16" fill="#c62828"/><circle cx="{jx-70}" cy="{jy}" r="5" fill="#111"/>',
         f'<line x1="{kx-56}" y1="{ky}" x2="{kx}" y2="{ky}" stroke="#1d2421" stroke-width="5"/><circle cx="{kx-70}" cy="{ky}" r="16" fill="#1d2421"/><circle cx="{kx-70}" cy="{ky}" r="5" fill="#666"/>']
text(jx - 70, jy - 24, "ROJA", 11, 700, "#c62828")
text(kx - 70, ky - 24, "COM", 11, 700, "#1d2421")

# Leyenda: una linea por red con su color y a donde conecta
W = OX * 2 + COLS * P + 380
H_ = OY + ROWS * P + 60
legend = []
lx = OX + COLS * P + 30
legend.append(f'<text x="{lx}" y="{OY - 6}" style="{F};font-size:15px;font-weight:800" fill="#17201c">Colores de cable</text>')
NOMBRES = {"+5V": "+5V", "+3V3": "+3.3V", "GND": "GND", "SDA": "SDA (ESP 5 – ADS)", "SCL": "SCL (ESP 6 – ADS)",
           "PROBE_R": "punta roja → K2", "K2NC": "K2 NC → K1 COM", "K2NO": "K2 NO → fusible", "I_SHUNT": "shunt → ADS A2",
           "V_IN": "K1 NC → divisor", "K1NO": "K1 NO → PTC", "V_ADC": "divisor → ADS A0", "FREQ": "frecuencia → ESP TX",
           "NODO_X": "NODO X", "X_ADC": "nodo X → ADS A1", "SENSE": "ESP 4 (lectura)", "REF_1K": "ESP 0 → R8",
           "REF_10K": "ESP 1 → R9", "REF_100K": "ESP 3 → R10", "REF_1M": "ESP 9 → R11", "DESC": "ESP 7 → R12",
           "K1_DRV": "ESP 8 → R3 (K1)", "K2_DRV": "ESP 10 → R1 (K2)", "Q1B": "base Q1", "Q2B": "base Q2", "Q1C": "colector Q1",
           "Q2C": "colector Q2", "BUZ": "ESP RX → R18", "Q3B": "base Q3", "BZ_N": "buzzer −", "BTN": "botones → ADS A3",
           "BTN_H": "R16 → HOLD", "BTN_R": "R17 → REL"}
row = 0
for n in ["+5V", "+3V3", "GND", "SDA", "SCL"] + sorted(k2 for k2 in routes if k2 not in ("+5V", "+3V3", "GND", "SDA", "SCL")):
    if n not in routes: continue
    y = OY + 18 + row * 24
    if n in POWER:
        legend.append(f'<line x1="{lx}" y1="{y}" x2="{lx+30}" y2="{y}" stroke="{COL[n]}" stroke-width="4" stroke-dasharray="7 5"/>')
        legend.append(f'<text x="{lx+40}" y="{y+5}" style="{F};font-size:12.5px" fill="#17201c">{NOMBRES.get(n, n)} (por debajo)</text>')
    else:
        legend.append(f'<line x1="{lx}" y1="{y}" x2="{lx+30}" y2="{y}" stroke="{COL[n]}" stroke-width="6" stroke-linecap="round"/>')
        legend.append(f'<text x="{lx+40}" y="{y+5}" style="{F};font-size:12.5px" fill="#17201c"><tspan font-weight="800" fill="{COL[n]}">{CORTO.get(n, n)}</tspan>  {NOMBRES.get(n, n)}</text>')
    row += 1
notes = ["Punteado = cable por debajo (lado de", "soldadura): GND, +3.3V y +5V.", "Vista desde arriba (lado de piezas).", "Placa perforada de 9 × 12 cm, rejilla 2.54 mm.",
         "Los cables van por encima de la placa,", "nunca por debajo de los módulos.",
         "Un cable que pasa sobre otro NO se", "conecta: solo se une donde hay un punto.",
         "Usa cable aislado (cable de red).", "Q1–Q3: S9014 · C1: cerámico 104."]
for i, t in enumerate(notes):
    legend.append(f'<text x="{lx}" y="{OY + 40 + row * 24 + i * 19}" style="{F};font-size:12.5px" fill="#40504a">{t}</text>')

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_}" width="{W}" height="{H_}">',
       f'<rect width="{W}" height="{H_}" fill="#ffffff"/>',
       f'<text x="{OX-20}" y="44" style="{F};font-size:30px;font-weight:700" fill="#17201c">Montaje en placa perforada</text>',
       f'<text x="{OX-20}" y="70" style="{F};font-size:14px" fill="#56635d">Multímetro ESP32-C3 (OLED 0.42") · v1.3 · cada pieza junto al pin al que se conecta · cables rectos sin pasar bajo los módulos</text>']
svg += hole_grid() + under + draw + wires + junctions + padsvg + jacks + labels + chips + legend + ["</svg>"]
open(OUT, "w", encoding="utf-8").write("\n".join(svg))
print("ok", W, H_)
