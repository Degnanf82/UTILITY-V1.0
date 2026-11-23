"""Genera Gerber RS-274X + Excellon (formato JLCPCB/PCBWay) a partir de board.py y route.json."""
import json, math, os, sys, zipfile
from HersheyFonts import HersheyFonts
from board import P, W, H, all_pads, MODULES, ESPX, ESPY, ADSX, ADSY, OLEDX, OLEDY
from route import VIA_D, VIA_DRILL

OUT = sys.argv[1] if len(sys.argv) > 1 else "../gerber"
os.makedirs(OUT, exist_ok=True)
NAME = "multimetro_esp32c3"
route = json.load(open("route.json"))
pads = all_pads()
MASK_EXP = 0.05

def gy(y): return H - y                      # Gerber: Y hacia arriba
def C(v): return int(round(v * 1e6))

class Gerber:
    def __init__(self, func, polarity="Positive"):
        self.apt = {}; self.body = []; self.func = func; self.pol = polarity; self.cur = None
    def ap(self, key):
        if key not in self.apt:
            self.apt[key] = 10 + len(self.apt)
        d = self.apt[key]
        if self.cur != d:
            self.body.append(f"D{d}*"); self.cur = d
    def flash(self, key, x, y):
        self.ap(key); self.body.append(f"X{C(x)}Y{C(gy(y))}D03*")
    def line(self, w, pts):
        self.ap(("C", round(w, 3)))
        x0, y0 = pts[0]
        self.body.append(f"X{C(x0)}Y{C(gy(y0))}D02*")
        for x, y in pts[1:]:
            self.body.append(f"X{C(x)}Y{C(gy(y))}D01*")
    def write(self, path):
        out = ["%TF.GenerationSoftware,multimetro-pcb,script,1.0*%", f"%TF.FileFunction,{self.func}*%",
               f"%TF.FilePolarity,{self.pol}*%", "%FSLAX46Y46*%", "%MOMM*%", "%LPD*%", "G01*"]
        for key, d in self.apt.items():
            if key[0] == "C": out.append(f"%ADD{d}C,{key[1]:.4f}*%")
            elif key[0] == "R": out.append(f"%ADD{d}R,{key[1]:.4f}X{key[2]:.4f}*%")
            elif key[0] == "O": out.append(f"%ADD{d}O,{key[1]:.4f}X{key[2]:.4f}*%")
        out += self.body + ["M02*"]
        open(path, "w").write("\n".join(out) + "\n")

def pad_key(p, grow=0.0):
    w, h = round(p["w"] + 2 * grow, 3), round(p["h"] + 2 * grow, 3)
    if p["shape"] == "circle": return ("C", max(w, h))
    if p["shape"] == "oval": return ("O", w, h)
    return ("R", w, h)

# ------------------------------------------------------------------ cobre y mascara
cu = [Gerber("Copper,L1,Top"), Gerber("Copper,L2,Bot")]
mask = [Gerber("Soldermask,Top", "Negative"), Gerber("Soldermask,Bot", "Negative")]
for p in pads:
    if p["kind"] == "thru_hole":
        for l in (0, 1):
            cu[l].flash(pad_key(p), p["x"], p["y"])
            mask[l].flash(pad_key(p, MASK_EXP), p["x"], p["y"])
    elif p["kind"] == "np_thru_hole":
        for l in (0, 1):
            mask[l].flash(("C", p["drill"][0] + 0.2), p["x"], p["y"])
for t in route["tracks"]:
    cu[t["layer"]].line(t["w"], t["pts"])
for v in route["vias"]:
    for l in (0, 1):
        cu[l].flash(("C", VIA_D), v["x"], v["y"])          # vias tapadas con mascara

# ------------------------------------------------------------------ serigrafia
silk = Gerber("Legend,Top")
SW = 0.15
font = HersheyFonts(); font.load_default_font("futural")

