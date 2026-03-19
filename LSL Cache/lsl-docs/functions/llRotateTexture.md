---
name: "llRotateTexture"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the texture rotation of the chosen face to angle.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llRotateTexture(float angle, integer face)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRotateTexture'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrotatetexture"]
---

Sets the texture rotation of the chosen face to angle.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llRotateTexture(float angle, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `angle` | angle expressed in radians |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRotateTexture)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRotateTexture) — scraped 2026-03-18_

Sets the rotation of a texture on the chosen face to angle.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- The function silently fails if its face value indicates a face that does not exist.

## Examples

```lsl
default
{
    touch_start(integer total_number) {
        // Makes the object's texture rotate a quarter of turn
        llRotateTexture(PI_BY_TWO, ALL_SIDES);
    }
}
```

## Notes

This function only sets the absolute orientation of the texture. See llSetTextureAnim for animations.

## See Also

### Functions

- **llGetTextureRot** — Gets the texture rotation
- **llSetTextureAnim** — Animates the texture

<!-- /wiki-source -->
