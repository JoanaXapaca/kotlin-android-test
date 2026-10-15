package com.connexall.kotlintest

/**
 * Represents a call point device located in a hospital room.
 *
 * A call point is the physical button that a patient or nurse presses
 * to trigger a nurse call alert.
 */
data class CallPoint(
    val id: Int,
    val room: String,
    val active: Boolean = false
)

/**
 * Manages a collection of call points.
 *
 * Provides functions to register call points, activate them, resolve
 * them, and query their state. Used by the MobileConnex application
 * to keep track of the physical devices on the network.
 */
class CallPointManager {

    private val callPoints = mutableListOf<CallPoint>()
    private var nextId = 1

    /**
     * Registers a new call point for a given room.
     * Returns the created call point with its assigned ID.
     */
    fun registerCallPoint(room: String): CallPoint {
        val callPoint = CallPoint(id = nextId++, room = room)
        callPoints.add(callPoint)
        return callPoint
    }

    /**
     * Returns all registered call points.
     */
    fun getAllCallPoints(): List<CallPoint> = callPoints.toList()

    /**
     * Returns all call points that are currently active.
     */
    fun getActiveCallPoints(): List<CallPoint> = callPoints.filter { it.active }

    /**
     * Counts the number of active call points in a specific room.
     */
    fun countActiveInRoom(room: String): Int =
        callPoints.count { it.room == room && it.active }

    /**
     * Activates a call point by its ID.
     * Returns true if the call point was found and activated, false otherwise.
     */
    fun activate(id: Int): Boolean {
        val index = callPoints.indexOfFirst { it.id == id }
        if (index == -1) return false
        callPoints[index] = callPoints[index].copy(active = true)
        return true
    }

    /**
     * Resolves (deactivates) a call point by its ID.
     * Returns true if the call point was found and resolved, false otherwise.
     */
    fun resolve(id: Int): Boolean {
        val index = callPoints.indexOfFirst { it.id == id }
        if (index == -1) return false
        callPoints[index] = callPoints[index].copy(active = false)
        return true
    }

    /**
     * Removes all call points (used for reset or testing).
     */
    fun clear() {
        callPoints.clear()
        nextId = 1
    }
}