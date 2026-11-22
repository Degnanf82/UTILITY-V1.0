# Esquema electrico completo del multimetro v1.1 (una hoja) con schemdraw.
import schemdraw
import schemdraw.elements as elm
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "esquema.svg"
NET = "#1f4f9e"     # color de etiquetas de red
SEC = "#6b7a74"     # color de recuadros de seccion

d = schemdraw.Drawing(file=OUT, show=False)
d.config(unit=2.0, fontsize=10, lw=1.4, font="DejaVu Sans")

refs = {"R": 0, "D": 0, "Q": 0}
def ref(k):
    refs[k] += 1
    return f"{k}{refs[k]}"

def net(pt, name, side="right", length=0.6):
    """Etiqueta de red (como 'global label' de KiCad) en el punto pt."""
    line = elm.Line().at(pt)
    line = {"right": line.right(length), "left": line.left(length),
            "up": line.up(length), "down": line.down(length)}[side]
    d.add(line)
    th = {"right": 0, "left": 180, "up": 90, "down": 270}[side]
    t = elm.Tag(width=0.19 * len(name) + 0.55, height=0.5).at(line.end).theta(th).fill("#e8eefb").color(NET)
    d.add(t.label(name, fontsize=8.5, color=NET))

def gnd(pt, down=0.4):
    l = d.add(elm.Line().at(pt).down(down))
    d.add(elm.Ground().at(l.end))

def vcc(pt, name="+3V3", up=0.4):
    l = d.add(elm.Line().at(pt).up(up))
    d.add(elm.Vdd().at(l.end).label(name, fontsize=9))

def box(x0, y0, x1, y1, title):
    d.add(elm.Line().at((x0, y0)).to((x1, y0)).color(SEC).linestyle("--").linewidth(0.8))
    d.add(elm.Line().at((x1, y0)).to((x1, y1)).color(SEC).linestyle("--").linewidth(0.8))
    d.add(elm.Line().at((x1, y1)).to((x0, y1)).color(SEC).linestyle("--").linewidth(0.8))
    d.add(elm.Line().at((x0, y1)).to((x0, y0)).color(SEC).linestyle("--").linewidth(0.8))
    d.add(elm.Label().at((x0 + 0.25, y1 - 0.35)).label(title, fontsize=11, color=SEC, halign="left", valign="top"))

def clamp_pair(pt, label_up="+3V3"):
    """Diodos Schottky al riel y a GND desde pt (pt es la linea a proteger)."""
    d.add(elm.Dot().at(pt))
    up = d.add(elm.Schottky().at(pt).up(1.6).label(ref("D"), loc="bot", fontsize=8.5).label("BAT85", loc="top", fontsize=7.5))
    vcc(up.end, label_up, up=0.2)
    dn = d.add(elm.Schottky().at(pt).down(1.6).reverse().label(ref("D"), loc="bot", fontsize=8.5).label("BAT85", loc="top", fontsize=7.5))
    gnd(dn.end, 0.2)

# =================================================================== U1 ESP32-C3
X, Y = 3, 30
box(-1.5, 17.5, 15.5, 36.5, "MICROCONTROLADOR")
_L = ["GPIO3", "GPIO4", "GPIO5/SDA", "GPIO6/SCL", "GPIO7", "GPIO8/LED", "GPIO9/BOOT", "GPIO10"]
_R = ["GPIO0", "GPIO1", "GPIO2", "TX/GPIO21", "RX/GPIO20", "3V3", "GND", "5V"]
u1 = d.add(elm.Ic(pins=[elm.IcPin(name=n, side="left") for n in reversed(_L)] +
                       [elm.IcPin(name=n, side="right") for n in reversed(_R)], edgepadW=5.6, edgepadH=0.6, pinspacing=1.0, leadlen=0.6, lofst=0.12, plblsize=9,
   label="U1\nESP32-C3\nOLED 0.42\"\nintegrada").right().at((7, 26.5)).anchor("center"))
