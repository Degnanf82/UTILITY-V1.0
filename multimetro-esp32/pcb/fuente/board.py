"""Multimetro ESP32-C3 v1.3: colocacion de piezas y lista de conexiones de la PCB (mm, y hacia abajo)."""
import math, os
from kmod import load

FP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fp")
W, H = 84.0, 100.0           # tamano de la placa

FOOT = {
    "R": "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
    "R1W": "R_Axial_DIN0414_L11.9mm_D4.5mm_P15.24mm_Horizontal",
    "D35": "D_DO-35_SOD27_P7.62mm_Horizontal",
    "D41": "D_DO-41_SOD81_P10.16mm_Horizontal",
    "C25": "C_Disc_D3.0mm_W2.0mm_P2.50mm",
    "C50": "C_Disc_D5.0mm_W2.5mm_P5.00mm",
    "TO92": "TO-92_Inline_Wide",
    "RELAY": "Relay_SPDT_SANYOU_SRD_Series_Form_C",
    "FUSE": "Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal",
    "SW": "SW_PUSH_6mm",
    "BUZ": "Buzzer_12x9.5RM7.6",
    "TB2": "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal",
    "S8": "PinSocket_1x08_P2.54mm_Vertical",
    "S10": "PinSocket_1x10_P2.54mm_Vertical",
    "S4": "PinSocket_1x04_P2.54mm_Vertical",
    "MH": "MountingHole_3.2mm_M3",
}
_cache = {}
def footprint(key):
    if key not in _cache:
        _cache[key] = load(os.path.join(FP, FOOT[key] + ".kicad_mod"))
    return _cache[key]

def rot_pt(x, y, rot):
    r = rot % 360
    if r == 0: return x, y
    if r == 90: return -y, x
    if r == 180: return -x, -y
    if r == 270: return y, -x
    a = math.radians(r); return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)

