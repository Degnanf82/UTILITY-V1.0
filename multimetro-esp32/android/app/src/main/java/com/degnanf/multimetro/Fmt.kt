package com.degnanf.multimetro

import java.util.Locale
import kotlin.math.abs
import kotlin.math.floor
import kotlin.math.log10
import kotlin.math.pow

object Fmt {
    private val PREFIX = arrayOf("p", "n", "µ", "m", "", "k", "M")

    fun unitSymbol(u: String): String = when (u) {
        "ohm" -> "Ω"
        else -> u
    }

    /** 0.0047 F -> ("4.700", "mF") */
    fun si(v: Double, unit: String): Pair<String, String> {
        var e = if (v != 0.0) floor(log10(abs(v)) / 3).toInt() else 0
        e = e.coerceIn(-4, 2)
        val m = v / 1000.0.pow(e)
        val am = abs(m)
        val txt = when {
            am < 9.9995 -> String.format(Locale.US, "%.3f", m)
            am < 99.995 -> String.format(Locale.US, "%.2f", m)
            else -> String.format(Locale.US, "%.1f", m)
        }
        return txt to PREFIX[e + 4] + unitSymbol(unit)
    }

    fun siText(v: Double, unit: String): String = si(v, unit).let { "${it.first} ${it.second}" }

    /** "4.7k" -> 4700, "100n" -> 1e-7, "2.5" -> 2.5 (acepta coma decimal y unidades al final). */
    fun parse(input: String): Double? {
        var s = input.trim().replace(',', '.').replace(" ", "")
        s = s.trimEnd('V', 'v', 'A', 'Ω', 'F', 'z', 'H').removeSuffix("ohm").removeSuffix("Ohm")
        if (s.isEmpty()) return null
        val mult = when (s.last()) {
            'p' -> 1e-12; 'n' -> 1e-9; 'u', 'µ' -> 1e-6; 'm' -> 1e-3
            'k', 'K' -> 1e3; 'M' -> 1e6
            else -> 1.0
        }
        if (mult != 1.0) s = s.dropLast(1)
        return s.toDoubleOrNull()?.times(mult)
    }
}
