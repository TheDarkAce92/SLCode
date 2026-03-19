---
name: "osSetPenCap"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the start, end or both caps to either \'diamond\', \'arrow\', \'round\', or default \'flat\' shape."
signature: "string osSetPenCap(string drawList, string direction, string type)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetPenCap"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the start, end or both caps to either "diamond", "arrow", "round", or default "flat" shape.

## Syntax

```lsl
string osSetPenCap(string drawList, string direction, string type)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `string` | `direction` |
| `string` | `type` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetPenCap](https://opensimulator.org/wiki/osSetPenCap)
