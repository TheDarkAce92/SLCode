---
name: "Offset Compression"
category: "example"
type: "example"
language: "LSL"
description: "In scripts that involve object manipulation and/or offsets for animations it is common to end up storing a vector and rotation for every such interaction, which can be memory intensive if the object has a lot of values to store. However, such offsets typically don't need to be very precise as linked objects won't move far from their root prim, and small errors in the rotation shouldn't result in any major issues, so long as those rotations aren't used as a reference for future actions."
wiki_url: "https://wiki.secondlife.com/wiki/Offset_Compression"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Offset Compression

  - 1.1 Functions
  - 1.2 Examples

  - 1.2.1 Functions
  - 1.2.2 Inline

Offset Compression

In scripts that involve object manipulation and/or offsets for animations it is common to end up storing a vector and rotation for every such interaction, which can be memory intensive if the object has a lot of values to store. However, such offsets typically don't need to be very precise as linked objects won't move far from their root prim, and small errors in the rotation shouldn't result in any major issues, so long as those rotations aren't used as a reference for future actions.

With this in mind, I've produced some functions that allow both a positional and rotational offset to be stored as a single vector value, effectively cutting memory requirements by more than half (especially when considering list overhead), though this comes at the cost of declaring the functions instead, so if only require these in a few places you may wish to consider inlining them instead.

## Functions

