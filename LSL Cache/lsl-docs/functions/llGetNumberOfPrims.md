---
name: "llGetNumberOfPrims"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the number of prims in a link set the script is attached to."
signature: "integer llGetNumberOfPrims()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetNumberOfPrims'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetnumberofprims"]
---

Returns an integer that is the number of prims in a link set the script is attached to.


## Signature

```lsl
integer llGetNumberOfPrims();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetNumberOfPrims)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetNumberOfPrims) — scraped 2026-03-18_

Returns an integer that is the number of prims in a link set the script is attached to.

## Caveats

- The number of prims returned also includes the number of avatars sitting on the object.

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay((string)llGetLinkNumber());
        llOwnerSay((string)llGetNumberOfPrims());
    }
}
```

## See Also

### Functions

- **llGetObjectPrimCount** — Returns the number of prims in any object.
- **llGetLinkNumber** — Returns the link number of the prim the script is in.

<!-- /wiki-source -->
