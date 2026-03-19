---
name: "osForceDropAttachment"
category: "function"
type: "function"
language: "OSSL"
description: "Attempts to drop the attachment the script is in to the ground bypassing script permissions."
signature: "void osForceDropAttachment()"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceDropAttachment"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Attempts to drop the attachment the script is in to the ground bypassing script permissions.

## Syntax

```lsl
void osForceDropAttachment()
```

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceDropAttachment](https://opensimulator.org/wiki/osForceDropAttachment)