def text(s, x, y, h=1.0, anchor="middle", rot=0, w=SW):
    font.normalize_rendering(h)
    segs = list(font.lines_for_text(s))
    if not segs: return
    xs = [a[0] for sgm in segs for a in sgm]; ys = [a[1] for sgm in segs for a in sgm]
    tw = max(xs) - min(xs)
    ox = {"start": 0, "middle": -tw / 2, "end": -tw}[anchor] - min(xs)
    oy = -h / 2
    r = math.radians(rot)
    for (x1, y1), (x2, y2) in segs:
        pts = []
        for px, py in ((x1, y1), (x2, y2)):
            lx, ly = px + ox, py + oy                    # y de la fuente hacia arriba
            rx = lx * math.cos(r) - ly * math.sin(r)
            ry = lx * math.sin(r) + ly * math.cos(r)
            pts.append((x + rx, y - ry))
        silk.line(w, pts)

def arc3(x1, y1, xm, ym, x2, y2, n=16):
    ax, ay, bx, by, cx, cy = x1, y1, xm, ym, x2, y2
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9: return [(x1, y1), (x2, y2)]
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    a1, am, a2 = (math.atan2(p[1] - uy, p[0] - ux) for p in ((ax, ay), (bx, by), (cx, cy)))
    def norm(a): return a % (2 * math.pi)
    ccw = norm(am - a1) < norm(a2 - a1)
    span = norm(a2 - a1) if ccw else -norm(a1 - a2)
    return [(ux + r * math.cos(a1 + span * i / n), uy + r * math.sin(a1 + span * i / n)) for i in range(n + 1)]

for part in P:
    for g in part.silk():
        if g[0] == "line": silk.line(max(g[5], SW), [(g[1], g[2]), (g[3], g[4])])
        elif g[0] == "circle":
            pts = [(g[1] + g[3] * math.cos(2 * math.pi * i / 36), g[2] + g[3] * math.sin(2 * math.pi * i / 36)) for i in range(37)]
            silk.line(max(g[4], SW), pts)
        elif g[0] == "arc": silk.line(max(g[7], SW), arc3(*g[1:7]))

# contornos de modulos
for name, x0, y0, x1, y1 in MODULES:
    silk.line(SW, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])
text("ESP32-C3 OLED 0.42\"", (MODULES[0][1] + MODULES[0][3]) / 2, ESPY - 3.6, 1.1)
text("USB", (MODULES[0][1] + MODULES[0][3]) / 2, MODULES[0][4] - 1.6, 1.0)
silk.line(SW, [((MODULES[0][1] + MODULES[0][3]) / 2 - 1, MODULES[0][4] - 0.5), ((MODULES[0][1] + MODULES[0][3]) / 2, MODULES[0][4] + 0.4),
               ((MODULES[0][1] + MODULES[0][3]) / 2 + 1, MODULES[0][4] - 0.5)])
for i, t in enumerate(["3", "4", "5", "6", "7", "8", "9", "10"]):
    text(t, ESPX + 1.6, ESPY + i * 2.54, 0.9, "start")
for i, t in enumerate(["0", "1", "2", "TX", "RX", "V3", "GD", "V5"]):
    text(t, ESPX + 17.78 - 1.6, ESPY + i * 2.54, 0.9, "end")
text("ADS1115: cuerpo hacia abajo", ADSX + 9.0, ADSY - 2.9, 1.0)
for i, t in enumerate(["A3", "A2", "A1", "A0", "ALRT", "ADDR", "SDA", "SCL", "GND", "VDD"]):
    text(t, ADSX + i * 2.54, ADSY + 1.7, 0.8, "end", rot=90)

