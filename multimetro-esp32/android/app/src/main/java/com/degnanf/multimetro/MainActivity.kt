package com.degnanf.multimetro

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.app.AlertDialog
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.Typeface
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.ParcelUuid
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : Activity(), LinkListener {

    private data class ModeInfo(val code: String, val label: String)

    private val modes = listOf(
        ModeInfo("DCV", "Voltaje DC"),
        ModeInfo("DCA", "Corriente (mA)"),
        ModeInfo("OHM", "Resistencia"),
        ModeInfo("CONT", "Continuidad"),
        ModeInfo("DIODE", "Diodo"),
        ModeInfo("CAP", "Capacitor"),
        ModeInfo("FREQ", "Frecuencia"),
    )

    private var link: MeterLink? = null
    private var connected = false
    private var currentMode = ""
    private var lastUnit = "V"
    private var info: JSONObject? = null
    private var cal: JSONObject? = null

    private val recording = ArrayList<String>()
    private var isRecording = false
    private var phoneBeep = true
    private var lastToneMs = 0L
    private val tone by lazy { ToneGenerator(AudioManager.STREAM_MUSIC, 80) }
    private val main = Handler(Looper.getMainLooper())

    // Vistas
    private lateinit var status: TextView
    private lateinit var modeLabel: TextView
    private lateinit var value: TextView
    private lateinit var unit: TextView
    private lateinit var flags: TextView
    private lateinit var stats: TextView
    private lateinit var graph: GraphView
    private lateinit var btnHold: Button
    private lateinit var btnRel: Button
    private lateinit var btnRec: Button
    private lateinit var recInfo: TextView
    private val modeButtons = HashMap<String, Button>()

    private val dp get() = resources.displayMetrics.density

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        setContentView(buildUi())
        showDisconnected()
    }

    override fun onDestroy() {
        stopScan()
        link?.close()
        super.onDestroy()
    }

    // ================================================================ UI
    private fun buildUi(): View {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(px(14), px(14), px(14), px(14))
            setBackgroundColor(Color.parseColor("#0B0E11"))
        }

        status = text("Desconectado", 14f, Color.LTGRAY)
        root.addView(status)
        root.addView(row(
            button("Bluetooth") { connectBle() },
            button("WiFi") { connectWifiDialog() },
            button("Desconectar") { disconnect() },
        ))

        // Pantalla
        val screen = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(px(14), px(10), px(14), px(10))
            setBackgroundColor(Color.parseColor("#16202A"))
        }
        modeLabel = text("—", 16f, Color.parseColor("#FFC107"))
        flags = text("", 13f, Color.parseColor("#FF8A65")).apply { gravity = Gravity.END }
        screen.addView(LinearLayout(this).apply {
            addView(modeLabel, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
            addView(flags)
        })
        value = text("----", 64f, Color.parseColor("#7CFC9A")).apply {
            typeface = Typeface.MONOSPACE
            gravity = Gravity.END
        }
        unit = text("", 26f, Color.parseColor("#7CFC9A")).apply { gravity = Gravity.END }
        stats = text("", 13f, Color.LTGRAY)
        screen.addView(value)
        screen.addView(unit)
        screen.addView(stats)
        root.addView(screen, lp(top = 8))

        graph = GraphView(this)
        root.addView(graph, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, px(170)).apply {
            topMargin = px(8)
        })

        // Modos
        root.addView(text("Función", 13f, Color.GRAY).apply { setPadding(0, px(10), 0, px(2)) })
        val modeBtns = modes.map { m ->
            button(m.label) { selectMode(m.code) }.also { modeButtons[m.code] = it }
        }
        root.addView(row(*modeBtns.subList(0, 4).toTypedArray()))
        root.addView(row(*modeBtns.subList(4, 7).toTypedArray()))

        // Acciones
        btnHold = button("HOLD") { sendCmd("HOLD") }
        btnRel = button("REL") { sendCmd("REL") }
        root.addView(row(btnHold, btnRel, button("Borrar MIN/MAX") { sendCmd("RESET"); graph.clear() }))

        // Registro CSV
        btnRec = button("Grabar") { toggleRecording() }
        recInfo = text("0 muestras", 13f, Color.LTGRAY).apply { gravity = Gravity.CENTER }
        root.addView(row(btnRec, button("Guardar CSV") { saveCsv() }, recInfo))

        // Ajustes
        root.addView(row(
            button("Calibrar") { calibrateDialog() },
            button("Info equipo") { infoDialog() },
        ))
        val beepBox = CheckBox(this).apply {
            text = "Pitido de continuidad en el teléfono"
            setTextColor(Color.LTGRAY)
            isChecked = true
            setOnCheckedChangeListener { _, c -> phoneBeep = c }
        }
        val beepDev = CheckBox(this).apply {
            text = "Buzzer del multímetro"
            setTextColor(Color.LTGRAY)
            isChecked = true
            setOnCheckedChangeListener { _, c -> sendCmd("BEEP ${if (c) 1 else 0}") }
        }
        root.addView(beepBox)
        root.addView(beepDev)
        root.addView(text(
            "Seguridad: solo baja tensión DC (máx. 40 V, 300 mA). No medir la red eléctrica. " +
                "Puntas: roja en VΩmA, negra en COM.",
            12f, Color.parseColor("#FF8A65")
        ).apply { setPadding(0, px(8), 0, 0) })

        return ScrollView(this).apply { addView(root) }
    }

    private fun px(v: Int) = (v * dp).toInt()

    private fun lp(top: Int = 0) = LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
    ).apply { topMargin = px(top) }

    private fun text(s: String, size: Float, color: Int) = TextView(this).apply {
        text = s; textSize = size; setTextColor(color)
    }

    private fun button(label: String, onClick: () -> Unit) = Button(this).apply {
        text = label
        isAllCaps = false
        textSize = 13f
        setOnClickListener { onClick() }
    }

    private fun row(vararg views: View) = LinearLayout(this).apply {
        orientation = LinearLayout.HORIZONTAL
        views.forEach { addView(it, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)) }
    }

    private fun toast(s: String) = Toast.makeText(this, s, Toast.LENGTH_SHORT).show()

    // ================================================================ Conexion
    private fun sendCmd(cmd: String) {
        if (!connected) { toast("Primero conecta el multímetro"); return }
        link?.send(cmd)
    }

    /** Corriente pide confirmacion: con las puntas sobre una fuente seria un cortocircuito. */
    private fun selectMode(code: String) {
        if (code != "DCA" || currentMode == "DCA") { sendCmd("MODE $code"); return }
        if (!connected) { toast("Primero conecta el multímetro"); return }
        AlertDialog.Builder(this)
            .setTitle("Medir corriente")
            .setMessage("Coloca las puntas EN SERIE con el circuito (abre el circuito y pon el multímetro en medio).\n\n" +
                "Nunca sobre una fuente o batería directamente: haría cortocircuito y fundiría el fusible.\n\nMáximo 300 mA.")
            .setPositiveButton("Entendido, medir") { _, _ -> sendCmd("MODE DCA") }
            .setNegativeButton("Cancelar", null)
            .show()
    }

    private fun disconnect() {
        link?.close()
        link = null
        connected = false
        showDisconnected()
    }

    private fun showDisconnected() {
        status.text = "Desconectado — elige Bluetooth o WiFi"
        value.text = "----"
        unit.text = ""
        flags.text = ""
        stats.text = ""
    }

    override fun onState(text: String, connected: Boolean) {
        this.connected = connected
        status.text = text
    }

    override fun onLine(line: String) {
        val j = try { JSONObject(line) } catch (_: Exception) { return }
        when (j.optString("t")) {
            "m" -> onMeasurement(j)
            "info" -> info = j
            "cal" -> { cal = j; calTextView?.text = calSummary() }
            "msg" -> toast(j.optString("s"))
        }
    }

    private fun onMeasurement(j: JSONObject) {
        val code = j.optString("m")
        val u = j.optString("u")
        lastUnit = u
        if (code != currentMode) {
            currentMode = code
            graph.clear()
            graph.unit = u
            modeButtons.forEach { (k, b) -> b.setTextColor(if (k == code) Color.parseColor("#FFC107") else Color.WHITE) }
        }
        modeLabel.text = modes.firstOrNull { it.code == code }?.label ?: code
        val ol = j.optInt("ol") == 1
        val hold = j.optInt("h") == 1
        val rel = j.optInt("rel") == 1
        val v = if (j.isNull("v")) null else j.optDouble("v")

        btnHold.setTextColor(if (hold) Color.parseColor("#FF8A65") else Color.WHITE)
        btnRel.setTextColor(if (rel) Color.parseColor("#FF8A65") else Color.WHITE)
        flags.text = listOfNotNull(if (hold) "HOLD" else null, if (rel) "REL" else null).joinToString("  ")

        when {
            ol -> {
                value.text = if (code == "CONT" || code == "DIODE") "ABIERTO" else "OL"
                unit.text = ""
            }
            v == null -> { value.text = if (code == "CAP") "midiendo…" else "----"; unit.text = "" }
            else -> {
                val (n, pu) = Fmt.si(v, u)
                value.text = n
                unit.text = pu
                graph.add(v)
            }
        }

        val parts = ArrayList<String>()
        if (j.has("mn") && !j.isNull("mn")) {
            parts += "MIN ${Fmt.siText(j.getDouble("mn"), u)}"
            parts += "MAX ${Fmt.siText(j.getDouble("mx"), u)}"
            parts += "PROM ${Fmt.siText(j.getDouble("av"), u)}"
        }
        if (code == "DIODE" && j.has("x")) parts += "If ${Fmt.siText(j.getDouble("x"), "A")}"
        stats.text = parts.joinToString("   ")

        // Pitido de continuidad en el telefono
        if (code == "CONT" && phoneBeep && !ol && v != null && v < 30.0) {
            val now = System.currentTimeMillis()
            if (now - lastToneMs > 150) {
                tone.startTone(ToneGenerator.TONE_PROP_BEEP, 140)
                lastToneMs = now
            }
        }

        if (isRecording && !hold) {
            val ts = SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US).format(Date())
            recording += "$ts,$code,${v ?: ""},${Fmt.unitSymbol(u)},${if (ol) 1 else 0}"
            recInfo.text = "${recording.size} muestras"
        }
    }

    // ---------------------------------------------------------------- Bluetooth
    private var scanCb: ScanCallback? = null

    private fun blePermissions(): Array<String> =
        if (Build.VERSION.SDK_INT >= 31) arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
        else arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)

    private fun hasPerms(p: Array<String>) = p.all { checkSelfPermission(it) == PackageManager.PERMISSION_GRANTED }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQ_BLE) {
            if (grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED }) connectBle()
            else toast("Sin permiso de Bluetooth no se puede buscar el multímetro")
        }
    }

    @SuppressLint("MissingPermission")
    private fun connectBle() {
        val perms = blePermissions()
        if (!hasPerms(perms)) { requestPermissions(perms, REQ_BLE); return }
        val adapter = (getSystemService(BLUETOOTH_SERVICE) as BluetoothManager).adapter
        if (adapter == null) { toast("Este teléfono no tiene Bluetooth"); return }
        if (!adapter.isEnabled) {
            startActivity(Intent(android.bluetooth.BluetoothAdapter.ACTION_REQUEST_ENABLE))
            return
        }
        val scanner = adapter.bluetoothLeScanner ?: run { toast("Bluetooth no disponible"); return }

        val found = ArrayList<BluetoothDevice>()
        val names = ArrayAdapter<String>(this, android.R.layout.simple_list_item_1)
        val dialog = AlertDialog.Builder(this)
            .setTitle("Buscando multímetros…")
            .setAdapter(names) { _, which ->
                stopScan()
                disconnect()
                link = BleLink(this, found[which], this)
            }
            .setNegativeButton("Cancelar", null)
            .setOnDismissListener { stopScan() }
            .create()

        scanCb = object : ScanCallback() {
            override fun onScanResult(callbackType: Int, result: ScanResult) {
                val d = result.device
                if (found.none { it.address == d.address }) {
                    found += d
                    names.add("${result.scanRecord?.deviceName ?: d.name ?: "Multímetro"}  (${d.address})")
                }
            }

            override fun onScanFailed(errorCode: Int) = toast("Error al buscar ($errorCode)")
        }
        val filter = ScanFilter.Builder().setServiceUuid(ParcelUuid(Uuids.SERVICE)).build()
        val settings = ScanSettings.Builder().setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY).build()
        scanner.startScan(listOf(filter), settings, scanCb)
        dialog.show()
        main.postDelayed({ stopScan(); if (dialog.isShowing) dialog.setTitle(if (found.isEmpty()) "No se encontró ninguno" else "Elige el multímetro") }, 8000)
        if (Build.VERSION.SDK_INT < 31) toast("En Android 11 o menos, activa la Ubicación para buscar")
    }

    @SuppressLint("MissingPermission")
    private fun stopScan() {
        val cb = scanCb ?: return
        scanCb = null
        try {
            (getSystemService(BLUETOOTH_SERVICE) as BluetoothManager).adapter?.bluetoothLeScanner?.stopScan(cb)
        } catch (_: Exception) {
        }
    }

    // ---------------------------------------------------------------- WiFi
    private fun connectWifiDialog() {
        val prefs = getSharedPreferences("mm", MODE_PRIVATE)
        val box = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(px(20), px(8), px(20), 0) }
        val ip = EditText(this).apply { setText(prefs.getString("ip", "192.168.4.1")); hint = "IP" }
        val pass = EditText(this).apply { setText(prefs.getString("pass", "12345678")); hint = "Clave WiFi del multímetro" }
        box.addView(TextView(this).apply {
            text = "El multímetro crea la red \"Multimetro-XXXX\" (clave por defecto 12345678, IP 192.168.4.1)."
        })
        box.addView(ip)
        box.addView(pass)

        AlertDialog.Builder(this)
            .setTitle("Conectar por WiFi")
            .setView(box)
            .setPositiveButton(if (Build.VERSION.SDK_INT >= 29) "Unirme a su red" else "Conectar") { _, _ ->
                prefs.edit().putString("ip", ip.text.toString()).putString("pass", pass.text.toString()).apply()
                disconnect()
                link = WifiLink(this, ip.text.toString().trim(), PORT, Build.VERSION.SDK_INT >= 29, pass.text.toString(), this)
            }
            .setNeutralButton("Ya estoy en su red") { _, _ ->
                prefs.edit().putString("ip", ip.text.toString()).apply()
                disconnect()
                link = WifiLink(this, ip.text.toString().trim(), PORT, false, "", this)
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }

    // ---------------------------------------------------------------- Registro CSV
    private fun toggleRecording() {
        isRecording = !isRecording
        if (isRecording) { recording.clear(); recInfo.text = "0 muestras" }
        btnRec.text = if (isRecording) "Detener" else "Grabar"
        btnRec.setTextColor(if (isRecording) Color.parseColor("#FF5252") else Color.WHITE)
    }

    private fun saveCsv() {
        if (recording.isEmpty()) { toast("No hay muestras grabadas"); return }
        val name = "multimetro_" + SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date()) + ".csv"
        val i = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "text/csv"
            putExtra(Intent.EXTRA_TITLE, name)
        }
        startActivityForResult(i, REQ_CSV)
    }

    @Deprecated("API de Activity")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        @Suppress("DEPRECATION")
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQ_CSV || resultCode != RESULT_OK) return
        val uri = data?.data ?: return
        try {
            contentResolver.openOutputStream(uri)?.use { os ->
                os.write("fecha_hora,modo,valor,unidad,fuera_de_rango\n".toByteArray())
                recording.forEach { os.write((it + "\n").toByteArray()) }
            }
            toast("CSV guardado (${recording.size} muestras)")
        } catch (e: Exception) {
            toast("No se pudo guardar: ${e.message}")
        }
    }

    // ---------------------------------------------------------------- Calibracion
    private var calTextView: TextView? = null

    private fun calSummary(): String {
        val c = cal ?: return "Cargando calibración…"
        val r = c.optJSONArray("r")
        val kc = c.optJSONArray("kc")
        return buildString {
            append("kV=${c.optDouble("kv")}  kI=${c.optDouble("ki")}\n")
            if (r != null) append("Ref Ω: ${(0 until r.length()).joinToString(", ") { Fmt.siText(r.getDouble(it), "ohm") }}\n")
            if (kc != null) append("kC: ${kc.optDouble(0)} (rango 1M), ${kc.optDouble(1)} (rango 1k)")
        }
    }

    private fun calibrateDialog() {
        if (!connected) { toast("Primero conecta el multímetro"); return }
        link?.send("CALGET")
        val box = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(px(20), px(8), px(20), 0) }
        box.addView(TextView(this).apply {
            text = "1. Elige la función (V, A, Ω o Capacitor).\n" +
                "2. Mide algo de valor conocido (fuente o multímetro de referencia, resistencia o capacitor de 1 %).\n" +
                "3. Escribe el valor real y pulsa Calibrar.\n\n" +
                "Acepta prefijos: 4.7k, 100n, 2.5m, 1M. En Ω se calibra el rango en uso."
        })
        val real = EditText(this).apply {
            hint = "Valor real (ej. 5.00 o 10k)"
            inputType = InputType.TYPE_CLASS_TEXT
        }
        box.addView(real)
        calTextView = TextView(this).apply { text = calSummary(); setPadding(0, px(8), 0, 0); textSize = 12f }
        box.addView(calTextView)

        AlertDialog.Builder(this)
            .setTitle("Calibración — ${modes.firstOrNull { it.code == currentMode }?.label ?: currentMode}")
            .setView(box)
            .setPositiveButton("Calibrar") { _, _ ->
                val v = Fmt.parse(real.text.toString())
                if (v == null || v <= 0) toast("Valor no válido") else link?.send("CAL $v")
            }
            .setNeutralButton("Restaurar fábrica") { _, _ ->
                AlertDialog.Builder(this)
                    .setMessage("¿Borrar toda la calibración del multímetro?")
                    .setPositiveButton("Sí") { _, _ -> link?.send("CALRESET") }
                    .setNegativeButton("No", null)
                    .show()
            }
            .setNegativeButton("Cerrar", null)
            .setOnDismissListener { calTextView = null }
            .show()
    }

    private fun infoDialog() {
        val i = info
        val msg = if (i == null) "Conecta el multímetro para ver sus datos." else
            "Nombre: ${i.optString("name")}\nFirmware: ${i.optString("fw")}\n" +
                "Red WiFi: ${i.optString("ssid")}\nClave: ${i.optString("pass")}\n" +
                "IP: ${i.optString("ip")}  Puerto: ${i.optInt("port")}\n" +
                "ADS1115: ${if (i.optInt("ads") == 1) "detectado" else "NO detectado (revisa cableado)"}"
        AlertDialog.Builder(this).setTitle("Multímetro").setMessage(msg).setPositiveButton("OK", null).show()
    }

    companion object {
        const val PORT = 3333
        const val REQ_BLE = 1
        const val REQ_CSV = 2
    }
}
