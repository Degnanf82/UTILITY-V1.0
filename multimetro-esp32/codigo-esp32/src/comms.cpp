#include "comms.h"
#include "config.h"
#include <NimBLEDevice.h>  // NimBLE: mucho mas liviano que la pila Bluedroid
#include <WiFi.h>

// Cola de comandos: los callbacks BLE corren en otra tarea, el loop los procesa.
static QueueHandle_t cmdQueue;
struct Cmd { char text[96]; };

static void pushCommand(const String &s) {
  String t = s;
  t.trim();
  if (t.isEmpty()) return;
  Cmd c;
  strlcpy(c.text, t.c_str(), sizeof(c.text));
  xQueueSend(cmdQueue, &c, 0);
}

// ---------------------------------------------------------------- BLE
static NimBLEServer *server = nullptr;
static NimBLECharacteristic *txChar = nullptr;
static volatile bool bleConnected = false;
static volatile uint16_t bleConnId = 0;
static String bleRxBuf;

class ServerCb : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer *s, ble_gap_conn_desc *desc) override {
    bleConnId = desc->conn_handle;
    bleConnected = true;
  }
  void onDisconnect(NimBLEServer *s) override {
    bleConnected = false;
    NimBLEDevice::startAdvertising();
  }
};

class RxCb : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *c) override {
    String v = c->getValue().c_str();
    bleRxBuf += v;
    int nl;
    while ((nl = bleRxBuf.indexOf('\n')) >= 0) {
      pushCommand(bleRxBuf.substring(0, nl));
      bleRxBuf.remove(0, nl + 1);
    }
    // Comandos sin '\n' (escritos de una sola vez) tambien se aceptan.
    if (bleRxBuf.length() > 0 && bleRxBuf.length() < 90 && v.indexOf('\n') < 0) {
      pushCommand(bleRxBuf);
      bleRxBuf = "";
    }
    if (bleRxBuf.length() > 200) bleRxBuf = "";
  }
};

static void bleSend(const String &line) {
  if (!bleConnected || !txChar) return;
  String data = line + "\n";
  uint16_t mtu = server->getPeerMTU(bleConnId);
  size_t chunk = (mtu > 23) ? mtu - 3 : 20;
  if (chunk > 240) chunk = 240;
  for (size_t i = 0; i < data.length(); i += chunk) {
    String part = data.substring(i, i + chunk);
    txChar->setValue((uint8_t *)part.c_str(), part.length());
    txChar->notify();
    if (data.length() > chunk) delay(4);
  }
}

// ---------------------------------------------------------------- WiFi / TCP
static WiFiServer tcpServer(TCP_PORT);
static WiFiClient tcpClient;
static String tcpRxBuf;
static String ssid;

void commsBegin(const char *deviceName) {
  cmdQueue = xQueueCreate(8, sizeof(Cmd));
  ssid = deviceName;
#ifdef SIN_RADIO
  return;  // compilacion de prueba: sin WiFi ni Bluetooth
#endif

  // WiFi en modo punto de acceso: la app se conecta a esta red.
  ssid = deviceName;
  // Las SuperMini se reinician (voltaje bajo) o no conectan con la potencia maxima:
  // se baja ANTES de encender el punto de acceso.
  WiFi.mode(WIFI_AP);
  WiFi.setTxPower(WIFI_POWER_8_5dBm);
  delay(50);
  WiFi.softAP(ssid.c_str(), WIFI_PASS);
  WiFi.setTxPower(WIFI_POWER_8_5dBm);
  delay(100);
  tcpServer.begin();
  tcpServer.setNoDelay(true);

  // BLE (NimBLE)
  NimBLEDevice::init(deviceName);
  NimBLEDevice::setMTU(247);
  NimBLEDevice::setPower(ESP_PWR_LVL_P3);  // potencia moderada (menos picos de corriente)
  server = NimBLEDevice::createServer();
  server->setCallbacks(new ServerCb());
  NimBLEService *svc = server->createService(BLE_SERVICE_UUID);
  txChar = svc->createCharacteristic(BLE_TX_UUID, NIMBLE_PROPERTY::NOTIFY);
  NimBLECharacteristic *rx = svc->createCharacteristic(BLE_RX_UUID, NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::WRITE_NR);
  rx->setCallbacks(new RxCb());
  svc->start();
  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();
  adv->addServiceUUID(BLE_SERVICE_UUID);
  adv->setName(deviceName);
  adv->setScanResponse(true);
  NimBLEDevice::startAdvertising();
}

void commsLoop() {
#ifdef SIN_RADIO
  return;
#endif
  if (tcpServer.hasClient()) {
    WiFiClient c = tcpServer.available();
    if (tcpClient && tcpClient.connected()) tcpClient.stop();  // un cliente a la vez
    tcpClient = c;
    tcpClient.setNoDelay(true);
    tcpRxBuf = "";
  }
  if (tcpClient && tcpClient.connected()) {
    while (tcpClient.available()) {
      char ch = tcpClient.read();
      if (ch == '\n') {
        pushCommand(tcpRxBuf);
        tcpRxBuf = "";
      } else if (tcpRxBuf.length() < 200) {
        tcpRxBuf += ch;
      }
    }
  }
}

void commsSend(const String &line) {
  bleSend(line);
  if (tcpClient && tcpClient.connected()) tcpClient.print(line + "\n");
  if (Serial) Serial.println(line);  // solo si hay una consola abierta en la PC
}

bool commsNextCommand(String &out) {
  Cmd c;
  if (xQueueReceive(cmdQueue, &c, 0) != pdTRUE) return false;
  out = c.text;
  return true;
}

bool commsBleConnected() { return bleConnected; }
bool commsWifiConnected() { return tcpClient && tcpClient.connected(); }
String commsSsid() { return ssid; }
String commsIp() { return WiFi.softAPIP().toString(); }
