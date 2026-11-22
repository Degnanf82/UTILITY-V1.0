package com.degnanf.multimetro

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothProfile
import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiNetworkSpecifier
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.PatternMatcher
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStream
import java.net.InetSocketAddress
import java.net.Socket
import java.util.UUID
import java.util.concurrent.Executors

/** Recibe lineas y cambios de estado en el hilo principal. */
interface LinkListener {
    fun onLine(line: String)
    fun onState(text: String, connected: Boolean)
}

/** Conexion con el multimetro: lineas de texto terminadas en '\n'. */
interface MeterLink {
    fun send(line: String)
    fun close()
}

object Uuids {
    val SERVICE: UUID = UUID.fromString("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
    val RX: UUID = UUID.fromString("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
    val TX: UUID = UUID.fromString("6e400003-b5a3-f393-e0a9-e50e24dcca9e")
    val CCCD: UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
}

// ------------------------------------------------------------------ Bluetooth LE
@SuppressLint("MissingPermission")
class BleLink(ctx: Context, device: BluetoothDevice, private val listener: LinkListener) : MeterLink {
    private val main = Handler(Looper.getMainLooper())
    private val buf = StringBuilder()
    private var gatt: BluetoothGatt? = null
    private var rx: BluetoothGattCharacteristic? = null
    @Volatile private var closed = false

    private val cb = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(g: BluetoothGatt, status: Int, newState: Int) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                post("Bluetooth: negociando…", false)
                g.requestMtu(247)
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                g.close()
                if (!closed) post("Bluetooth desconectado", false)
            }
        }

        override fun onMtuChanged(g: BluetoothGatt, mtu: Int, status: Int) {
            g.discoverServices()
        }

        override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
            val svc = g.getService(Uuids.SERVICE)
            val tx = svc?.getCharacteristic(Uuids.TX)
            rx = svc?.getCharacteristic(Uuids.RX)
            if (tx == null || rx == null) {
                post("El equipo no es un multímetro compatible", false)
                g.disconnect()
                return
            }
            g.setCharacteristicNotification(tx, true)
            val d = tx.getDescriptor(Uuids.CCCD)
            if (Build.VERSION.SDK_INT >= 33) {
                g.writeDescriptor(d, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE)
            } else {
                @Suppress("DEPRECATION")
                d.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                @Suppress("DEPRECATION")
                g.writeDescriptor(d)
            }
        }

        override fun onDescriptorWrite(g: BluetoothGatt, d: BluetoothGattDescriptor, status: Int) {
            post("Conectado por Bluetooth", true)
            send("INFO")
        }

        override fun onCharacteristicChanged(g: BluetoothGatt, c: BluetoothGattCharacteristic, value: ByteArray) {
            onData(value)
        }

        @Deprecated("Android 12 o inferior")
        override fun onCharacteristicChanged(g: BluetoothGatt, c: BluetoothGattCharacteristic) {
            @Suppress("DEPRECATION")
            if (Build.VERSION.SDK_INT < 33) onData(c.value ?: return)
        }
    }

    init {
        post("Bluetooth: conectando a ${device.name ?: device.address}…", false)
        gatt = device.connectGatt(ctx, false, cb, BluetoothDevice.TRANSPORT_LE)
    }

    private fun onData(bytes: ByteArray) {
        synchronized(buf) {
            buf.append(String(bytes, Charsets.UTF_8))
            while (true) {
                val i = buf.indexOf("\n")
                if (i < 0) break
                val line = buf.substring(0, i)
                buf.delete(0, i + 1)
                main.post { listener.onLine(line) }
            }
            if (buf.length > 4096) buf.setLength(0)
        }
    }

    private fun post(text: String, connected: Boolean) = main.post { listener.onState(text, connected) }

    override fun send(line: String) {
        val g = gatt ?: return
        val c = rx ?: return
        val data = (line + "\n").toByteArray()
        if (Build.VERSION.SDK_INT >= 33) {
            g.writeCharacteristic(c, data, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
        } else {
            @Suppress("DEPRECATION")
            c.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
            @Suppress("DEPRECATION")
            c.value = data
            @Suppress("DEPRECATION")
            g.writeCharacteristic(c)
        }
    }

    override fun close() {
        closed = true
        gatt?.disconnect()
        gatt = null
    }
}

