#include "measure.h"
#include "config.h"
#include <Adafruit_ADS1X15.h>
#include <Preferences.h>
#include <math.h>

Calib cal;
const char *MODE_NAMES[M_COUNT] = {"DCV", "DCA", "OHM", "CONT", "DIODE", "CAP", "FREQ"};
const char *MODE_UNITS[M_COUNT] = {"V", "A", "ohm", "ohm", "V", "F", "Hz"};

static Adafruit_ADS1115 ads;
static const uint8_t REF_PINS[4] = {PIN_REF_1K, PIN_REF_10K, PIN_REF_100K, PIN_REF_1M};
static int8_t ohmRange = 1;  // rango actual de resistencia (histeresis del autorango)

// ---------------------------------------------------------------- ADS1115
// Impedancia de entrada en modo comun del ADS1115 segun ganancia (valores tipicos del datasheet).
// Afecta al divisor de voltaje y a resistencias altas; se compensa en el calculo.
static float zinForGain(adsGain_t g) {
  switch (g) {
    case GAIN_TWOTHIRDS: return 10e6f;
    case GAIN_ONE: return 6e6f;
    case GAIN_TWO: return 6e6f;
    case GAIN_FOUR: return 3e6f;
    default: return 100e6f;
  }
}

// Lee un canal en modo simple con ganancia automatica y promedia n muestras.
static float readAuto(uint8_t ch, int n, adsGain_t *gainOut = nullptr) {
  ads.setGain(GAIN_ONE);  // +-4.096 V (la entrada nunca supera 3.3 V)
  float v = ads.computeVolts(ads.readADC_SingleEnded(ch));
  float a = fabsf(v);
  adsGain_t g = GAIN_ONE;
  if (a < 0.23f) g = GAIN_SIXTEEN;
  else if (a < 0.46f) g = GAIN_EIGHT;
  else if (a < 0.93f) g = GAIN_FOUR;
  else if (a < 1.9f) g = GAIN_TWO;
  ads.setGain(g);
  float sum = 0;
  for (int i = 0; i < n; i++) sum += ads.computeVolts(ads.readADC_SingleEnded(ch));
  if (gainOut) *gainOut = g;
  return sum / n;
}

static float readVcc() { return cal.vcc; }

int measureButtons() {
  ads.setGain(GAIN_ONE);
  float v = ads.computeVolts(ads.readADC_SingleEnded(CH_BTN));
  if (v < BTN_TH_MODE) return 1;
  if (v < BTN_TH_HOLD) return 2;
  if (v < BTN_TH_REL) return 3;
  return 0;
}

bool modeUsesOhmRelay(Mode m) { return m == M_OHM || m == M_CONT || m == M_DIODE || m == M_CAP; }

// ---------------------------------------------------------------- Reles
static int8_t relayState = -1;  // 0 = V, 1 = Ohm, 2 = mA
static void setRelays(int8_t want) {
  if (want == relayState) return;
  // Primero se abren los dos (nunca quedan ambos cerrados), luego se cierra el pedido.
  digitalWrite(PIN_RELAY_OHM, LOW);
  digitalWrite(PIN_RELAY_MA, LOW);
  delay(RELAY_MS);
  if (want == 1) digitalWrite(PIN_RELAY_OHM, HIGH);
  if (want == 2) digitalWrite(PIN_RELAY_MA, HIGH);
  if (want != 0) delay(RELAY_MS);
  relayState = want;
}

// ---------------------------------------------------------------- Nodo X
static void allRefsOff() {
  for (uint8_t p : REF_PINS) pinMode(p, INPUT);
  pinMode(PIN_DISCHARGE, INPUT);
}

static void driveRef(int idx) {
  allRefsOff();
  pinMode(REF_PINS[idx], OUTPUT);
  digitalWrite(REF_PINS[idx], HIGH);
}

static void discharge(bool on) {
  if (on) {
    pinMode(PIN_DISCHARGE, OUTPUT);
    digitalWrite(PIN_DISCHARGE, LOW);
  } else {
    pinMode(PIN_DISCHARGE, INPUT);
  }
}

// ---------------------------------------------------------------- Frecuencia
static volatile uint32_t fCount = 0;
static volatile uint32_t fFirst = 0, fLast = 0;
static uint32_t gateStart = 0;
static void IRAM_ATTR freqIsr() {
  uint32_t t = micros();
  if (fCount == 0) fFirst = t;
  fLast = t;
  fCount++;
}

// ---------------------------------------------------------------- API
bool measureBegin() {
  pinMode(PIN_RELAY_OHM, OUTPUT);
  pinMode(PIN_RELAY_MA, OUTPUT);
  setRelays(0);
  allRefsOff();
  pinMode(PIN_X_SENSE, INPUT);
  analogReadResolution(12);
  analogSetPinAttenuation(PIN_X_SENSE, ADC_11db);
  pinMode(PIN_FREQ, INPUT);
  if (!ads.begin(ADS_ADDR)) return false;
  ads.setDataRate(RATE_ADS1115_860SPS);
  return true;
}

