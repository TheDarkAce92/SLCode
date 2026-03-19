---
name: "osDrawLine"
category: "function"
type: "function"
language: "OSSL"
description: "Draws a line from the current drawing position to a target position (pixels x y)."
signature: "string osDrawLine(string drawList, integer endX, integer endY)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawLine"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Draws a line from the current drawing position to a target position (pixels x y).

## Syntax

```lsl
string osDrawLine(string drawList, integer endX, integer endY)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `integer` | `endX` |
| `integer` | `endY` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawLine](https://opensimulator.org/wiki/osDrawLine)
