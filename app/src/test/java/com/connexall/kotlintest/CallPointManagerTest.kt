package com.connexall.kotlintest

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

/**
 * Unit tests for the CallPointManager class.
 */
class CallPointManagerTest {

    private lateinit var manager: CallPointManager

    @Before
    fun setUp() {
        manager = CallPointManager()
    }

    // --- registerCallPoint ---

    @Test
    fun registerCallPoint_assignsSequentialIds() {
        val cp1 = manager.registerCallPoint("Room 101")
        val cp2 = manager.registerCallPoint("Room 102")
        val cp3 = manager.registerCallPoint("Room 103")

        assertEquals(1, cp1.id)
        assertEquals(2, cp2.id)
        assertEquals(3, cp3.id)
    }

    @Test
    fun registerCallPoint_startsInactive() {
        val cp = manager.registerCallPoint("Room 101")
        assertFalse(cp.active)
    }

    @Test
    fun registerCallPoint_storesRoom() {
        val cp = manager.registerCallPoint("Room 101")
        assertEquals("Room 101", cp.room)
    }

    // --- getAllCallPoints ---

    @Test
    fun getAllCallPoints_returnsEmptyListInitially() {
        assertEquals(0, manager.getAllCallPoints().size)
    }

    @Test
    fun getAllCallPoints_returnsAllRegistered() {
        manager.registerCallPoint("Room 101")
        manager.registerCallPoint("Room 102")
        assertEquals(2, manager.getAllCallPoints().size)
    }

    // --- activate ---

    @Test
    fun activate_returnsTrueForExistingCallPoint() {
        val cp = manager.registerCallPoint("Room 101")
        assertTrue(manager.activate(cp.id))
    }

    @Test
    fun activate_setsCallPointActive() {
        val cp = manager.registerCallPoint("Room 101")
        manager.activate(cp.id)
        assertTrue(manager.getAllCallPoints().first { it.id == cp.id }.active)
    }

    @Test
    fun activate_returnsFalseForUnknownId() {
        assertFalse(manager.activate(999))
    }

    // --- resolve ---

    @Test
    fun resolve_deactivatesCallPoint() {
        val cp = manager.registerCallPoint("Room 101")
        manager.activate(cp.id)
        assertTrue(manager.resolve(cp.id))
        assertFalse(manager.getAllCallPoints().first { it.id == cp.id }.active)
    }

    @Test
    fun resolve_returnsFalseForUnknownId() {
        assertFalse(manager.resolve(999))
    }

    // --- getActiveCallPoints ---

    @Test
    fun getActiveCallPoints_returnsEmptyWhenNoneActive() {
        manager.registerCallPoint("Room 101")
        manager.registerCallPoint("Room 102")
        assertEquals(0, manager.getActiveCallPoints().size)
    }

    @Test
    fun getActiveCallPoints_returnsOnlyActive() {
        val cp1 = manager.registerCallPoint("Room 101")
        val cp2 = manager.registerCallPoint("Room 102")
        manager.registerCallPoint("Room 103")

        manager.activate(cp1.id)
        manager.activate(cp2.id)

        val active = manager.getActiveCallPoints()
        assertEquals(2, active.size)
        assertTrue(active.all { it.active })
    }

    // --- countActiveInRoom ---

    @Test
    fun countActiveInRoom_countsOnlyMatchingRoom() {
        val cp1 = manager.registerCallPoint("Room 101")
        val cp2 = manager.registerCallPoint("Room 101")
        val cp3 = manager.registerCallPoint("Room 102")

        manager.activate(cp1.id)
        manager.activate(cp2.id)
        manager.activate(cp3.id)

        assertEquals(2, manager.countActiveInRoom("Room 101"))
        assertEquals(1, manager.countActiveInRoom("Room 102"))
        assertEquals(0, manager.countActiveInRoom("Room 103"))
    }

    @Test
    fun countActiveInRoom_ignoresInactive() {
        val cp = manager.registerCallPoint("Room 101")
        manager.activate(cp.id)
        manager.resolve(cp.id)
        assertEquals(0, manager.countActiveInRoom("Room 101"))
    }

    // --- clear ---

    @Test
    fun clear_removesAllCallPoints() {
        manager.registerCallPoint("Room 101")
        manager.registerCallPoint("Room 102")
        manager.clear()
        assertEquals(0, manager.getAllCallPoints().size)
    }

    @Test
    fun clear_resetsIdCounter() {
        manager.registerCallPoint("Room 101")
        manager.clear()
        val newCp = manager.registerCallPoint("Room 102")
        assertEquals(1, newCp.id)
    }
}