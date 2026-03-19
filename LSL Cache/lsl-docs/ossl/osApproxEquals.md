---
name: "osApproxEquals"
category: "function"
type: "function"
language: "OSSL"
description: "Returns an integer whether two rotations are within a given margin equal."
signature: "integer osApproxEquals(rotation ra, rotation rb, float margin)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osApproxEquals"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns an integer whether two rotations are within a given margin equal.

## Syntax

```lsl
integer osApproxEquals(rotation ra, rotation rb, float margin)
```

## Parameters

| Type | Name |
|------|------|
| `rotation` | `ra` |
| `rotation` | `rb` |
| `float` | `margin` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osApproxEquals](https://opensimulator.org/wiki/osApproxEquals)
