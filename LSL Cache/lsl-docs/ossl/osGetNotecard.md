---
name: "osGetNotecard"
category: "function"
type: "function"
language: "OSSL"
description: "Directly returns the entire contents of a given notecard as a string."
signature: "string osGetNotecard(string name)"
return_type: "string"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetNotecard"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Directly returns the entire contents of a given notecard as a string.

## Syntax

```lsl
string osGetNotecard(string name)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `name` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetNotecard](https://opensimulator.org/wiki/osGetNotecard)
