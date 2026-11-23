# Diagrama pictorico v1.1: dos puntas, reles y botones en escalera.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = sys.argv[1], sys.argv[2]
from gen_prims import wire, dot, chip, res_h, res_v, diode_h, diode_v, jack, svg
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_css.py"), encoding="utf-8").read())

old = open(SRC, encoding="utf-8").read()

# ------------------------------------------------------------------ piezas nuevas
def relay(x, y, name, sub):
    """Rele SRD visto desde arriba. COM a la izquierda, NO a la derecha, NC abajo."""
    s = f'<rect class="relay" x="{x}" y="{y}" width="120" height="100" rx="5"/>'
    s += f'<text class="relay-t" x="{x+60}" y="{y+48}" text-anchor="middle">{name}</text>'
    s += f'<text class="relay-s" x="{x+60}" y="{y+64}" text-anchor="middle">{sub}</text>'
    return s

def ptc(x1, x2, y, label="PTC 50 mA"):
    cx = (x1 + x2) / 2
    s = wire([(x1, y), (x2, y)], "w-lead")
    s += f'<circle class="ptc" cx="{cx}" cy="{y}" r="13"/>'
    s += f'<text class="lbl" x="{cx}" y="{y-20}" text-anchor="middle">{label}</text>'
    return s

def fuse(x1, x2, y, label):
    s = wire([(x1, y), (x2, y)], "w-lead")
    cx = (x1 + x2) / 2
    s += f'<rect class="fglass" x="{cx-40}" y="{y-10}" width="80" height="20" rx="4"/>'
    s += f'<rect class="fcap" x="{cx-40}" y="{y-10}" width="14" height="20" rx="2"/><rect class="fcap" x="{cx+26}" y="{y-10}" width="14" height="20" rx="2"/>'
    s += f'<line class="fwire" x1="{cx-26}" y1="{y}" x2="{cx+26}" y2="{y}"/>'
    s += f'<text class="lbl" x="{cx}" y="{y-18}" text-anchor="middle">{label}</text>'
    return s

def pin_lbl(x, y, t, anchor="middle"):
    return f'<text class="relay-p" x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'

def pad(x, y):
    return f'<circle class="pad" cx="{x}" cy="{y}" r="5.5"/>'

def button(x, y, name):
    s = f'<rect class="btn" x="{x-20}" y="{y}" width="40" height="40" rx="4"/><circle class="btn-cap" cx="{x}" cy="{y+20}" r="11"/>'
    s += f'<text class="lbl-b" x="{x+28}" y="{y+25}">{name}</text>'
    return s

def transistor(bx, gpio, top_net):
    """Transistor NPN con base por 1k desde gpio; colector sube a top_net (x=300). bx: no usado."""
    s = '<path class="to92" d="M206,206 L206,166 A24,24 0 0 1 254,166 L254,206 Z"/>'
    s += '<text class="silk" x="230" y="190" text-anchor="middle">S9014</text>'
    s += '<text class="lbl-b" x="196" y="222" text-anchor="end">E</text><text class="lbl-b" x="238" y="290">B</text><text class="lbl-b" x="262" y="222">C</text>'
    s += wire([(216, 206), (216, 232), (150, 232)], "w-gnd") + chip(150, 232, "GND", "gnd", "end", w=48)
    s += wire([(230, 206), (230, 300), (190, 300)], "w-lead")
    s += res_h(100, 190, 300, "nnrn", "1 kΩ")
    s += chip(98, 300, gpio, "esp", "end", w=82)
    return s

