---
name: "osStopSound"
category: "function"
type: "function"
language: "OSSL"
description: "Stops the sound for a given link."
signature: "void osStopSound(integer linknum)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osStopSound"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Stops the sound for a given link.

## Syntax

```lsl
void osStopSound(integer linknum)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknum` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osStopSound](https://opensimulator.org/wiki/osStopSound)
