# Multímetro ESP32-C3 + ADS1115 + OLED, con app Android (Bluetooth y WiFi)

Multímetro de banco para electrónica de **baja tensión DC**. La lectura sale en la
pantalla OLED y en el teléfono, conectado por **Bluetooth LE** o por **WiFi**.

| Función | Rango aprox. | Entrada |
|---|---|---|
| Voltaje DC | 0 – 40 V | jack **V** |
| Corriente DC | 0 – 2.5 A (shunt en el lado de GND) | jack **A** |
| Resistencia (autorango 1k/10k/100k/1M) | 1 Ω – 10 MΩ | jack **Ω** |
| Continuidad (pita por debajo de 30 Ω) | — | jack **Ω** |
| Prueba de diodos (unos 2.5 mA) | Vf hasta ~3 V | jack **Ω** |
| Capacitancia (tiempo de carga RC, 2 rangos) | ~1 nF – 10 000 µF | jack **Ω** |
| Frecuencia (onda cuadrada de 3.3 V) | ~1 Hz – ~100 kHz | jack **F** |

La app muestra la lectura grande, MIN/MAX/promedio, una gráfica en vivo, HOLD y REL,
graba a CSV, pita en continuidad y sirve para calibrar.

> ⚠️ **Seguridad.** Sin aislamiento ni categoría CAT. **Nunca** medir 110/220 V AC
> ni nada conectado a la red eléctrica. Úsalo solo con baterías, fuentes de laboratorio y
> circuitos de hasta 40 V DC. No midas voltaje en el jack Ω.

---

## Archivos

```
multimetro-esp32/
├── binarios/
│   ├── Multimetro-v1.0.apk                      ← instalar en el teléfono
│   └── multimetro-firmware-v1.0-completo.bin    ← firmware completo (dirección 0x0)
├── codigo-esp32/    firmware (PlatformIO / Arduino)
└── android/         código de la app (Kotlin, sin librerías externas)
```

Con cada cambio en esta carpeta, GitHub Actions vuelve a compilar la APK y el firmware
(pestaña **Actions → Artifacts**).

---

## Materiales

| Cant. | Componente | Uso |
|---|---|---|
| 1 | ESP32-C3 Super Mini | microcontrolador, BLE y WiFi |
| 1 | ADS1115 | ADC de 16 bits |
| 1 | OLED SSD1306 0.96" I2C (128×64) | pantalla |
| 1 | 1 MΩ 1 % + 1 | 100 kΩ 1 % | divisor de voltaje (÷11) |
| 1 | Shunt 0.1 Ω 1 %, 1 W o más | corriente |
| 1 c/u | 1 kΩ, 10 kΩ, 100 kΩ, 1 MΩ al 1 % | referencias de Ω, diodo y capacitancia |
| 1 | 220 Ω | descarga de capacitores |
| 3 | 10 kΩ | pull-up del botón REL, serie de la entrada F, base del transistor (1 k también sirve) |
| 6 | Diodos Schottky BAT85 / BAT43 / 1N5819 | protección de entradas (pares a 3.3 V y a GND) |
| 1 | Fusible rápido de 3 A o polifusible | protección del shunt |
| 1 | Polifusible de 50–100 mA (opcional) | protección del jack Ω |
| 3 | Pulsadores | MODO, HOLD, REL |
| 1 | Buzzer **activo** de 3–5 V + transistor NPN (2N2222/S8050) + 1 kΩ | pitido |
| 1 | Capacitor 100 nF | desacople del ADS1115 |
| — | Jacks banana o bornes: COM, V, A, Ω, F | puntas |

---

## Conexiones

### Bus I2C y alimentación

| ESP32-C3 | ADS1115 | OLED |
|---|---|---|
| 3.3 | VDD | VCC |
| G | GND **y ADDR** (dirección 0x48) | GND |
| GPIO 8 | SDA | SDA |
| GPIO 9 | SCL | SCL |