# ------------------------------------------------------------------ mapas de pines
def esp_map():
    b = '<rect class="board-c3" x="150" y="30" width="120" height="350" rx="10"/>'
    b += '<rect class="usb" x="166" y="36" width="18" height="12" rx="2"/><rect class="usb" x="236" y="36" width="18" height="12" rx="2"/>'
    b += '<text class="silk" x="175" y="60" text-anchor="middle" font-size="8">RST</text><text class="silk" x="245" y="60" text-anchor="middle" font-size="8">BOOT</text>'
    b += '<rect class="oled-win" x="186" y="92" width="48" height="104" rx="3"/>'
    b += '<text class="scr-t2" x="210" y="138" text-anchor="middle" font-size="11">OLED</text><text class="scr-t2" x="210" y="156" text-anchor="middle" font-size="11">0.42"</text>'
    b += '<rect class="usb" x="185" y="352" width="50" height="40" rx="7"/>'
    b += '<text class="silk-b" x="210" y="226" text-anchor="middle">ESP32</text><text class="silk-b" x="210" y="244" text-anchor="middle">C3</text>'
    left = [("3", "100kΩ → nodo X", "ana"), ("4", "1kΩ → nodo X", "ana"), ("5", "SDA → ADS1115", "sda"),
            ("6", "SCL → ADS1115", "scl"), ("7", "220Ω → nodo X", "ana"), ("8", "Relé K1 (Ω)", "relay"),
            ("9", "1MΩ → nodo X", "ana"), ("10", "Relé K2 (mA)", "relay")]
    right = [("0", "1kΩ → nodo X", "ana"), ("1", "10kΩ → nodo X", "ana"), ("2", "libre", "none"),
             ("TX", "100kΩ ← K1 NC", "ana"), ("RX", "1kΩ → buzzer", "gray"), ("V3", "3.3V → ADS1115", "v33"),
             ("GD", "GND común", "gnd"), ("V5", "Relés y buzzer", "v33")]
    for i, (p, t, k) in enumerate(left):
        y = 84 + i * 34
        b += f'<line class="lead l-{k}" x1="150" y1="{y}" x2="140" y2="{y}"/>'
        b += f'<circle class="pad" cx="150" cy="{y}" r="7"/><text class="silk" x="163" y="{y+4}">{p}</text>'
        b += chip(140, y, t, k, "end")
    for i, (p, t, k) in enumerate(right):
        y = 84 + i * 34
        b += f'<line class="lead l-{k}" x1="270" y1="{y}" x2="280" y2="{y}"/>'
        b += f'<circle class="pad" cx="270" cy="{y}" r="7"/><text class="silk" x="257" y="{y+4}" text-anchor="end">{p}</text>'
        b += chip(280, y, t, k, "start")
    return svg(420, 400, b, "Destino de cada pin del ESP32-C3")

def ads_map():
    pins = [("VDD", "3.3V (ESP pin 3.3)", "v33"), ("GND", "GND (ESP pin G)", "gnd"),
            ("SCL", "ESP pin 6", "scl"), ("SDA", "ESP pin 5", "sda"),
            ("ADDR", "GND (puente)", "gnd"), ("ALRT", "sin conectar", "none"),
            ("A0", "voltaje (paso 4)", "ana"), ("A1", "nodo X (paso 5)", "ana"),
            ("A2", "shunt (paso 6)", "ana"), ("A3", "botones (paso 2)", "btn")]
    b = '<rect class="board-mod" x="10" y="14" width="256" height="100" rx="7"/>'
    b += '<circle class="hole" cx="28" cy="32" r="7"/><circle class="hole" cx="248" cy="32" r="7"/>'
    b += '<text class="silk-b" x="138" y="40" text-anchor="middle">ADS1115</text>'
    for j, (p, t, k) in enumerate(pins):
        x = 26 + j * 25
        yrow = 140 + (9 - j) * 25
        b += f'<polyline class="lead l-{k}" points="{x},114 {x},{yrow} 268,{yrow}"/>'
        b += f'<circle class="pad" cx="{x}" cy="114" r="6.5"/>'
        b += f'<text class="silk" x="{x+4}" y="100" transform="rotate(-90 {x+4} 100)">{p}</text>'
        b += chip(272, yrow, t, k, "start", w=144)
    return svg(420, 375, b, "Destino de cada pin del ADS1115")

