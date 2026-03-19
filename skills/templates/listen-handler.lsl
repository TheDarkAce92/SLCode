// Skill: listen-handler
// Version: 0.1.0.0
// Purpose: Boilerplate listen/dialog pattern for LSL
// Usage: Copy and adapt channel, filter, and dialog options as needed
// Created: 2026-03-09
// Last modified: 2026-03-09

// ── Listen / Dialog Handler Boilerplate ───────────────────────────────────
// Always store the listen handle so you can remove it when done.
// Remove listeners in state_exit or when no longer needed — each active
// listener costs memory and CPU even when idle.

integer g_listenHandle = 0;
integer g_dialogChannel;

// Generate a unique negative channel to avoid collisions
integer dialogChannel() {
    return (integer)("0x" + llGetSubString(llMD5String((string)llGetKey(), 0), 0, 6)) * -1;
}

default {
    state_entry() {
        g_dialogChannel = dialogChannel();
    }

    touch_start(integer num_detected) {
        key toucher = llDetectedKey(0);

        // Remove any previous listener before creating a new one
        if (g_listenHandle) {
            llListenRemove(g_listenHandle);
        }

        // Show dialog — listen only to the toucher on the private channel
        g_listenHandle = llListen(g_dialogChannel, "", toucher, "");
        llDialog(toucher, "Choose an option:", ["Option A", "Option B", "Close"], g_dialogChannel);

        // Timeout after 60 seconds
        llSetTimerEvent(60.0);
    }

    listen(integer channel, string name, key id, string message) {
        if (message == "Close") {
            llListenRemove(g_listenHandle);
            g_listenHandle = 0;
            llSetTimerEvent(0.0);
        } else if (message == "Option A") {
            llOwnerSay("Option A selected by " + name);
            llListenRemove(g_listenHandle);
            g_listenHandle = 0;
            llSetTimerEvent(0.0);
        } else if (message == "Option B") {
            llOwnerSay("Option B selected by " + name);
            llListenRemove(g_listenHandle);
            g_listenHandle = 0;
            llSetTimerEvent(0.0);
        }
    }

    timer() {
        // Timeout — clean up listener
        llListenRemove(g_listenHandle);
        g_listenHandle = 0;
        llSetTimerEvent(0.0);
        llOwnerSay("Dialog timed out.");
    }
}