For simplicity, these functions handle rotations as Euler vectors, which can be converted using llRot2Euler() and llEuler2Rot(), this is also a convenient format for devices where rotation offsets may be specified in the user-friendly format in degrees (to match the build tools), such as in parsed notecards. These should still be converted to rotations for transformations in order to avoid [Gimbal Lock](http://en.wikipedia.org/wiki/Gimbal_Lock). **NOTE:** the combinedOffset() function below expects euler rotations to contain no component that exceeds positive or negative PI (just as the build tools do not allow this); for convenience the clampEulerRot() function is provided below to ensure that an Euler rotation is safe to use, but if your script is not vulnerable to this (for example, if your Euler rotations are created with llRot2Euler) then this function may be omitted.

```lsl
// Ensures that an euler rot is within the required range (no values exceed plus or minus PI)
vector clampEulerRot(vector eulerRot) {
    @loopX1; @loopX2;
    if (eulerRot.x > PI) { eulerRot.x -= TWO_PI; jump loopX1; }
    else if (eulerRot.x < -PI) { eulerRot.x += TWO_PI; jump loopX2; }
    @loopY1; @loopY2;
    if (eulerRot.y > PI) { eulerRot.y -= TWO_PI; jump loopY1; }
    else if (eulerRot.y < -PI) { eulerRot.y += TWO_PI; jump loopY2; }
    @loopZ1; @loopZ2;
    if (eulerRot.z > PI) { eulerRot.z -= TWO_PI; jump loopZ1; }
    else if (eulerRot.z < -PI) { eulerRot.z += TWO_PI; jump loopZ2; }
    return eulerRot;
}

// Creates a combined vector from a position and Euler rotation. The rotation *must* be within the required range (no values exceed plus or minus PI) or it will not be possible to restore the values correctly
vector combinedOffset(vector offsetPos, vector offsetEulerRot) {
    return <
        (float)((integer)(offsetPos.x * 1000.0) * 10) + ((float)(((offsetPos.x < 0) * -2) + 1) * (offsetEulerRot.x + 5.0)),
        (float)((integer)(offsetPos.y * 1000.0) * 10) + ((float)(((offsetPos.y < 0) * -2) + 1) * (offsetEulerRot.y + 5.0)),
        (float)((integer)(offsetPos.z * 1000.0) * 10) + ((float)(((offsetPos.z < 0) * -2) + 1) * (offsetEulerRot.z + 5.0))
    >;
}

// Retrieve the positional part from the combined offset
vector offsetToPos(vector offset) {
    return <
        (float)((integer)(offset.x / 10.0)) / 1000.0,
        (float)((integer)(offset.y / 10.0)) / 1000.0,
        (float)((integer)(offset.z / 10.0)) / 1000.0
    >;
}

// Retrieve the rotation part from the combined offset
vector offsetToEulerRot(vector offset) {
    return <
        (offset.x - ((integer)(offset.x / 10.0) * 10)) * (float)(((offset.x < 0) * -2) + 1) - 5.0,
        (offset.y - ((integer)(offset.y / 10.0) * 10)) * (float)(((offset.y < 0) * -2) + 1) - 5.0,
        (offset.z - ((integer)(offset.z / 10.0) * 10)) * (float)(((offset.z < 0) * -2) + 1) - 5.0
    >;
}
```

## Examples

### Functions

The silly example below can be placed inside the root prim of a linked-set that you don't care much about (as it may be ruined). It will store the offsets of all prims and allow you to "crush" the object and then restore it by touching.

```lsl
// Paste the above functions in here

list prim_offsets = []; integer crushed = FALSE;
default {
    state_entry() {
        integer prims = llGetNumberOfPrims();
        if (prims < 2) { llOwnerSay("This object is not a linked set"); return; }

        integer link;
        for (link = LINK_ROOT + 1; link <= prims; ++link) {
            list params = llGetLinkPrimitiveParams(link, [PRIM_POS_LOCAL, PRIM_ROT_LOCAL]);
            prim_offsets += [combinedOffset(llList2Vector(params, 0), llRot2Euler(llList2Rot(params, 1)))];
        }
        llSetText("Touch to crush!", <1.0, 1.0, 1.0>, 1.0);
    }

    changed(integer changes) { if (changes & CHANGED_LINK) llOwnerSay("Object has changed, script should be reset"); }

    touch_start(integer x) {
        // If the object was crushed, restore it
        if (crushed) {
            integer x = prim_offsets != [];
            while ((--x) >= 0) {
                vector offset = llList2Vector(prim_offsets, x);
                llSetLinkPrimitiveParamsFast(x + 2,
                    [PRIM_POS_LOCAL, offsetToPos(offset), PRIM_ROT_LOCAL, llEuler2Rot(offsetToEulerRot(offset))]
                );
            }
            llSetText("Touch to crush!", <1.0, 1.0, 1.0>, 1.0);
            crushed = FALSE;
        } else {
            integer x = prim_offsets != [];
            while ((--x) >= 0) llSetLinkPrimitiveParamsFast(x + 2, [PRIM_POS_LOCAL, ZERO_VECTOR, PRIM_ROT_LOCAL, ZERO_ROTATION]);
            llSetText("Ouch!", <1.0, 0.0, 0.0>, 1.0);
            crushed = TRUE;
        }
    }
}
```

### Inline

This second example is an identical script, but instead of using the functions as-is it shows how they can be inlined. You may wish to do this in a script that only uses offset conversion in a few places, e.g- on load and on use, as this will eliminate the memory and performance costs of declaring and executing functions.

```lsl
list prim_offsets = []; integer crushed = FALSE;
default {
    state_entry() {
        integer prims = llGetNumberOfPrims();
        if (prims < 2) { llOwnerSay("This object is not a linked set"); return; }

        integer link;
        for (link = LINK_ROOT + 1; link <= prims; ++link) {
            list params = llGetLinkPrimitiveParams(link, [PRIM_POS_LOCAL, PRIM_ROT_LOCAL]);
            vector offsetPos = llList2Vector(params, 0);
            vector offsetEulerRot = llList2Vector(params, 1);
            prim_offsets += [< // Inline conversion to offset
                (float)((integer)(offsetPos.x * 1000.0) * 10) + ((float)(((offsetPos.x < 0) * -2) + 1) * (offsetEulerRot.x + 5.0)),
                (float)((integer)(offsetPos.y * 1000.0) * 10) + ((float)(((offsetPos.y < 0) * -2) + 1) * (offsetEulerRot.y + 5.0)),
                (float)((integer)(offsetPos.z * 1000.0) * 10) + ((float)(((offsetPos.z < 0) * -2) + 1) * (offsetEulerRot.z + 5.0))
            >];
        }
        llSetText("Touch to crush!", <1.0, 1.0, 1.0>, 1.0);
    }

    changed(integer changes) { if (changes & CHANGED_LINK) llOwnerSay("Object has changed, script should be reset"); }

    touch_start(integer x) {
        // If the object was crushed, restore it
        if (crushed) {
            integer x = prim_offsets != [];
            while ((--x) >= 0) {
                vector offset = llList2Vector(prim_offsets, x);
                llSetLinkPrimitiveParamsFast(x + 2,
                    [
                        PRIM_POS_LOCAL, < // Inline conversion from offset
                            (float)((integer)(offset.x / 10.0)) / 1000.0,
                            (float)((integer)(offset.y / 10.0)) / 1000.0,
                            (float)((integer)(offset.z / 10.0)) / 1000.0
                        >,
                        PRIM_ROT_LOCAL, llEuler2Rot(< // Inline conversion from offset
                            (offset.x - ((integer)(offset.x / 10.0) * 10)) * (float)(((offset.x < 0) * -2) + 1) - 5.0,
                            (offset.y - ((integer)(offset.y / 10.0) * 10)) * (float)(((offset.y < 0) * -2) + 1) - 5.0,
                            (offset.z - ((integer)(offset.z / 10.0) * 10)) * (float)(((offset.z < 0) * -2) + 1) - 5.0
                        >)]
                );
            }
            llSetText("Touch to crush!", <1.0, 1.0, 1.0>, 1.0);
            crushed = FALSE;
        } else {
            integer x = prim_offsets != [];
            while ((--x) >= 0) llSetLinkPrimitiveParamsFast(x + 2, [PRIM_POS_LOCAL, ZERO_VECTOR, PRIM_ROT_LOCAL, ZERO_ROTATION]);
            llSetText("Ouch!", <1.0, 0.0, 0.0>, 1.0);
            crushed = TRUE;
        }
    }
}
```