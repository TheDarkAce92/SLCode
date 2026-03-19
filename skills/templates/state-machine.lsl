// Skill: state-machine
// Version: 0.1.0.0
// Purpose: Boilerplate FSM (Finite State Machine) pattern for LSL
// Usage: Copy and adapt states as needed
// Created: 2026-03-09
// Last modified: 2026-03-09

// ── State Machine Boilerplate ──────────────────────────────────────────────
// LSL scripts have one active state at a time. State changes clear the event
// queue and reset all local variables. Use states to cleanly separate modes.

default {
    state_entry() {
        llOwnerSay("Entering default state.");
        // Initialise script — set up listeners, timers, etc.
    }

    touch_start(integer num_detected) {
        // Transition to active state on touch
        state active;
    }

    on_rez(integer start_param) {
        llResetScript();
    }
}

state active {
    state_entry() {
        llOwnerSay("Entering active state.");
        // Set up behaviour for active mode
        llSetTimerEvent(30.0); // Example: 30-second timeout
    }

    state_exit() {
        llSetTimerEvent(0.0); // Always cancel timers on exit
    }

    touch_start(integer num_detected) {
        // Return to default on touch
        state default;
    }

    timer() {
        llOwnerSay("Timer fired in active state.");
        state default; // Example: return to default after timeout
    }
}
