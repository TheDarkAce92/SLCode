---
name: "llGetScale"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the scale of the prim."
signature: "vector llGetScale()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetScale'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetscale"]
---

Returns a vector that is the scale of the prim.


## Signature

```lsl
vector llGetScale();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetScale)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetScale) — scraped 2026-03-18_

Returns a vector that is the scale of the prim.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        llSay(0, "My dimensions are: " + (string)llGetScale());
    }
}
```

## See Also

### Functions

- **llSetScale** — Sets the prims size
- **llSetPrimitiveParams** — Sets prims attributes
- **llGetPrimitiveParams** — Gets prims attributes

<!-- /wiki-source -->
