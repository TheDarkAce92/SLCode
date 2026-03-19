---
name: "llGetHealth"
category: "function"
type: "function"
language: "LSL"
description: "Returns the current health of an avatar."
signature: "float llGetHealth(key id)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetHealth'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experimental"
---

Returns the current health of an avatar.


## Signature

```lsl
float llGetHealth(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (handle)` | `agent_id` | The ID of an agent in the region. |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.
- **Experimental** — behaviour may change.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetHealth)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetHealth) — scraped 2026-03-18_

Returns the current health of an avatar or object in the region.Returns a float

## Caveats

- Seems to be able to return current health of avatars in neighbouring regions as well

## See Also

### Constants

- PRIM_HEALTH
- OBJECT_HEALTH

### Functions

- llGetObjectDetails
- LlSetPrimitiveParams
- LlSetLinkPrimitiveParams
- LlGetPrimitiveParams
- LlGetLinkPrimitiveParams

<!-- /wiki-source -->
