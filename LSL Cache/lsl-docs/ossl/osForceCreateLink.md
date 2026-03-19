---
name: "osForceCreateLink"
category: "function"
type: "function"
language: "OSSL"
description: "Add a link to a linkset bypassing object owner permissions."
signature: "void osForceCreateLink(string target, integer parent)"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceCreateLink"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Add a link to a linkset bypassing object owner permissions.

## Syntax

```lsl
void osForceCreateLink(string target, integer parent)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `target` |
| `integer` | `parent` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceCreateLink](https://opensimulator.org/wiki/osForceCreateLink)
