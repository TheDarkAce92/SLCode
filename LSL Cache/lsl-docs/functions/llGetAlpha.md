---
name: "llGetAlpha"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the Blinn-Phong alpha of face.

If face is ALL_SIDES then the function returns the sum of alpha of all the faces on the prim, range [0, sides].
Otherwise the return is in the range [0, 1], with 0.0 being fully transparent and 1.0 being fully solid.'
signature: "float llGetAlpha(integer face)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAlpha'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetalpha"]
---

Returns a float that is the Blinn-Phong alpha of face.

If face is ALL_SIDES then the function returns the sum of alpha of all the faces on the prim, range [0, sides].
Otherwise the return is in the range [0, 1], with 0.0 being fully transparent and 1.0 being fully solid.


## Signature

```lsl
float llGetAlpha(integer face);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAlpha)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAlpha) — scraped 2026-03-18_

Returns a float that is the Blinn-Phong alpha of face.

## Caveats

- If face indicates a face that does not exist the  return is 1.0

## Examples

```lsl
//Tells the owner the alpha on all sides
default
{
    state_entry()
    {
        integer i = 0;
        integer max = llGetNumberOfSides();
        while(i < max)
        {
            llSay(0,"Face "+(string)i+" alpha is " + (string)llGetAlpha(i));
            ++i;
        }
    }
}
```

## See Also

### Functions

- **llSetAlpha** — Sets the prim's alpha
- **llGetColor** — Gets the prim's color
- **llSetColor** — Sets the prim's color
- **llSetLinkColor** — Sets link's color
- **llSetLinkAlpha** — Sets link's alpha
- **llGetNumberOfSides** — Gets the number of faces on the prim

### Articles

- Translucent Color

<!-- /wiki-source -->
