---
name: "osResetAllScripts"
category: "function"
type: "function"
language: "OSSL"
description: "Resets all scripts in the inventory of a link, the entire linkset or itself."
signature: "void osResetAllScripts(integer AllLinkset)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osResetAllScripts"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Resets all scripts in the inventory of a link, the entire linkset or itself.

## Syntax

```lsl
void osResetAllScripts(integer AllLinkset)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `AllLinkset` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osResetAllScripts](https://opensimulator.org/wiki/osResetAllScripts)