pins_l = ["GPIO3", "GPIO4", "GPIO5/SDA", "GPIO6/SCL", "GPIO7", "GPIO8/LED", "GPIO9/BOOT", "GPIO10"]
pins_r = ["GPIO0", "GPIO1", "GPIO2", "TX/GPIO21", "RX/GPIO20", "3V3", "GND", "5V"]
def pin_pt(name):
    return u1.absanchors[name] if hasattr(u1, "absanchors") and name in u1.absanchors else getattr(u1, name.replace("/", "_"), None)
for name, n in zip(pins_l, ["REF_100K", "SENSE", "SDA", "SCL", "DESC", "K1_DRV", "REF_1M", "K2_DRV"]):
    net(u1.absanchors[name], n, "left", 0.5)
for name, n in zip(pins_r, ["REF_1K", "REF_10K", None, "FREQ", "BUZ", "+3V3", None, "+5V"]):
    pt = u1.absanchors[name]
    if name == "GND":
        d.add(elm.Line().at(pt).right(2.6)); gnd((pt[0] + 2.6, pt[1]), 0.0)
    elif name == "GPIO2":
        d.add(elm.Line().at(pt).right(0.4))
        d.add(elm.Label().at((pt[0] + 0.5, pt[1])).label("× sin conectar", fontsize=8, halign="left"))
    else:
        net(pt, n, "right", 0.5)
d.add(elm.Label().at((7, 19.2)).label("Pantalla integrada 72×40 (SSD1306, 0x3C) ya conectada a GPIO5/6", fontsize=8, color=SEC))

# =================================================================== U2 ADS1115 + U3 OLED
box(16.5, 17.5, 37.5, 36.5, "ADC, PANTALLA Y ALIMENTACIÓN")
u2 = d.add(elm.Ic(pins=[elm.IcPin(name=n, side="left") for n in reversed(["VDD", "GND", "SCL", "SDA", "ADDR", "ALRT"])] +
                       [elm.IcPin(name=n, side="right") for n in reversed(["A0", "A1", "A2", "A3"])], edgepadW=1.4, edgepadH=0.6, pinspacing=1.0, leadlen=0.6, plblsize=9, label="U2\nADS1115\n0x48").right().at((24, 27)).anchor("center"))
net(u2.VDD, "+3V3", "left", 0.5)
d.add(elm.Line().at(u2.GND).left(2.6)); gnd((u2.GND[0] - 2.6, u2.GND[1]), 0.0)
net(u2.SCL, "SCL", "left", 0.5)
net(u2.SDA, "SDA", "left", 0.5)
d.add(elm.Line().at(u2.ADDR).left(3.4)); gnd((u2.ADDR[0] - 3.4, u2.ADDR[1]), 0.0)
d.add(elm.Line().at(u2.ALRT).left(0.4))
d.add(elm.Label().at((u2.ALRT[0] - 0.5, u2.ALRT[1])).label("×", fontsize=9, halign="right"))
for pin, n in [("A0", "V_ADC"), ("A1", "X_ADC"), ("A2", "I_SHUNT"), ("A3", "BTN")]:
    net(getattr(u2, pin), n, "right", 0.5)

u3 = d.add(elm.Ic(pins=[elm.IcPin(name=n, side="left") for n in reversed(["VCC", "GND", "SCL", "SDA"])],
                  edgepadW=3.4, edgepadH=0.6, pinspacing=1.0, leadlen=0.6, plblsize=9,
                  label="U3 (opcional)\nOLED 0.96\"\n128×64 · 0x3D").right().at((34, 31)).anchor("center"))
net(u3.VCC, "+3V3", "left", 0.5)
d.add(elm.Line().at(u3.GND).left(2.6)); gnd((u3.GND[0] - 2.6, u3.GND[1]), 0.0)
net(u3.SCL, "SCL", "left", 0.5)
net(u3.SDA, "SDA", "left", 0.5)

# C1 y zener del riel
c1 = d.add(elm.Capacitor().at((29, 22)).down(1.6).label("C1\n100 nF", loc="bot", fontsize=8.5))
vcc(c1.start, "+3V3", 0.3); gnd(c1.end, 0.2)
dz = d.add(elm.Zener().at((32.5, 22)).down(1.6).reverse().label("DZ1\n1N4729A\n3.6 V 1 W", loc="bot", fontsize=8.5))
vcc(dz.start, "+3V3", 0.3); gnd(dz.end, 0.2)
d.add(elm.Label().at((29.5, 19.2)).label("C1 junto a U2 · DZ1 protege el riel", fontsize=8, color=SEC))