void measureSetMode(Mode m) {
  detachInterrupt(digitalPinToInterrupt(PIN_FREQ));
  allRefsOff();
  setRelays(modeUsesOhmRelay(m) ? 1 : (m == M_DCA ? 2 : 0));
  if (m == M_CONT || m == M_DIODE) driveRef(0);  // 1k: unos 2.5 mA
  if (m == M_OHM) driveRef(ohmRange);
  if (m == M_FREQ) {
    fCount = 0;
    gateStart = millis();
    attachInterrupt(digitalPinToInterrupt(PIN_FREQ), freqIsr, RISING);
  }
}

static Reading readVoltage() {
  Reading r;
  adsGain_t g;
  float vn = readAuto(CH_VOLT, 16, &g);
  float rb = 1.0f / (1.0f / DIV_BOTTOM + 1.0f / zinForGain(g));  // 100k en paralelo con el ADS
  r.value = vn * (DIV_TOP + rb) / rb * cal.kV;
  r.ol = vn > 3.45f;
  r.valid = true;
  return r;
}

static Reading readCurrent() {
  Reading r;
  float vs = readAuto(CH_SHUNT, 16);
  r.value = vs / SHUNT_OHMS * cal.kI;
  r.ol = r.value > MAX_AMPS;
  r.valid = true;
  return r;
}

// Resistencia con la referencia idx: R = Rref * Vx / (Vcc - Vx), corrigiendo la carga del ADS.
static float lastVx = 0;
// Nuestro circuito nunca lleva el nodo por encima de Vcc ni por debajo de 0: si pasa, es voltaje externo.
static bool externalVoltage(float vx, float vcc) { return vx > vcc + 0.12f || vx < -0.08f; }

static float ohmsWith(int idx, float vcc, float *ratio) {
  adsGain_t g;
  float vx = readAuto(CH_X, 8, &g);
  lastVx = vx;
  *ratio = vx / vcc;
  if (vx >= vcc * 0.995f) return INFINITY;
  float r = cal.rRef[idx] * vx / (vcc - vx);
  float zin = zinForGain(g);
  if (r < zin * 0.9f) r = 1.0f / (1.0f / r - 1.0f / zin);
  else return INFINITY;
  return r < 0 ? 0 : r;
}

static Reading readOhms() {
  Reading r;
  float vcc = readVcc();
  float ratio;
  float rx = ohmsWith(ohmRange, vcc, &ratio);
  // Autorango: la mejor precision se da con Rref parecida a Rx (relacion cerca de 0.5).
  int best = ohmRange;
  if (isinf(rx)) best = 3;
  else {
    float bestErr = 1e9;
    for (int i = 0; i < 4; i++) {
      float e = fabsf(log10f((rx + 0.01f) / cal.rRef[i]));
      if (e < bestErr) { bestErr = e; best = i; }
    }
  }
  // Histeresis: solo cambia si la relacion esta lejos del centro.
  if (best != ohmRange && (ratio < 0.15f || ratio > 0.85f || isinf(rx))) {
    ohmRange = best;
    driveRef(ohmRange);
    delay(3);
    rx = ohmsWith(ohmRange, vcc, &ratio);
  }
  r.range = ohmRange;
  r.ext = externalVoltage(lastVx, vcc);
  r.ol = isinf(rx) || rx > 30e6f;
  r.value = r.ol ? 0 : rx;
  r.valid = true;
  return r;
}

static Reading readContinuity() {
  Reading r;
  float vcc = readVcc();
  float ratio;
  float rx = ohmsWith(0, vcc, &ratio);
  r.ext = externalVoltage(lastVx, vcc);
  r.ol = isinf(rx) || rx > 2000.0f;
  r.value = r.ol ? 0 : rx;
  r.range = 0;
  r.valid = true;
  return r;
}

static Reading readDiode() {
  Reading r;
  float vcc = readVcc();
  float vf = readAuto(CH_X, 8);
  r.ext = externalVoltage(vf, vcc);
  r.ol = vf > vcc * 0.95f;  // abierto o Vf mayor de lo que se puede medir
  r.value = r.ol ? 0 : vf;
  r.aux = (vcc - vf) / cal.rRef[0];
  r.valid = true;
  return r;
}

// Espera (con limite) a que el nodo X baje de limit mV.
static bool dischargeUntil(float limitMv, uint32_t timeoutMs) {
  allRefsOff();
  discharge(true);
  uint32_t t0 = millis();
  while (analogReadMilliVolts(PIN_X_SENSE) > limitMv) {
    if (millis() - t0 > timeoutMs) return false;
    feedLoopWDT();
    delay(2);
  }
  delay(5);
  return true;
}

