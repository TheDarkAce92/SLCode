---
name: "osGetLinkInventoryKey"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the asset UUID of a given inventory item filtered by type in a given link."
signature: "key osGetLinkInventoryKey(integer linkNumber, string name, integer type)"
return_type: "key"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetLinkInventoryKey"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns the asset UUID of a given inventory item filtered by type in a given link.

## Syntax

```lsl
key osGetLinkInventoryKey(integer linkNumber, string name, integer type)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `string` | `name` |
| `integer` | `type` |

## Return Value

`key`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkInventoryKey](https://opensimulator.org/wiki/osGetLinkInventoryKey)
