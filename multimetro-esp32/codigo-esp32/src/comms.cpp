#include "comms.h"
#include "config.h"
#include <BLE2902.h>
#include <BLEDevice.h>
#include <BLEServer.h>
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
static BLEServer *server = nullptr;
static BLECharacteristic *txChar = nullptr;
static volatile bool bleConnected = false;
static volatile uint16_t bleConnId = 0;
static String bleRxBuf;

class ServerCb : public BLEServerCallbacks {
  void onConnect(BLEServer *s, esp_ble_gatts_cb_param_t *param) override {
    bleConnId = param->connect.conn_id;
    bleConnected = true;
  }
  void onDisconnect(BLEServer *s) override {
    bleConnected = false;
    delay(50);
    BLEDevice::startAdvertising();
  }
};

class RxCb : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *c) override {
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

  // BLE
  BLEDevice::init(deviceName);
  BLEDevice::setMTU(247);
  server = BLEDevice::createServer();
  server->setCallbacks(new ServerCb());
  BLEService *svc = server->createService(BLE_SERVICE_UUID);
  txChar = svc->createCharacteristic(BLE_TX_UUID, BLECharacteristic::PROPERTY_NOTIFY);
  txChar->addDescriptor(new BLE2902());
  BLECharacteristic *rx = svc->createCharacteristic(
      BLE_RX_UUID, BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_WRITE_NR);
  rx->setCallbacks(new RxCb());
  svc->start();
  BLEAdvertising *adv = BLEDevice::getAdvertising();
  adv->addServiceUUID(BLE_SERVICE_UUID);
  adv->setScanResponse(true);
  BLEDevice::startAdvertising();
}

void commsLoop() {
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
  Serial.println(line);
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
