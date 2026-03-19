---
name: "osSetWindParam"
category: "function"
type: "function"
language: "OSSL"
description: "Set a parameter in a given wind plugin."
signature: "void osSetWindParam(string plugin, string param, float value)"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetWindParam"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Set a parameter in a given wind plugin.

## Syntax

```lsl
void osSetWindParam(string plugin, string param, float value)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `plugin` |
| `string` | `param` |
| `float` | `value` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetWindParam](https://opensimulator.org/wiki/osSetWindParam)
