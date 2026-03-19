---
name: "osDrawRotationTransform"
category: "function"
type: "function"
language: "OSSL"
description: "Appends a rotation transform drawing command to the string provided in drawList and returns the result."
signature: "string osDrawRotationTransform(string drawList, float x)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawRotationTransform"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Appends a rotation transform drawing command to the string provided in drawList and returns the result.

## Syntax

```lsl
string osDrawRotationTransform(string drawList, float x)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `float` | `x` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawRotationTransform](https://opensimulator.org/wiki/osDrawRotationTransform)
