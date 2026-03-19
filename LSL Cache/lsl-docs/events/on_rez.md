---
name: "on_rez"
category: "event"
type: "event"
language: "LSL"
description: "Fires when the object is rezzed (by script or by user), and when an attachment's owner logs in"
wiki_url: "https://wiki.secondlife.com/wiki/On_rez"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "on_rez(integer start_param)"
parameters:
  - name: "start_param"
    type: "integer"
    description: "Parameter from llRezObject or llRezAtRoot; 0 if rezzed by user or from inventory without a rezzing function"
deprecated: "false"
---

# on_rez

```lsl
on_rez(integer start_param)
{
    // handle rez
}
```

Fires when an object is rezzed (by user or by `llRezObject`/`llRezAtRoot`), or when an attachment's owner logs in, or when the object is attached from inventory.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start_param` | integer | Value passed to `llRezObject`/`llRezAtRoot`; 0 if rezzed by user |

## Caveats

- `start_param` is 0 when the user rezzes the object manually.
- `start_param` can be retrieved later via `llGetStartParameter()`.
- `state_entry` fires before `on_rez` if it hasn't fired yet.
- `on_rez` fires before `attach` during inventory attachment or login.
- Timing between `object_rez` (parent) and `on_rez` (child) is not guaranteed.
- Unlike `state_entry`, `on_rez` fires even when the object is rezzed with saved script status.

## Example

```lsl
default
{
    on_rez(integer start_param)
    {
        llResetScript();  // reinitialise on every rez
    }
}
```

```lsl
// Use start_param for configuration
default
{
    on_rez(integer start_param)
    {
        if (start_param > 0)
            llOwnerSay("Rezzed with param: " + (string)start_param);
    }
}
```

## See Also

- `state_entry` — fires on script start/reset/state change
- `attach` — fires when object is attached to or detached from an avatar
- `llRezObject` — rez an object with a start parameter
- `llGetStartParameter` — retrieve start_param at any time


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/on_rez) — scraped 2026-03-18_

## Caveats

- If an object is rezzed by another object then the object_rez event in the parent object does not trigger at the same time as the on_rez event in the child object and the order of the events is not guaranteed. See the examples in object_rez for how to reliably establish communications between objects when rezzing.

## Examples

```lsl
default
{
    on_rez(integer start_param)
    {
        // Restarts the script every time the object is rezzed
        llResetScript();
    }
}
```

## Notes

### state_entry & on_rez

state_entry will be triggered prior to on_rez if state_entry has not been run prior.

### on_rez & attach

on_rez will be triggered prior to attach when attaching from inventory or during login.

### on_rez & slow events

If the script was already processing an event at rez time, on_rez does not **not** trigger until the current event handler is completed. (same with attach)

## See Also

### Events

- **object_rez** — triggered when this object rezzes an object from inventory
- **state_entry** — triggered during script startup, reset and state change

### Functions

- llGetStartParameter
- llRezObject
- llRezAtRoot

<!-- /wiki-source -->
