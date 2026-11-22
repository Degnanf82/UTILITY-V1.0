// Comunicacion con la app: Bluetooth LE (estilo Nordic UART) y WiFi (punto de acceso + TCP).
// Protocolo: lineas de texto terminadas en '\n'. El equipo envia JSON; la app envia comandos.
#pragma once
#include <Arduino.h>

void commsBegin(const char *deviceName);
void commsLoop();                   // atiende clientes TCP
void commsSend(const String &line); // envia una linea (sin '\n') a todos los clientes
bool commsNextCommand(String &out); // saca el siguiente comando recibido (si hay)
bool commsBleConnected();
bool commsWifiConnected();
String commsSsid();
String commsIp();

// Diagnostico: parpadea el LED azul (GPIO 8) n veces. Solo hace algo si se compila con PASOS_LED.
void dbgStep(int n);
