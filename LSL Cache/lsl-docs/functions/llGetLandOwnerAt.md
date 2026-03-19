---
name: "llGetLandOwnerAt"
category: "function"
type: "function"
language: "LSL"
description: "Returns a key that is the land owner at pos."
signature: "key llGetLandOwnerAt(vector pos)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetLandOwnerAt'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetlandownerat"]
---

Returns a key that is the land owner at pos.


## Signature

```lsl
key llGetLandOwnerAt(vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | region coordinate |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetLandOwnerAt)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetLandOwnerAt) — scraped 2026-03-18_

Returns a key that is the land owner at pos.

## Examples

```lsl
default {
    state_entry() {
        //llKey2Name does not work for groups, and it requires avatars to be on sim (owner is not known when absent tested 2019-06-10).
        //Actually printing the owner name (also for groups) is somewhat tricky - if you feel otherwise, please update this example.
        llOwnerSay("The land owner under this object is " + llKey2Name(llGetLandOwnerAt(llGetPos())) + ".");
    }
}
```

## See Also

### Functions

- llGetParcelDetails

<!-- /wiki-source -->
