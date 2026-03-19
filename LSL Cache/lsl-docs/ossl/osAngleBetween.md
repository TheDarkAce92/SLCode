---
name: "osAngleBetween"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the angle between two vectors."
signature: "float osAngleBetween(vector a, vector b)"
return_type: "float"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osAngleBetween"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the angle between two vectors.

## Syntax

```lsl
float osAngleBetween(vector a, vector b)
```

## Parameters

| Type | Name |
|------|------|
| `vector` | `a` |
| `vector` | `b` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAngleBetween](https://opensimulator.org/wiki/osAngleBetween)
