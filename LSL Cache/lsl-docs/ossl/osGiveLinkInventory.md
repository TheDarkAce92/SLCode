---
name: "osGiveLinkInventory"
category: "function"
type: "function"
language: "OSSL"
description: "Send a given inventory item (name) from a given link to a destination object or avatar (key)."
signature: "void osGiveLinkInventory(integer linkNumber, key destination, string inventory)"
return_type: "void"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGiveLinkInventory"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Send a given inventory item (name) from a given link to a destination object or avatar (key).

## Syntax

```lsl
void osGiveLinkInventory(integer linkNumber, key destination, string inventory)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `key` | `destination` |
| `string` | `inventory` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGiveLinkInventory](https://opensimulator.org/wiki/osGiveLinkInventory)
