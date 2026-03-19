---
name: "osRegionNotice"
category: "function"
type: "function"
language: "OSSL"
description: "Send a notice message to a given avatar in the region."
signature: "void osRegionNotice(key agent_id, string msg)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osRegionNotice"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Send a notice message to a given avatar in the region.

## Syntax

```lsl
void osRegionNotice(key agent_id, string msg)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agent_id` |
| `string` | `msg` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osRegionNotice](https://opensimulator.org/wiki/osRegionNotice)
