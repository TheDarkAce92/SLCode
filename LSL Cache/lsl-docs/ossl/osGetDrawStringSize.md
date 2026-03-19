---
name: "osGetDrawStringSize"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a vector containing the horizontal and vertical dimensions in pixels of the specified text, if drawn in the specified font and at the specified point size. The horizontal extent is returned in the .x component of the vector, and the vertical extent is returned in .y. The .z component is not "
signature: "vector osGetDrawStringSize(string contentType, string text, string fontName, integer fontSize)"
return_type: "vector"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetDrawStringSize"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a vector containing the horizontal and vertical dimensions in pixels of the specified text, if drawn in the specified font and at the specified point size. The horizontal extent is returned in the .x component of the vector, and the vertical extent is returned in .y. The .z component is not used.

## Syntax

```lsl
vector osGetDrawStringSize(string contentType, string text, string fontName, integer fontSize)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `contentType` |
| `string` | `text` |
| `string` | `fontName` |
| `integer` | `fontSize` |

## Return Value

`vector`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetDrawStringSize](https://opensimulator.org/wiki/osGetDrawStringSize)
