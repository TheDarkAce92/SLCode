---
name: "osOldList2ListStrided"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a strided list of a given list."
signature: "list osOldList2ListStrided(list src, integer start, integer end, integer stride)"
return_type: "list"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osOldList2ListStrided"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a strided list of a given list.

## Syntax

```lsl
list osOldList2ListStrided(list src, integer start, integer end, integer stride)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `integer` | `start` |
| `integer` | `end` |
| `integer` | `stride` |

## Return Value

`list`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osOldList2ListStrided](https://opensimulator.org/wiki/osOldList2ListStrided)
