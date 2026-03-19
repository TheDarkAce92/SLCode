---
name: "llModifyLand"
category: "function"
type: "function"
language: "LSL"
description: 'Modify land with action on brush

The position of the prim is used to determine the input for various flags.'
signature: "void llModifyLand(integer action, integer brush)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llModifyLand'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llmodifyland"]
---

Modify land with action on brush

The position of the prim is used to determine the input for various flags.


## Signature

```lsl
void llModifyLand(integer action, integer brush);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `action` | LAND_* flag |
| `integer` | `brush` | LAND_*_BRUSH flag |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llModifyLand)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llModifyLand) — scraped 2026-03-18_

Modify land with action on brush

## Caveats

- This function has no effect if the script's owner is offline or not in the same sim as the scripted object.
- Uncontrolled use of llModifyLand in scripted objects may force the region's navmesh to rebake continually and cause Memory Allocated for the region to exceed its limit, making it impossible to rez objects. ([BUG-9047](https://jira.secondlife.com/browse/BUG-9047))
- This function has no effect if the scripted object is deeded to a group.
- Playing with this command, I have found that the LAND_SMALL_BRUSH edits a 4m x 4m area. The LAND_MEDIUM_BRUSH and the LAND_LARGE_BRUSH, both edit an 8m x 8m area. However using 0 instead of LAND_SMALL_BRUSH will edit a 2m x 2m area. I have bug reported this, but until it gets fixed, it should be noted. correct values for the brushes are 0, 1 and 2, not 1, 2, and 3. - Bev
- If the script is in a prim that is attached to an avatar or is in the child prim of a linkset, then the local position relative to it's attachment point or root prim is used rather than the position within the region. ([BUG-4929](https://jira.secondlife.com/browse/BUG-4929))
- If land is not owned by script owner or the owner doesn't have terraform permissions, the script will silently fail.
- You cannot change altitude beyond land terraform limits for the specified parcel..

## Examples

```lsl
default
{
    state_entry()
    {
        llSetTimerEvent(0.1);
    }

    timer()
    {
        llModifyLand(LAND_LEVEL, 0);
    }
}
```

<!-- /wiki-source -->