# =================================================================== Puntas y reles
box(38.5, 17.5, 62.5, 36.5, "PUNTAS Y SELECCIÓN DE CIRCUITO (RELÉS)")
j1 = d.add(elm.Dot(open=True).right().at((40.5, 33.5)).label("J1  Punta ROJA (VΩmA)", loc="top", fontsize=9, color="#c62828"))
k2 = d.add(elm.Relay(switch="spdt", unit=2.2).right().at((46, 31)).anchor("a"))
k1 = d.add(elm.Relay(switch="spdt", unit=2.2).right().at((57, 31)).anchor("a"))
d.add(elm.Label().at((46.35, 31.9)).label("K2 · relé mA", fontsize=9, halign="left"))
d.add(elm.Label().at((57.35, 31.9)).label("K1 · relé Ω", fontsize=9, halign="left"))
d.add(elm.Label().at((46.35, 31.35)).label("SRD-05VDC", fontsize=7.5, halign="left", color=SEC))
d.add(elm.Label().at((57.35, 31.35)).label("SRD-05VDC", fontsize=7.5, halign="left", color=SEC))
d.add(elm.Wire("-|").at(j1.center).to(k2.a))
# K2 NO (c) -> F1 -> I_SHUNT, R_SH a GND
l = d.add(elm.Line().at(k2.c).down(28.8 - 24))
f1 = d.add(elm.Fuse().right().at(l.end).right(2.6).label("F1  315 mA", loc="top", fontsize=8.5))
d.add(elm.Dot().at(f1.end))
rsh = d.add(elm.Resistor().at(f1.end).down(1.8).label("R_SH\n1 Ω 1 W", loc="top", fontsize=8.5))
gnd(rsh.end, 0.2)
net(f1.end, "I_SHUNT", "right", 1.2)
d.add(elm.Label().at((k2.c[0] - 0.15, 27.9)).label("NO", fontsize=7.5, halign="right", color=SEC))
d.add(elm.Label().at((k2.b[0] + 0.15, 27.9)).label("NC", fontsize=7.5, halign="left", color=SEC))
d.add(elm.Label().at((k1.c[0] - 0.15, 27.9)).label("NO", fontsize=7.5, halign="right", color=SEC))
d.add(elm.Label().at((k1.b[0] + 0.15, 27.9)).label("NC", fontsize=7.5, halign="left", color=SEC))
# K2 NC (b) -> K1 COM (a)
d.add(elm.Wire("|-").at(k2.b).to((51.5, 27.4)))
d.add(elm.Line().at((51.5, 27.4)).to((51.5, 33.5)))
d.add(elm.Wire("-|").at((51.5, 33.5)).to(k1.a))
# K1 NO (c) -> RT1 -> NODO_X ; K1 NC (b) -> V_IN
l = d.add(elm.Line().at(k1.c).down(28.8 - 24))
rt = d.add(elm.Thermistor().right().at(l.end).right(2.4).label("RT1 PTC 50 mA", loc="top", fontsize=8.5))
net(rt.end, "NODO_X", "right", 0.3)
d.add(elm.Wire("|-").at(k1.b).to((59.2, 27.4)))
net((59.2, 27.4), "V_IN", "right", 0.2)
# J2 negra
j2 = d.add(elm.Dot(open=True).right().at((40.5, 20.3)).label("J2  Punta NEGRA (COM)", loc="right", fontsize=9))
gnd(j2.center, 0.4)

