---
name: "llGetPos"
category: "function"
type: "function"
language: "LSL"
description: "Returns the prim's position in region coordinates"
wiki_url: "https://wiki.secondlife.com/wiki/llGetPos"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "vector llGetPos()"
parameters: []
return_type: "vector"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llgetpos"]
deprecated: "false"
---

# llGetPos

```lsl
vector llGetPos()
```

Returns the prim's position in region coordinates.

## Return Value

`vector` — position in region coordinates.

## Caveats

- **Attachments:** When called from the root of an attachment, returns the wearer's region position.
- **Child prims in attachments:** Returns a position relative to the avatar root position and rotation, plus the offset from the root prim.
- **Accuracy:** Position is only accurate if the root is attached to `ATTACH_AVATAR_CENTER` at `ZERO_ROTATION` and `ZERO_VECTOR`.
- **Avatar animations:** Avatar animations are invisible to the simulator and do not affect reported position.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        vector pos = llGetPos();
        llSay(0, "Position: " + (string)pos);
    }
}
```

```lsl
default
{
    on_rez(integer param)
    {
        if (llGetPos().z > 500.0)
            llOwnerSay("I'm up high!");
    }
}
```

## See Also

- `llGetLocalPos` — position relative to parent prim or avatar
- `llSetPos` — move prim to position
- `llSetRegionPos` — set position with no distance cap


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetPos) — scraped 2026-03-18_

Returns the vector position of the task in region coordinates

## Caveats

- When called from the root of an attachment, returns the wearer's region position. To see the position used, enable **Develop>Avatar>Display Agent Target** and use the red crosshair. If the avatar is sitting on an object, the red crosshair may be hidden by the white one, in the same position.

- When called in an attachment's child prim, the position given is again relative to the *avatar's* root position and rotation, but with the offset from the root prim added. Visually, the reported position will only be correct if the object's root is attached to ATTACH_AVATAR_CENTER, at ZERO_ROTATION and ZERO_VECTOR. Moving the attachment's root or changing the attachment point will not affect the reported position. Avatar animation is invisible to the simulator, so it also does not affect the reported position.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        // When touched, check the position of
        // the object, save it to "position",
        // then convert it into a string and
        // say it.
        vector position = llGetPos();
        llSay(0, (string)position);
    }
}
```

```lsl
default
{
    on_rez(integer param)
    {
        // Adding .x .y or .z after the vector name can be used to get the float value of just that axis.
        vector pos = llGetPos();
        float Z = pos.z; // <--- Like this.
        if(Z > 500.0)
        llOwnerSay("Oooh! I'm up high!");
    }
}
```

## See Also

### Functions

- **llGetLocalPos** — local
- **llGetPrimitiveParams** — Gets prim properties
- **llGetRootPosition** — Gets the root prims position
- **llSetPos** — Sets the prim position
- **llSetPrimitiveParams** — Sets prim properties
- **llSetLinkPrimitiveParams** — Sets linked prim properties

<!-- /wiki-source -->
