---
name: "llResetScript"
category: "function"
type: "function"
language: "LSL"
description: "Resets the script to its initial state, clearing all variables and listeners"
wiki_url: "https://wiki.secondlife.com/wiki/llResetScript"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llResetScript()"
parameters: []
return_type: "void"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llresetscript"]
deprecated: "false"
---

# llResetScript

```lsl
void llResetScript()
```

Resets the script. All global variables return to their initial values, all listeners are removed, all timers are cancelled, and the script re-enters the `default` state, triggering `state_entry`.

## Behaviour

- All global variables reset to their initial values.
- All `llListen` registrations are removed.
- `llSetTimerEvent` is reset (timer cancelled).
- `llSensorRepeat` is cancelled.
- `llTarget` / `llRotTarget` are cancelled.
- The script re-enters `default` state — `state_entry` fires.
- Code after `llResetScript()` in the same handler does NOT execute.

## Common Uses

```lsl
// Reset on owner change
default
{
    changed(integer change)
    {
        if (change & CHANGED_OWNER)
            llResetScript();
    }
}

// Reset on rez
default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }
}
```

## See Also

- `llResetOtherScript` — reset another script in the same prim
- `llSetScriptState` — enable/disable a script
- `state_entry` — fires after reset
- `on_rez` — alternative reset trigger point


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llResetScript) — scraped 2026-03-18_

Resets the script.

## Examples

```lsl
default
{
    // reset script when the object is rezzed
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        // reset script when the owner or the inventory changed
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    // script initialization here
    state_entry()
    {
        ;
    }
}
```

## See Also

### Functions

- llResetOtherScript

<!-- /wiki-source -->
