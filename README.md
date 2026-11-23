# TOOL UTILITY BY DEGNANF — V1.2

Utilidad en Windows (archivo `.bat`) con herramientas Android (ADB, fastboot, scrcpy),
drivers, firmware y utilidades varias.

> Historial completo de cambios en [`CHANGELOG.md`](CHANGELOG.md).

## Uso

1. Ejecuta **`TOOL UTILITY DEGNANF-V1.0.bat`** (clic derecho → *Ejecutar como administrador*
   para las opciones que lo requieran).
2. Elige una opción del menú escribiendo su número.

## Novedades (Fase 6: más marcas en OTA)

### Opción 11 — OTA UPDATES (multi-marca)
Ahora detecta la marca y desactiva las apps de actualización OTA de:
- **Samsung, Xiaomi/Redmi/POCO, Oppo** (ya estaban)
- **Vivo / iQOO**, **Realme**, **OnePlus**, **Transsion (Tecno / Infinix / itel)** (nuevas)

Usa `pm disable-user --user 0` (reversible con `pm enable`), probando una lista de paquetes conocidos por marca. Los paquetes que no existan en el equipo se omiten sin error, y el menú indica cuáles desactivó.

> Nota: estos nombres de paquete son los habituales por marca, pero pueden variar según el modelo y la versión. Si una marca saca una versión nueva, puede que no coincida; en ese caso úsalo junto al debloat manual (opción 14 → 6 → 4).

## Novedades (Fase 5: firmware Samsung oficial)

### Opción 14 → 8 — FIRMWARE SAMSUNG (descarga oficial)
Usa **samloader** (incluido en `samloader/`, licencia Apache-2.0, ver `samloader/NOTICE.txt`). El menú elige automáticamente `samloader-x64.exe` o `samloader-arm64.exe` según la arquitectura de Windows.
- **[1] Ver última versión disponible:** consulta los servidores de Samsung (`check-update`).
- **[2] Descargar firmware oficial:** descarga la última versión a `FIRMWARE\<modelo>_<region>\` (`download`).
- **[3] Flashear firmware descargado:** en modo Download, extrae el `.zip` con `7za`, detecta BL/AP/CP y HOME_CSC/CSC (prefiere HOME_CSC para conservar datos) y flashea con `samloader flash --wait`. Haz el backup anti-brick (opción 5) antes y ten instalado el driver USB Samsung (menú 6).
- No necesita el equipo conectado. Pide **modelo** (ej. `SM-A325M`) y **CSC/región** (ej. `COO`, `UNE`, `XAA`).
- Los binarios (x86_64 y ARM64) son los releases oficiales de `topjohnwu/samloader-rs`, sin modificar (SHA-256 en el NOTICE).
- **[4] Frija (alternativa gráfica):** abre la fuente oficial de Frija (XDA) para descargarla aparte. No se incluye el binario (freeware); solo se enlaza. samloader sigue siendo la herramienta integrada.

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
- **[3] Listar apps instaladas:** guarda y abre la lista de paquetes (solo terceros, o todas incluyendo precargadas) para ver el nombre exacto.
- **[4] Quitar una app por nombre (manual):** quita cualquier app precargada sin root (`pm uninstall -k --user 0`), reversible, pidiendo confirmar con `SI`.
- Fuente y licencia de la lista: `debloat/NOTICE.txt` (GPL-3.0).

## Versión

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
