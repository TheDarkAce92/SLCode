---
name: "llScaleTexture"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the texture u & v scales for the chosen face.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llScaleTexture(float u, float v, integer face)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llScaleTexture'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llscaletexture"]
---

Sets the texture u & v scales for the chosen face.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llScaleTexture(float u, float v, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `u` | horizontal (x) scale in the interval [-100.0, 100.0] |
| `float` | `v` | vertical (y) scale in the interval [-100.0, 100.0] |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llScaleTexture)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llScaleTexture) — scraped 2026-03-18_

Sets the texture u & v scales for the chosen face.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- The function silently fails if its face value indicates a face that does not exist.

## Examples

```lsl
// WARNING:
//      llScaleTexture has a delay of 200 miliseconds
//      that means every time the function is called within a script it'll take 0.2 seconds
//      for example the script below would take about 1.2 seconds....that's REALLY SLOW !!!
//
//      To work around that delay use the following instead:
//
//
//      llSetLinkPrimitiveParamsFast(integer link,
//          [PRIM_TEXTURE, integer face, string texture, vector repeats, vector offsets, float rotation_in_radians]);

// ***

//Scales the textures on 6 sides
float scale;

default
{
    state_entry()
    {
        integer index;
        while (index < 7)
        {
            scale += 0.1;
            llScaleTexture((float)scale, (float)scale, index);

            ++index;
        }
    }
}

// output:
//      face 0 >> 0.1
//      face 1 >> 0.2
//      face 2 >> 0.3
//      face 3 >> 0.4
//      face 4 >> 0.5
//      face 5 >> 0.6
//      face 6 >> 0.7
```

## See Also

### Functions

- llGetTextureScale

<!-- /wiki-source -->
