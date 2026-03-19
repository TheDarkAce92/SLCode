---
name: "llGetAgentSize"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is an estimated size of the requested avatar.

ZERO_VECTOR is returned if avatar is not in the region or if it is not an avatar.'
signature: "vector llGetAgentSize(key id)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAgentSize'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetagentsize"]
---

Returns a vector that is an estimated size of the requested avatar.

ZERO_VECTOR is returned if avatar is not in the region or if it is not an avatar.


## Signature

```lsl
vector llGetAgentSize(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentSize)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentSize) — scraped 2026-03-18_

Returns a vector that is an estimated size of the requested avatar.

## Caveats

- The returned vector is an estimate calculated from the avatar's current shape including shoes. x is a constant 0.45, y is a constant 0.60, z is the approximate total height of all avatar's bones, with an arbitrary amount added or subtracted based on the current shape's "Hover" setting. Reported height is constrained to the range 1.1 to 2.45 meters, and does not include animation or mesh bone offsets.

  - Due to the shape Hover setting, and mesh and animation offsets, it is not possible to use this function to determine the rendered height of an avatar with any degree of confidence.
- As of Second Life Server 13.11.19.284082, the return value is the avatar's reported bounding box - <0.1, 0.1, 0.2> when standing. (Avatar bounding boxes have historically been redefined with major physics upgrades.) An avatar's bounding box changes when an avatar sits, while llGetAgentSize is constant for as long as the shape does not change.

## Examples

```lsl
//A simple script that makes a box hover above the owner's head.
default
{
    state_entry()
    {
        key    owner = llGetOwner();
        vector pos   = llList2Vector(llGetObjectDetails(owner, [OBJECT_POS]), 0);
        vector agent = llGetAgentSize(owner);

    //  "pos" needs to be adjusted so it appears above the owner.
        pos.z += 0.5 + agent.z / 2;

    //  makes sure it found the owner, a zero vector evaluates as false
        if(agent)
            llSetPos(pos);
    }

    touch_start(integer num)
    {
        llResetScript();
    }
}
```

## Notes

- This function is a good way to quickly test...

  - if an avatar is in the same region.
  - if a UUID known to be in the region is an avatar.

To use this function to test either case use as follows

```lsl
if(llGetAgentSize(uuid)) {
    //uuid is an avatar in the region
} else {
    //uuid is not an avatar in the region
}
```

- `DEFAULT_AGENT_HEIGHT` in [indra/llcommon/indra_constants.h](https://github.com/secondlife/viewer/blob/0ca239e469b3/indra/llcommon/indra_constants.h#L96) is 1.9. This will be the z value if an avatar's shape has not loaded yet. It is possible but extremely rare to see a fully loaded avatar with this exact size, so:

```lsl
vector agentSize = llGetAgentSize(uuid);
if (agentSize.z == 1.9) {
    // avatar is probably Ruthed
}
```

## See Also

### Functions

- llGetObjectDetails
- llGetBoundingBox
- llGetAgentInfo
- llRequestAgentData

### Articles

- Avatar body size

<!-- /wiki-source -->
