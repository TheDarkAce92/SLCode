---
name: "control"
category: "event"
type: "event"
language: "LSL"
description: "Result of llTakeControls library function call and user input."
signature: "control(key id, integer level, integer edge)"
wiki_url: 'https://wiki.secondlife.com/wiki/control'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Result of llTakeControls library function call and user input.


## Signature

```lsl
control(key id, integer level, integer edge)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` |  |
| `integer (bit_field)` | `level` | bitfield of CONTROL_* flags, non-zero while one or more keys is being held down. |
| `integer (bit_field)` | `edge` | bitfield of CONTROL_* flags, non-zero when one or more keys have been just pressed or released. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/control)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/control) — scraped 2026-03-18_

## Caveats

- CONTROL_ROT_LEFT and CONTROL_ROT_RIGHT can be triggered when an object is selected or edited. If the user is running Viewer 2.0 and later, llGetAgentInfo will have AGENT_AUTOPILOT set in this case.

  - Sitting upon an object that takes control may also trigger CONTROL_FWD, CONTROL_BACK, CONTROL_DOWN and CONTROL_UP, depending on avatar position relative to the seat.
  - Autopilot control events can continue for a short time after AGENT_AUTOPILOT drops.
- The 'levels' and 'edges' of the control() event both receive (CONTROL_FWD + CONTROL_BACK) (value 3) after teleport, effecting scripts that use this combination for faster movement. Calling llTakeControls() again after a llSleep(3) will filter this out.

## Examples

```lsl
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);
    }
    run_time_permissions(integer perm)
    {
        if(PERMISSION_TAKE_CONTROLS & perm)
        {
            llTakeControls(
                            CONTROL_FWD |
                            CONTROL_BACK |
                            CONTROL_LEFT |
                            CONTROL_RIGHT |
                            CONTROL_ROT_LEFT |
                            CONTROL_ROT_RIGHT |
                            CONTROL_UP |
                            CONTROL_DOWN |
                            CONTROL_LBUTTON |
                            CONTROL_ML_LBUTTON |
                            0, TRUE, FALSE);
                            // | 0 is for edit convenience,
                            // it does not change the mask.
        }
    }
    control(key id, integer level, integer edge)
    {
        integer start = level & edge;
        integer end = ~level & edge;
        integer held = level & ~edge;
        integer untouched = ~(level | edge);
        llOwnerSay(llList2CSV([level, edge, start, end, held, untouched]));
    }
}
```

## Notes

llGetRot in mouselook for an attachment returns the angle the avatar is looking in.

There are some bugs when you put two scripts in the same prim and call LlTakeControls(), the **id** may not be the intended one. See [SVC-3187](http://jira.secondlife.com/browse/SVC-3187).

## See Also

### Events

- run_time_permissions

### Functions

- llTakeControls
- llReleaseControls
- llRequestPermissions

<!-- /wiki-source -->
