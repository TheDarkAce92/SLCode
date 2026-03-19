---
name: "osSetFontName"
category: "function"
type: "function"
language: "OSSL"
description: "Set the name of the font that will be used by osDrawText.\n- Threat Level: Not Checked."
signature: "string osSetFontName(string drawList, string fontName)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetFontName"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Set the name of the font that will be used by osDrawText.\n- Threat Level: Not Checked.

## Syntax

```lsl
string osSetFontName(string drawList, string fontName)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `string` | `fontName` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetFontName](https://opensimulator.org/wiki/osSetFontName)
