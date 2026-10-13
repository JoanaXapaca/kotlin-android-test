package com.connexall.kotlintest

import org.junit.Assert.assertNotNull
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

/**
 * E2E tests for the Android application using Robolectric.
 *
 * These tests verify that the app starts and runs correctly on a
 * simulated Android environment, without requiring an emulator.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class MainActivityE2ETest {

    @Test
    fun e2e001_mainActivityStartsWithoutCrashing() {
        val activity = Robolectric
            .buildActivity(MainActivity::class.java)
            .setup()
            .get()

        assertNotNull("MainActivity should not be null", activity)
    }

    @Test
    fun e2e002_calculatorWorksInAndroidContext() {
        val calculator = Calculator()
        val result = calculator.add(2, 3)
        assert(result == 5) { "Calculator should work in Android context" }
    }

    @Test
    fun e2e003_calculatorSubtractInAndroidContext() {
        val calculator = Calculator()
        val result = calculator.subtract(10, 4)
        assert(result == 6) { "Calculator subtract should work in Android context" }
    }
}