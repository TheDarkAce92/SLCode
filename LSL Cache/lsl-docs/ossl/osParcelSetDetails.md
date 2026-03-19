---
name: "osParcelSetDetails"
category: "function"
type: "function"
language: "OSSL"
description: "DEPRECATED. Use osSetParcelDetails instead."
signature: "void osParcelSetDetails(vector pos, list rules)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osParcelSetDetails"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

DEPRECATED. Use osSetParcelDetails instead.

## Syntax

```lsl
void osParcelSetDetails(vector pos, list rules)
```

## Parameters

| Type | Name |
|------|------|
| `vector` | `pos` |
| `list` | `rules` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osParcelSetDetails](https://opensimulator.org/wiki/osParcelSetDetails)
