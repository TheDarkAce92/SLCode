---
name: "osLoopSoundSlave"
category: "function"
type: "function"
language: "OSSL"
description: "Sets a looping sound and volume of a given link as slave."
signature: "void osLoopSoundSlave(integer linknum, string sound, float volume)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osLoopSoundSlave"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets a looping sound and volume of a given link as slave.

## Syntax

```lsl
void osLoopSoundSlave(integer linknum, string sound, float volume)
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
- Reference: [https://opensimulator.org/wiki/osLoopSoundSlave](https://opensimulator.org/wiki/osLoopSoundSlave)
