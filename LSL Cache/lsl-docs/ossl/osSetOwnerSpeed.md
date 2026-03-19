---
name: "osSetOwnerSpeed"
category: "function"
type: "function"
language: "OSSL"
description: "Sets a modifier for the movement speed of the object owner."
signature: "void osSetOwnerSpeed(float SpeedModifier)"
return_type: "void"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetOwnerSpeed"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets a modifier for the movement speed of the object owner.

## Syntax

```lsl
void osSetOwnerSpeed(float SpeedModifier)
```

## Parameters

| Type | Name |
|------|------|
| `float` | `SpeedModifier` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetOwnerSpeed](https://opensimulator.org/wiki/osSetOwnerSpeed)
