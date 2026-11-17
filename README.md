# TOOL UTILITY BY DEGNANF

Utilidad en Windows (archivo `.bat`) con herramientas Android (ADB, fastboot, scrcpy),
drivers, firmware y utilidades varias.

## Uso

1. Ejecuta **`TOOL UTILITY DEGNANF-V1.0.bat`** (clic derecho → *Ejecutar como administrador*
   para las opciones que lo requieran).
2. Elige una opción del menú escribiendo su número.

## Versión 1.1

## Novedades (Fase 2)

### Opción 14 → 5 — BACKUP ANTI-BRICK (requiere root / su)

| Opción | Función |
|--------|---------|
| 1 | **Respaldar particiones críticas** (`efs`, `persist`, `modemst1/2`, `nvram`, `fsc`, `fsg`) a la carpeta `BACKUPS\<serial>_<fecha>\` como `.img`. |
| 2 | **Restaurar una partición** desde un respaldo **de ese mismo equipo**. Pide confirmar escribiendo `SI`, y solo permite las particiones de la lista anterior. |
| 3 | **Respaldar apps y datos** con `adb backup` (confirmas en la pantalla del teléfono). |

> Haz el respaldo de `efs`/`persist` **antes** de flashear firmware. Guarda esas carpetas fuera del equipo.

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
