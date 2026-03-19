---
name: "llSetPrimitiveParams"
category: "function"
type: "function"
language: "LSL"
description: "Sets multiple prim parameters in a single call using PRIM_* constant flag-value pairs"
wiki_url: "https://wiki.secondlife.com/wiki/llSetPrimitiveParams"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llSetPrimitiveParams(list rules)"
parameters:
  - name: "rules"
    type: "list"
    description: "Alternating PRIM_* constant and value pairs"
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.2"
patterns: ["llsetprimitiveparams"]
deprecated: "false"
---

# llSetPrimitiveParams

```lsl
void llSetPrimitiveParams(list rules)
void llSetLinkPrimitiveParams(integer link, list rules)
void llSetLinkPrimitiveParamsFast(integer link, list rules)
```

Sets multiple prim parameters in one call. Prefer `llSetLinkPrimitiveParamsFast` — it has no forced delay.

## Variants

| Function | Delay | Link Parameter |
|----------|-------|----------------|
| `llSetPrimitiveParams` | 0.2s | No (sets current prim) |
| `llSetLinkPrimitiveParams` | 0.2s | Yes |
| `llSetLinkPrimitiveParamsFast` | 0.0s | Yes (preferred) |

## PRIM_* Parameter Reference

### Position & Rotation

```lsl
PRIM_POSITION, vector pos           // global coords (root) or local (child)
PRIM_POS_LOCAL, vector pos          // local to root prim
PRIM_ROTATION, rotation rot         // global (buggy on child prims — use PRIM_ROT_LOCAL)
PRIM_ROT_LOCAL, rotation rot        // local to root
PRIM_SIZE, vector size
PRIM_OMEGA, vector axis, float spinrate, float gain
```

### Physics

```lsl
PRIM_PHYSICS, integer boolean
PRIM_PHANTOM, integer boolean
PRIM_TEMP_ON_REZ, integer boolean
PRIM_MATERIAL, integer flag          // PRIM_MATERIAL_STONE, METAL, GLASS, WOOD, FLESH, PLASTIC, RUBBER
PRIM_PHYSICS_SHAPE_TYPE, integer     // PRIM_PHYSICS_SHAPE_PRIM, CONVEX, NONE
```

### Appearance

```lsl
PRIM_NAME, string name
PRIM_DESC, string description        // max 127 bytes; no pipe char '|'
PRIM_TEXT, string text, vector color, float alpha
PRIM_COLOR, integer face, vector color, float alpha
PRIM_TEXTURE, integer face, string texture, vector repeats, vector offsets, float rotation
PRIM_BUMP_SHINY, integer face, integer shiny, integer bump
PRIM_FULLBRIGHT, integer face, integer boolean
PRIM_GLOW, integer face, float intensity
PRIM_ALPHA_MODE, integer face, integer alpha_mode, integer mask_cutoff
```

### Lighting

```lsl
PRIM_POINT_LIGHT, integer boolean, vector color, float intensity, float radius, float falloff
PRIM_NORMAL, integer face, string texture, vector repeats, vector offsets, float rotation
PRIM_SPECULAR, integer face, string texture, vector repeats, vector offsets, float rotation, vector color, integer glossiness, integer environment
```

### GLTF/PBR

```lsl
PRIM_RENDER_MATERIAL, integer face, string material_uuid
PRIM_GLTF_BASE_COLOR, integer face, string texture, vector repeats, vector offsets, float rotation, vector color, float alpha, integer alpha_mode, float alpha_mask_cutoff, integer double_sided
PRIM_GLTF_NORMAL, integer face, string texture, vector repeats, vector offsets, float rotation
PRIM_GLTF_METALLIC_ROUGHNESS, integer face, string texture, vector repeats, vector offsets, float rotation, float metallic_factor, float roughness_factor
PRIM_GLTF_EMISSIVE, integer face, string texture, vector repeats, vector offsets, float rotation, vector emissive_tint
```

### Shape

```lsl
PRIM_TYPE, integer flag, ...         // type-specific params (see below)
PRIM_SLICE, vector slice
PRIM_FLEXIBLE, integer boolean, integer softness, float gravity, float friction, float wind, float tension, vector force
PRIM_SIT_TARGET, integer boolean, vector offset, rotation rot
PRIM_CLICK_ACTION, integer action
```

### Multi-Prim Targeting

```lsl
PRIM_LINK_TARGET, integer link       // switch target prim mid-list (no delay between prims)
```

