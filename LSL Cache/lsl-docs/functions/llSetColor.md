---
name: "llSetColor"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the Blinn-Phong color on face of the prim.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llSetColor(vector color, integer face)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetColor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetcolor"]
---

Sets the Blinn-Phong color on face of the prim.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llSetColor(vector color, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `color` | color in RGB <R, G, B> (<0.0, 0.0, 0.0> = black, <1.0, 1.0, 1.0> = white) |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetColor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetColor) — scraped 2026-03-18_

Sets the Blinn-Phong color on face of the prim.

## Caveats

- The function silently fails if its face value indicates a face that does not exist.
- llSetColor will have no visible effect on faces with a PBR material. To work on faces both with and without a PBR material, use this snippet:

```lsl
llSetColor(color, ALL_SIDES);
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_GLTF_BASE_COLOR, ALL_SIDES, "", "", "", "", llsRGB2Linear(color), "", "", "", ""]);
```

## Examples

```lsl
integer face = -1;
vector color = <1.0, 1.0, 1.0>;

default
{
    touch_start(integer num)
    {
        if(~face)       //quick & dirty but efficient way of testing if face is not equal to -1
            llSetColor(color, face); //restore the color
        face = (face + 1) % llGetNumberOfSides(); //increment and keep the face number in range
        color = llGetColor(face); //save the face's color
        llSetColor(<0.5, 0.0, 0.0>, face );  //change the face's color
    }
}
```

## See Also

### Events

- **changed** — CHANGED_COLOR

### Functions

- **llGetAlpha** — Gets the prim's alpha
- **llSetAlpha** — Sets the prim's alpha
- **llGetColor** — Gets the prim's color
- **llSetLinkColor** — Sets link's color
- **llSetLinkAlpha** — Sets link's alpha
- **PRIM_COLOR** — llSetPrimitiveParams
- **PRIM_GLTF_BASE_COLOR** — llSetPrimitiveParams

### Articles

- Color in LSL
- Color and Scripting

<!-- /wiki-source -->
