---
name: "osForceBreakLink"
category: "function"
type: "function"
language: "OSSL"
description: "Break a link of a linkset bypassing object owner permissions."
signature: "void osForceBreakLink(integer linknum)"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceBreakLink"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Break a link of a linkset bypassing object owner permissions.

## Syntax

```lsl
void osForceBreakLink(integer linknum)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknum` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceBreakLink](https://opensimulator.org/wiki/osForceBreakLink)
