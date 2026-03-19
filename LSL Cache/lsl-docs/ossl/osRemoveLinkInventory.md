---
name: "osRemoveLinkInventory"
category: "function"
type: "function"
language: "OSSL"
description: "Removes a inventory item by name in a given link."
signature: "void osRemoveLinkInventory(integer linkNumber, string name)"
return_type: "void"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osRemoveLinkInventory"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Removes a inventory item by name in a given link.

## Syntax

```lsl
void osRemoveLinkInventory(integer linkNumber, string name)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `string` | `name` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osRemoveLinkInventory](https://opensimulator.org/wiki/osRemoveLinkInventory)
