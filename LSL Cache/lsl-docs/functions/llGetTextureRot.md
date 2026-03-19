---
name: "llGetTextureRot"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the texture rotation, expressed as an angle, on face"
signature: "float llGetTextureRot(integer side)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetTextureRot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgettexturerot"]
---

Returns a float that is the texture rotation, expressed as an angle, on face


## Signature

```lsl
float llGetTextureRot(integer side);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number or ALL_SIDES |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetTextureRot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTextureRot) — scraped 2026-03-18_

Returns a float that is the texture rotation, expressed as an angle, on face

## Caveats

- If face indicates a face that does not exist the  return is 0.0

## Examples

```lsl
//Tells the owner the texture rotation on all sides
default
{
    state_entry()
    {
        integer i = 0;
        integer max = llGetNumberOfSides();
        while(i < max)
        {
            llSay(0,"Face "+(string)i+" texture rotation is " + (string)llGetTextureRot(i));
            ++i;
        }
    }
}
```

## See Also

### Functions

- llRotateTexture
- llGetNumberOfSides

<!-- /wiki-source -->
