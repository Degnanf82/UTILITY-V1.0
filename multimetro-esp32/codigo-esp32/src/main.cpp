// Multimetro ESP32-C3 Super Mini + ADS1115 + OLED SSD1306 0.96"
// Funciones: DCV, DCA, Ohm (autorango), continuidad, diodo, capacitancia, frecuencia.
// Solo dos puntas (roja y negra); dos reles eligen el circuito segun la funcion.
// Conexion con la app Android por Bluetooth LE y por WiFi (punto de acceso + TCP 3333).
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>
#include <math.h>

#include "comms.h"
#include "config.h"
#include "measure.h"

static Adafruit_SSD1306 oled(128, 64, &Wire, -1);
static bool oledOk = false, adsOk = false;

static Mode mode = M_DCV;
static bool hold = false, relOn = false, beepOn = true;
static float relValue = 0;
static Reading last;       // ultima lectura sin REL (para calibrar)
static float shown = 0;    // valor mostrado (con REL, congelado con HOLD)
static bool shownOl = false, shownValid = false;
static float vMin, vMax, vSum;
static uint32_t vCount;
static uint32_t beepUntil = 0, infoUntil = 0;
static String devName;
static String warnText;
static uint32_t warnUntil = 0;
static void sendMsg(const String &m);

// ---------------------------------------------------------------- utilidades
static void resetStats() {
  vMin = INFINITY;
  vMax = -INFINITY;
  vSum = 0;
  vCount = 0;
}

static void beep(uint16_t ms) {
  uint32_t until = millis() + ms;
  if (beepOn && until > beepUntil) beepUntil = until;
}

static String num(float v) {
  if (isinf(v) || isnan(v)) return "null";
  char b[20];
  snprintf(b, sizeof(b), "%.6g", v);
  return b;
}

// Convierte a texto con prefijo SI: 0.00123 V -> "1.230" "m"
static void formatSI(float v, String &txt, String &prefix) {
  static const char *P[] = {"p", "n", "u", "m", "", "k", "M"};
  int e = 0;
  float a = fabsf(v);
  if (a > 0) e = (int)floorf(log10f(a) / 3.0f);
  if (e < -4) e = -4;
  if (e > 2) e = 2;
  float m = v / powf(1000.0f, e);
  float am = fabsf(m);
  char b[16];
  if (am < 9.9995f) snprintf(b, sizeof(b), "%.3f", m);
  else if (am < 99.995f) snprintf(b, sizeof(b), "%.2f", m);
  else snprintf(b, sizeof(b), "%.1f", m);
  txt = b;
  prefix = P[e + 4];
}

static const char *modeLabel(Mode m) {
  static const char *L[M_COUNT] = {"DC V", "CORRIENTE", "OHM", "CONTINUIDAD", "DIODO", "CAPACITOR", "FRECUENCIA"};
  return L[m];
}

static String unitLabel(Mode m) {
  switch (m) {
    case M_DCV: case M_DIODE: return "V";
    case M_DCA: return "A";
    case M_OHM: case M_CONT: return String((char)234);  // Omega en la fuente cp437
    case M_CAP: return "F";
    default: return "Hz";
  }
}

static void warn(const String &t) {
  warnText = t;
  warnUntil = millis() + 3000;
  beep(400);
  sendMsg(t);
}

static void setMode(Mode m) {
  // Antes de conectar la punta roja al nodo X, comprueba que no haya voltaje en las puntas.
  if (adsOk && modeUsesOhmRelay(m) && !modeUsesOhmRelay(mode)) {
    measureSetMode(M_DCV);
    delay(30);
    Reading v = measureOnce(M_DCV);
    if (v.valid && (v.ol || fabsf(v.value) > 1.0f)) {
      m = M_DCV;
      warn("Hay voltaje en las puntas: retiralas antes de medir Ohm/diodo/capacitor");
    }
  }
  mode = m;
  hold = false;
  relOn = false;
  relValue = 0;
  shownValid = false;
  last = Reading();
  resetStats();
  measureSetMode(m);
  beep(15);
}

