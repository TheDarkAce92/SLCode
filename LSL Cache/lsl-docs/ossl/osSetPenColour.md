---
name: "osSetPenColour"
category: "function"
type: "function"
language: "OSSL"
description: "DEPRECATED. Use osSetPenColor instead."
signature: "string osSetPenColour(string drawList, string colour)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetPenColour"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

DEPRECATED. Use osSetPenColor instead.

## Syntax

```lsl
string osSetPenColour(string drawList, string colour)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `string` | `colour` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetPenColour](https://opensimulator.org/wiki/osSetPenColour)
