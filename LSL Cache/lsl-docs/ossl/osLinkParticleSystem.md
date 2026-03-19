---
name: "osLinkParticleSystem"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the particle system rules of a given link."
signature: "void osLinkParticleSystem(integer linknumber, list rules)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osLinkParticleSystem"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the particle system rules of a given link.

## Syntax

```lsl
void osLinkParticleSystem(integer linknumber, list rules)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknumber` |
| `list` | `rules` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osLinkParticleSystem](https://opensimulator.org/wiki/osLinkParticleSystem)
