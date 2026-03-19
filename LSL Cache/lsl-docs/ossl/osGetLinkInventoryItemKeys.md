---
name: "osGetLinkInventoryItemKeys"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of inventory item keys filtered by type in a given link."
signature: "list osGetLinkInventoryItemKeys(integer linkNumber, integer type)"
return_type: "list"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetLinkInventoryItemKeys"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a list of inventory item keys filtered by type in a given link.

## Syntax

```lsl
list osGetLinkInventoryItemKeys(integer linkNumber, integer type)
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
- Reference: [https://opensimulator.org/wiki/osGetLinkInventoryItemKeys](https://opensimulator.org/wiki/osGetLinkInventoryItemKeys)
