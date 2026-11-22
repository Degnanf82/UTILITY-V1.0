// Configuracion de pines y constantes del multimetro.
// Placa: ESP32-C3 Super Mini. Pines libres: 0-10, 20, 21.
//
// Solo dos puntas: ROJA (jack VΩmA) y NEGRA (COM = GND).
// Dos reles SPDT eligen a que circuito llega la punta roja:
//   K2 (mA)  comun = punta roja;  NA -> fusible -> shunt;  NC -> comun de K1
//   K1 (Ohm) comun = NC de K2;    NA -> PTC -> nodo X;      NC -> divisor V (+ frecuencia)
// Con los dos reles apagados (arranque, reset) la punta queda en voltaje: alta impedancia.
#pragma once
#include <Arduino.h>

// ---------- Bus I2C (ADS1115 0x48 + OLED 0x3C) ----------
#define PIN_SDA 8
#define PIN_SCL 9
#define ADS_ADDR 0x48
#define OLED_ADDR 0x3C

// ---------- Reles (via transistor NPN, activos en alto) ----------
#define PIN_RELAY_OHM 5  // K1: punta roja -> nodo X
#define PIN_RELAY_MA 6   // K2: punta roja -> shunt de corriente

// ---------- Nodo "X" (resistencia / diodo / capacitor / continuidad) ----------
#define PIN_REF_1K 10    // 1 kOhm   -> nodo X
#define PIN_REF_10K 3    // 10 kOhm  -> nodo X
#define PIN_REF_100K 1   // 100 kOhm -> nodo X
#define PIN_REF_1M 0     // 1 MOhm   -> nodo X
#define PIN_DISCHARGE 7  // 220 Ohm  -> nodo X (descarga de capacitores)
#define PIN_X_SENSE 4    // ADC del ESP32 al nodo X (por 1k) para tiempos rapidos

// ---------- Otros ----------
#define PIN_FREQ 20      // frecuencia: 100k desde el lado "V" de K1 + diodos de proteccion
#define PIN_BUZZER 21    // buzzer activo via transistor NPN
// GPIO 2 queda libre (es pin de arranque: no conectarle nada que lo baje).

// ---------- Canales del ADS1115 ----------
#define CH_VOLT 0        // A0: divisor 1M / 100k
#define CH_X 1           // A1: nodo X (por 1k)
#define CH_SHUNT 2       // A2: lado alto del shunt de 1 Ohm (shunt a GND)
#define CH_BTN 3         // A3: los 3 botones en escalera de resistencias

// Botones en A3: pull-up de 10k a 3.3 V y cada boton a GND con su resistencia.
//   MODO: directo (0 V)   HOLD: 10k (1.65 V)   REL: 33k (2.53 V)   sin pulsar: 3.3 V
#define BTN_TH_MODE 0.80f
#define BTN_TH_HOLD 2.10f
#define BTN_TH_REL 2.95f

// ---------- Valores nominales (se corrigen con calibracion) ----------
#define DIV_TOP 1000000.0f   // resistencia superior del divisor de voltaje
#define DIV_BOTTOM 100000.0f // resistencia inferior del divisor de voltaje
#define SHUNT_OHMS 1.0f      // 1 Ohm 1 W: rango hasta ~300 mA (fusible 315 mA)
#define MAX_AMPS 0.35f
#define RELAY_MS 25          // tiempo de conmutacion y rebote de los reles

// ---------- WiFi (modo punto de acceso) ----------
#define WIFI_PASS "12345678"  // minimo 8 caracteres
#define TCP_PORT 3333

// ---------- BLE (servicio estilo Nordic UART) ----------
#define BLE_SERVICE_UUID "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
#define BLE_RX_UUID "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  // app -> equipo (write)
#define BLE_TX_UUID "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  // equipo -> app (notify)

#define FW_VERSION "1.1"
