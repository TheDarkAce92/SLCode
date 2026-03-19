---
name: "llOffsetTexture"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the texture u & v offsets for the chosen face.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llOffsetTexture(float u, float v, integer face)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llOffsetTexture'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lloffsettexture"]
---

Sets the texture u & v offsets for the chosen face.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llOffsetTexture(float u, float v, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `u` | horizontal (x) offset in the interval [-1.0, 1.0] |
| `float` | `v` | vertical (y) offset in the interval [-1.0, 1.0] |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llOffsetTexture)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llOffsetTexture) — scraped 2026-03-18_

Sets the texture u & v offsets for the chosen face.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- The function silently fails if its face value indicates a face that does not exist.

## Examples

```lsl
//Offsets the textures on 6 sides
float offset;
default
{
    state_entry()
    {
        integer i;

        for( i = 1; i < 7; i++ )
        {
            offset = offset + .1;
            llOffsetTexture( (float)offset, (float)offset, i);
        }
    }
}
```

## Notes

If you use `vector offsetVec = llGetTextureOffset()` to get the vector of the current offset, then `u = offsetVec.x` and `v = offsetVec.y`

## See Also

### Functions

- **llGetTextureOffset** — Returns a vector in the form

<!-- /wiki-source -->
