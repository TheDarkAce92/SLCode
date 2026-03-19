---
name: "osGetLinkPrimitiveParams"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of the primitive parameters given its link number."
signature: "list osGetLinkPrimitiveParams(integer linknumber, list rules)"
return_type: "list"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetLinkPrimitiveParams"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a list of the primitive parameters given its link number.

## Syntax

```lsl
list osGetLinkPrimitiveParams(integer linknumber, list rules)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknumber` |
| `list` | `rules` |

## Return Value

`list`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkPrimitiveParams](https://opensimulator.org/wiki/osGetLinkPrimitiveParams)