## PRIM_TYPE Box/Cylinder/Prism

```lsl
[PRIM_TYPE, PRIM_TYPE_BOX,
 integer hole_shape,
 vector cut,      // <begin, end, 0>
 float hollow,    // 0.0–0.95
 vector twist,    // <begin, end, 0>
 vector top_size, // <x, y, 0>
 vector top_shear // <x, y, 0>
]
```

## PRIM_TYPE Sphere

```lsl
[PRIM_TYPE, PRIM_TYPE_SPHERE,
 integer hole_shape,
 vector cut,
 float hollow,
 vector twist,
 vector dimple   // <begin, end, 0>
]
```

## Critical Caveats

- `llSetLinkPrimitiveParamsFast` is asynchronous — rapid sequential calls may execute out of order.
- `PRIM_ROTATION` on child prims is buggy — use `PRIM_ROT_LOCAL` instead.
- `PRIM_POSITION` for unattached root prims is capped to 10m per call.
- `PRIM_TYPE` has no effect on mesh prims.
- Prim description: max 127 bytes; pipe character `|` not allowed.

## Examples

```lsl
// Set colour on all sides, switch to child prim 2, set colour there
llSetLinkPrimitiveParamsFast(LINK_ROOT, [
    PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, 1.0,
    PRIM_LINK_TARGET, 2,
    PRIM_COLOR, ALL_SIDES, <0.0, 1.0, 0.0>, 1.0
]);

// Enable point light
llSetLinkPrimitiveParamsFast(LINK_THIS, [
    PRIM_POINT_LIGHT, TRUE,
    <1.0, 0.9, 0.7>,  // warm white
    1.0,               // intensity
    10.0,              // radius (metres)
    0.5                // falloff
]);

// Set hover text via params
llSetLinkPrimitiveParamsFast(LINK_THIS, [
    PRIM_TEXT, "Status: OK", <0.0, 1.0, 0.0>, 1.0
]);
```

## See Also

- `llGetPrimitiveParams` — read prim parameters
- `llGetLinkPrimitiveParams` — read linked prim parameters
- `PRIM_TYPE`, `PRIM_COLOR`, `PRIM_TEXTURE` etc. — constant pages


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetPrimitiveParams) — scraped 2026-03-18_

Sets the prim's parameters according to rules.

## Caveats

- The prim description is limited to 127 bytes; any string longer then that will be truncated. This truncation does not always happen when the attribute is set or read.
- The prim description may only contain printable ASCII characters (code points 32-126), except the pipe character '|', which is not permitted for historical reasons. All other characters will be replaced with one '?' character per illegal UTF-8 byte.
- Note that when people have "Hover Tips on All Objects" selected in the viewer's "View" menu, they'll see the object description pop-up for any object under their mouse pointer.  For that reason, it is good practice to only set human-friendly information in the description, e.g. keys and such.
- When an attached object is detached, changes made by script to the name and description (of the root prim) of the attachment will be lost. While the object is attached the name and description can be changed but it will not be reflected in inventory. This caveat does *not* apply to child prims.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- repeats is not only used to set the number of repeats but the sign of the individual components is also used to set the "Flip" attribute.
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If render_material is missing from the prim's inventory  and it is not a UUID or it is not a material then an error is shouted on DEBUG_CHANNEL.
- If render_material is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If render_material is provided as NULL_KEY, the glTF Material is removed from face, reverting back to any underlying Blinn-Phong materials.
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- Do not rely on Floating Text as a storage medium; it is neither secure nor finalized.

  - Floating text has been altered in past server updates, breaking existing content; future changes may occur.
  - Even "invisible" floating text is transmitted to the client.

  - It can be viewed by anyone with a client that is capable of rendering text that is supposed to be invisible.
  - The network packets that contain the text can be sniffed and the text read.
