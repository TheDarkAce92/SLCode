---
name: "State Machines"
category: "tutorials"
type: "reference"
language: "LSL"
description: "How to use LSL states to build finite state machines — state_entry, state_exit, variable persistence, and safe transition patterns"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# State Machines

LSL scripts are structured around **states**. Every script has exactly one active state at a time. Each state defines which events it responds to. Switching states is how LSL scripts implement finite state machines (FSMs).

## The `default` State

Every script must contain a `default` state. It is always the starting state when a script is saved, reset, or first runs. Additional states are user-defined.

```lsl
default
{
    state_entry()
    {
        llSay(0, "Script started.");
    }
}
```

## Defining Additional States

```lsl
default
{
    touch_end(integer num_detected)
    {
        state active;
    }
}

state active
{
    state_entry()
    {
        llSay(0, "Now active.");
    }

    touch_end(integer num_detected)
    {
        state default;
    }
}
```

The `state <name>` keyword triggers a transition immediately — no code after it in the same event handler is executed.

## State Transition Order

When `state <name>` is reached:

1. The current event handler finishes executing up to the `state` keyword.
2. `state_exit` fires in the old state.
3. All active listeners and sensors are **automatically cancelled**. The timer is **not** cancelled — it persists across state changes and will fire in the new state if that state has a `timer()` handler.
4. `state_entry` fires in the new state.

Any events that arrive during the transition are discarded.

## Global Variables Persist Across States

Variables declared at script scope (outside any state or function) retain their values when states change. Local variables inside event handlers are always reset.

```lsl
integer visit_count = 0;  // persists across all state changes

default
{
    state_entry()
    {
        llSay(0, "Visits: " + (string)visit_count);
    }

    touch_end(integer num_detected)
    {
        visit_count++;
        state active;
    }
}

state active
{
    state_entry()
    {
        // visit_count still has the value set in default
        llSay(0, "Active. Total visits: " + (string)visit_count);
    }

    touch_end(integer num_detected)
    {
        state default;
    }
}
```

## Cleanup in `state_exit`

Listeners and sensors are auto-cancelled on state change, but the **timer is not** — it continues running. If you do not want the timer to carry over into the next state, stop it explicitly in `state_exit`.

The example below shows `llListenRemove` called explicitly in `state_exit` even though listeners are auto-cancelled. This is redundant in the normal state-change path, but is good practice: if you ever call `llSetTimerEvent(0.0)` or another early-exit path before reaching the `state` keyword, the explicit removal guarantees cleanup regardless.

```lsl
integer listen_handle;

default
{
    state_entry()
    {
        listen_handle = llListen(0, "", NULL_KEY, "");
        llSetTimerEvent(30.0);
    }

    timer()
    {
        state idle;
    }

    state_exit()
    {
        llListenRemove(listen_handle);
        llSetTimerEvent(0.0);
    }
}

state idle
{
    state_entry()
    {
        llSay(0, "Timed out. Now idle.");
    }
}
```

## Use `touch_end`, Not `touch_start`, for State Changes

State changes inside `touch_start` can cause problems. Always trigger state changes from `touch_end`.

```lsl
// Correct
touch_end(integer num_detected)
{
    state active;
}

// Avoid
touch_start(integer num_detected)
{
    state active;  // can cause unexpected behaviour
}
```

## `state_exit` Does Not Fire on Script Reset

When a script resets — whether via the viewer reset button or being saved — `state_exit` does not fire. `state_entry` fires immediately in `default` on the next run. Keep this in mind if your `state_exit` performs important cleanup — consider putting that cleanup in `state_entry` of `default` as well.

## Practical Example: Lockable Object

```lsl
default
{
    state_entry()
    {
        llSetText("Unlocked — touch to lock", <0,1,0>, 1.0);
    }

    touch_end(integer num_detected)
    {
        if (llDetectedKey(0) != llGetOwner())
        {
            llSay(0, "Only the owner can lock this.");
            return;
        }
        state locked;
    }
}

state locked
{
    state_entry()
    {
        llSetText("Locked — touch to unlock", <1,0,0>, 1.0);
    }

    touch_end(integer num_detected)
    {
        if (llDetectedKey(0) != llGetOwner())
        {
            llSay(0, "This object is locked.");
            return;
        }
        state default;
    }
}
```

## Key Points

- `default` is mandatory and always the starting state.
- `state <name>` inside an event handler triggers a transition; code after it in the same handler does not run.
- On transition: `state_exit` fires, then listeners and sensors are cancelled (timer persists), then `state_entry` fires.
- Global variables survive state changes; local variables do not.
- `state_exit` does **not** fire when the script resets.
- Use `touch_end` (not `touch_start`) to trigger state changes safely.
