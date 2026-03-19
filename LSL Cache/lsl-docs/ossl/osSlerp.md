---
name: "osSlerp"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a spherical interpolation of two vectors shifted by amount."
signature: "vector osSlerp(vector a, vector b, float amount)"
return_type: "vector"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSlerp"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a spherical interpolation of two vectors shifted by amount.

## Syntax

```lsl
vector osSlerp(vector a, vector b, float amount)
```

## Parameters

| Type | Name |
|------|------|
| `vector` | `a` |
| `vector` | `b` |
| `float` | `amount` |

## Return Value

`vector`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSlerp](https://opensimulator.org/wiki/osSlerp)
