package com.degnanf.multimetro

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.view.View

/** Grafica de las ultimas lecturas con escala automatica. */
class GraphView(ctx: Context) : View(ctx) {
    private val max = 300
    private val data = DoubleArray(max)
    private var count = 0
    private var head = 0
    var unit = "V"

    private val dp = resources.displayMetrics.density
    private val line = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#7CFC9A"); strokeWidth = 2 * dp; style = Paint.Style.STROKE
    }
    private val grid = Paint().apply { color = Color.parseColor("#33FFFFFF"); strokeWidth = 1f }
    private val text = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.LTGRAY; textSize = 11 * dp }
    private val path = Path()

    fun add(v: Double) {
        data[head] = v
        head = (head + 1) % max
        if (count < max) count++
        invalidate()
    }

    fun clear() {
        count = 0; head = 0; invalidate()
    }

    private fun at(i: Int) = data[(head - count + i + max) % max]

    override fun onDraw(c: Canvas) {
        c.drawColor(Color.parseColor("#101418"))
        val w = width.toFloat()
        val h = height.toFloat()
        for (k in 1..3) c.drawLine(0f, h * k / 4, w, h * k / 4, grid)
        if (count < 2) {
            c.drawText("Sin datos", 8 * dp, h / 2, text)
            return
        }
        var lo = Double.MAX_VALUE
        var hi = -Double.MAX_VALUE
        for (i in 0 until count) { val v = at(i); if (v < lo) lo = v; if (v > hi) hi = v }
        if (hi - lo < 1e-12) { hi += 1e-9 + kotlin.math.abs(hi) * 0.01; lo -= 1e-9 + kotlin.math.abs(lo) * 0.01 }
        val pad = (hi - lo) * 0.08
        lo -= pad; hi += pad
        path.reset()
        for (i in 0 until count) {
            val x = w * i / (max - 1)
            val y = (h - (at(i) - lo) / (hi - lo) * h).toFloat()
            if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
        }
        c.drawPath(path, line)
        c.drawText(Fmt.siText(hi - pad, unit), 6 * dp, 14 * dp, text)
        c.drawText(Fmt.siText(lo + pad, unit), 6 * dp, h - 6 * dp, text)
    }
}
