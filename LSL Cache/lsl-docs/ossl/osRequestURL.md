---
name: "osRequestURL"
category: "function"
type: "function"
language: "OSSL"
description: "Request a new URL and directly return the assigned key."
signature: "key osRequestURL(list options)"
return_type: "key"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osRequestURL"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Request a new URL and directly return the assigned key.

## Syntax

```lsl
key osRequestURL(list options)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `options` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osRequestURL](https://opensimulator.org/wiki/osRequestURL)
