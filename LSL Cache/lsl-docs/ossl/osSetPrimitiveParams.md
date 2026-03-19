---
name: "osSetPrimitiveParams"
category: "function"
type: "function"
language: "OSSL"
description: "Sets primitive params of a given primitive (object UUID)."
signature: "void osSetPrimitiveParams(key prim, list rules)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetPrimitiveParams"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets primitive params of a given primitive (object UUID).

## Syntax

```lsl
void osSetPrimitiveParams(key prim, list rules)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `prim` |
| `list` | `rules` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetPrimitiveParams](https://opensimulator.org/wiki/osSetPrimitiveParams)
