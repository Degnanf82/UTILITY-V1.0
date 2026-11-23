# CHANGELOG — TOOL UTILITY BY DEGNANF

Formato por versiones. El menú principal y el submenú **Herramientas ADB/FASTBOOT**
(opción 14) concentran las funciones nuevas.

---

## V1.2 — 2026-11-23

### Guía de cuenta / FRP por proceso oficial
- Opción **14 → 9**: pantalla que guía el **camino legítimo** cuando un cliente
  trae un equipo bloqueado por cuenta Google / FRP: exige prueba de propiedad,
  deriva a los canales oficiales de recuperación (Google, Samsung, Xiaomi,
  Huawei) y al operador para candado de red, y propone reinstalar firmware
  oficial como servicio cobrable. **No salta ni evade el FRP.**

### Correcciones
- Rutinas de lectura por fastboot (`:fastbootreadmiqcom`, `:fastbootreadmotoqcom`):
  eliminado un paréntesis `)` de más que dejaba los bloques `if/else`
  desbalanceados. Estas rutinas todavía **no están conectadas al menú**
  (código para una futura función de info por fastboot); además la rama `cid`
  de Motorola tiene una limitación de *delayed expansion* pendiente si se
  llegara a usar.

### Fase 6 — OTA multi-marca
- Opción **11** ampliada: además de Samsung, Xiaomi/Redmi/POCO y Oppo, ahora
  desactiva las apps de actualización OTA de **Vivo/iQOO**, **Realme**,
  **OnePlus** y **Transsion (Tecno/Infinix/itel)**.
- Usa `pm disable-user --user 0` (reversible con `pm enable`), probando una
  lista de paquetes candidatos por marca; los que no existen se omiten.

---

## V1.1 — 2026-11-17

### Correcciones de base
- Submenú de drivers, opción 5 (OPPO): `:goto:OPPO` era una etiqueta, no un salto.
- Opción 11 (OTA Xiaomi): flag inválido `-usuario` corregido a `--user`.
- Opción 1 (Visual C++): `pause >null` creaba un archivo basura `null`.
- platform-tools (adb, fastboot y DLLs) actualizadas a **37.0.1** (raíz y `scrcpy/`).

### Fase 1 — Base del submenú Herramientas
- Estado del dispositivo en el encabezado (ADB / FASTBOOT / NINGUNO).
- Soporte multi-dispositivo (`adb -s`).
- Enlaces de descarga movidos a `config.ini`.
- Opción 14: [1] Instalar APK, [2] Reiniciar a modo, [3] Reporte a `.txt`,
  [4] Estado de red y guía de desbloqueo oficial.

### Fase 2 — Backup anti-brick
- Opción 14 → 5: respaldo de particiones críticas (efs, persist, modemst, nvram,
  fsc, fsg) con root, restauración con lista blanca y confirmación, y
  `adb backup` de apps.

### Fase 3 — Debloat seguro
- Opción 14 → 6: quitar paquetes `Recommended` de UAD-ng (GPL-3.0) sin root,
  reversible; listar apps instaladas y quitar una app por nombre (manual).

### Fase 4 — Recuperación de equipo
- Opción 14 → 7: diagnóstico fastboot, ejecución del script oficial de flasheo
  de una carpeta de firmware, y guía para EDL/BROM/Download (servicio oficial).

### Fase 5 — Firmware Samsung oficial
- Opción 14 → 8: ver versión y descargar firmware oficial con **samloader**
  (Apache-2.0), binarios x64 y ARM64 incluidos con licencia y SHA-256.

---

## Fuera de alcance (por decisión de seguridad)
No se incluye ni se incluirá: bypass de FRP o cuenta Google, desbloqueo de red
por exploits/edición de NV-EFS, activadores de licencias, desactivación de
Windows Defender, ni loaders EDL/BROM de terceros.

## Nota de pruebas
Todo el trabajo está validado de forma **estática** (estructura, etiquetas,
enrutamiento, alineación del menú). Aún **no se ha ejecutado en Windows con un
dispositivo real**. Conviene probar en un equipo de prueba antes de usarlo con
clientes, sobre todo el respaldo/restauración de particiones y el flasheo.
