---
name: "osMovePen"
category: "function"
type: "function"
language: "OSSL"
description: "Move the drawing position to a given coordinate (pixels x y)."
signature: "string osMovePen(string drawList, integer x, integer y)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osMovePen"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Move the drawing position to a given coordinate (pixels x y).

## Syntax

```lsl
string osMovePen(string drawList, integer x, integer y)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `integer` | `x` |
| `integer` | `y` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osMovePen](https://opensimulator.org/wiki/osMovePen)
