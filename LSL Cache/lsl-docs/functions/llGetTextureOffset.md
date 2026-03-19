---
name: "llGetTextureOffset"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the texture offset of face in the x ('U', horizontal) and y ('V', vertical) components. The z component is unused."
signature: "vector llGetTextureOffset(integer face)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetTextureOffset'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgettextureoffset"]
---

Returns a vector that is the texture offset of face in the x ("U", horizontal) and y ("V", vertical) components. The z component is unused.


## Signature

```lsl
vector llGetTextureOffset(integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number or ALL_SIDES |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetTextureOffset)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTextureOffset) — scraped 2026-03-18_

Returns a vector that is the texture offset of face in the x ("U", horizontal) and y ("V", vertical) components. The z component is unused.

## Caveats

- If face indicates a face that does not exist the  return is <0.0, 0.0, 0.0>

## Examples

```lsl
//Tells the owner the texture offset on all sides
default
{
    state_entry()
    {
        integer i = 0;
        integer max = llGetNumberOfSides();
        while(i < max)
        {
            llSay(0,"Face "+(string)i+" texture offset is " + (string)llGetTextureOffset(i));
            ++i;
        }
    }
}
```

```lsl
vector offsetVec = llGetTextureOffset(0);
float u = offsetVec.x;
float v = offsetVec.y;
// z is not used.
```

## See Also

### Functions

- llOffsetTexture
- llGetNumberOfSides

<!-- /wiki-source -->