def oled_map():
    pins = [("VCC", "3.3V (ESP pin 3.3)", "v33"), ("GND", "GND (ESP pin G)", "gnd"),
            ("SCL", "ESP 6 y ADS SCL", "scl"), ("SDA", "ESP 5 y ADS SDA", "sda")]
    b = '<rect class="board-mod" x="10" y="122" width="200" height="140" rx="6"/>'
    b += '<rect class="scr" x="24" y="166" width="172" height="80" rx="3"/>'
    b += '<text class="scr-t" x="110" y="214" text-anchor="middle">12.345 V</text>'
    for j, (p, t, k) in enumerate(pins):
        x = 50 + j * 40
        yrow = 24 + j * 24
        b += f'<polyline class="lead l-{k}" points="{x},122 {x},{yrow} 268,{yrow}"/>'
        b += f'<circle class="pad" cx="{x}" cy="122" r="6.5"/>'
        b += f'<text class="silk" x="{x}" y="148" text-anchor="middle">{p}</text>'
        b += chip(272, yrow, t, k, "start", w=144)
    return svg(420, 275, b, "Destino de cada pin de la OLED")

# ------------------------------------------------------------------ botones (escalera en A3)
def buttons_ladder():
    b = chip(60, 24, "3.3V", "v33", "middle", w=52)
    b += res_v(60, 36, 116, "nnon", "10 kΩ", side="right")
    b += wire([(60, 116), (60, 140), (330, 140)], "w-btn")
    b += chip(332, 140, "ADS1115 A3", "ads", "start", w=86)
    # MODO: directo
    b += dot(110, 140, "d-btn") + wire([(110, 140), (110, 210)], "w-btn") + button(110, 210, "MODO")
    b += wire([(110, 250), (110, 284)], "w-gnd") + chip(110, 296, "GND", "gnd", "middle", w=48)
    # HOLD: 10k
    b += dot(200, 140, "d-btn") + res_v(200, 140, 210, "nnon", "10k", side="left") + button(200, 210, "HOLD")
    b += wire([(200, 250), (200, 284)], "w-gnd") + chip(200, 296, "GND", "gnd", "middle", w=48)
    # REL: 33k
    b += dot(290, 140, "d-btn") + res_v(290, 140, 210, "ooon", "33k", side="left") + button(290, 210, "REL")
    b += wire([(290, 250), (290, 284)], "w-gnd") + chip(290, 296, "GND", "gnd", "middle", w=48)
    return svg(420, 312, b, "Tres botones en una sola entrada")

# ------------------------------------------------------------------ puntas y reles
def probes_relays():
    b = '<text class="lbl-m" x="10" y="18">Relés apagados = punta en VOLTAJE (estado seguro)</text>'
    b += jack(40, 100, "r", "ROJA", lx=40, anchor="middle").replace('y="105"', 'y="132"')
    b += '<text class="lbl-m" x="40" y="148" text-anchor="middle">VΩmA</text>'
    # K2
    b += relay(110, 50, "K2 · relé mA", "SRD-05VDC")
    b += wire([(53, 100), (110, 100)], "w-v33") + pad(110, 100) + pin_lbl(100, 92, "COM", "end").replace('relay-p','relay-o')
    b += pad(230, 75) + pin_lbl(238, 94, "NO", "start").replace('relay-p','relay-o')
    b += pad(170, 150) + pin_lbl(180, 172, "NC", "start").replace('relay-p','relay-o')
    b += fuse(230, 330, 75, "fusible 315 mA")
    b += wire([(330, 75), (340, 75)], "w-v33") + chip(342, 75, "shunt (6)", "ana", "start", w=74)
    # K2 NC -> K1 COM
    b += wire([(170, 150), (170, 210)], "w-v33")
    b += relay(110, 210, "K1 · relé Ω", "SRD-05VDC")
    b += pad(170, 210) + pin_lbl(180, 196, "COM", "start").replace('relay-p','relay-o')
    b += pad(230, 260) + pin_lbl(238, 251, "NO", "start").replace('relay-p','relay-o')
    b += pad(170, 310) + pin_lbl(180, 332, "NC", "start").replace('relay-p','relay-o')
    b += ptc(230, 330, 260) + wire([(330, 260), (340, 260)], "w-ana") + chip(342, 260, "nodo X (5)", "ana", "start", w=74)
    b += wire([(170, 310), (170, 352)], "w-ana") + chip(170, 364, "voltaje y frecuencia (4)", "ana", "middle", w=180)
    # COM
    b += jack(40, 430, "k", "NEGRA", lx=40, anchor="middle").replace('y="435"', 'y="400"')
    b += '<text class="lbl-m" x="40" y="462" text-anchor="middle">COM</text>'
    b += wire([(53, 430), (110, 430)], "w-gnd") + chip(112, 430, "GND del circuito", "gnd", "start", w=124)
    return svg(420, 472, b, "Puntas roja y negra con los dos reles")

