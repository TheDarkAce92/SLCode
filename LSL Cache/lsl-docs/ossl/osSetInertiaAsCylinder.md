---
name: "osSetInertiaAsCylinder"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the inertia data for the object containing the script based on a cylindrical bounding box calculation."
signature: "void osSetInertiaAsCylinder(float mass, float radius, float length, vector centerOfMass, rotation lslrot)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetInertiaAsCylinder"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the inertia data for the object containing the script based on a cylindrical bounding box calculation.

## Syntax

```lsl
void osSetInertiaAsCylinder(float mass, float radius, float length, vector centerOfMass, rotation lslrot)
```

## Parameters

| Type | Name |
|------|------|
| `float` | `mass` |
| `float` | `radius` |
| `float` | `length` |
| `vector` | `centerOfMass` |
| `rotation` | `lslrot` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetInertiaAsCylinder](https://opensimulator.org/wiki/osSetInertiaAsCylinder)
