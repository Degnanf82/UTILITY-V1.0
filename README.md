# TOOL UTILITY BY DEGNANF

Utilidad en Windows (archivo `.bat`) con herramientas Android (ADB, fastboot, scrcpy),
drivers, firmware y utilidades varias.

## Uso

1. Ejecuta **`TOOL UTILITY DEGNANF-V1.0.bat`** (clic derecho → *Ejecutar como administrador*
   para las opciones que lo requieran).
2. Elige una opción del menú escribiendo su número.

## Novedades (Fase 4: recuperación de equipo)

### Opción 14 → 7 — RECUPERACION DE EQUIPO (solo firmware oficial)
- **[1] Diagnóstico fastboot:** muestra producto, estado `unlocked` del bootloader y slot activo.
- **[2] Ejecutar script oficial de flasheo:** arrastras la carpeta del firmware **oficial** (la que trae `flash-all.bat`, `flash_all.bat` o `flashfile`). El menú lo busca, pide confirmar con `SI` y lo ejecuta. No escribo comandos de flasheo por modelo.
- **[3] Guía:** EDL (9008), BROM y modo Download sin acceso van al servicio oficial.

**Fuera de alcance por ahora:** Samsung (depende de Heimdall y de los flags de samloader-rs, pendientes de verificar), EDL/BROM sin autorización y cualquier bypass de autenticación.

## Novedades (Fase 3: debloat)

### Opción 14 → 6 — DEBLOAT SEGURO
- **[1] Quitar paquetes seguros:** usa la lista `debloat/uad_recommended.txt` (solo paquetes marcados como *Recommended* en UAD-ng). Desinstala con `pm uninstall -k --user 0`, sin root. Pide confirmar con `SI` y guarda un registro en `debloat/log_<serial>.txt`.
- **[2] Restaurar un paquete:** reinstala para el usuario 0 un paquete quitado (`cmd package install-existing`).
- Fuente y licencia de la lista: `debloat/NOTICE.txt` (GPL-3.0).

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