def relay_driver():
    b = chip(300, 24, "5V", "v33", "middle", w=44)
    b += wire([(300, 36), (300, 60)], "w-v33") + dot(300, 46, "d-v33")
    b += '<rect class="relay" x="262" y="60" width="76" height="50" rx="4"/>'
    b += '<text class="relay-t" x="300" y="84" text-anchor="middle">bobina</text>'
    b += '<text class="relay-s" x="300" y="100" text-anchor="middle">del relé</text>'
    b += wire([(300, 46), (370, 46)], "w-v33")
    b += diode_v(370, 46, 136, "top", "")
    b += '<text class="lbl" x="370" y="156" text-anchor="middle">1N4148</text>'
    b += wire([(370, 136), (300, 136)], "w-lead") + dot(300, 136, "d-ink")
    b += wire([(300, 110), (300, 226), (244, 226), (244, 206)], "w-lead")
    b += transistor(0, "GPIO 8 / 10", "")
    # pull-down de la base
    b += dot(230, 262, "d-ink") + wire([(230, 262), (262, 262)], "w-lead")
    b += res_h(262, 340, 262, "nnon", "10 kΩ") + chip(342, 262, "GND", "gnd", "start", w=48)
    return svg(420, 320, b, "Circuito para manejar cada rele")

# ------------------------------------------------------------------ voltaje + frecuencia
def volt_freq():
    b = chip(10, 80, "K1 NC", "relay", "start", w=64)
    b += wire([(74, 80), (90, 80)], "w-ana") + dot(90, 80)
    # V
    b += res_h(90, 190, 80, "nngn", "1 MΩ")
    b += wire([(190, 80), (300, 80)], "w-ana") + dot(215, 80) + dot(255, 80)
    b += chip(302, 80, "ADS1115 A0", "ads", "start", w=110)
    b += res_v(215, 80, 170, "nnyn", "100k", side="left")
    b += chip(215, 184, "GND", "gnd", "middle", w=48)
    b += diode_v(255, 80, 34, "top", "") + chip(255, 24, "3.3V", "v33", "middle", w=52)
    b += diode_v(255, 80, 138, "top", "") + chip(255, 150, "GND", "gnd", "middle", w=48)
    # F
    b += wire([(90, 80), (90, 290)], "w-ana")
    b += res_h(90, 200, 290, "nnyn", "100 kΩ")
    b += wire([(200, 290), (300, 290)], "w-ana") + dot(255, 290)
    b += chip(302, 290, "GPIO 21 (TX)", "esp", "start", w=110)
    b += diode_v(255, 290, 244, "top", "") + chip(255, 234, "3.3V", "v33", "middle", w=52)
    b += diode_v(255, 290, 336, "top", "") + chip(255, 348, "GND", "gnd", "middle", w=48)
    b += '<text class="lbl-m" x="300" y="44">← voltaje</text><text class="lbl-m" x="300" y="254">← frecuencia</text>'
    return svg(420, 365, b, "Entrada de voltaje y de frecuencia")

# ------------------------------------------------------------------ nodo X
def ohm_node():
    rows = [("GPIO 0", "nnrn", "1 kΩ"), ("GPIO 1", "nnon", "10 kΩ"), ("GPIO 3", "nnyn", "100 kΩ"),
            ("GPIO 9", "nngn", "1 MΩ"), ("GPIO 7", "rrnu", "220 Ω")]
    X = 300
    b = f'<text class="t-ana" x="{X}" y="22" text-anchor="middle">NODO X (punto común)</text>'
    b += wire([(X, 50), (X, 500)], "w-strip")
    for i, (g, bands, val) in enumerate(rows):
        y = 56 + i * 58
        b += chip(10, y, g, "esp", w=78)
        b += wire([(88, y), (105, y)], "w-lead")
        b += res_h(105, 235, y, bands, val)
        b += wire([(235, y), (X, y)], "w-ana")
        b += dot(X, y)
    for y, name, kind in ((352, "ADS1115 A1", "ads"), (404, "ESP32 GPIO 4", "esp")):
        b += dot(X, y) + wire([(X, y), (250, y)], "w-ana")
        b += res_h(160, 250, y, "nnrn", "1 kΩ") + chip(158, y, name, kind, "end", w=104)
    b += wire([(X, 456), (262, 456)], "w-ana") + dot(X, 456)
    b += diode_h(140, 262, 456, "left")
    b += chip(140, 456, "3.3V", "v33", "end")
    b += diode_h(X, 372, 456, "left")
    b += chip(374, 456, "GND", "gnd", "start", w=44)
    b += chip(X, 512, "K1 NO (por el PTC)", "relay", "middle", w=150)
    return svg(420, 530, b, "Nodo X")

