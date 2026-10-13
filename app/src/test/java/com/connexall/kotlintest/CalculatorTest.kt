package com.connexall.kotlintest

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * Unit tests for the Calculator class.
 */
class CalculatorTest {

    private val calculator = Calculator()

    @Test
    fun add_withPositiveNumbers_returnsSum() {
        assertEquals(5, calculator.add(2, 3))
        assertEquals(300, calculator.add(100, 200))
    }

    @Test
    fun add_withNegativeNumbers_returnsSum() {
        assertEquals(-300, calculator.add(-100, -200))
        assertEquals(0, calculator.add(-1, 1))
    }

    @Test
    fun add_withZero_returnsSameNumber() {
        assertEquals(0, calculator.add(0, 0))
        assertEquals(5, calculator.add(5, 0))
        assertEquals(5, calculator.add(0, 5))
    }

    @Test
    fun subtract_withPositiveNumbers_returnsDifference() {
        assertEquals(6, calculator.subtract(10, 4))
        assertEquals(100, calculator.subtract(200, 100))
    }

    @Test
    fun subtract_withNegativeNumbers_returnsDifference() {
        assertEquals(100, calculator.subtract(-100, -200))
        assertEquals(0, calculator.subtract(-5, -5))
    }

    @Test
    fun subtract_withZero_returnsSameNumber() {
        assertEquals(-100, calculator.subtract(0, 100))
        assertEquals(100, calculator.subtract(100, 0))
    }
}