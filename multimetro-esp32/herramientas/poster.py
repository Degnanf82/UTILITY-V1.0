# Lamina unica de armado (PNG grande) reutilizando los dibujos de gen2.py.
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
sys.argv = ["gen2.py", SRC, os.path.join(HERE, "_tmp_guia.html")]
sys.path.insert(0, HERE)
g = importlib.import_module("gen2")

def card(title, svg_s, notes=(), num=None):
    n = f'<span class="num">{num}</span>' if num else ""
    s = f'<div class="card"><h3>{n}{title}</h3>' + svg_s.replace("<svg ", '<svg class="p" ')
    if notes:
        s += "<ul>" + "".join(f"<li>{x}</li>" for x in notes) + "</ul>"
    return s + "</div>"

cables = "".join(
    f'<tr><td>{i+1}</td><td><span class="sw" style="background:var(--{k})"></span></td><td>{a}</td><td>{b}</td></tr>'
    for i, (k, a, b) in enumerate(g.cables))

css = g.old[g.old.index("<style>") + 7:g.old.index("</style>")]
html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap">
<style>{css}
body {{ margin: 0; background: #eef2f0; }}
.poster {{ width: 1800px; padding: 36px 40px 40px; box-sizing: border-box; display: grid; gap: 22px; }}
.top {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; border-bottom: 3px solid var(--fg); padding-bottom: 14px; }}
.top h1 {{ font-size: 52px; }}
.top .sub {{ font-size: 18px; color: var(--muted); margin-top: 6px; }}
.top .meta {{ text-align: right; font: 600 15px var(--f-mono); color: var(--muted); line-height: 1.6; }}
.warnbar {{ background: var(--warn-bg); border-left: 6px solid var(--warn); padding: 10px 16px; font-size: 17px; border-radius: 4px; }}
.cols {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; align-items: start; }}
.col {{ display: grid; gap: 22px; }}
.card {{ background: #fff; border: 1.5px solid var(--rule); border-radius: 14px; padding: 14px 16px 12px; }}
.card h3 {{ color: var(--fg); font-size: 22px; margin: 0 0 6px; display: flex; align-items: center; gap: 10px; }}
.card .num {{ font: 700 16px var(--f-mono); color: #fff; background: var(--accent); border-radius: 50%; width: 30px; height: 30px; display: inline-grid; place-items: center; flex: none; }}
.card svg.p {{ width: 100%; height: auto; display: block; }}
.card ul {{ margin: 6px 0 0; padding-left: 20px; font-size: 14.5px; display: grid; gap: 3px; }}
table.cb {{ width: 100%; border-collapse: collapse; font-size: 15px; }}
table.cb td {{ padding: 6px 6px; border-bottom: 1px solid var(--rule); }}
table.cb td:first-child {{ font: 700 15px var(--f-mono); color: var(--muted); width: 22px; }}
.sw {{ display: inline-block; width: 18px; height: 18px; border-radius: 4px; }}
.bom {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px 18px; font-size: 14.5px; }}
.bom b {{ font-family: var(--f-head); font-size: 16px; }}
ol.chk {{ margin: 0; padding-left: 22px; display: grid; gap: 7px; font-size: 15px; }}
ol.chk span {{ color: var(--accent); font-weight: 600; }}
.foot {{ font-size: 13px; color: var(--muted); text-align: right; }}
</style></head><body><div class="poster">
<div class="top"><div><h1>Multímetro ESP32-C3 · lámina de armado</h1>
<div class="sub">Placa ESP32-C3 SuperMini con OLED 0.42" · ADS1115 · dos puntas (roja VΩmA, negra COM) · 2 relés · Bluetooth y WiFi</div></div>
<div class="meta">Firmware 1.3.3 · App 1.3<br>Vista desde arriba, USB-C abajo<br>Cada pin dice a dónde va</div></div>
<div class="warnbar"><b style="color:var(--warn)">Solo baja tensión DC:</b> máximo 40 V y 300 mA. Nunca a 110/220 V. Arma por pasos y prueba cada uno antes de seguir.</div>
<div class="cols">
<div class="col">
{card("ESP32-C3: destino de cada pin", g.esp_map(), ["El LED azul (GPIO 8) se apaga cuando el relé K1 está encendido: es normal.", "GPIO 2 queda libre."], 1)}
<div class="card"><h3><span class="num">1</span>ESP32-C3 ↔ ADS1115 (5 cables)</h3><table class="cb">{cables}</table>
<ul><li>Capacitor cerámico <b>104</b> entre VDD y GND del ADS1115, pegado al módulo.</li><li><b>Prueba:</b> RST → la pantalla muestra «DC V»; en la app, Info equipo → «ADS1115: detectado».</li></ul></div>
{card("ADS1115: a dónde va cada pin", g.ads_map(), [], 1)}
<div class="card"><h3>Orden de armado</h3><ol class="chk">
<li>ESP32 + ADS1115 (5 cables) → <span>«ADS1115: detectado»</span></li>
<li>Botones → <span>MODO cambia la función</span></li>
<li>Relés y bobinas → <span>se oye el clic al pasar a Ω</span></li>
<li>Voltaje y frecuencia → <span>pila de 9 V ≈ 9 V</span></li>
<li>Nodo X → <span>10 kΩ ≈ 10 kΩ · capacitor 104 ≈ 100 nF</span></li>
<li>Corriente → <span>≈ 85–90 mA con 9 V y 100 Ω</span></li>
<li>Buzzer → <span>pita en continuidad</span></li>
<li>Calibrar desde la app (Calibrar)</li>
</ol></div>
</div>
<div class="col">
{card("Botones en una sola entrada (A3)", g.buttons_ladder(), ["MODO directo, HOLD con 10 kΩ, REL con 33 kΩ.", "<b>Prueba:</b> MODO cambia la función en pantalla."], 2)}
{card("Puntas y relés", g.probes_relays(), ["Relés apagados = la punta roja mide voltaje (estado seguro).", "Cable grueso desde la punta roja hasta el shunt."], 3)}
{card("Bobina de cada relé (hacer 2 veces)", g.relay_driver(), ["GPIO 8 → K1 (Ω) · GPIO 10 → K2 (mA).", "Transistor S9014 (o S8050), cara plana al frente: E · B · C.", "Diodo 1N4148 con la raya hacia 5V."], 3)}
{card("Buzzer", g.buzzer(), ["Buzzer activo de 5V; la pata + es la más larga."], 7)}
</div>
<div class="col">
{card("Voltaje y frecuencia", g.volt_freq(), ["Diodos BAT85: raya hacia 3.3V (arriba) y hacia la línea verde (abajo).", "<b>Prueba:</b> pila de 9 V entre las puntas → ~9 V."], 4)}
{card("Nodo X: Ω, continuidad, diodo, capacitor", g.ohm_node(), ["Zener 1N4729A (3.6 V) entre 3.3V y GND, raya hacia 3.3V.", "<b>Prueba:</b> resistencia de 10 kΩ → ~10 kΩ; capacitor 104 → ~100 nF."], 5)}
{card("Corriente", g.amp_in(), ["<b>Prueba:</b> 9 V → 100 Ω → punta roja; negra al − de la pila; MODO largo → ~85–90 mA."], 6)}
<div class="card"><h3>Materiales</h3><div class="bom">
<div><b>Placas</b><br>ESP32-C3 OLED 0.42"<br>ADS1115</div>
<div><b>Relés y transistores</b><br>2 relés SRD-05VDC<br>3 × S9014 (o S8050)<br>2 × 1N4148</div>
<div><b>Resistencias 1 %</b><br>1 kΩ ×6 · 10 kΩ ×5 · 33 kΩ ×1<br>100 kΩ ×3 · 1 MΩ ×2 · 220 Ω ×1<br>Shunt 1 Ω 1 W</div>
<div><b>Protección</b><br>6 × BAT85 · zener 1N4729A<br>Fusible 315 mA · PTC 50 mA<br>Cerámico 104 (100 nF)</div>
<div><b>Otros</b><br>3 pulsadores · buzzer activo 5V<br>Jacks rojo y negro + puntas</div>
<div><b>Carga</b><br>Firmware 1.3.3 en 0x0<br>App 1.3 (APK)</div>
</div></div>
</div>
</div>
<div class="foot">Esquema completo, montaje en placa perforada y app: carpeta multimetro-esp32/docs del repositorio.</div>
</div></body></html>"""
open(OUT, "w", encoding="utf-8").write(html)
print("ok", OUT)