// ---------------------------------------------------------------- mensajes a la app
static void sendInfo() {
  String s = "{\"t\":\"info\",\"fw\":\"" FW_VERSION "\",\"name\":\"" + devName + "\",\"ssid\":\"" +
             commsSsid() + "\",\"pass\":\"" WIFI_PASS "\",\"ip\":\"" + commsIp() + "\",\"port\":" +
             String(TCP_PORT) + ",\"beep\":" + (beepOn ? "1" : "0") + ",\"ads\":" + (adsOk ? "1" : "0") + "}";
  commsSend(s);
}

static void sendCal() {
  String s = "{\"t\":\"cal\",\"kv\":" + num(cal.kV) + ",\"ki\":" + num(cal.kI) + ",\"vcc\":" + num(cal.vcc) + ",\"r\":[";
  for (int i = 0; i < 4; i++) s += num(cal.rRef[i]) + (i < 3 ? "," : "");
  s += "],\"kc\":[" + num(cal.kC[0]) + "," + num(cal.kC[1]) + "]}";
  commsSend(s);
}

static void sendMsg(const String &m) { commsSend("{\"t\":\"msg\",\"s\":\"" + m + "\"}"); }

static void sendReading() {
  String s = "{\"t\":\"m\",\"m\":\"";
  s += MODE_NAMES[mode];
  s += "\",\"u\":\"";
  s += MODE_UNITS[mode];
  s += "\",\"v\":" + (shownValid && !shownOl ? num(shown) : String("null"));
  s += ",\"ol\":" + String(shownOl ? 1 : 0);
  s += ",\"h\":" + String(hold ? 1 : 0);
  s += ",\"rel\":" + String(relOn ? 1 : 0);
  s += ",\"r\":" + String(last.range);
  if (vCount > 0) s += ",\"mn\":" + num(vMin) + ",\"mx\":" + num(vMax) + ",\"av\":" + num(vSum / vCount);
  if (mode == M_DIODE && last.valid && !last.ol) s += ",\"x\":" + num(last.aux);
  s += "}";
  commsSend(s);
}

// ---------------------------------------------------------------- comandos
// MODE <DCV|DCA|OHM|CONT|DIODE|CAP|FREQ> | HOLD [0|1] | REL [0|1] | RESET | BEEP 0|1
// CAL <valor real> | CALGET | CALSET <kv|ki|r0..r3|c0|c1> <valor> | CALRESET | INFO
static void handleCommand(String c) {
  c.trim();
  int sp = c.indexOf(' ');
  String cmd = (sp < 0 ? c : c.substring(0, sp));
  String arg = (sp < 0 ? "" : c.substring(sp + 1));
  cmd.toUpperCase();
  arg.trim();

  if (cmd == "MODE") {
    arg.toUpperCase();
    for (int i = 0; i < M_COUNT; i++)
      if (arg == MODE_NAMES[i]) { setMode((Mode)i); return; }
    sendMsg("Modo desconocido");
  } else if (cmd == "HOLD") {
    hold = arg.isEmpty() ? !hold : arg.toInt() != 0;
  } else if (cmd == "REL") {
    bool want = arg.isEmpty() ? !relOn : arg.toInt() != 0;
    if (want && last.valid && !last.ol) { relValue = last.value; relOn = true; }
    else relOn = false;
    resetStats();
  } else if (cmd == "RESET") {
    resetStats();
  } else if (cmd == "BEEP") {
    beepOn = arg.toInt() != 0;
    sendInfo();
  } else if (cmd == "CAL") {
    float real = arg.toFloat();
    if (calApply(mode, last, real)) { sendMsg("Calibrado"); sendCal(); }
    else sendMsg("No se pudo calibrar (modo o lectura no valida)");
  } else if (cmd == "CALGET") {
    sendCal();
  } else if (cmd == "CALSET") {
    int sp2 = arg.indexOf(' ');
    String key = arg.substring(0, sp2);
    float v = arg.substring(sp2 + 1).toFloat();
    if (sp2 < 0 || v <= 0) { sendMsg("Uso: CALSET clave valor"); return; }
    key.toLowerCase();
    if (key == "kv") cal.kV = v;
    else if (key == "ki") cal.kI = v;
    else if (key.length() == 2 && key[0] == 'r' && key[1] >= '0' && key[1] <= '3') cal.rRef[key[1] - '0'] = v;
    else if (key == "c0") cal.kC[0] = v;
    else if (key == "c1") cal.kC[1] = v;
    else if (key == "vcc" && v > 3.0f && v < 3.6f) cal.vcc = v;
    else { sendMsg("Clave desconocida"); return; }
    calSave();
    sendCal();
  } else if (cmd == "CALRESET") {
    calReset();
    sendMsg("Calibracion de fabrica");
    sendCal();
  } else if (cmd == "INFO") {
    sendInfo();
  } else {
    sendMsg("Comando desconocido: " + cmd);
  }
}

