---
name: "llsRGB2Linear"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector Transforms a color specified in the sRGB colorspace to the linear RGB colorspace."
signature: "vector llsRGB2Linear(vector srgb)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llsRGB2Linear'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a vector Transforms a color specified in the sRGB colorspace to the linear RGB colorspace.


## Signature

```lsl
vector llsRGB2Linear(vector srgb);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `srgb` | Color in the sRGB color space. |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llsRGB2Linear)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llsRGB2Linear) — scraped 2026-03-18_

Returns a vector Transforms a color specified in the sRGB colorspace to the linear RGB colorspace.

## Caveats

- The name of this function is actually a misnomer as LSL color is actually in [Rec.709](https://www.color.org/chardata/rgb/BT709.xalter) space, not [sRGB](https://www.color.org/chardata/rgb/srgb.xalter) space. While they are very similar, the gamma value for sRGB is approx. 2.2, whereas the gamma value for Rec.709 is approx. 2.4.
- Scripting for PBR-enabled viewers: If you enter color vectors manually, using the viewer's color picker, enter them as sRGB values. The color picker automatically converts them internally to Linear RGB, so someone using a PBR-enabled viewer will see them correctly. When you apply color vectors directly with a script, however, you must apply sRGB to Blinn-Phong textured faces and Linear RGB to PBR materials.

## See Also

### Functions

- **llLinear2sRGB** — To convert from the Linear colorspace to sRGB. (Inverse EOTF)

<!-- /wiki-source -->