// ------------------------------------------------------------------ WiFi (TCP)
/**
 * Conecta por TCP al multimetro. Si [joinNetwork] es true (Android 10+), pide al sistema
 * unirse a la red "Multimetro-XXXX"; si no, usa la red WiFi a la que ya esta conectado el telefono.
 */
class WifiLink(
    ctx: Context,
    private val host: String,
    private val port: Int,
    joinNetwork: Boolean,
    password: String,
    private val listener: LinkListener,
) : MeterLink {
    private val main = Handler(Looper.getMainLooper())
    private val cm = ctx.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    private val writer = Executors.newSingleThreadExecutor()
    private var netCallback: ConnectivityManager.NetworkCallback? = null
    @Volatile private var socket: Socket? = null
    @Volatile private var out: OutputStream? = null
    @Volatile private var closed = false

    init {
        if (joinNetwork && Build.VERSION.SDK_INT >= 29) {
            post("WiFi: busca la red Multimetro-… y acepta la conexión", false)
            val spec = WifiNetworkSpecifier.Builder()
                .setSsidPattern(PatternMatcher("Multimetro-", PatternMatcher.PATTERN_PREFIX))
                .setWpa2Passphrase(password)
                .build()
            val req = NetworkRequest.Builder()
                .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
                .removeCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .setNetworkSpecifier(spec)
                .build()
            val cb = object : ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: Network) = open(network)
                override fun onUnavailable() { post("No se pudo unir a la red del multímetro", false) }
                override fun onLost(network: Network) {
                    if (!closed) post("Red WiFi del multímetro perdida", false)
                }
            }
            netCallback = cb
            cm.requestNetwork(req, cb)
        } else {
            // "Ya estoy en su red": se pide al sistema la red WiFi actual aunque no tenga internet.
            // Sin esto, Android (sobre todo Samsung) corta las conexiones (ECONNABORTED).
            post("WiFi: preparando la red…", false)
            val req = NetworkRequest.Builder()
                .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
                .removeCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .build()
            var opened = false
            val cb = object : ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: Network) {
                    if (!opened) { opened = true; open(network) }
                }
                override fun onLost(network: Network) {
                    if (!closed) post("Red WiFi del multímetro perdida", false)
                }
            }
            netCallback = cb
            cm.requestNetwork(req, cb)
            main.postDelayed({ if (!opened && !closed) { opened = true; open(findWifiNetwork()) } }, 3000)
        }
    }

    @Suppress("DEPRECATION")
    private fun findWifiNetwork(): Network? = cm.allNetworks.firstOrNull {
        cm.getNetworkCapabilities(it)?.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) == true
    }

    private fun open(network: Network?) {
        Thread {
            try {
                // Se usa la red WiFi aunque no tenga internet (si no, Android usaria los datos moviles).
                var s: Socket? = null
                var last: Exception? = null
                for (intento in 1..3) {
                    if (closed) return@Thread
                    post("WiFi: conectando a $host:$port (intento $intento de 3)…", false)
                    try {
                        val sock = network?.socketFactory?.createSocket() ?: Socket()
                        sock.connect(InetSocketAddress(host, port), 5000)
                        s = sock
                        break
                    } catch (e: Exception) {
                        last = e
                        Thread.sleep(1200)
                    }
                }
                if (s == null) throw last ?: Exception("sin respuesta")
                s.tcpNoDelay = true
                socket = s
                out = s.getOutputStream()
                post("Conectado por WiFi", true)
                send("INFO")
                val reader = BufferedReader(InputStreamReader(s.getInputStream(), Charsets.UTF_8))
                while (!closed) {
                    val line = reader.readLine() ?: break
                    main.post { listener.onLine(line) }
                }
                if (!closed) post("WiFi desconectado", false)
            } catch (e: Exception) {
                if (!closed) post("WiFi: error (${e.message})", false)
            }
        }.start()
    }

    private fun post(text: String, connected: Boolean) = main.post { listener.onState(text, connected) }

    override fun send(line: String) {
        writer.execute {
            try {
                out?.write((line + "\n").toByteArray())
                out?.flush()
            } catch (_: Exception) {
            }
        }
    }

    override fun close() {
        closed = true
        try { socket?.close() } catch (_: Exception) {}
        netCallback?.let { try { cm.unregisterNetworkCallback(it) } catch (_: Exception) {} }
        writer.shutdown()
    }
}
