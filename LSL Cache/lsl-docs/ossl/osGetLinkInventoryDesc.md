---
name: "osGetLinkInventoryDesc"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the description of a given inventory item key or name in a given link."
signature: "string osGetLinkInventoryDesc(integer linkNumber, string itemNameorid)"
return_type: "string"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetLinkInventoryDesc"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns the description of a given inventory item key or name in a given link.

## Syntax

```lsl
string osGetLinkInventoryDesc(integer linkNumber, string itemNameorid)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `string` | `itemNameorid` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkInventoryDesc](https://opensimulator.org/wiki/osGetLinkInventoryDesc)
