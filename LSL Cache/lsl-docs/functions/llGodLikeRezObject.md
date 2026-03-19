---
name: "llGodLikeRezObject"
category: "function"
type: "function"
language: "LSL"
description: "Rez directly off of UUID if owner has god-bit set."
signature: "void llGodLikeRezObject(key inventory, vector pos)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGodLikeRezObject'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "god-mode"
---

Rez directly off of UUID if owner has god-bit set.


## Signature

```lsl
void llGodLikeRezObject(key inventory, vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `inventory` |  |
| `vector` | `pos` | position in region coordinates |


## Caveats

- Energy cost: **10.0**.
- Available to **god-mode** (Linden Lab internal) only.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGodLikeRezObject)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGodLikeRezObject) — scraped 2026-03-18_

Rez directly off of UUID if owner has god-bit set.

## Caveats

- This function can only be executed in God Mode.

## Examples

```lsl
// This will only work if you have the god-bit set.
key object = "a822ff2b-ff02-461d-b45d-dcd10a2de0c2"; // Our object key
vector pos = <127,127,50>; // Our object pos
llGodLikeRezObject(object, pos); // This will rez the object
```

<!-- /wiki-source -->
