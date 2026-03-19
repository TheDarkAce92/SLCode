---
name: "llGetColor"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the Blinn-Phong color on face."
signature: "vector llGetColor(integer face)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetColor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetcolor"]
---

Returns a vector that is the Blinn-Phong color on face.


## Signature

```lsl
vector llGetColor(integer face);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetColor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetColor) — scraped 2026-03-18_

Returns a vector that is the Blinn-Phong color on face.

## Caveats

- If face indicates a face that does not exist the  return is <0.0, 0.0, 0.0>

## Examples

```lsl
// Tells the owner the color on all sides
default
{
    state_entry()
    {
        integer i = 0;
        integer max = llGetNumberOfSides();
        while(i < max)
        {
            llOwnerSay("Face " + (string) i + " color is " + (string) llGetColor(i));
            ++i;
        }
    }
}
```

## See Also

### Functions

- **llGetAlpha** — Gets the prim's alpha
- **llSetAlpha** — Sets the prim's alpha
- **llSetColor** — Sets the prim's color
- **llSetLinkColor** — Sets link's color
- **llSetLinkAlpha** — Sets link's alpha
- **llGetNumberOfSides** — Gets the number of faces on the prim

### Articles

- Color in LSL

<!-- /wiki-source -->
