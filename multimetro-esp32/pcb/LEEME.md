# PCB del multímetro DEGNANTECH (ESP32-C3 con OLED 0.42")

Placa de **2 capas, 84 × 100 mm**, con todas las piezas de agujero pasante (fáciles de soldar a mano).
La ESP32-C3, el ADS1115 y la OLED 0.96" opcional van **enchufados en tiras de pines hembra**.

| Archivo | Para qué |
|---|---|
| `multimetro_esp32c3_gerbers_JLCPCB.zip` | **Lo que se sube a JLCPCB / PCBWay** (cobre, máscara, serigrafía, contorno y taladros) |
| `vista-superior.png`, `vista-inferior.png` | Cómo se verá la placa (dibujada a partir de los Gerbers) |
| `BOM.csv` | Lista de piezas con referencias (R1, D3, Q2…) |
| `fuente/` | Scripts que generan la placa (colocación, ruteo, verificación y Gerbers) y huellas de KiCad |

## Verificación hecha antes de exportar

- Separación mínima entre cobres de redes distintas: **0.40 mm** (JLCPCB admite 0.13 mm).
- Las 33 redes conectadas por completo; ningún cobre a menos de 0.3 mm del borde ni cerca de los tornillos.
- Los Gerbers se volvieron a leer con un lector independiente (gerbonara) para dibujar las vistas.
- Pistas: 0.4 mm señales, 0.5–0.6 mm alimentación, 0.8 mm GND y **1.0 mm** en el camino de la corriente.
- Vías de 0.8 mm con agujero de 0.4 mm.

## Cómo pedirla en JLCPCB

1. Entra a jlcpcb.com → **Order now** → **Add gerber file** y sube el `.zip`.
2. Revisa que detecte **2 capas** y **84 × 100 mm**. Deja lo demás por defecto: FR-4, 1.6 mm, HASL, 1 oz.
3. Color de máscara a tu gusto. Cantidad mínima: 5 placas.
4. **No** pidas ensamblaje (PCBA): todas las piezas son de soldar a mano.

## Orden de soldado (de lo más bajo a lo más alto)

1. Resistencias (R1–R18 y RSH de 1 W).
2. Diodos: **la raya del diodo coincide con la raya dibujada** (pad cuadrado = cátodo).
   - D1, D2: 1N4148 · D3–D8: BAT85 · DZ1: zener 1N4729A.
3. C1 (cerámico 104) y RT1 (PTC).
4. Transistores Q1–Q3 (S9014): **la cara plana coincide con el dibujo**; patas E · B · C rotuladas.
5. Tiras de pines hembra: 2 × 1x8 (ESP32), 1 × 1x10 (ADS1115), 1 × 1x4 (OLED 0.96" opcional).
6. Pulsadores, buzzer (pata **+** en el pad cuadrado), clips del fusible, bornera y por último los relés.

## Cómo se enchufan los módulos

- **ESP32-C3 OLED 0.42":** con el **USB-C hacia el borde inferior** (dice «USB» en la placa). Los números de pin están rotulados.
- **ADS1115:** con el **cuerpo hacia abajo**, encima de las resistencias R8–R14, o sea girado 180°: el texto del módulo queda al revés.
  El orden de la placa es A3 … VDD de izquierda a derecha.
- **OLED 0.96" (opcional):** pines VCC · GND · SCL · SDA. Antes cámbiala a la dirección **0x3D**: mueve la resistencia de su parte
  trasera de «0x78» a «0x7A». El firmware la detecta sola.

## Antes de enchufar los módulos la primera vez

Con la placa soldada y **sin** módulos, revisa con un multímetro:

- **Que no haya corto:** entre V3 y GD, y entre V5 y GD de la tira del ESP32.
- **Continuidad entre bornera y relé:** borne **ROJA** con el pin central (COM) de K2.