# ------------------------------------------------------------------ corriente
def amp_in():
    y = 80
    b = chip(10, y, "K2 NO (por el fusible)", "relay", "start", w=160)
    b += wire([(170, y), (300, y)], "w-ana") + dot(240, y)
    b += chip(302, y, "ADS1115 A2", "ads", "start", w=110)
    b += res_v(240, y, 205, None, "shunt|1 Ω · 1 W", side="left", big=True)
    b += chip(240, 218, "GND", "gnd", "middle", w=48)
    return svg(420, 236, b, "Shunt de corriente")

# ------------------------------------------------------------------ buzzer
def buzzer():
    b = '<text class="lbl-m" x="10" y="20">Transistor con la cara plana hacia ti: E · B · C</text>'
    b += '<circle class="buzz" cx="330" cy="76" r="32"/><circle class="buzz-h" cx="330" cy="76" r="5"/>'
    b += '<text class="silk-b" x="346" y="62">+</text>'
    b += wire([(342, 108), (342, 140), (372, 140)], "w-v33") + chip(374, 140, "5V", "v33", "start", w=40)
    b += wire([(318, 108), (318, 226), (244, 226), (244, 206)], "w-lead")
    b += '<text class="lbl-m" x="306" y="125" text-anchor="end">−</text>'
    b += transistor(0, "GPIO 20 (RX)", "")
    return svg(420, 320, b, "Buzzer con transistor")

# ------------------------------------------------------------------ pagina
CSS2 = CSS_EXTRA + """
.c-relay rect { fill: var(--relay); stroke: var(--relay); } .c-relay text { fill: #fff; }
.l-relay { stroke: var(--relay); }
.relay { fill: var(--relay); stroke: #0d2a63; stroke-width: 1.2; }
.relay-t { fill: #fff; font-size: 13px; font-weight: 700; }
.relay-s { fill: #cfe0ff; font-size: 10.5px; }
.relay-p { fill: #fff; font-size: 11px; font-weight: 700; }
.relay-o { fill: var(--relay); font-size: 12px; font-weight: 700; }
.board-c3 { fill: #3b1f63; stroke: #24113f; stroke-width: 1.5; }
.oled-win { fill: #0d1030; stroke: #9aa0a6; stroke-width: 2; }
.scr-t2 { fill: #8fb8ff; font-size: 14px; font-weight: 700; }
.ptc { fill: #e8b100; stroke: #8a6a00; stroke-width: 1.2; }
.fig .note { padding: 0 16px; }
.docs { display: grid; gap: 14px; }
.doc { margin: 0; background: var(--panel); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; }
.doc img { display: block; width: 100%; height: auto; background: #fff; }
.doc figcaption { padding: 10px 16px 12px; font-size: 14px; border-top: 1px solid var(--rule); }
.doc .shots { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding: 8px; background: #0b0e11; }
.doc .shots img { border-radius: 6px; background: #0b0e11; }
"""
old = old.replace("--tag: #e6ece9;\n", "--tag: #e6ece9; --btn: #7b3fbf; --lead: #8b9690; --relay: #2557b0;\n", 1)
for a in ("--esp: #08090a; --mod: #1d5ea8; --pad: #d9b23a; --silk: #f4f6f8; --tag: #232d29;\n  color-scheme: dark } }",
          "--esp: #08090a; --mod: #1d5ea8; --pad: #d9b23a; --silk: #f4f6f8; --tag: #232d29;\n  color-scheme: dark }\n"):
    assert a in old
    old = old.replace(a, a.replace("--tag: #232d29;", "--tag: #232d29; --btn: #b98cf0; --lead: #a9b3ae; --relay: #2f63c4;"))
