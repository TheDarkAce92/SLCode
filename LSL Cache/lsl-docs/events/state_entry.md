---
name: "state_entry"
category: "event"
type: "event"
language: "LSL"
description: "Fires when a script enters a state, on script start, reset, or state change"
wiki_url: "https://wiki.secondlife.com/wiki/State_entry"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "state_entry()"
parameters: []
deprecated: "false"
---

# state_entry

```lsl
state_entry()
{
    // initialisation code
}
```

Triggered when the script enters a state. Equivalent to the constructor/initialiser for each state.

## When Triggered

- Script is saved or added to an object
- Script is reset (`llResetScript`, `llResetOtherScript`, or viewer Reset)
- A `state` change completes (after `state_exit` fires in the previous state)
- Object is rezzed without saved script status (e.g., copy taken from in-world; rezzed into no-script zone then into scripted zone)

## When NOT Triggered

- Object is rezzed with saved script status — use `on_rez` instead
- Script moves between simulators or a simulator restarts

## Caveats

- Do not perform state changes inside `touch_start`; use `touch_end` instead to avoid missing subsequent touch events.
- All active listeners, sensors, and targets from the previous state are cancelled before `state_entry` fires. The timer is **not** cancelled — it persists across state changes and will fire in the new state if it has a `timer()` handler.
- Global variables retain their values across state changes.

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0, "Script started in default state");
        llSetText("Click me", <1.0, 1.0, 1.0>, 1.0);
    }

    touch_end(integer num_detected)
    {
        state active;
    }

    state_exit()
    {
        llSay(0, "Leaving default state");
    }
}

state active
{
    state_entry()
    {
        llSay(0, "Entered active state");
        llSetTimerEvent(5.0);
    }

    timer()
    {
        state default;
    }
}
```

## See Also

- `state_exit` — fires just before leaving a state
- `on_rez` — fires when object is rezzed (including with saved status)
- `state` keyword — triggers state changes


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/state_entry) — scraped 2026-03-18_

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0,
            "You either just saved the script after editing it"
            + "\nand/or the script (re)entered the default state.");

        llSetText("Click to change states", <1.0, 1.0, 1.0>, 1.0);
    }

    touch_end(integer num_detected)
    {
        // Note: NEVER do a state change from within a touch_start event -
        // - that can lead to the next touch_start on return to this state to be missed.
        // Here we do the state change safely, from within touch_end
        state two;
    }

    state_exit()
    {
        llSay(0, "The script leaves the default state.");
    }
}

state two
{
    state_entry()
    {
        llSay(0, "The script entered state 'two'");
        state default;
    }

    state_exit()
    {
        llSay(0, "The script leaves state 'two'");
    }
}
```

## See Also

### Events

- **on_rez** — Triggered when the object is rezzed
- **state_exit** — Triggered when the state is exited at state change

### Functions

- **llResetScript** — Resets the script
- **llResetOtherScript** — Resets another script in the prim
- **llGetStartParameter** — on_rez

<!-- /wiki-source -->
