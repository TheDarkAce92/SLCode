---
name: "osListFindListNext"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the nth index of the sublist constrained with start and end count."
signature: "integer osListFindListNext(list src, list test, integer start, integer end, integer instance)"
return_type: "integer"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osListFindListNext"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns the nth index of the sublist constrained with start and end count.

## Syntax

```lsl
integer osListFindListNext(list src, list test, integer start, integer end, integer instance)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `list` | `test` |
| `integer` | `start` |
| `integer` | `end` |
| `integer` | `instance` |

## Return Value

`integer`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListFindListNext](https://opensimulator.org/wiki/osListFindListNext)
