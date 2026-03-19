---
name: "osSunSetParam"
category: "function"
type: "function"
language: "OSSL"
description: "DEPRECATED. Use osSetSunParam instead."
signature: "void osSunSetParam(string param, float value)"
return_type: "void"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSunSetParam"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

DEPRECATED. Use osSetSunParam instead.

## Syntax

```lsl
void osSunSetParam(string param, float value)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `param` |
| `float` | `value` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSunSetParam](https://opensimulator.org/wiki/osSunSetParam)
