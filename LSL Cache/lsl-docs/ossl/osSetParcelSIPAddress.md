---
name: "osSetParcelSIPAddress"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the voice module SIP address to a given address."
signature: "void osSetParcelSIPAddress(string SIPAddress)"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetParcelSIPAddress"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the voice module SIP address to a given address.

## Syntax

```lsl
void osSetParcelSIPAddress(string SIPAddress)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `SIPAddress` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetParcelSIPAddress](https://opensimulator.org/wiki/osSetParcelSIPAddress)
