// Configuracion de pines y constantes del multimetro.
// Placa: ESP32-C3 Super Mini. Pines libres: 0-10, 20, 21.
#pragma once
#include <Arduino.h>

// ---------- Bus I2C (ADS1115 0x48 + OLED 0x3C) ----------
#define PIN_SDA 8
#define PIN_SCL 9
#define ADS_ADDR 0x48
#define OLED_ADDR 0x3C

// ---------- Nodo "X" (jack Ohm / Diodo / Capacitor / Continuidad) ----------
// Cada pin maneja una resistencia de referencia hacia el nodo X.
#define PIN_REF_1K 10    // 1 kOhm   -> nodo X
#define PIN_REF_10K 3    // 10 kOhm  -> nodo X
#define PIN_REF_100K 1   // 100 kOhm -> nodo X
#define PIN_REF_1M 0     // 1 MOhm   -> nodo X
#define PIN_DISCHARGE 7  // 220 Ohm  -> nodo X (descarga de capacitores)
#define PIN_X_SENSE 4    // ADC del ESP32 conectado directo al nodo X (tiempos rapidos)

// ---------- Botones (a GND, con pull-up) ----------
#define PIN_BTN_MODE 5
#define PIN_BTN_HOLD 6
#define PIN_BTN_REL 2    // pin de arranque: lleva pull-up EXTERNO de 10k a 3.3V

// ---------- Otros ----------
#define PIN_FREQ 20      // entrada de frecuencia (10k serie + diodos de proteccion)
#define PIN_BUZZER 21    // buzzer activo via transistor NPN

// ---------- Canales del ADS1115 ----------
#define CH_VOLT 0        // A0: divisor 1M / 100k del jack V
#define CH_X 1           // A1: nodo X
#define CH_SHUNT 2       // A2: lado alto del shunt 0.1 Ohm (shunt a GND)
#define CH_VCC 3         // A3: riel de 3.3 V (referencia ratiometrica)

// ---------- Valores nominales (se corrigen con calibracion) ----------
#define DIV_TOP 1000000.0f   // resistencia superior del divisor de voltaje
#define DIV_BOTTOM 100000.0f // resistencia inferior del divisor de voltaje
#define SHUNT_OHMS 0.1f
#define R_DISCHARGE 220.0f

// ---------- WiFi (modo punto de acceso) ----------
#define WIFI_PASS "12345678"  // minimo 8 caracteres
#define TCP_PORT 3333

// ---------- BLE (servicio estilo Nordic UART) ----------
#define BLE_SERVICE_UUID "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
#define BLE_RX_UUID "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  // app -> equipo (write)
#define BLE_TX_UUID "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  // equipo -> app (notify)

#define FW_VERSION "1.0"
