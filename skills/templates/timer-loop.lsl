// Skill: timer-loop
// Version: 0.1.0.0
// Purpose: Boilerplate timer pattern for LSL
// Usage: Copy and adapt interval and timer body as needed
// Created: 2026-03-09
// Last modified: 2026-03-09

// ── Timer Loop Boilerplate ─────────────────────────────────────────────────
// LSL only supports one timer per script. llSetTimerEvent(0.0) stops the timer.
// Minimum reliable interval is ~0.01 seconds, but high-frequency timers are
// expensive — use the lowest frequency that meets your needs.
// A timer event will NOT fire if the previous one has not yet finished.

float TIMER_INTERVAL = 5.0; // seconds — adjust as needed
integer g_timerRunning = FALSE;

default {
    state_entry() {
        // Start the timer on rez/reset
        llSetTimerEvent(TIMER_INTERVAL);
        g_timerRunning = TRUE;
    }

    touch_start(integer num_detected) {
        // Toggle timer on touch
        if (g_timerRunning) {
            llSetTimerEvent(0.0);
            g_timerRunning = FALSE;
            llOwnerSay("Timer stopped.");
        } else {
            llSetTimerEvent(TIMER_INTERVAL);
            g_timerRunning = TRUE;
            llOwnerSay("Timer started.");
        }
    }

    timer() {
        // ── Your repeating logic here ──────────────────────────────────
        llOwnerSay("Timer fired at: " + (string)llGetUnixTime());
        // ──────────────────────────────────────────────────────────────
    }

    on_rez(integer start_param) {
        llResetScript();
    }
}
