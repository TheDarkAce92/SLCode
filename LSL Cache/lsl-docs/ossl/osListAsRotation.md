---
name: "osListAsRotation"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a rotation that is at index(>=0) in src or zero rotation if that is not a vector"
signature: "rotation osListAsRotation(list src, integer index)"
return_type: "rotation"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osListAsRotation"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a rotation that is at index(>=0) in src or zero rotation if that is not a vector

## Syntax

```lsl
rotation osListAsRotation(list src, integer index)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `integer` | `index` |

## Return Value

`rotation`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListAsRotation](https://opensimulator.org/wiki/osListAsRotation)
