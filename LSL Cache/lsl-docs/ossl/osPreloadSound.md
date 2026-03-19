---
name: "osPreloadSound"
category: "function"
type: "function"
language: "OSSL"
description: "Sets a sound to preload for a given link."
signature: "void osPreloadSound(integer linknum, string sound)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osPreloadSound"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets a sound to preload for a given link.

## Syntax

```lsl
void osPreloadSound(integer linknum, string sound)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknum` |
| `string` | `sound` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osPreloadSound](https://opensimulator.org/wiki/osPreloadSound)
