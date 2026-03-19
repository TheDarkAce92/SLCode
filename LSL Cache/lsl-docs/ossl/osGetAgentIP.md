---
name: "osGetAgentIP"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the IP address of a given avatar."
signature: "string osGetAgentIP(string agent)"
return_type: "string"
threat_level: "Severe"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetAgentIP"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the IP address of a given avatar.

## Syntax

```lsl
string osGetAgentIP(string agent)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `agent` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Severe
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetAgentIP](https://opensimulator.org/wiki/osGetAgentIP)