// ---------------------------------------------------------------- botones
// Los 3 botones se leen por A3 del ADS1115 (escalera de resistencias).
struct Button {
  bool down = false, longDone = false;
  uint32_t since = 0;
};
static Button bMode, bHold, bRel;

// Devuelve 1 = pulsacion corta, 2 = larga (> longMs), 0 = nada.
static int pollButton(Button &b, bool pressed, uint32_t longMs = 900) {
  uint32_t now = millis();
  if (pressed && !b.down) {
    b.down = true; b.longDone = false; b.since = now;
  } else if (!pressed && b.down) {
    b.down = false;
    if (!b.longDone && now - b.since > 40) return 1;
  } else if (pressed && b.down && !b.longDone && now - b.since > longMs) {
    b.longDone = true;
    return 2;
  }
  return 0;
}

// Orden del boton MODO. mA no esta en el ciclo: se entra con pulsacion larga (evita cortos).
static const Mode CYCLE[] = {M_DCV, M_FREQ, M_OHM, M_CONT, M_DIODE, M_CAP};

static void handleButtons() {
  static uint32_t lastPoll = 0;
  static int stable = 0, cand = 0, candCount = 0;
  if (!adsOk || millis() - lastPoll < 25) return;
  lastPoll = millis();
  int raw = measureButtons();
  if (raw == cand) { if (candCount < 3) candCount++; } else { cand = raw; candCount = 1; }
  if (candCount >= 2) stable = cand;  // dos lecturas iguales seguidas

  int e;
  if ((e = pollButton(bMode, stable == 1, 1500)) == 1) {
    if (mode == M_DCA) setMode(M_DCV);
    else {
      int i = 0;
      while (i < 6 && CYCLE[i] != mode) i++;
      setMode(CYCLE[(i + 1) % 6]);
    }
  } else if (e == 2) {
    if (mode == M_DCA) setMode(M_DCV);
    else { setMode(M_DCA); warnText = "Puntas EN SERIE"; warnUntil = millis() + 2000; }
  }
  if ((e = pollButton(bHold, stable == 2)) == 1) { hold = !hold; beep(15); }
  else if (e == 2) { resetStats(); beep(60); }                         // largo: borra MIN/MAX
  if ((e = pollButton(bRel, stable == 3)) == 1) { handleCommand("REL"); beep(15); }
  else if (e == 2) { infoUntil = millis() + 5000; }                    // largo: datos WiFi/BT
}

