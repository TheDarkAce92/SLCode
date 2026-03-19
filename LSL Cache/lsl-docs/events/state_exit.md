---
name: "state_exit"
category: "event"
type: "event"
language: "LSL"
description: "Fires just before the script leaves the current state due to a state change"
wiki_url: "https://wiki.secondlife.com/wiki/State_exit"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "state_exit()"
parameters: []
deprecated: "false"
---

# state_exit

```lsl
state_exit()
{
    // cleanup before leaving state
}
```

Fires at the end of the current event handler, just before the script transitions to a new state. Use it to clean up resources (listeners, timers, sensors) before the state change completes.

## Order of Events on State Change

1. Current event handler finishes executing
2. `state_exit` fires in the current state
3. All listeners, sensors, and targets are cancelled. The timer is **not** cancelled — it persists into the new state.
4. `state_entry` fires in the new state

## Caveats

- `state_exit` does NOT fire on script reset (`llResetScript`).
- By the time `state_exit` fires, it is too late to cancel the state change.
- Global variables retain their values through state transitions.
- Events queued during `state_exit` are dumped before the next state is entered — use `state_entry` to handle post-transition logic.

## Example

```lsl
default
{
    state_entry()
    {
        llSetTimerEvent(5.0);
    }

    state_exit()
    {
        llSetTimerEvent(0.0);  // stop timer — it persists across state changes, so cancel explicitly if not wanted
        llOwnerSay("Leaving default state");
    }

    timer()
    {
        state active;
    }
}

state active
{
    state_entry()
    {
        llOwnerSay("Entered active state");
    }
}
```

## See Also

- `state_entry` — fires when entering a state
- `state` keyword — triggers state transitions


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/state_exit) — scraped 2026-03-18_

## Caveats

- Events queued during state_exit, are dumped before the next state is entered. use state_entry to avoid this, when possible. See state for further caveats.

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay("Entering default state");
    }
    touch_end(integer detected)
    {
        // Note: NEVER do a state change from a touch_start event -
        // - this can result in a missed touch_start on re-entering this state
        // Here we do the state change safely from within touch_end
        state other;
    }
    state_exit()
    {
        llOwnerSay("leaving default state");
    }
}

state other
{
    state_entry()
    {
        llOwnerSay("Entering state \"other\"");
    }
    touch_end(integer detected)
    {
        state default;
    }
    state_exit()
    {
        llOwnerSay("leaving state \"other\"");
    }
}
```

## Notes

While the default state_entry is triggered on script reset, state_exit is not triggered prior to the reset.

<!-- /wiki-source -->