old = old.replace("</style>", CSS2 + "</style>", 1)
head = old[:old.index("<!-- ============================================================ FIG 1 -->")]
head = head.replace("<div class=\"eyebrow\">Guía de armado · v1.0</div>", "<div class=\"eyebrow\">Guía de armado · v1.2 · ESP32-C3 con OLED 0.42\"</div>")
head = head.replace("Cableado completo para tus tres placas: ESP32-C3 Super Mini, ADS1115 y OLED 0.96\". Arma por partes en el orden de la sección final y prueba cada una antes de seguir.",
    "Como un multímetro comercial: <b>solo dos puntas</b>, roja y negra. La función se elige con el botón MODO o desde la app, y dos relés llevan la punta roja al circuito correcto. Cada pieza está dibujada como se ve en la mano y cada pin dice a dónde va.")
head = head.replace("Máximo 40 V y 2.5 A.", "Máximo 40 V y 300 mA.")

def fig(title, svgs, notes):
    s = '<div class="fig">' + (f"<h3>{title}</h3>" if title else "")
    s += svgs.replace("<svg ", '<svg class="p" ')
    if notes:
        s += '<div class="cap"><ul>' + "".join(f"<li>{n}</li>" for n in notes) + "</ul></div>"
    return s + "</div>"

cables = [
    ("v33", "ESP32 pin <b>V3</b> (3.3V)", "ADS1115 <b>VDD</b>"),
    ("gnd", "ESP32 pin <b>GD</b> (GND)", "ADS1115 <b>GND</b>"),
    ("gnd", "ADS1115 <b>ADDR</b>", "ADS1115 <b>GND</b> (puente corto)"),
    ("sda", "ESP32 pin <b>5</b>", "ADS1115 <b>SDA</b>"),
    ("scl", "ESP32 pin <b>6</b>", "ADS1115 <b>SCL</b>"),
]
names = {"v33": "rojo", "gnd": "negro", "sda": "amarillo", "scl": "azul"}
rows = "".join(
    f'<tr><td class="n">{i+1}</td><td><span class="sw" style="background:var(--{k})"></span>{names[k]}</td><td>{a}</td><td>{b}</td></tr>'
    for i, (k, a, b) in enumerate(cables))
cable_table = ('<div class="tbl"><table class="cables"><thead><tr><th>#</th><th>Cable</th><th>Desde</th><th>Hasta</th></tr></thead>'
               f"<tbody>{rows}</tbody></table></div>")

pins = [("V5", "+ de las 2 bobinas de relé y + del buzzer", "3"), ("GD", "GND común (COM, ADS1115, shunt, botones)", "1"),
        ("V3", "VDD del ADS1115, pull-up de botones, diodos, zener", "1"),
        ("5", "SDA del ADS1115 (la pantalla integrada ya está en este bus)", "1"),
        ("6", "SCL del ADS1115", "1"),
        ("8", "1 kΩ → base del transistor del relé K1 (Ω)", "3"), ("10", "1 kΩ → base del transistor del relé K2 (mA)", "3"),
        ("TX (21)", "100 kΩ desde K1 NC (frecuencia)", "4"),
        ("0", "1 kΩ → nodo X", "5"), ("1", "10 kΩ → nodo X", "5"), ("3", "100 kΩ → nodo X", "5"), ("9", "1 MΩ → nodo X", "5"),
        ("7", "220 Ω → nodo X (descarga)", "5"), ("4", "1 kΩ → nodo X", "5"),
        ("RX (20)", "1 kΩ → base del transistor del buzzer", "7"), ("2", "libre: no conectar nada", "—")]
pin_table = ('<div class="tbl"><table><thead><tr><th>Pin</th><th>Conectar a</th><th>Paso</th></tr></thead><tbody>'
             + "".join(f'<tr><td class="pin">{p}</td><td>{t}</td><td>{s}</td></tr>' for p, t, s in pins)
             + "</tbody></table></div>")