El ADS1115 y la OLED ya traen resistencias pull-up de I2C. Pon el capacitor de 100 nF entre VDD y GND del ADS1115.

### Mapa de pines del ESP32-C3

| GPIO | Función |
|---|---|
| 0 | referencia **1 MΩ** → nodo X |
| 1 | referencia **100 kΩ** → nodo X |
| 3 | referencia **10 kΩ** → nodo X |
| 10 | referencia **1 kΩ** → nodo X |
| 7 | **220 Ω** → nodo X (descarga) |
| 4 | directo al nodo X (ADC rápido para capacitancia) |
| 5 | botón MODO (a GND) |
| 6 | botón HOLD (a GND) |
| 2 | botón REL (a GND) **+ pull-up externo de 10 kΩ a 3.3 V** (pin de arranque) |
| 20 | entrada de frecuencia (por 10 kΩ en serie) |
| 21 | buzzer (1 kΩ a la base del NPN) |
| 8 / 9 | I2C SDA / SCL |

### Esquema de entradas

```
            JACK V                                    ADS1115
   V ───[1M]───┬──────────────────────────────────── A0
               │        ┌─|>|─ 3.3V   (Schottky: cátodo a 3.3V)
              [100k]    ├─|<|─ GND    (Schottky: ánodo a GND)
               │        (los dos diodos van en el nodo A0)
   COM ────────┴── GND


            JACK A  (corriente: la carga va entre la fuente y el jack A)
   A ──[FUSIBLE 3A]──┬──────────────────────────────── A2
                    [0.1Ω]  shunt
   COM ──────────────┴── GND  (cable corto y grueso hasta el GND del ADS)


            JACK Ω  = "nodo X"
   GPIO10 ─[1k]───┐
   GPIO3  ─[10k]──┤
   GPIO1  ─[100k]─┤
   GPIO0  ─[1M]───┼──────────────┬───────────────── A1 (ADS1115)
   GPIO7  ─[220]──┤              └───────────────── GPIO4 (ESP32)
                  ├─|>|─ 3.3V   ┐ protección
                  ├─|<|─ GND    ┘
   Ω ──[polifusible opcional]─┘
   COM ── GND


            Referencia ratiométrica
   3.3V ────────────────────────────────────────── A3


            JACK F (frecuencia)
   F ──[10k]──┬───────────────────────────────── GPIO20
              ├─|>|─ 3.3V
              └─|<|─ GND


            Buzzer activo
   GPIO21 ─[1k]── base NPN;  emisor → GND;  colector → (−) buzzer;  (+) buzzer → 5V
```

**Puntas:** la negra siempre en **COM**. La roja va en **V**, **A**, **Ω** o **F** según la función.

---

## 1. Cargar el firmware al ESP32-C3

**Opción A, binario listo (sin programar nada):**
1. En la PC abre <https://espressif.github.io/esptool-js/> en Chrome o Edge.
2. Conecta la placa por USB-C. Si no aparece, mantén **BOOT**, pulsa **RST** y suelta BOOT.
3. **Connect**, dirección **0x0**, elige `binarios/multimetro-firmware-v1.0-completo.bin` y pulsa **Program**.
4. Pulsa **RST**. La OLED muestra el nombre `Multimetro-XXXX` y la clave WiFi.

**Opción B, compilar con PlatformIO:**
```bash
cd multimetro-esp32/codigo-esp32
pio run -t upload        # compila y sube
pio device monitor       # ve las lecturas en JSON (115200)
```

## 2. Instalar la app

Copia `binarios/Multimetro-v1.0.apk` al teléfono e instálala (Android 7 o superior). Tendrás
que permitir la instalación de *orígenes desconocidos*. Al actualizar con una APK compilada en
otra máquina (por ejemplo, la de GitHub Actions), primero desinstala la anterior, porque cambia la firma de depuración.

## 3. Conectar

- **Bluetooth:** botón **Bluetooth** → acepta permisos → elige `Multimetro-XXXX`.
  En Android 11 o menos hay que tener la Ubicación activada para buscar.
