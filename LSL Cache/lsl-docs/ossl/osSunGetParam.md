---
name: "osSunGetParam"
category: "function"
type: "function"
language: "OSSL"
description: "DEPRECATED. Use osGetSunParam instead."
signature: "float osSunGetParam(string param)"
return_type: "float"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSunGetParam"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

DEPRECATED. Use osGetSunParam instead.

## Syntax

```lsl
float osSunGetParam(string param)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `param` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSunGetParam](https://opensimulator.org/wiki/osSunGetParam)
