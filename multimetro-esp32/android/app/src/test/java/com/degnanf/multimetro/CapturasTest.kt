package com.degnanf.multimetro

import android.graphics.Bitmap
import android.graphics.Canvas
import android.view.View
import android.view.ViewGroup
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import kotlin.math.sin

/**
 * Genera capturas de la app con datos de ejemplo (no es una prueba funcional).
 * Las imagenes quedan en app/build/capturas/.
 */
@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(sdk = [34], qualifiers = "w360dp-h740dp-xhdpi")
class CapturasTest {

    private fun capture(name: String, feed: (MainActivity) -> Unit) {
        val act = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        feed(act)
        val content = act.findViewById<ViewGroup>(android.R.id.content).getChildAt(0) as ViewGroup
        // Se mide como la pantalla real del telefono (alto fijo), para ver que no sobra espacio
        val inner = content
        val w = act.resources.displayMetrics.widthPixels
        val h = act.resources.displayMetrics.heightPixels
        inner.measure(View.MeasureSpec.makeMeasureSpec(w, View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(h, View.MeasureSpec.EXACTLY))
        inner.layout(0, 0, inner.measuredWidth, inner.measuredHeight)
        val bmp = Bitmap.createBitmap(inner.measuredWidth, inner.measuredHeight, Bitmap.Config.ARGB_8888)
        inner.draw(Canvas(bmp))
        val dir = File("build/capturas").apply { mkdirs() }
        File(dir, "$name.png").outputStream().use { bmp.compress(Bitmap.CompressFormat.PNG, 100, it) }
    }

    private fun stats(vals: List<Double>) =
        ",\"mn\":${vals.min()},\"mx\":${vals.max()},\"av\":${vals.average()}"

    @Test
    fun voltaje() = capture("app-voltaje") { a ->
        a.onState("Conectado por Bluetooth", true)
        val vals = ArrayList<Double>()
        for (i in 0 until 160) {
            val v = 12.07 + 0.35 * sin(i / 14.0) + 0.02 * sin(i * 1.7)
            vals += v
            a.onLine("{\"t\":\"m\",\"m\":\"DCV\",\"u\":\"V\",\"v\":$v,\"ol\":0,\"h\":0,\"rel\":0,\"r\":-1${stats(vals)}}")
        }
    }

    @Test
    fun resistencia() = capture("app-resistencia") { a ->
        a.onState("Conectado por WiFi", true)
        val vals = ArrayList<Double>()
        for (i in 0 until 80) {
            val v = 4688.0 + 6.0 * sin(i / 5.0)
            vals += v
            a.onLine("{\"t\":\"m\",\"m\":\"OHM\",\"u\":\"ohm\",\"v\":$v,\"ol\":0,\"h\":0,\"rel\":0,\"r\":1${stats(vals)}}")
        }
    }

    @Test
    fun capacitor() = capture("app-capacitor") { a ->
        a.onState("Conectado por Bluetooth", true)
        val vals = ArrayList<Double>()
        for (i in 0 until 30) {
            val v = 98.6e-9 + 0.4e-9 * sin(i / 4.0)
            vals += v
            a.onLine("{\"t\":\"m\",\"m\":\"CAP\",\"u\":\"F\",\"v\":$v,\"ol\":0,\"h\":1,\"rel\":0,\"r\":0${stats(vals)}}")
        }
    }
}