def driver(relay, drvnet, qref):
    x = relay.in2[0]
    vcc(relay.in1, "+5V", 0.4)
    l = d.add(elm.Line().at(relay.in2).down(0.8))           # nodo del colector
    q = d.add(elm.BjtNpn(circle=True).right().at((x, l.end[1] - 0.6)).anchor("collector")
              .label(qref + "\nS8050", loc="right", fontsize=8.5))
    d.add(elm.Line().at(l.end).to(q.collector))
    dx = x - 1.0
    d.add(elm.Line().at(l.end).to((dx, l.end[1]))); d.add(elm.Dot().at(l.end))
    dd = d.add(elm.Diode().at((dx, l.end[1])).up(relay.in1[1] + 0.4 - l.end[1]).label(ref("D") + "\n1N4148", loc="top", fontsize=8))
    d.add(elm.Line().at(dd.end).to((x, relay.in1[1] + 0.4))); d.add(elm.Dot().at((x, relay.in1[1] + 0.4)))
    gnd(q.emitter, 0.2)
    rb = d.add(elm.Resistor().at(q.base).left(1.8).label(ref("R") + " 1k", loc="top", fontsize=8))
    d.add(elm.Dot().at(rb.end))
    rp = d.add(elm.Resistor().at(rb.end).down(1.5).label(ref("R") + "\n10k", loc="bot", fontsize=8))
    gnd(rp.end, 0.2)
    net(rb.end, drvnet, "left", 0.3)
driver(k2, "K2_DRV", "Q1")
driver(k1, "K1_DRV", "Q2")
d.add(elm.Label().at((50.5, 18.3)).label("En reposo (K1 y K2 apagados) la punta roja queda en V_IN", fontsize=8, color=SEC))

# =================================================================== Voltaje / frecuencia
box(-1.5, -2.5, 19.5, 16.5, "VOLTAJE Y FRECUENCIA")
net_pt = (0.8, 12)
net((net_pt[0] + 0.01, net_pt[1]), "V_IN", "left", 0.01)
r = d.add(elm.Resistor().at(net_pt).right(3).label(ref("R") + "\n1 MΩ 1%", loc="top", fontsize=8.5))
d.add(elm.Line().at(r.end).right(1.6))
p = r.end
rb = d.add(elm.Resistor().at(p).down(3).label(ref("R") + "\n100 kΩ 1%", loc="bot", fontsize=8.5))
d.add(elm.Dot().at(p)); gnd(rb.end, 0.2)
clamp_pair((p[0] + 1.6, p[1]))
d.add(elm.Line().at((p[0] + 1.6, p[1])).right(2.4))
net((p[0] + 4.0, p[1]), "V_ADC", "right", 0.3)
d.add(elm.Label().at((10.5, 13.6)).label("÷11 → A0 (hasta 40 V)", fontsize=8, color=SEC))
# frecuencia
d.add(elm.Line().at(net_pt).down(6.5))
d.add(elm.Dot().at(net_pt))
r = d.add(elm.Resistor().at((net_pt[0], net_pt[1] - 6.5)).right(3).label(ref("R") + "\n100 kΩ", loc="top", fontsize=8.5))
d.add(elm.Line().at(r.end).right(1.6))
clamp_pair((r.end[0] + 1.6, r.end[1]))
d.add(elm.Line().at((r.end[0] + 1.6, r.end[1])).right(2.4))
net((r.end[0] + 4.0, r.end[1]), "FREQ", "right", 0.3)

# =================================================================== Nodo X
box(20.5, -2.5, 43.5, 16.5, "NODO X: RESISTENCIA, CONTINUIDAD, DIODO, CAPACITOR")
bx = 33
d.add(elm.Line().at((bx, 14.5)).down(14).linewidth(2.4).color("#138a55"))
d.add(elm.Label().at((bx, 15.1)).label("NODO_X", fontsize=9, color="#138a55"))
for i, (n, val) in enumerate([("REF_1K", "1 kΩ 1%"), ("REF_10K", "10 kΩ 1%"), ("REF_100K", "100 kΩ 1%"),
                              ("REF_1M", "1 MΩ 1%"), ("DESC", "220 Ω")]):
    y = 14 - i * 2.4
    r = d.add(elm.Resistor().at((bx - 5.5, y)).right(3.5).label(ref("R") + "  " + val, loc="top", fontsize=8.5))
    d.add(elm.Line().at(r.end).to((bx, y))); d.add(elm.Dot().at((bx, y)))
    net(r.start, n, "left", 0.3)
