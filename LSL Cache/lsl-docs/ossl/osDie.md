---
name: "osDie"
category: "function"
type: "function"
language: "OSSL"
description: "Similar to llDie, but works on a given object UUID."
signature: "void osDie(key uuid)"
return_type: "void"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDie"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Similar to llDie, but works on a given object UUID.

## Syntax

```lsl
void osDie(key uuid)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `uuid` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDie](https://opensimulator.org/wiki/osDie)
