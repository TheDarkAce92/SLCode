---
name: "osRezObject"
category: "function"
type: "function"
language: "OSSL"
description: "Rezzes an inventory object with explicit position, velocity, rotation, and advanced rez flags."
signature: "void osRezObject(string inventory, vector pos, vector vel, rotation rot, integer param, integer isRezAtRoot, integer doRecoil, integer SetDieAtEdge, integer CheckPos)"
return_type: "void"
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osRezObject"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Rezzes an inventory object with explicit position, velocity, rotation, and advanced rez flags.

## Syntax

```lsl
void osRezObject(string inventory, vector pos, vector vel, rotation rot, integer param, integer isRezAtRoot, integer doRecoil, integer SetDieAtEdge, integer CheckPos)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `inventory` |
| `vector` | `pos` |
| `vector` | `vel` |
| `rotation` | `rot` |
| `integer` | `param` |
| `integer` | `isRezAtRoot` |
| `integer` | `doRecoil` |
| `integer` | `SetDieAtEdge` |
| `integer` | `CheckPos` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- See: [https://opensimulator.org/wiki/osRezObject](https://opensimulator.org/wiki/osRezObject)
