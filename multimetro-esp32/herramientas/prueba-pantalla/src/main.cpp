// Diagnostico de la ESP32-C3 SuperMini con OLED 0.42".
// 1) El LED azul (GPIO 8) parpadea: el programa esta corriendo.
// 2) Busca dispositivos I2C en varios pares de pines y lo informa por el puerto serie (115200).
// 3) Si encuentra la pantalla (0x3C/0x3D), dibuja un marco, "OK" y un contador.
#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

static const int PAIRS[][2] = {{5, 6}, {6, 5}, {8, 9}, {9, 8}, {4, 5}, {3, 4}, {0, 1}};
static U8G2 *disp = nullptr;
static int foundSda = -1, foundScl = -1, foundAddr = 0;

static void scan() {
  for (auto &p : PAIRS) {
    Wire.end();
    Wire.begin(p[0], p[1]);
    Wire.setClock(100000);
    Serial.printf("SDA=%d SCL=%d :", p[0], p[1]);
    int n = 0;
    for (uint8_t a = 1; a < 127; a++) {
      Wire.beginTransmission(a);
      if (Wire.endTransmission() == 0) {
        Serial.printf(" 0x%02X", a);
        n++;
        if ((a == 0x3C || a == 0x3D) && foundSda < 0) { foundSda = p[0]; foundScl = p[1]; foundAddr = a; }
      }
    }
    Serial.println(n ? "" : " (nada)");
  }
  Wire.end();
}

void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(115200);
  delay(1500);
  Serial.println("\n=== Diagnostico ESP32-C3 OLED 0.42 ===");
  Serial.printf("Chip %s rev %d, flash %u MB\n", ESP.getChipModel(), ESP.getChipRevision(), ESP.getFlashChipSize() / 1048576);
  scan();
  if (foundSda >= 0) {
    Serial.printf("Pantalla en 0x%02X (SDA=%d SCL=%d)\n", foundAddr, foundSda, foundScl);
    disp = new U8G2_SSD1306_72X40_ER_F_HW_I2C(U8G2_R0, U8X8_PIN_NONE, foundScl, foundSda);
    disp->setI2CAddress(foundAddr << 1);
    disp->begin();
    disp->setContrast(255);
  } else {
    Serial.println("No se encontro la pantalla en ningun par de pines.");
  }
}

void loop() {
  static uint32_t n = 0;
  digitalWrite(8, (n & 1) ? HIGH : LOW);  // parpadeo del LED azul
  if (disp) {
    disp->clearBuffer();
    disp->drawFrame(0, 0, 72, 40);
    disp->setFont(u8g2_font_6x10_tf);
    disp->drawStr(4, 12, "OK  OLED");
    char b[16];
    snprintf(b, sizeof(b), "SDA%d SCL%d", foundSda, foundScl);
    disp->drawStr(4, 24, b);
    snprintf(b, sizeof(b), "%lu", (unsigned long)n);
    disp->drawStr(4, 36, b);
    disp->sendBuffer();
  }
  if (n % 10 == 0) {
    Serial.printf("vivo %lu  pantalla=%s\n", (unsigned long)n, disp ? "si" : "no");
    if (!disp && n % 50 == 0) scan();
  }
  n++;
  delay(500);
}
