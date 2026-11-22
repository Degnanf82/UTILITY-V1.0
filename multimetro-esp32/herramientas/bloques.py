# Diagrama de bloques del multimetro (SVG).
import sys
OUT = sys.argv[1]
W, H = 1500, 880
F = "font-family:Inter,DejaVu Sans,Arial,sans-serif"
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#33403a"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="40" y="50" style="{F};font-size:30px;font-weight:700" fill="#17201c">Multímetro ESP32-C3 · diagrama de bloques</text>',
         f'<text x="40" y="78" style="{F};font-size:15px" fill="#56635d">Dos puntas · 2 relés eligen el circuito · ADC de 16 bits · Bluetooth y WiFi</text>']

def box(x, y, w, h, title, sub="", fill="#eef3f8", stroke="#2557b0", tcol="#17201c"):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>')
    parts.append(f'<text x="{x+w/2}" y="{y+ (h/2 if not sub else h/2-6)}" text-anchor="middle" style="{F};font-size:17px;font-weight:700" fill="{tcol}">{title}</text>')
    for i, line in enumerate(sub.split("|") if sub else []):
        parts.append(f'<text x="{x+w/2}" y="{y+h/2+16+i*17}" text-anchor="middle" style="{F};font-size:13px" fill="#40504a">{line}</text>')

def line(pts, label=None, lx=None, ly=None, color="#33403a", arrow=True, dash=False, anchor="middle"):
    p = " ".join(f"{x},{y}" for x, y in pts)
    parts.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="2.4" '
                 f'{"stroke-dasharray=\"7 6\"" if dash else ""} {"marker-end=\"url(#ar)\"" if arrow else ""}/>')
    if label:
        parts.append(f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" style="{F};font-size:13px;font-weight:600" fill="{color}">{label}</text>')

RED, GRN, BLU, PUR, GRY = "#c62828", "#138a55", "#1d64c8", "#7b3fbf", "#56635d"

# puntas
box(40, 270, 140, 64, "Punta ROJA", "VΩmA", fill="#fdecec", stroke=RED)
box(40, 590, 140, 64, "Punta NEGRA", "COM = GND", fill="#eceeee", stroke="#1d2421")
# reles
box(230, 110, 190, 420, "Relés", "K2 · mA|K1 · Ω||apagados = voltaje", fill="#e8eefb", stroke="#2557b0")
line([(180, 302), (228, 302)], color=RED)
# front-end
box(500, 120, 280, 80, "Fusible 315 mA + shunt 1 Ω", "corriente hasta 300 mA", fill="#eaf6ef", stroke=GRN)
box(500, 250, 280, 90, "Divisor 1 MΩ / 100 kΩ", "voltaje hasta 40 V|+ toma de frecuencia", fill="#eaf6ef", stroke=GRN)
box(500, 420, 280, 110, "Nodo X", "referencias 1k·10k·100k·1M|descarga 220 Ω · PTC|Ω, continuidad, diodo, capacitor", fill="#eaf6ef", stroke=GRN)
line([(420, 160), (498, 160)], "K2 NO", 459, 152, color=GRN)
line([(420, 295), (498, 295)], "K1 NC", 459, 287, color=GRN)
line([(420, 475), (498, 475)], "K1 NO", 459, 467, color=GRN)

# ADS1115
box(1000, 110, 200, 440, "ADS1115", "ADC 16 bits|A0 voltaje|A1 nodo X|A2 corriente|A3 botones", fill="#e3ecfa", stroke="#1c5aa6")
line([(780, 160), (998, 160)], "A2", 960, 152, color=GRN)
line([(780, 280), (998, 280)], "A0", 960, 272, color=GRN)
# nodo X -> A1 (pasa por encima de la linea de frecuencia con un puente)
line([(780, 450), (838, 450), (838, 450)], arrow=False, color=GRN)
parts.append(f'<path d="M838,450 a12,12 0 0 1 24,0" fill="none" stroke="{GRN}" stroke-width="2.4"/>')
line([(862, 450), (998, 450)], "A1", 960, 442, color=GRN)
# botones
box(1260, 300, 200, 80, "3 botones", "MODO · HOLD · REL", fill="#f3ecfb", stroke=PUR)
line([(1260, 340), (1202, 340)], "A3", 1232, 332, color=PUR)

# ESP32
box(500, 640, 700, 130, "ESP32-C3", "WiFi + Bluetooth LE · firmware del multímetro|pantalla OLED 0.42\" integrada (I2C GPIO 5/6)", fill="#f1ebfa", stroke="#3b1f63")
line([(1100, 552), (1100, 638)], "I2C · GPIO 5/6", 1112, 600, color=BLU, anchor="start")
line([(1100, 638), (1100, 552)], color=BLU)
# frecuencia: divisor -> ESP
line([(780, 320), (850, 320), (850, 638)], "frecuencia · GPIO 21", 858, 600, color=GRN, anchor="start")
# referencias: ESP <-> nodo X
line([(760, 638), (760, 532)], color=GRN)
parts.append(f'<text x="680" y="590" text-anchor="end" style="{F};font-size:13px;font-weight:600" fill="{GRN}">referencias GPIO 0·1·3·9·7</text>')
parts.append(f'<text x="680" y="607" text-anchor="end" style="{F};font-size:13px;font-weight:600" fill="{GRN}">lectura rápida GPIO 4</text>')
# reles <- ESP
line([(498, 705), (325, 705), (325, 532)], "GPIO 8 → K1 · GPIO 10 → K2", 410, 728, color="#2557b0")
# GND
line([(110, 656), (110, 790), (500, 790)], "GND común", 300, 782, color="#1d2421", arrow=False)
parts.append('<line x1="500" y1="790" x2="500" y2="772" stroke="#1d2421" stroke-width="2.4"/>')

# salidas
box(1260, 610, 200, 60, "Buzzer", "GPIO 20", fill="#f6f6f2", stroke=GRY)
line([(1200, 640), (1258, 640)], color=GRY)
box(1260, 720, 200, 90, "App Android", "lectura · gráfica · CSV|calibración", fill="#fff6e0", stroke="#c68300")
line([(1200, 740), (1258, 760)], "BLE / WiFi", 1229, 700, color="#c68300", dash=True)
line([(1258, 760), (1200, 740)], color="#c68300", dash=True)
parts.append(f'<text x="40" y="850" style="{F};font-size:13px" fill="#56635d">Opcional: OLED 0.96" externa en el mismo I2C (dirección 0x3D).</text>')
parts.append("</svg>")
open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print("ok")
