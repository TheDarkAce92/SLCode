---
name: "osGetLinkInventoryName"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the name of a given inventory item key in a given link."
signature: "string osGetLinkInventoryName(integer linkNumber, key itemId)"
return_type: "string"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetLinkInventoryName"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns the name of a given inventory item key in a given link.

## Syntax

```lsl
string osGetLinkInventoryName(integer linkNumber, key itemId)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `key` | `itemId` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkInventoryName](https://opensimulator.org/wiki/osGetLinkInventoryName)
