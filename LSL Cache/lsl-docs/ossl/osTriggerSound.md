---
name: "osTriggerSound"
category: "function"
type: "function"
language: "OSSL"
description: "Trigger a given preloaded sound with volume for a given link."
signature: "void osTriggerSound(integer linknum, string sound, float volume)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osTriggerSound"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Trigger a given preloaded sound with volume for a given link.

## Syntax

```lsl
void osTriggerSound(integer linknum, string sound, float volume)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknum` |
| `string` | `sound` |
| `float` | `volume` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osTriggerSound](https://opensimulator.org/wiki/osTriggerSound)
