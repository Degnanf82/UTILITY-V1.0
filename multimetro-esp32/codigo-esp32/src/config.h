// Configuracion de pines y constantes del multimetro.
// Placa: ESP32-C3 con OLED 0.42" integrada (72x40, SSD1306, I2C en GPIO 5/6).
// Pines: izquierda 3,4,5,6,7,8,9,10 · derecha 0,1,2,TX(21),RX(20),3V3,GND,5V.
//
// Solo dos puntas: ROJA (jack VΩmA) y NEGRA (COM = GND).
// Dos reles SPDT eligen a que circuito llega la punta roja:
//   K2 (mA)  comun = punta roja;  NA -> fusible -> shunt;  NC -> comun de K1
//   K1 (Ohm) comun = NC de K2;    NA -> PTC -> nodo X;      NC -> divisor V (+ frecuencia)
// Con los dos reles apagados (arranque, reset) la punta queda en voltaje: alta impedancia.
#pragma once
#include <Arduino.h>

// ---------- Bus I2C (fijo en la placa: pantalla integrada + ADS1115) ----------
#define PIN_SDA 5
#define PIN_SCL 6
#define ADS_ADDR 0x48
#define OLED_ADDR 0x3C      // pantalla integrada 0.42" (72x40)
#define OLED_EXT_ADDR 0x3D  // OLED externa 0.96" opcional (cambiarla a 0x3D)

// ---------- Reles (via transistor NPN, activos en alto) ----------
#define PIN_RELAY_OHM 8  // K1: punta roja -> nodo X (comparte el LED azul de la placa)
#define PIN_RELAY_MA 10  // K2: punta roja -> shunt de corriente

// ---------- Nodo "X" (resistencia / diodo / capacitor / continuidad) ----------
#define PIN_REF_1K 0     // 1 kOhm   -> nodo X
#define PIN_REF_10K 1    // 10 kOhm  -> nodo X
#define PIN_REF_100K 3   // 100 kOhm -> nodo X
#define PIN_REF_1M 9     // 1 MOhm   -> nodo X (GPIO 9 = BOOT: el 1M no afecta el arranque)
#define PIN_DISCHARGE 7  // 220 Ohm  -> nodo X (descarga de capacitores)
#define PIN_X_SENSE 4    // ADC del ESP32 al nodo X (por 1k) para tiempos rapidos

// ---------- Otros ----------
#define PIN_FREQ 21      // TX: frecuencia, 100k desde el lado "V" de K1 + diodos de proteccion
#define PIN_BUZZER 20    // RX: buzzer activo via transistor NPN
// GPIO 2 queda libre (es pin de arranque: no conectarle nada).

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

#define FW_VERSION "1.2.1"
