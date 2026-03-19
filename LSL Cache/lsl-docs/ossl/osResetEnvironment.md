---
name: "osResetEnvironment"
category: "function"
type: "function"
language: "OSSL"
description: "Resets either the parcel or region environment to their default values."
signature: "integer osResetEnvironment(integer parcelOrRegion, integer transition)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osResetEnvironment"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Resets either the parcel or region environment to their default values.

## Syntax

```lsl
integer osResetEnvironment(integer parcelOrRegion, integer transition)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `parcelOrRegion` |
| `integer` | `transition` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osResetEnvironment](https://opensimulator.org/wiki/osResetEnvironment)
