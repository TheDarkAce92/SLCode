---
name: "osParcelSubdivide"
category: "function"
type: "function"
language: "OSSL"
description: "Subdivides a parcel as rectangle given a start and end position as vector."
signature: "void osParcelSubdivide(vector pos1, vector pos2)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osParcelSubdivide"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Subdivides a parcel as rectangle given a start and end position as vector.

## Syntax

```lsl
void osParcelSubdivide(vector pos1, vector pos2)
```

## Parameters

| Type | Name |
|------|------|
| `vector` | `pos1` |
| `vector` | `pos2` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osParcelSubdivide](https://opensimulator.org/wiki/osParcelSubdivide)
