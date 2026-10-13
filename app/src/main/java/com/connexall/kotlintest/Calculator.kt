package com.connexall.kotlintest

/**
 * Calculator provides basic arithmetic operations.
 *
 * This class is intentionally simple so that the pipeline can verify
 * the full cycle of build, test, and static analysis.
 */
class Calculator {

    /**
     * Returns the sum of two integers.
     */
    fun add(a: Int, b: Int): Int {
        return a + b
    }

    /**
     * Returns the difference between two integers.
     */
    fun subtract(a: Int, b: Int): Int {
        return a - b
    }
}