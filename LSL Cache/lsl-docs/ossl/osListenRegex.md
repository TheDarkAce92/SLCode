---
name: "osListenRegex"
category: "function"
type: "function"
language: "OSSL"
description: "Creates a listener that parses matches for name and message through regex."
signature: "integer osListenRegex(integer channelID, string name, string ID, string msg, integer regexBitfield)"
return_type: "integer"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osListenRegex"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Creates a listener that parses matches for name and message through regex.

## Syntax

```lsl
integer osListenRegex(integer channelID, string name, string ID, string msg, integer regexBitfield)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `channelID` |
| `string` | `name` |
| `string` | `ID` |
| `string` | `msg` |
| `integer` | `regexBitfield` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListenRegex](https://opensimulator.org/wiki/osListenRegex)
