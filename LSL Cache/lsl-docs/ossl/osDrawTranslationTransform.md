---
name: "osDrawTranslationTransform"
category: "function"
type: "function"
language: "OSSL"
description: "Appends a translation transform drawing command to the string provided in drawList and returns the result."
signature: "string osDrawTranslationTransform(string drawList, float x, float y)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawTranslationTransform"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Appends a translation transform drawing command to the string provided in drawList and returns the result.

## Syntax

```lsl
string osDrawTranslationTransform(string drawList, float x, float y)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `float` | `x` |
| `float` | `y` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawTranslationTransform](https://opensimulator.org/wiki/osDrawTranslationTransform)
