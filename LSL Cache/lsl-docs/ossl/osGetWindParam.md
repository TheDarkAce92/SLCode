---
name: "osGetWindParam"
category: "function"
type: "function"
language: "OSSL"
description: "Get a parameter from a given wind plugin."
signature: "float osGetWindParam(string plugin, string param)"
return_type: "float"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetWindParam"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Get a parameter from a given wind plugin.

## Syntax

```lsl
float osGetWindParam(string plugin, string param)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `plugin` |
| `string` | `param` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetWindParam](https://opensimulator.org/wiki/osGetWindParam)
