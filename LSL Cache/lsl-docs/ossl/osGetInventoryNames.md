---
name: "osGetInventoryNames"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of inventory names filtered by type in the object containing the script."
signature: "list osGetInventoryNames(integer type)"
return_type: "list"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetInventoryNames"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a list of inventory names filtered by type in the object containing the script.

## Syntax

```lsl
list osGetInventoryNames(integer type)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `type` |

## Return Value

`list`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetInventoryNames](https://opensimulator.org/wiki/osGetInventoryNames)
