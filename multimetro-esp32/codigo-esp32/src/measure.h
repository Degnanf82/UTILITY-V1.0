// Mediciones: voltaje, corriente, resistencia, continuidad, diodo, capacitancia, frecuencia.
#pragma once
#include <Arduino.h>

enum Mode : uint8_t { M_DCV = 0, M_DCA, M_OHM, M_CONT, M_DIODE, M_CAP, M_FREQ, M_COUNT };

struct Calib {
  float kV = 1.0f;        // factor de voltaje
  float kI = 1.0f;        // factor de corriente
  float rRef[4] = {1030.0f, 10030.0f, 100030.0f, 1000030.0f};  // ref efectivas (incluye ~30 Ohm del GPIO)
  float kC[2] = {1.0f, 1.0f};  // factor de capacitancia por rango (1M, 1k)
  float vcc = 3.30f;           // voltaje real del riel de 3.3 V
};

struct Reading {
  float value = 0;     // en unidad base SI (V, A, Ohm, F, Hz)
  bool ol = false;     // fuera de rango
  bool valid = false;  // false = sin dato todavia
  int8_t range = -1;   // rango usado (indice de referencia / rango de capacitancia)
  float aux = 0;       // dato extra: corriente del diodo (A)
  bool ext = false;    // hay voltaje externo en la punta (modos de Ohm)
};

extern Calib cal;
extern const char *MODE_NAMES[M_COUNT];
extern const char *MODE_UNITS[M_COUNT];

bool measureBegin();
void measureSetMode(Mode m);    // prepara el hardware para el modo (pone todo en alta impedancia)
Reading measureOnce(Mode m);    // toma una lectura del modo actual (puede tardar en CAP)
// Boton pulsado segun el voltaje de A3: 0 = ninguno, 1 = MODO, 2 = HOLD, 3 = REL.
int measureButtons();
// true si el modo usa el rele K1 (punta roja al nodo X).
bool modeUsesOhmRelay(Mode m);
void calLoad();
void calSave();
void calReset();
// Ajusta la calibracion del modo con un valor real conocido. measured = ultima lectura sin REL.
bool calApply(Mode m, const Reading &last, float realValue);