- PRIM_TYPE can only be used with LINK_SET if the object contains 10 or fewer prims. It can only be used with LINK_ALL_OTHERS or LINK_ALL_CHILDREN if the object contains 11 or fewer prims. If there are more prims, the operation will fail and an error will be shouted to DEBUG_CHANNEL. Work around this by looping through the prims with llSetLinkPrimitiveParamsFast.
- PRIM_TYPE will silently fail when executed by a script placed inside a mesh, whether the affect object is the mesh or not (in linksets for example), use a normal prim as your root prim.
- top_size and client values are different, the ranges do not line up, conversion is required. This simple equation can be used: answer = 1.0 - value. See top_size Explained for more information.
- PRIM_POSITION caveats

  - Depending upon the situation position may need to be in local coordinates or region coordinates, See llSetPos#Specification for details.

  - It is usually not a good idea to combine PRIM_POSITION with LINK_SET. The root will treat the coordinates as world or attachment, while the children will treat them as local, yielding inconsistent results or failure. If you want to move the object as a unit, use LINK_ROOT instead.
  - The range the prim can move is limited if it is an unattached root prim. The distance is capped to 10m per PRIM_POSITION call. See WarpPos. This is a very special case. Do not rely on rule duplication of other flags - the results are undefined, and things *will* break in the future.
  - Moving avatars with PRIM_POSITION

  - Moving the prim the avatar sat upon does not move the avatar.
  - Moving an avatar does not move the prim they sat upon.
  - Sit-target coordinates do not easily map to prim coordinates, use UpdateSitTarget.
  - If you have explicitally set your object as "static obstacle" for pathfinding , the function will fail with the error in the debug channel : "Unable to set prim position or scale: object contributes to the navmesh."
  - If position is greater than 54 meters away from the center, the repositioning will silently fail.
