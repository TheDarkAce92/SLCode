---
name: "osListSortInPlaceStrided"
category: "function"
type: "function"
language: "OSSL"
description: "Sorts a given strided list in place."
signature: "void osListSortInPlaceStrided(list src, integer stride, integer stride_index, integer ascending)"
return_type: "void"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osListSortInPlaceStrided"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Sorts a given strided list in place.

## Syntax

```lsl
void osListSortInPlaceStrided(list src, integer stride, integer stride_index, integer ascending)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `integer` | `stride` |
| `integer` | `stride_index` |
| `integer` | `ascending` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListSortInPlaceStrided](https://opensimulator.org/wiki/osListSortInPlaceStrided)