- **WiFi:** botón **WiFi** → **Unirme a su red** (Android 10+). El sistema pide confirmar la red
  `Multimetro-XXXX` (clave `12345678`). Otra forma: conéctate a esa red desde los Ajustes
  y pulsa **Ya estoy en su red**. La IP es `192.168.4.1` y el puerto `3333`.

Se puede usar Bluetooth y WiFi a la vez (por ejemplo, dos teléfonos).

---

## Botones del equipo

| Botón | Pulsación corta | Pulsación larga (>0.8 s) |
|---|---|---|
| MODO | siguiente función | función anterior |
| HOLD | congela/descongela la lectura | borra MIN/MAX |
| REL | toma la lectura actual como cero (relativo) | muestra los datos de conexión 5 s |

En la OLED, arriba a la derecha: **H** = HOLD, **R** = REL, **B** = Bluetooth conectado, **W** = WiFi conectado.

## Consejos de medición

- **Resistencias bajas:** junta las puntas en modo Ω y pulsa **REL**. Así resta la resistencia de los cables.
- **Capacitores pequeños:** en modo capacitor, sin nada conectado, pulsa **REL** para restar la capacitancia de los cables.
  **Descarga** siempre el capacitor antes de medirlo. Los electrolíticos van con el **+ en Ω** y el − en COM.
  Uno de 1000 µF tarda unos segundos en medirse.
- **Diodos:** ánodo en Ω, cátodo en COM. LED rojo ≈ 1.8 V; los LED azules o blancos (~3 V) pueden marcar ABIERTO.
- **Corriente:** el amperímetro va **en serie**, en el lado negativo de la carga. Si conectas el jack A directo a una fuente, la pones en cortocircuito.
- **Voltaje negativo:** no se mide (marca 0). Invierte las puntas.

## Calibración (recomendado)

En la app: **Calibrar**. Mide algo de valor conocido, escribe el valor real (acepta `5.00`,
`10k`, `100n`…) y pulsa **Calibrar**. El factor queda guardado en el ESP32.
- **V:** una fuente medida con un multímetro de referencia.
- **A:** una carga con corriente conocida.
- **Ω:** calibra cada rango con una resistencia de 1 % cercana a 1k, 10k, 100k y 1M.
- **Capacitor:** un capacitor de film conocido (por ejemplo 100 nF para el rango 1M y 10 µF para el rango 1k).

**Restaurar fábrica** borra la calibración.

---

## Protocolo (para quien quiera extenderlo)

Son líneas de texto terminadas en `\n`, por BLE (servicio Nordic UART `6e400001-…`, RX `…0002`,
TX `…0003`), por TCP en el puerto 3333 o por el puerto serie USB.

El equipo envía unas 10 veces por segundo:
```json
{"t":"m","m":"DCV","u":"V","v":12.345,"ol":0,"h":0,"rel":0,"r":-1,"mn":12.3,"mx":12.4,"av":12.35}
```
Otros mensajes: `{"t":"info",...}`, `{"t":"cal",...}` y `{"t":"msg","s":"..."}`.

Comandos que acepta: `MODE DCV|DCA|OHM|CONT|DIODE|CAP|FREQ`, `HOLD [0|1]`, `REL [0|1]`, `RESET`,
`BEEP 0|1`, `CAL <valor real>`, `CALGET`, `CALSET <kv|ki|r0..r3|c0|c1> <valor>`, `CALRESET`, `INFO`.

## Limitaciones conocidas

- La precisión depende de las resistencias (usa 1 %) y de calibrar. Esperable: ±0.5–1 % en V y Ω, ±2–3 % en capacitancia.
- La corriente se mide solo en el lado de GND (el ADS1115 no acepta voltajes de modo común altos).
- No hay medición de AC ni de hFE (no quedan pines libres en el C3 Super Mini).
- Algunas OLED de 0.96" vienen con controlador SH1106 en vez de SSD1306. Si la imagen se ve corrida 2 píxeles, avisa y se cambia la librería.