- PRIM_OMEGA on nonphysical objects, and child prims of physical objects, is only a client side effect; the object or prim will collide as non-moving geometry.
- PRIM_OMEGA cannot be used on avatars sitting on the object. It will emit the error message "PRIM_OMEGA disallowed on agent".
- If PRIM_OMEGA does not appear to be working, make sure that that Develop > Network > Velocity Interpolate Objects is enabled on the viewer.
- In the parameters returned by `llGetPrimitiveParams([PRIM_OMEGA])`, the vector is normalized, and the spinrate is multiplied by the magnitude of the original vector.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- repeats is not only used to set the number of repeats but the sign of the individual components is also used to set the "Flip" attribute.
- offsets and rotation_in_radians are limited to positive values only, unlike PRIM_TEXTURE and GLTF Overrides. To convert a negative offset to positive, add 1, and to convert a negative rotation to positive, add TWO_PI.
- To clear the normal map parameters from the face (and possibly remove the material), set  texture to NULL_KEY (the other parameters must be supplied in this case but will be ignored).
- Note that whenever any face in a linkset contains a material (i.e. has a non-default PRIM_NORMAL, PRIM_SPECULAR, or PRIM_ALPHA_MODE), the linkset will use the [new accounting system](http://community.secondlife.com/t5/English-Knowledge-Base/Calculating-land-impact/ta-p/974163).
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- repeats is not only used to set the number of repeats but the sign of the individual components is also used to set the "Flip" attribute.
- offsets and rotation_in_radians are limited to positive values only, unlike PRIM_TEXTURE and GLTF Overrides. To convert a negative offset to positive, add 1, and to convert a negative rotation to positive, add TWO_PI.
- To clear the specular map parameters from the face (and possibly remove the material), set  texture to NULL_KEY (the other parameters must be supplied in this case but will be ignored).
- Note that whenever any face in a linkset contains a material (i.e. has a non-default PRIM_NORMAL, PRIM_SPECULAR, or PRIM_ALPHA_MODE), the linkset will use the [new accounting system](http://community.secondlife.com/t5/English-Knowledge-Base/Calculating-land-impact/ta-p/974163).
- In the default texture mapping mode the texture repeats units are in texture repeats per face. In the planar texture mapping mode the texture repeats units are in texture repeats per half meter. This is in contrast to the in-world editing tool, in which the planar texture scaling units are repeats per meter.
- If face is ALL_SIDES then the flag works on all sides.
- The flag silently fails if its face value indicates a face that does not exist.
- PRIM_SIZE has similar constraints to llSetScale and fails silently on physical prims/links. One workaround is to set items to non-physical before changing their size, then changing them back to physical; this can be accomplished in a single llSetLinkPrimitiveParamsFast command using PRIM_LINK_TARGET.
- PRIM_PHANTOM, PRIM_PHYSICS and PRIM_TEMP_ON_REZ applies to the entire object (linkset).
- Values may drift, become truncated or be range-limited. Some limits are applied by the client during deserialization and before rendering, others are applied by the simulator before storing the values.

  - When testing vectors and rotations use llVecDist and llAngleBetween (respectively) to perform fuzzy tests.
- PRIM_LINK_TARGET is a special parameter which can be inserted to perform actions on multiple prims on the linkset with one call.
- Scripts written before September 2004 that use PRIM_TYPE depend on PRIM_TYPE to have the value 1; if these scripts are recompiled, the new value of PRIM_TYPE will be used, causing errors at runtime.

  - To fix this, replace the PRIM_TYPE flag with the value 1 or update to the newer PRIM_TYPE syntax.
- PRIM_ROTATION is bugged in child prims. See Useful Snippets for a workaround, or the linked SVC-93 issue below.
- This function will return an error if given data of the wrong type. This is problematic when providing data from user input or notecard. To remedy this, see List Cast function.
- Applying an operation to LINK_SET will apply it first to the root prim, then to each child prim.
- The sim will clamp attributes before storing them.
- The client will clamp attributes before rendering.
- **Some prim properties are reset** by this function

  - A flexible prim will become not flexible
  - A sliced prim will become unsliced

In order to preserve properties they must be saved and explicitly set in the function call

|  | Important: When wanting to change the alpha value of a face, please consider using llSetLinkAlpha(integer link, float alpha, integer face); instead of llSetLinkPrimitiveParamsFast(integer link, [ PRIM_COLOR, integer face, vector color, float alpha ]);, that way you don't have to mess with the color settings. Also don't expect llSetLinkPrimitiveParamsFast being faster than llSetText when setting a float text property within a loop like at "% loading" status bars. Measurements showed llSetText being 3-4 times faster. That also might applies for similar functions. |
| --- | --- |

- Attempting to change PRIM_TYPE of a mesh object has no effect.

  - Keeping the PRIM_TYPE as PRIM_TYPE_SCULPT and trying to set a different sculpt map or sculpt flags on a mesh also does nothing. Additionally, a script residing inside a mesh type prim cannot change the sculpt parameters of *any* prim in the linkset.
- The caveats described at |llSetClickAction all apply to PRIM_CLICK_ACTION.

## Examples

A simple script to light up a prim in a linkset when touched, and unlight the others using llSetLinkPrimitiveParams, when script is installed in the root prim of the linkset.

```lsl
// Turn all prims off and the one touched turn on

default
{
    touch_start(integer num_detected)
    {
        llSetLinkPrimitiveParamsFast(LINK_SET, [
                PRIM_FULLBRIGHT, ALL_SIDES, FALSE,
            PRIM_LINK_TARGET, llDetectedLinkNumber(0),
                PRIM_FULLBRIGHT, ALL_SIDES, TRUE]);
    }
}
```

A simple script which moves all child prims .25m forward on the root's Z axis, when touched.

```lsl
default
{
    touch_start(integer total_number)
    {
        integer numberOfPrims = llGetNumberOfPrims();

        if (numberOfPrims < 2) return;

        vector  link_pos;
        list    params;

        integer link = 2;// start with first child prim
        do
        {
//          get a child prim's local position (i.e, relative to the root prim)
            link_pos = llList2Vector(llGetLinkPrimitiveParams(link, [PRIM_POS_LOCAL]), 0);

            link_pos.z += 0.25;// relative to root's local z-axis !!!

            params += [PRIM_LINK_TARGET, link,
                            PRIM_POS_LOCAL, link_pos];
        }
        while (++link <= numberOfPrims);

        if (!llGetListLength(params)) return;

//      the params list starts with a PRIM_LINK_TARGET (a hack so we can start
//      with the first child prim), so it doesn't really matter which number you
//      put as first parameter in this function call
        llSetLinkPrimitiveParamsFast(2, params);
    }
}
```

|  | Important: You can use one function call instead of two when making use of PRIM_LINK_TARGET. |
| --- | --- |

| Preferred method using PRIM_LINK_TARGET | Second method does the same effect-wise. |
| --- | --- |
| ```lsl // color the root prim red and the first linked-prim green default { touch_start(integer num_detected) { llSetLinkPrimitiveParamsFast(LINK_ROOT, [ PRIM_COLOR, ALL_SIDES, , 1.0, PRIM_LINK_TARGET, 2, PRIM_COLOR, ALL_SIDES, , 1.0]); } } ``` | ```lsl // color the root prim red and the first linked-prim green default { touch_start(integer num_detected) { llSetLinkPrimitiveParamsFast(LINK_ROOT, [ PRIM_COLOR, ALL_SIDES, , 1.0]); llSetLinkPrimitiveParamsFast(2, [ PRIM_COLOR, ALL_SIDES, , 1.0]); } } ``` |

| Combining function calls |
| --- |
| ```lsl // Combined function calls default { touch_start(integer num_detected) { // color prim faces, set texture and set fullbright llSetPrimitiveParams([ PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 1.0, PRIM_COLOR, 3, , 1.0, PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", , ZERO_VECTOR, 0.0, PRIM_FULLBRIGHT, 3, TRUE]); } } ``` |
| ```lsl // Single function calls default { touch_start(integer num_detected) { // color prim faces llSetPrimitiveParams([ PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 1, PRIM_COLOR, 3, , 1.0]); // set texture llSetPrimitiveParams([ PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", , ZERO_VECTOR, 0.0]); // set fullbright llSetPrimitiveParams([ PRIM_FULLBRIGHT, 3, TRUE]); } } ``` |

```lsl
// And if you want to place it above your bed, to make you sleep well, and the coords
// of that place are, for example,
llSetPrimitiveParams([
    PRIM_COLOR, ALL_SIDES, ZERO_VECTOR, 1.0,
    PRIM_COLOR, 3, <1.0,1.0,1.0>, 1.0,
    PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR,0.0,
    PRIM_FULLBRIGHT, 3, TRUE,
    PRIM_POSITION, ]);

// You can set the texture of several sides at once, with no time penalty,
// just by repeating the param for that:
llSetPrimitiveParams([
    PRIM_TEXTURE, 3, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR, 0.0,
    PRIM_TEXTURE, 4, "4d304955-2b01-c6c6-f545-c1ae1e618288", <1.0, 1.0, 0.0>, ZERO_VECTOR, 0.0]);
```

### Top-size (taper)

```lsl
default
{
    state_entry()
    {
        vector scale = llGetScale();
        float  X     = scale.x;
        float  Y     = scale.y;

        llSetPrimitiveParams([
            PRIM_SIZE, , // keep the prim thin
            PRIM_TYPE, PRIM_TYPE_BOX, 0, <0.0,1.0,0.0>, 0.0, ZERO_VECTOR,
                <1.0 - (0.4 / X), 1.0 - (0.4 / Y), 0.0>, ZERO_VECTOR]);
        // We used the equation "answer = 1 - desired_taper"

        // The proportions of the top-size (taper) will be maintained (as close as possible)
        // whenever the prim is resized. The proportion above will produce a reasonably
        // pleasing picture frame kinda thing.
    }

    changed(integer change)
    {
        if(change & CHANGED_SCALE)
        {
            llResetScript();
        }
    }
}
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.
The old PRIM_TYPE interface (labeled PRIM_TYPE_LEGACY), while technically retired, can still be used.

### PRIM_POSITION

Avatars sitting on the object can be moved with llSetLinkPrimitiveParams and PRIM_POSITION. This was originally a mis-feature but according to [Andrew Linden](http://jira.secondlife.com/browse/SVC-3408?focusedCommentId=88574#action_88574) LL has decided to support it.

Examples

The below example moves an avatar to x,y,z without moving the prim they are sitting on. If x,y,z is more than 54 meters away the call will silently fail. Remember x,y,z is in object relative coordinates just like any other linked prim in a set.

Avatars are always the last prims in the set, so llGetNumberOfPrims can be used for a single avatar sitting on a vehicle.

Example:

```lsl
llSetLinkPrimitiveParams(llGetNumberOfPrims(), [PRIM_POSITION, ]);
```

## See Also

### Functions

- **llGetLinkNumber** — prim
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- **llGetPrimitiveParams** — Get many primitive parameters
- **llSetLinkPrimitiveParams** — Set parameters on other prims in linkset
- **llGetLinkPrimitiveParams** — Get many primitive parameters of other prims in likset
- **llSetLinkPrimitiveParamsFast** — Set parameters on other prims in linkset without sleep
- **llSetAlpha** — Simpler way to set alpha (transparency) without (re-)setting color.
- **llSetTexture** — Simpler way to set texture
- **llSetColor** — Simpler way to set color
- **llSetScale** — Simpler way to set scale
- **llSetStatus** — Simpler way to set physics and phantom

### Articles

- **Limits** — SL limits and constrictions
- **Limits** — SL limits and constrictions
- Color in LSL
- Translucent Color
- Color in LSL
- Color in LSL
- Translucent Color
- Internal Textures

<!-- /wiki-source -->
