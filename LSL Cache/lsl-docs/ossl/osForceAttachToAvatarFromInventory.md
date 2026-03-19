---
name: "osForceAttachToAvatarFromInventory"
category: "function"
type: "function"
language: "OSSL"
description: "Forcefully attaches an object from the inventory of the object containing this script to the object owner bypassing attach permissions."
signature: "void osForceAttachToAvatarFromInventory(string itemName, integer attachment)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceAttachToAvatarFromInventory"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Forcefully attaches an object from the inventory of the object containing this script to the object owner bypassing attach permissions.

## Syntax

```lsl
void osForceAttachToAvatarFromInventory(string itemName, integer attachment)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `itemName` |
| `integer` | `attachment` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceAttachToAvatarFromInventory](https://opensimulator.org/wiki/osForceAttachToAvatarFromInventory)
