---
name: "osGetSittingAvatarsCount"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the number of avatars seated on a given object (key)."
signature: "integer osGetSittingAvatarsCount(key object_id)"
return_type: "integer"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetSittingAvatarsCount"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns the number of avatars seated on a given object (key).

## Syntax

```lsl
integer osGetSittingAvatarsCount(key object_id)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `object_id` |

## Return Value

`integer`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetSittingAvatarsCount](https://opensimulator.org/wiki/osGetSittingAvatarsCount)
