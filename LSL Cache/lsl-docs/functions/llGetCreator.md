---
name: "llGetCreator"
category: "function"
type: "function"
language: "LSL"
description: "Returns a key for the creator of the prim."
signature: "key llGetCreator()"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetCreator'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetcreator"]
---

Returns a key for the creator of the prim.


## Signature

```lsl
key llGetCreator();
```


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetCreator)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetCreator) — scraped 2026-03-18_

Returns a key for the creator of the prim.

## Examples

```lsl
default
{
    state_entry()
    {
        key owner = llGetOwner();
        key creatorThisPrim = llGetCreator();

        llSay(0, "The creator of this prim has the key '"+(string)creatorThisPrim + "'.");
        llSay(0, "My owner has the key '" + (string)owner + "'.");
    }
}
```

## See Also

### Functions

- llGetInventoryCreator
- llGetOwner

<!-- /wiki-source -->
