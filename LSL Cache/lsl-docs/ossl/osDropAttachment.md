---
name: "osDropAttachment"
category: "function"
type: "function"
language: "OSSL"
description: "Attempts to drop the attachment the script is in to the ground."
signature: "void osDropAttachment()"
return_type: "void"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDropAttachment"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Attempts to drop the attachment the script is in to the ground.

## Syntax

```lsl
void osDropAttachment()
```

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDropAttachment](https://opensimulator.org/wiki/osDropAttachment)
