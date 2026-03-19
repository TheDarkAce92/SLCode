---
name: "osGetAgentCountry"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the country of a user."
signature: "string osGetAgentCountry(key agentId)"
return_type: "string"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetAgentCountry"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the country of a user.

## Syntax

```lsl
string osGetAgentCountry(key agentId)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentId` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetAgentCountry](https://opensimulator.org/wiki/osGetAgentCountry)
