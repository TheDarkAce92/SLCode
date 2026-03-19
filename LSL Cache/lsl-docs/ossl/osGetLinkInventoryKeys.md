---
name: "osGetLinkInventoryKeys"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of asset UUIDs of inventory items filtered by type in a given link."
signature: "list osGetLinkInventoryKeys(integer linkNumber, integer type)"
return_type: "list"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetLinkInventoryKeys"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a list of asset UUIDs of inventory items filtered by type in a given link.

## Syntax

```lsl
list osGetLinkInventoryKeys(integer linkNumber, integer type)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `integer` | `type` |

## Return Value

`list`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkInventoryKeys](https://opensimulator.org/wiki/osGetLinkInventoryKeys)
