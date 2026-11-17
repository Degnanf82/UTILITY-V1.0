# TOOL UTILITY BY DEGNANF

Utilidad en Windows (archivo `.bat`) con herramientas Android (ADB, fastboot, scrcpy),
drivers, firmware y utilidades varias.

## Uso

1. Ejecuta **`TOOL UTILITY DEGNANF-V1.0.bat`** (clic derecho → *Ejecutar como administrador*
   para las opciones que lo requieran).
2. Elige una opción del menú escribiendo su número.

## Novedades (Fase 1)

### Estado del dispositivo en el menú
El encabezado ahora muestra si hay un dispositivo conectado y en qué modo:
`ADB`, `FASTBOOT` o `NINGUNO`.

### Opción 14 — HERRAMIENTAS ADB/FASTBOOT
Submenú con:

| Opción | Función |
|--------|---------|
| 1 | **Instalar APK** — arrastra el `.apk` a la ventana y se instala (`adb install -r`). |
| 2 | **Reiniciar a modo** — recovery, bootloader, fastbootd, download/Odin, EDL 9008 o sistema. |
| 3 | **Reporte del dispositivo a .txt** — genera `REPORTE_<serial>.txt` con marca, modelo, Android, parche de seguridad, chipset, IMEI, etc. |
| 4 | **Estado de red y desbloqueo oficial** — muestra (solo lectura) operador, estado SIM, IMEI y CSC, y explica cómo pedir el desbloqueo **oficial** al operador/fabricante. No fuerza ni evade el candado de red. |

Todas detectan automáticamente el dispositivo y, si hay **varios conectados**,
piden el serial a usar (`adb -s`).

## Configuración de enlaces — `config.ini`

Los links de descarga (Visual C++, drivers, firmware Samsung) están en **`config.ini`**.
Si un enlace deja de funcionar, edítalo ahí **sin tocar el `.bat`**:

```
CLAVE=valor        # las líneas que empiezan con # se ignoran
```

> Guarda `config.ini` con codificación normal (LF o ANSI). No pongas espacios
> alrededor del `=`.

## Herramientas incluidas

- **platform-tools 37.0.1** (`adb.exe`, `fastboot.exe`) — Android SDK Platform Tools de Google.
- **scrcpy** — espejo de pantalla Android.
- Drivers, lectura de info por fastboot (Xiaomi, Motorola, Huawei), desactivar OTA, etc.
