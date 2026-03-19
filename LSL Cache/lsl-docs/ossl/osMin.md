---
name: "osMin"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the smaller of two given numbers."
signature: "float osMin(float a, float b)"
return_type: "float"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osMin"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the smaller of two given numbers.

## Syntax

```lsl
float osMin(float a, float b)
```

## Parameters

| Type | Name |
|------|------|
| `float` | `a` |
| `float` | `b` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osMin](https://opensimulator.org/wiki/osMin)
