---
name: "llGetBoundingBox"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list that is the bounding box of object relative to its root prim, in local coordinates.
Format: [ (vector) min_corner, (vector) max_corner ]

The bounding box is for the entire link set, not just the requested prim.
Returns an empty list ([]) if object is not found.'
signature: "list llGetBoundingBox(key object)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetBoundingBox'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetboundingbox"]
---

Returns a list that is the bounding box of object relative to its root prim, in local coordinates.
Format: [ (vector) min_corner, (vector) max_corner ]

The bounding box is for the entire link set, not just the requested prim.
Returns an empty list ([]) if object is not found.


## Signature

```lsl
list llGetBoundingBox(key object);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `object` | avatar or prim UUID that is in the same region |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetBoundingBox)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetBoundingBox) — scraped 2026-03-18_

Returns a list that is the bounding box of object relative to its root prim, in local coordinates.Format: [ (vector) min_corner, (vector) max_corner ]

## Caveats

- Regardless if object is a non-root prim, the bounding box of the object is returned.  This also applies if object is an agent sitting on an object - the bounding box of the sat-upon object (including the agent's shape) is returned.
- The bounding box is determined by the physics models, not the visual representation.

  - A child prim with its physics mode set to none will not affect the bounding box.
  - Phantom and volume detect objects do have physics interactions, which is why they still have bounding boxes.
  - Attachments have no bounding boxes of their own as they have no physics interaction, instead the bounding box of the avatar is returned.

## Examples

```lsl
default//An avatar bounding box ruler thingy
{
    state_entry()
    {
        llSetStatus(STATUS_PHANTOM, TRUE);
    }

    touch_start(integer total_number)
    {
        key target = llDetectedKey(0);
        list box = llGetBoundingBox(target);
        vector center = llDetectedPos(0) + (llList2Vector(box, 0) + llList2Vector(box, 1)) * 0.5;
        vector size = llList2Vector(box, 1) - llList2Vector(box, 0);
        llSetPrimitiveParams([PRIM_POSITION, center, PRIM_SIZE, size]);
        llSetText("Name: " + llDetectedName(0) + ", UUID: " + (string)target +
                "\nBounding Box Size: " + (string)size, <1.0, 1.0, 1.0>, 1.0);
    }
}
```

```lsl
// Enclose a named object in the tightest possible box
// that is aligned with the object's root prim axes.
// Drop this script in a box near the object to enclose
// (must be in a 10m range)

string ObjectNameToEnclose = "SearchMe";
key UUID;

default
{
    state_entry()
    {
        llSensor(ObjectNameToEnclose, "", ACTIVE | PASSIVE, 10, PI);
    }

    sensor(integer n)
    {
        UUID = llDetectedKey(0);
        llSetTimerEvent(1);
    }

    timer()
    {
        list info = llGetObjectDetails(UUID, [OBJECT_POS, OBJECT_ROT]) + llGetBoundingBox(UUID);
        vector pos = llList2Vector(info, 0);
        rotation rot = llList2Rot(info, 1);
        vector corner1 = llList2Vector(info, 2) * rot + pos;
        vector corner2 = llList2Vector(info, 3) * rot + pos;
        vector size = llList2Vector(info, 3) - llList2Vector(info, 2);

        llSetPos((corner1 + corner2) * 0.5); // Set position to the midpoint (average) of the corners
        llSetRot(rot);
        llSetScale(size);
    }
}
```

## See Also

### Functions

- llGetAgentSize

<!-- /wiki-source -->
