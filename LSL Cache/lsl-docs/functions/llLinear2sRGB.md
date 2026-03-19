---
name: "llLinear2sRGB"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector Transforms a color specified in linear RGB colorspace into the sRGB colorspace."
signature: "vector llLinear2sRGB(vector color)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinear2sRGB'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a vector Transforms a color specified in linear RGB colorspace into the sRGB colorspace.


## Signature

```lsl
vector llLinear2sRGB(vector color);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `color` | Color in the linear color space. |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinear2sRGB)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinear2sRGB) — scraped 2026-03-18_

Returns a vector Transforms a color specified in linear RGB colorspace into the sRGB colorspace.

## Caveats

- The name of this function is actually a misnomer as LSL color is actually in [Rec.709](https://www.color.org/chardata/rgb/BT709.xalter) space, not [sRGB](https://www.color.org/chardata/rgb/srgb.xalter) space. While they are very similar, the gamma value for sRGB is approx. 2.2, whereas the gamma value for Rec.709 is approx. 2.4.
- Scripting for PBR-enabled viewers: If you enter color vectors manually, using the viewer's color picker, enter them as sRGB values. The color picker automatically converts them internally to Linear RGB, so someone using a PBR-enabled viewer will see them correctly. When you apply color vectors directly with a script, however, you must apply sRGB to Blinn-Phong textured faces and Linear RGB to PBR materials.

## See Also

### Functions

- **llsRGB2Linear** — To convert from sRGB to the Linear colorspace. (EOTF)

<!-- /wiki-source -->
