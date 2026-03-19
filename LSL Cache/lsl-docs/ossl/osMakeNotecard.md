---
name: "osMakeNotecard"
category: "function"
type: "function"
language: "OSSL"
description: "Creates a new notecard in the primitive inventory with given contents."
signature: "void osMakeNotecard(string notecardName, list contents)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osMakeNotecard"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Creates a new notecard in the primitive inventory with given contents.

## Syntax

```lsl
void osMakeNotecard(string notecardName, list contents)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `notecardName` |
| `list` | `contents` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osMakeNotecard](https://opensimulator.org/wiki/osMakeNotecard)