// ---------------------------------------------------------------- pantalla
static void drawScreen(bool busy) {
  if (!oledOk) return;
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);

  if (millis() < warnUntil) {
    oled.setCursor(0, 0);
    oled.setTextSize(2);
    oled.println("ATENCION");
    oled.setTextSize(1);
    oled.println();
    oled.println(warnText);
    oled.display();
    return;
  }
  if (millis() < infoUntil) {
    oled.setCursor(0, 0);
    oled.println("CONEXION");
    oled.println("BT/WiFi: " + devName);
    oled.println("Clave: " WIFI_PASS);
    oled.println("IP: " + commsIp());
    oled.println("Puerto: " + String(TCP_PORT));
    oled.println("FW " FW_VERSION);
    oled.display();
    return;
  }

  oled.setCursor(0, 0);
  oled.print(modeLabel(mode));
  String flags;
  if (hold) flags += "H ";
  if (relOn) flags += "R ";
  if (commsBleConnected()) flags += "B";
  if (commsWifiConnected()) flags += "W";
  oled.setCursor(128 - flags.length() * 6, 0);
  oled.print(flags);
  oled.drawFastHLine(0, 10, 128, SSD1306_WHITE);

  String big, prefix;
  if (!adsOk && mode != M_FREQ && mode != M_CAP) {
    oled.setTextSize(2);
    oled.setCursor(0, 22);
    oled.print("SIN ADS");
  } else if (busy && !shownValid) {
    oled.setTextSize(2);
    oled.setCursor(0, 22);
    oled.print("Midiendo");
  } else if (!shownValid) {
    oled.setTextSize(3);
    oled.setCursor(0, 18);
    oled.print("----");
  } else if (shownOl) {
    oled.setTextSize(3);
    oled.setCursor(0, 18);
    oled.print(mode == M_CONT || mode == M_DIODE ? "OPEN" : "OL");
  } else {
    formatSI(shown, big, prefix);
    oled.setTextSize(3);
    oled.setCursor(0, 18);
    oled.print(big);
    oled.setTextSize(2);
    String u = prefix + unitLabel(mode);
    oled.setCursor(128 - u.length() * 12, 42);
    oled.print(u);
  }

  oled.setTextSize(1);
  oled.setCursor(0, 56);
  if (mode == M_DIODE && shownValid && !shownOl) {
    formatSI(last.aux, big, prefix);
    oled.print("If " + big + prefix + "A");
  } else if (vCount > 1) {
    String a, pa, b, pb;
    formatSI(vMin, a, pa);
    formatSI(vMax, b, pb);
    oled.print("^" + b + pb + " v" + a + pa);
  } else if (busy) {
    oled.print("...");
  }
  oled.display();
}

// ---------------------------------------------------------------- setup / loop
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);
  pinMode(PIN_RELAY_OHM, OUTPUT);  // reles apagados lo antes posible
  digitalWrite(PIN_RELAY_OHM, LOW);
  pinMode(PIN_RELAY_MA, OUTPUT);
  digitalWrite(PIN_RELAY_MA, LOW);
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);

  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(400000);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  if (oledOk) oled.cp437(true);

  calLoad();
  adsOk = measureBegin();

  uint64_t mac = ESP.getEfuseMac();  // bytes de la MAC en orden inverso
  char name[24];
  snprintf(name, sizeof(name), "Multimetro-%02X%02X", (uint8_t)(mac >> 32), (uint8_t)(mac >> 40));
  devName = name;
  commsBegin(name);

  resetStats();
  setMode(M_DCV);
  infoUntil = millis() + 2500;  // muestra los datos de conexion al encender
  drawScreen(false);
}

void loop() {
  static uint32_t lastSend = 0, lastDraw = 0;
  commsLoop();

  String c;
  while (commsNextCommand(c)) handleCommand(c);
  if (Serial.available()) handleCommand(Serial.readStringUntil('\n'));
  handleButtons();

  bool needAds = (mode != M_FREQ);
  if (!needAds || adsOk) {
    if (mode == M_CAP) drawScreen(true);  // la medicion puede tardar varios segundos
    Reading r = measureOnce(mode);
    if (r.valid && r.ext) {
      setMode(M_DCV);
      warn("Voltaje externo en la punta: cambiado a DC V");
    } else if (r.valid) {
      last = r;
      if (!hold) {
        shownOl = r.ol;
        shown = r.ol ? 0 : r.value - (relOn ? relValue : 0);
        shownValid = true;
        if (!r.ol) {
          vMin = fminf(vMin, shown);
          vMax = fmaxf(vMax, shown);
          vSum += shown;
          vCount++;
        }
      }
      // Continuidad: suena por debajo de 30 Ohm.
      if (mode == M_CONT) {
        bool on = beepOn && !r.ol && r.value < 30.0f;
        digitalWrite(PIN_BUZZER, on ? HIGH : LOW);
      }
    }
  } else {
    delay(50);
  }

  if (mode != M_CONT) digitalWrite(PIN_BUZZER, millis() < beepUntil ? HIGH : LOW);

  uint32_t now = millis();
  if (now - lastSend >= 100) { lastSend = now; sendReading(); }
  if (now - lastDraw >= 120) { lastDraw = now; drawScreen(false); }
}