# referencias y valores
SKIP = {"U1L", "U1R", "U2", "U3", "H1", "H2", "H3", "H4"}
NODEX = {"R8", "R9", "R10", "R11", "R12", "R13", "R14"}
for part in P:
    if part.ref in SKIP: continue
    bb = part.courtyard()
    lbl = f"{part.ref} {part.value}".strip()
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    if part.ref.startswith("SW"):
        text(part.value, cx, bb[3] + 0.9, 1.1); continue
    if part.ref == "J3":
        text("ROJA", part.x, bb[3] + 0.9, 1.0); text("COM", part.x + 5.08, bb[3] + 0.9, 1.0); continue
    if part.ref.startswith("K"):
        text(part.ref + (" mA" if part.ref == "K2" else " Ohm"), part.x + 8.0, part.y - 4.0, 1.1); continue
    if part.ref.startswith("Q"):
        text(part.ref + " " + part.value, part.x + 2.54, part.y + 2.3, 0.9)
        for k, t in enumerate("EBC"): text(t, part.x + k * 2.54, part.y - 1.6, 0.7)
        continue
    if part.ref == "BZ1":
        text("BZ1", cx, cy, 1.1); text("+", part.x, part.y - 2.2, 1.2); continue
    if part.ref in NODEX:
        text(lbl, part.x + 10.16 + 1.3, part.y, 0.8, "start"); continue
    if part.ref == "RSH":
        text(lbl, cx, bb[3] + 0.7, 0.85); continue
    if part.ref == "R3":
        text(lbl, bb[0] - 0.6, cy, 0.85, "middle", rot=90); continue
    if bb[2] - bb[0] >= bb[3] - bb[1]:
        text(lbl, cx, bb[1] - 0.6, 0.85)
    else:
        if bb[2] + 2.0 > W - 1.0:
            text(lbl, bb[0] - 0.6, cy, 0.85, "middle", rot=90)
        else:
            text(lbl, bb[2] + 0.6, cy, 0.85, "middle", rot=90)

text("DEGNANTECH", 41.0, 93.6, 2.2, w=0.25)
text("MULTIMETRO ESP32-C3  v1.0", 41.0, 96.3, 1.1)
text("max 40V DC / 300mA - NO MEDIR LA RED", 41.0, 98.1, 0.8)
# OLED 0.96" opcional
for i, t in enumerate(["VCC", "GND", "SCL", "SDA"]):
    text(t, OLEDX + i * 2.54, OLEDY + 2.4, 0.8)
text("OLED 0.96\" opcional (0x3D)", OLEDX - 2.2, OLEDY, 0.85, "end")

# ------------------------------------------------------------------ contorno
edge = Gerber("Profile,NP")
edge.line(0.1, [(0, 0), (W, 0), (W, H), (0, H), (0, 0)])

# ------------------------------------------------------------------ taladros
def excellon(holes, path, plated):
    tools = {}
    for x, y, d in holes:
        tools.setdefault(round(d, 3), []).append((x, y))
    out = ["M48", "; multimetro ESP32-C3", "; FORMAT={-:-/ 3:3/ absolute / metric / decimal}",
           f"; #@! TF.FileFunction,{'Plated,1,2,PTH' if plated else 'NonPlated,1,2,NPTH'}", "FMAT,2", "METRIC"]
    for i, d in enumerate(sorted(tools), 1):
        out.append(f"T{i}C{d:.3f}")
    out.append("%")
    out.append("G90"); out.append("G05")
    for i, d in enumerate(sorted(tools), 1):
        out.append(f"T{i}")
        for x, y in tools[d]:
            out.append(f"X{x:.3f}Y{gy(y):.3f}")
    out.append("M30")
    open(path, "w").write("\n".join(out) + "\n")

pth = [(p["x"], p["y"], p["drill"][0]) for p in pads if p["kind"] == "thru_hole"]
pth += [(v["x"], v["y"], VIA_DRILL) for v in route["vias"]]
npth = [(p["x"], p["y"], p["drill"][0]) for p in pads if p["kind"] == "np_thru_hole"]

files = {
    f"{NAME}-F_Cu.gtl": cu[0], f"{NAME}-B_Cu.gbl": cu[1],
    f"{NAME}-F_Mask.gts": mask[0], f"{NAME}-B_Mask.gbs": mask[1],
    f"{NAME}-F_Silkscreen.gto": silk, f"{NAME}-Edge_Cuts.gm1": edge,
}
for fn, g in files.items():
    g.write(os.path.join(OUT, fn))
excellon(pth, os.path.join(OUT, f"{NAME}-PTH.drl"), True)
excellon(npth, os.path.join(OUT, f"{NAME}-NPTH.drl"), False)
zp = os.path.join(os.path.dirname(OUT), f"{NAME}_gerbers_JLCPCB.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir(OUT)):
        z.write(os.path.join(OUT, fn), fn)
print("ok", zp, len(pth), "agujeros PTH", len(npth), "NPTH")
