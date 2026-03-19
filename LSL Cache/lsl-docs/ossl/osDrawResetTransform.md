---
name: "osDrawResetTransform"
category: "function"
type: "function"
language: "OSSL"
description: "Reset all transforms."
signature: "string osDrawResetTransform(string drawList)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawResetTransform"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Reset all transforms.

## Syntax

```lsl
string osDrawResetTransform(string drawList)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawResetTransform](https://opensimulator.org/wiki/osDrawResetTransform)