for i, n in enumerate(["X_ADC", "SENSE"]):
    y = 13 - i * 2.6
    d.add(elm.Line().at((bx, y)).right(0.5)); d.add(elm.Dot().at((bx, y)))
    r = d.add(elm.Resistor().at((bx + 0.5, y)).right(2.8).label(ref("R") + "  1 kΩ", loc="top", fontsize=8.5))
    net(r.end, n, "right", 0.3)
clamp_pair((bx + 2.2, 4.0))
d.add(elm.Line().at((bx, 4.0)).right(2.2))
d.add(elm.Line().at((bx, 1.0)).right(1.0))
net((bx + 1.0, 1.0), "NODO_X", "right", 0.3)
d.add(elm.Label().at((bx + 0.4, -1.4)).label("viene de RT1 (K1 NO)", fontsize=8, color=SEC, halign="left"))

# =================================================================== Botones
box(44.5, -2.5, 62.5, 16.5, "BOTONES (en A3) Y BUZZER")
vx, vy = 46.5, 13.5
rpu = d.add(elm.Resistor().at((vx, vy)).down(2).label(ref("R") + "\n10 kΩ", loc="bot", fontsize=8.5))
vcc(rpu.start, "+3V3", 0.2)
bus = d.add(elm.Line().at(rpu.end).right(6.3))
net(bus.end, "BTN", "right", 0.3)
def btn(x, rval, name):
    d.add(elm.Dot().at((x, rpu.end[1])))
    top = (x, rpu.end[1])
    if rval:
        r = d.add(elm.Resistor().at(top).down(2).label(ref("R") + "\n" + rval, loc="bot", fontsize=8.5))
        top = r.end
    else:
        top = d.add(elm.Line().at(top).down(2)).end
    sw = d.add(elm.Button().at(top).down(1.8).label(name, loc="bot", fontsize=8.5))
    gnd(sw.end, 0.2)
btn(48.0, None, "SW1\nMODO")
btn(50.0, "10 kΩ", "SW2\nHOLD")
btn(52.0, "33 kΩ", "SW3\nREL")
# buzzer
sp = d.add(elm.Speaker().right().at((59.6, 12.2)).label("BZ1 buzzer activo 5V", loc="bot", fontsize=8.5))
d.add(elm.Line().at(sp.in1).left(0.4)); vcc((sp.in1[0] - 0.4, sp.in1[1]), "+5V", 0.6)
d.add(elm.Line().at(sp.in2).left(0.9))
q3 = d.add(elm.BjtNpn(circle=True).right().at((sp.in2[0] - 0.9, sp.in2[1] - 1.0)).anchor("collector").label("Q3\nS8050", loc="right", fontsize=8.5))
d.add(elm.Line().at((sp.in2[0] - 0.9, sp.in2[1])).to(q3.collector))
gnd(q3.emitter, 0.2)
rb = d.add(elm.Resistor().at(q3.base).left(1.8).label(ref("R") + " 1k", loc="top", fontsize=8))
net(rb.end, "BUZ", "left", 0.3)

# =================================================================== cuadro de titulo
tx, ty = 44.5, -6.8
for a, b in [((tx, ty), (62.5, ty)), ((62.5, ty), (62.5, -3.2)), ((62.5, -3.2), (tx, -3.2)), ((tx, -3.2), (tx, ty))]:
    d.add(elm.Line().at(a).to(b).linewidth(1.2))
d.add(elm.Label().at((tx + 0.3, -3.7)).label("Multímetro ESP32-C3 (OLED 0.42\") · dos puntas", fontsize=13, halign="left", valign="top"))
d.add(elm.Label().at((tx + 0.3, -5.0)).label("Esquema eléctrico · v1.2 · Hoja 1/1", fontsize=9.5, halign="left", valign="top"))
d.add(elm.Label().at((tx + 0.3, -5.9)).label("Firmware: codigo-esp32 · Redes con el mismo nombre están unidas", fontsize=8, halign="left", valign="top", color=SEC))
d.add(elm.Label().at((-1.5, -4.0)).label("Nota: las etiquetas azules (SDA, +3V3, NODO_X…) son conexiones. Todos los puntos con la misma etiqueta van unidos.",
                                         fontsize=9, halign="left", color=SEC))

d.save(OUT)
print("ok", OUT)
