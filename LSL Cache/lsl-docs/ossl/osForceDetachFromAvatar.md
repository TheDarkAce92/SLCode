---
name: "osForceDetachFromAvatar"
category: "function"
type: "function"
language: "OSSL"
description: "Forcefully detach the object containing this script from the avatar it is attached to bypassing attach permissions."
signature: "void osForceDetachFromAvatar()"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceDetachFromAvatar"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Forcefully detach the object containing this script from the avatar it is attached to bypassing attach permissions.

## Syntax

```lsl
void osForceDetachFromAvatar()
```

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceDetachFromAvatar](https://opensimulator.org/wiki/osForceDetachFromAvatar)
