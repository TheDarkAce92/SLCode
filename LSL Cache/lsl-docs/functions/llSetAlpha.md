---
name: "llSetAlpha"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the Blinn-Phong alpha on face

If face is ALL_SIDES then the function works on all sides.'
signature: "void llSetAlpha(float alpha, integer face)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetAlpha'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetalpha"]
---

Sets the Blinn-Phong alpha on face

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llSetAlpha(float alpha, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `alpha` | from 0.0 (clear) to 1.0 (solid) (0.0 <= alpha <= 1.0) |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetAlpha)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetAlpha) — scraped 2026-03-18_

Sets the Blinn-Phong alpha on face

## Caveats

- The function silently fails if its face value indicates a face that does not exist.
- llSetAlpha will have no visible effect on faces with a PBR material. To work on faces both with and without a PBR material, use one of these snippets:

  - invisible

```lsl
llSetAlpha(0.0, ALL_SIDES);
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_GLTF_BASE_COLOR, ALL_SIDES, "", "", "", "", "", 0.0, PRIM_GLTF_ALPHA_MODE_MASK, 1.0, ""]);
```
  - visible

```lsl
llSetAlpha(1.0, ALL_SIDES);
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_GLTF_BASE_COLOR, ALL_SIDES, "", "", "", "", "", "", "", "", ""]);
```

## Examples

```lsl
float cloakSpeed = 0.1;

default
{
    touch_end(integer total_number)
    {
        float alpha = 1.0;
        while(alpha > 0.0)
        {
            alpha -= 0.1;
            llSetAlpha(alpha, ALL_SIDES);
            llSleep(cloakSpeed);
        }
        state cloaked;
    }
}

state cloaked
{
    touch_end(integer total_number)
    {
        float alpha;
        while (alpha < 1.0)
        {
            alpha += 0.1;
            llSetAlpha(alpha, ALL_SIDES);
            llSleep(cloakSpeed);
        }
        state default;
    }
}
```

## Notes

In practical terms, "alpha" means "transparency" or "visibility".

To be clear, llSetAlpha will only affect the prim that the script it is in. It will not affect any linked prims. To set the alpha state for those, use llSetLinkAlpha

## See Also

### Events

- **changed** — CHANGED_COLOR

### Functions

- **llGetAlpha** — Gets the prim's alpha
- **llGetColor** — Gets the prim's color
- **llSetColor** — Sets the prim's color
- **llSetLinkColor** — Sets link's color
- **llSetLinkAlpha** — Sets link's alpha
- **PRIM_COLOR** — llSetPrimitiveParams
- **PRIM_GLTF_BASE_COLOR** — llSetPrimitiveParams

### Articles

- Translucent Color

<!-- /wiki-source -->