class Part:
    def __init__(self, ref, key, x, y, rot, nets, value="", label_pos=None):
        self.ref, self.key, self.x, self.y, self.rot = ref, key, x, y, rot
        self.nets, self.value, self.label_pos = nets, value, label_pos

    def pads(self):
        pads, _ = footprint(self.key)
        out = []
        for p in pads:
            px, py = rot_pt(p["x"], p["y"], self.rot)
            w, h = p["w"], p["h"]
            if (self.rot + p["rot"]) % 180 == 90: w, h = h, w
            out.append(dict(ref=self.ref, num=p["num"], x=self.x + px, y=self.y + py, w=w, h=h,
                            shape=p["shape"], drill=p["drill"], kind=p["kind"],
                            net=self.nets.get(p["num"], None) if p["kind"] == "thru_hole" else None))
        return out

    def courtyard(self):
        from kmod import courtyard
        bb = courtyard(os.path.join(FP, FOOT[self.key] + ".kicad_mod"))
        if not bb: return None
        pts = [rot_pt(x, y, self.rot) for x, y in ((bb[0], bb[1]), (bb[2], bb[3]))]
        xs = [self.x + p[0] for p in pts]; ys = [self.y + p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def silk(self):
        _, silk = footprint(self.key)
        out = []
        for g in silk:
            if g[0] == "line":
                x1, y1 = rot_pt(g[1], g[2], self.rot); x2, y2 = rot_pt(g[3], g[4], self.rot)
                out.append(("line", self.x + x1, self.y + y1, self.x + x2, self.y + y2, g[5]))
            elif g[0] == "circle":
                cx, cy = rot_pt(g[1], g[2], self.rot)
                out.append(("circle", self.x + cx, self.y + cy, g[3], g[4]))
            elif g[0] == "arc":
                pts = [rot_pt(g[1], g[2], self.rot), rot_pt(g[3], g[4], self.rot), rot_pt(g[5], g[6], self.rot)]
                out.append(("arc", self.x + pts[0][0], self.y + pts[0][1], self.x + pts[1][0], self.y + pts[1][1],
                            self.x + pts[2][0], self.y + pts[2][1], g[7]))
        return out

P = []
def add(*a, **k):
    P.append(Part(*a, **k)); return P[-1]

def R(ref, x, y, rot, n1, n2, val):      return add(ref, "R", x, y, rot, {"1": n1, "2": n2}, val)
def Dd(ref, x, y, rot, k, a, val, key="D35"): return add(ref, key, x, y, rot, {"1": k, "2": a}, val)   # pad 1 = catodo

# ---------------- puntas y reles
add("J3", "TB2", 9.0, 7.5, 0, {"1": "PROBE_R", "2": "GND"}, "PUNTAS")
add("K2", "RELAY", 8.0, 23.0, 0, {"1": "PROBE_R", "2": "+5V", "5": "Q1C", "3": "K2NO", "4": "K2NC"}, "SRD-05VDC (mA)")
add("K1", "RELAY", 33.0, 23.0, 0, {"1": "K2NC", "2": "+5V", "5": "Q2C", "3": "K1NO", "4": "V_IN"}, "SRD-05VDC (Ohm)")
# ---------------- drivers de las bobinas
add("Q1", "TO92", 7.0, 38.0, 0, {"1": "GND", "2": "Q1B", "3": "Q1C"}, "S9014")
Dd("D1", 16.5, 33.5, 90, "+5V", "Q1C", "1N4148")
R("R1", 11.0, 42.0, 90, "Q1B", "K2_DRV", "1k")
R("R2", 6.0, 42.0, 90, "Q1B", "GND", "10k")
add("Q2", "TO92", 38.0, 38.0, 0, {"1": "GND", "2": "Q2B", "3": "Q2C"}, "S9014")
Dd("D2", 49.5, 33.5, 90, "+5V", "Q2C", "1N4148")
R("R3", 42.5, 42.0, 90, "Q2B", "K1_DRV", "1k")
R("R4", 46.0, 42.0, 90, "Q2B", "GND", "10k")
# ---------------- fusible y shunt
add("F1", "FUSE", 15.5, 46.0, 0, {"1": "K2NO", "2": "I_SHUNT"}, "315mA")
R("RSH", 18.5, 52.0, 0, "GND", "I_SHUNT", "1R 1W").key = "R1W"
# ---------------- divisor de voltaje y frecuencia
R("R5", 56.0, 10.0, 0, "V_IN", "V_ADC", "1M")
R("R6", 78.5, 10.0, 90, "V_ADC", "GND", "100k")
Dd("D3", 58.0, 15.0, 0, "+3V3", "V_ADC", "BAT85")
Dd("D4", 58.0, 20.0, 0, "V_ADC", "GND", "BAT85")
R("R7", 56.0, 25.0, 0, "V_IN", "FREQ", "100k")
Dd("D5", 58.0, 30.0, 0, "+3V3", "FREQ", "BAT85")
Dd("D6", 58.0, 35.0, 0, "FREQ", "GND", "BAT85")
Dd("DZ1", 58.0, 41.0, 0, "+3V3", "GND", "1N4729A", key="D41")
add("RT1", "C50", 52.0, 45.0, 0, {"1": "K1NO", "2": "NODO_X"}, "PTC 50mA")
# ---------------- buzzer
add("BZ1", "BUZ", 63.0, 52.0, 0, {"1": "+5V", "2": "BZ_N"}, "BUZZER")
add("Q3", "TO92", 72.0, 61.0, 0, {"1": "GND", "2": "Q3B", "3": "BZ_N"}, "S9014")
R("R18", 81.0, 61.0, 90, "Q3B", "BUZ", "1k")
# ---------------- ESP32-C3 (OLED 0.42") en zocalos: filas a 17.78 mm, USB hacia el borde inferior
ESPX, ESPY = 9.0, 72.0
add("U1L", "S8", ESPX, ESPY, 0, {str(i + 1): n for i, n in enumerate(
    ["REF_100K", "SENSE", "SDA", "SCL", "DESC", "K1_DRV", "REF_1M", "K2_DRV"])}, "ESP32-C3")
add("U1R", "S8", ESPX + 17.78, ESPY, 0, {str(i + 1): n for i, n in enumerate(
    ["REF_1K", "REF_10K", None, "FREQ", "BUZ", "+3V3", "GND", "+5V"])}, "")
# ---------------- ADS1115 en zocalo de 10 pines (horizontal)
ADSX, ADSY = 31.0, 62.0
add("U2", "S10", ADSX, ADSY, 270, {str(i + 1): n for i, n in enumerate(
    # el modulo entra con el cuerpo hacia abajo (girado 180 grados): de izquierda a derecha A3 ... VDD
    ["BTN", "I_SHUNT", "X_ADC", "V_ADC", None, "GND", "SDA", "SCL", "GND", "+3V3"])}, "ADS1115")
add("C1", "C25", 51.5, 57.5, 0, {"1": "GND", "2": "+3V3"}, "104")
# ---------------- nodo X (resistencias de referencia)
for i, (ref, net, val) in enumerate([("R8", "REF_1K", "1k"), ("R9", "REF_10K", "10k"), ("R10", "REF_100K", "100k"),
                                     ("R11", "REF_1M", "1M"), ("R12", "DESC", "220"), ("R14", "SENSE", "1k")]):
    R(ref, 31.0, 68.5 + i * 3.3, 0, net, "NODO_X", val)
R("R13", 31.0, 68.5 + 6 * 3.3, 0, "NODO_X", "X_ADC", "1k")
Dd("D7", 50.5, 76.0, 90, "+3V3", "NODO_X", "BAT85")
Dd("D8", 54.0, 76.0, 90, "NODO_X", "GND", "BAT85")
# ---------------- botones (escalera en A3)
R("R15", 56.0, 70.0, 0, "+3V3", "BTN", "10k")
add("SW1", "SW", 54.0, 88.0, 0, {"1": "BTN", "2": "GND"}, "MODO")
R("R16", 69.0, 74.0, 90, "BTN", "BTN_H", "10k")
add("SW2", "SW", 64.0, 88.0, 0, {"1": "BTN_H", "2": "GND"}, "HOLD")
R("R17", 78.0, 74.0, 90, "BTN", "BTN_R", "33k")
add("SW3", "SW", 74.0, 88.0, 0, {"1": "BTN_R", "2": "GND"}, "REL")
# ---------------- OLED 0.96" externa opcional (I2C, direccion 0x3D): VCC GND SCL SDA
OLEDX, OLEDY = 64.19, 3.6
add("U3", "S4", OLEDX, OLEDY, 270, {"1": "+3V3", "2": "GND", "3": "SCL", "4": "SDA"}, "OLED 0.96")
# ---------------- agujeros de montaje
for i, (x, y) in enumerate([(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)]):
    add(f"H{i+1}", "MH", x, y, 0, {}, "")

# contornos de los modulos (serigrafia) y su zona sin piezas altas
MODULES = [
    ("ESP32-C3 OLED 0.42\"  (USB hacia abajo)", ESPX - 2.2, ESPY - 6.0, ESPX + 17.78 + 2.2, ESPY + 17.78 + 8.5),
    ("ADS1115", ADSX - 2.0, ADSY - 2.0, ADSX + 22.86 + 2.0, ADSY + 16.0),
]

def all_pads():
    out = []
    for p in P:
        out += p.pads()
    return out

if __name__ == "__main__":
    pads = all_pads()
    print(len(P), "piezas", len(pads), "pads")
    for p in pads:
        if p["x"] < 1 or p["x"] > W - 1 or p["y"] < 1 or p["y"] > H - 1:
            print("FUERA", p["ref"], p["num"], p["x"], p["y"])
    cy = [(p.ref, p.courtyard()) for p in P if not p.ref.startswith("H")]
    for (ra, a), (rb, b) in itertools.combinations(cy, 2) if False else []:
        pass
    import itertools
    for (ra, a), (rb, b) in itertools.combinations(cy, 2):
        if a and b and a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
            print("SOLAPE", ra, rb)
    for ref, bb in cy:
        if bb and (bb[0] < 0.3 or bb[1] < 0.3 or bb[2] > W - 0.3 or bb[3] > H - 0.3):
            print("BORDE", ref, [round(v, 1) for v in bb])
    # pads que se tocan entre piezas distintas
    import itertools
    for a, b in itertools.combinations(pads, 2):
        if a["ref"] == b["ref"]: continue
        d = math.hypot(a["x"] - b["x"], a["y"] - b["y"])
        if d < (max(a["w"], a["h"]) + max(b["w"], b["h"])) / 2 + 0.3:
            print("PADS CERCA", a["ref"], a["num"], b["ref"], b["num"], round(d, 2))
