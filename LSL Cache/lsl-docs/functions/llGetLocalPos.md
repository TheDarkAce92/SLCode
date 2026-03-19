---
name: "llGetLocalPos"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the position relative (local) to the root.

If called from the root prim it returns the position in the region unless it is attached to which it returns the position relative to the attach point.'
signature: "vector llGetLocalPos()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetLocalPos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetlocalpos"]
---

Returns a vector that is the position relative (local) to the root.

If called from the root prim it returns the position in the region unless it is attached to which it returns the position relative to the attach point.


## Signature

```lsl
vector llGetLocalPos();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetLocalPos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetLocalPos) — scraped 2026-03-18_

Returns a vector that is the position relative (local) to the root.

## Examples

```lsl
default
{
    touch_start(integer vIntTouched)
    {
        string vStrMessage = "The touched prim is ";
        if (llDetectedLinkNumber(0) > 1)
        {
            vStrMessage += (string)llVecMag(llGetLocalPos()) + "m from ";
        }
        llSay(0, vStrMessage + "the root prim");
    }
}
```

## See Also

### Functions

- **llGetRootPosition** — Gets the root prims global position
- **llGetPos** — Gets the prims global position
- **llSetPos** — Sets the prims global position

<!-- /wiki-source -->