body = f"""
<section>
  <h2>Documentos</h2>
  <div class="docs">
    <figure class="doc"><img src="docs/diagrama-de-bloques.png" alt="Diagrama de bloques"><figcaption><b>Diagrama de bloques.</b> Qué hace cada parte y cómo se comunican.</figcaption></figure>
    <figure class="doc"><img src="docs/esquema-electrico.png" alt="Esquema eléctrico completo"><figcaption><b>Esquema eléctrico completo</b> (hoja A3; en el repositorio también está en PDF: <code>docs/esquema-electrico.pdf</code>). Las etiquetas azules con el mismo nombre están unidas.</figcaption></figure>
    <figure class="doc"><img src="docs/montaje-placa-perforada.png" alt="Montaje en placa perforada"><figcaption><b>Montaje en placa perforada</b> (7 × 9 cm). Disposición sugerida de piezas y cables.</figcaption></figure>
    <figure class="doc"><div class="shots"><img src="docs/app-voltaje.png" alt="App: voltaje"><img src="docs/app-resistencia.png" alt="App: resistencia"><img src="docs/app-capacitor.png" alt="App: capacitor"></div><figcaption><b>Pantallas de la app</b> (la app real, dibujada con datos de ejemplo): voltaje con gráfica, resistencia y capacitor en HOLD.</figcaption></figure>
  </div>
</section>

<section>
  <h2>Cómo funciona con dos puntas</h2>
  <div class="tbl"><table>
    <thead><tr><th>Función</th><th>Relé K1</th><th>Relé K2</th><th>La punta roja va a</th></tr></thead>
    <tbody>
      <tr><td>Voltaje y frecuencia</td><td>apagado</td><td>apagado</td><td>divisor de voltaje y GPIO 20</td></tr>
      <tr><td>Ω, continuidad, diodo, capacitor</td><td><b>encendido</b></td><td>apagado</td><td>nodo X</td></tr>
      <tr><td>Corriente (mA)</td><td>apagado</td><td><b>encendido</b></td><td>fusible y shunt</td></tr>
    </tbody></table></div>
  <p><b>Botón MODO:</b> V → Hz → Ω → continuidad → diodo → capacitor → V. <b>Corriente:</b> mantén MODO 1.5 s, o elígela en la app (pide confirmación). Así nunca pasas por mA sin querer con las puntas sobre una fuente. Antes de pasar a Ω, el multímetro revisa que no haya voltaje en las puntas.</p>
</section>

<section>
  <h2>Paso 1 · ESP32-C3 y ADS1115 (5 cables)</h2>
  <p>Tu placa ya trae la pantalla integrada, conectada por dentro a los pines 5 y 6. Solo falta conectar el ADS1115 a esos mismos pines.</p>
  {cable_table}
  <div class="figs">
    {fig("ADS1115: a dónde va cada pin", ads_map(), ["Suelda también un capacitor cerámico «104» (100 nF) entre VDD y GND, pegado al módulo.", "Prueba: carga el firmware; la pantalla integrada muestra «DC V»."])}
    {fig("OLED 0.96\" externa (opcional)", oled_map(), ["Solo si quieres una pantalla más grande. Primero cámbiala a la dirección <b>0x3D</b>: en la parte trasera, mueve la resistencia de «0x78» a «0x7A». Si no, choca con la pantalla integrada.", "El firmware la detecta sola y muestra la lectura en las dos."])}
  </div>
  {fig("ESP32-C3 visto desde arriba (USB-C abajo): a dónde va cada pin", esp_map(), ["Vista desde arriba, con el USB-C abajo, igual que en tu foto. Incluye los pines de los pasos siguientes.", "El LED azul de la placa (GPIO 8) se apaga cuando el relé K1 está encendido; es normal."])}
</section>

<section>
  <h2>Paso 2 · Los 3 botones (una sola entrada)</h2>
  <div class="figs">
    {fig("", buttons_ladder(), ["Los 3 botones comparten el pin A3 del ADS1115. El multímetro sabe cuál pulsaste por la resistencia de cada uno: MODO directo, HOLD con 10 kΩ y REL con 33 kΩ.", "Cada botón tiene 4 patas: usa dos en diagonal.", "Prueba: MODO cambia la función en la pantalla."])}
  </div>
</section>

<section>
  <h2>Paso 3 · Puntas y relés</h2>
  <div class="figs">
    {fig("A · Cómo se conectan las puntas", probes_relays(), ["Cada relé tiene 5 patas: COM, NO (normalmente abierto), NC (normalmente cerrado) y 2 de bobina. En la base del relé vienen marcadas.", "El número entre paréntesis es el paso donde sigue ese cable.", "Usa cable grueso desde la punta roja hasta el shunt: por ahí pasa la corriente."])}
    {fig("B · Circuito de cada bobina (hazlo 2 veces)", relay_driver(), ["<b>GPIO 8</b> maneja K1 (Ω) y <b>GPIO 10</b> maneja K2 (mA).", "El diodo 1N4148 va con la raya hacia 5V. Protege al transistor cuando el relé se apaga.", "Alternativa: un módulo de 2 relés de 5V que se active con 3.3V en alto."])}
  </div>
</section>

<section>
  <h2>Paso 4 · Voltaje y frecuencia</h2>
  <div class="figs">
    {fig("", volt_freq(), ["Todo sale del pin <b>NC de K1</b>.", "Diodos BAT85: el de arriba con la raya hacia 3.3V; el de abajo con la raya hacia la línea verde.", "Prueba: una pila de 9 V entre las puntas marca unos 9 V."])}
  </div>
</section>

<section>
  <h2>Paso 5 · Nodo X: resistencia, continuidad, diodo y capacitor</h2>
  <div class="figs">
    {fig("", ohm_node(), ["El nodo X es un solo punto: una tira de cobre o un cable pelado donde se sueldan todas estas piezas.", "Suelda también un <b>zener de 3.6 V 1 W (1N4729A)</b> entre 3.3V y GND, con la raya hacia 3.3V. Si mides voltaje en Ω por error, protege al ESP32 mientras el PTC se corta.", "Prueba: una resistencia de 10 kΩ marca unos 10 kΩ. Se oye el clic del relé al entrar en Ω."])}
  </div>
</section>

<section>
  <h2>Paso 6 · Corriente</h2>
  <div class="figs">
    {fig("", amp_in(), ["El fusible ya quedó en el paso 3, entre K2 NO y este punto.", "Prueba: pila de 9 V → resistencia de 100 Ω → punta roja, y la punta negra al − de la pila. Mantén MODO 1.5 s: debe marcar unos 85–90 mA."])}
  </div>
</section>

<section>
  <h2>Paso 7 · Buzzer</h2>
  <div class="figs">
    {fig("", buzzer(), ["Buzzer <b>activo</b> de 5V: el que pita solo con conectarlo. La pata + suele ser la más larga."])}
  </div>
</section>

<section>
  <h2>Mapa de pines del ESP32-C3</h2>
  {pin_table}
</section>

<section>
  <h2>Materiales</h2>
  <div class="bom">
    <div><h4>Ya los tienes</h4><ul><li>ESP32-C3 con OLED 0.42" integrada</li><li>ADS1115</li><li>OLED 0.96" (opcional, en 0x3D)</li></ul></div>
    <div><h4>Relés y transistores</h4><ul><li>2 relés 5V SPDT (SRD-05VDC-SL-C)</li><li>3 transistores NPN S9014 (o S8050)</li><li>2 diodos 1N4148</li></ul></div>
    <div><h4>Resistencias (1 %)</h4><ul><li>1 kΩ ×6</li><li>10 kΩ ×5</li><li>33 kΩ ×1</li><li>100 kΩ ×3</li><li>1 MΩ ×2</li><li>220 Ω ×1</li><li>Shunt 1 Ω 1 W ×1</li></ul></div>
    <div><h4>Protección</h4><ul><li>6 diodos Schottky BAT85 (o BAT43)</li><li>Fusible rápido 315 mA 5×20 con portafusible</li><li>PTC de 50 mA (MF-R005)</li><li>Zener 3.6 V 1 W (1N4729A)</li><li>Capacitor cerámico 104 (100 nF)</li></ul></div>
    <div><h4>Otros</h4><ul><li>3 pulsadores</li><li>Buzzer activo de 5V</li><li>2 jacks banana (rojo y negro) y un par de puntas</li><li>Placa perforada y cable</li></ul></div>
  </div>
</section>
"""
html = head + body + "\n</div>\n"
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(html))