// Mide el tiempo de carga entre V1 y V2 a traves de la referencia idx.
// C = t / (R * ln((Vcc - V1) / (Vcc - V2)))
static float chargeTime(int idx, float vcc, uint32_t timeoutUs, bool *timeout) {
  const float v1 = vcc * 100.0f;  // 10 % en mV
  const float v2 = vcc * 600.0f;  // 60 % en mV
  discharge(false);
  driveRef(idx);
  uint32_t start = micros(), tA = 0, lastYield = start;
  bool passedA = false;
  *timeout = false;
  while (true) {
    float mv = analogReadMilliVolts(PIN_X_SENSE);
    uint32_t now = micros();
    if (!passedA && mv >= v1) { tA = now; passedA = true; }
    if (passedA && mv >= v2) return (now - tA) * 1e-6f;
    if (now - start > timeoutUs) { *timeout = true; return 0; }
    // En cargas lentas cede la CPU (vigilancia de tareas) lejos de los umbrales.
    if (now - lastYield > 100000 && (passedA ? mv < v2 * 0.9f : mv < v1 * 0.9f)) {
      feedLoopWDT();
      delay(1);
      lastYield = micros();
    }
  }
}

static Reading readCap() {
  Reading r;
  r.valid = true;
  float vcc = readVcc();
  const float lnK = logf((1.0f - 0.10f) / (1.0f - 0.60f));
  struct { int ref; uint32_t timeoutUs; } ranges[2] = {{3, 1500000}, {0, 15000000}};
  for (int k = 0; k < 2; k++) {
    if (!dischargeUntil(vcc * 30.0f, 20000)) { r.ol = true; break; }  // < 3 % de Vcc
    bool to;
    float t = chargeTime(ranges[k].ref, vcc, ranges[k].timeoutUs, &to);
    if (!to) {
      r.value = t / (cal.rRef[ranges[k].ref] * lnK) * cal.kC[k];
      r.range = k;
      break;
    }
    if (k == 1) r.ol = true;
  }
  dischargeUntil(vcc * 30.0f, 20000);  // deja el capacitor descargado
  discharge(false);
  return r;
}

static Reading readFreq() {
  Reading r;
  // Ventana de 1 s; si hay pocos pulsos espera hasta 3 s (frecuencias bajas).
  uint32_t el = millis() - gateStart;
  if (el < 1000 || (fCount < 3 && el < 3000)) {
    r.valid = false;
    return r;
  }
  noInterrupts();
  uint32_t n = fCount, a = fFirst, b = fLast;
  fCount = 0;
  interrupts();
  gateStart = millis();
  r.valid = true;
  r.value = (n >= 2 && b != a) ? (n - 1) * 1e6f / (float)(b - a) : 0;
  return r;
}

Reading measureOnce(Mode m) {
  switch (m) {
    case M_DCV: return readVoltage();
    case M_DCA: return readCurrent();
    case M_OHM: return readOhms();
    case M_CONT: return readContinuity();
    case M_DIODE: return readDiode();
    case M_CAP: return readCap();
    case M_FREQ: return readFreq();
    default: return Reading();
  }
}

// ---------------------------------------------------------------- Calibracion
void calLoad() {
  Preferences p;
  p.begin("mm", true);
  cal.kV = p.getFloat("kv", cal.kV);
  cal.kI = p.getFloat("ki", cal.kI);
  char key[4] = "r0";
  for (int i = 0; i < 4; i++) { key[1] = '0' + i; cal.rRef[i] = p.getFloat(key, cal.rRef[i]); }
  cal.kC[0] = p.getFloat("c0", cal.kC[0]);
  cal.kC[1] = p.getFloat("c1", cal.kC[1]);
  cal.vcc = p.getFloat("vc", cal.vcc);
  p.end();
}

void calSave() {
  Preferences p;
  p.begin("mm", false);
  p.putFloat("kv", cal.kV);
  p.putFloat("ki", cal.kI);
  char key[4] = "r0";
  for (int i = 0; i < 4; i++) { key[1] = '0' + i; p.putFloat(key, cal.rRef[i]); }
  p.putFloat("c0", cal.kC[0]);
  p.putFloat("c1", cal.kC[1]);
  p.putFloat("vc", cal.vcc);
  p.end();
}

void calReset() {
  cal = Calib();
  Preferences p;
  p.begin("mm", false);
  p.clear();
  p.end();
}

bool calApply(Mode m, const Reading &last, float real) {
  if (!last.valid || last.ol || last.value == 0 || real <= 0) return false;
  float f = real / last.value;
  if (f < 0.5f || f > 2.0f) return false;  // proteccion contra valores absurdos
  switch (m) {
    case M_DCV: cal.kV *= f; break;
    case M_DCA: cal.kI *= f; break;
    case M_OHM:
      if (last.range < 0) return false;
      cal.rRef[last.range] *= f;
      break;
    case M_CAP:
      if (last.range < 0) return false;
      cal.kC[last.range] *= f;
      break;
    default: return false;
  }
  calSave();
  return true;
}
