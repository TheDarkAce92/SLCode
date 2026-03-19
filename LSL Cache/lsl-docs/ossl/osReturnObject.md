---
name: "osReturnObject"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a rezzed object identified by key back to its owner."
signature: "void osReturnObject(key userID)"
return_type: "void"
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osReturnObject"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a rezzed object identified by key back to its owner.

## Syntax

```lsl
void osReturnObject(key userID)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `userID` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- See: [https://opensimulator.org/wiki/osReturnObject](https://opensimulator.org/wiki/osReturnObject)
