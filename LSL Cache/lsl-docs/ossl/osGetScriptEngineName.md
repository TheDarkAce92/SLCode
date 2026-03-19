---
name: "osGetScriptEngineName"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the name of the active script engine."
signature: "string osGetScriptEngineName()"
return_type: "string"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetScriptEngineName"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the name of the active script engine.

## Syntax

```lsl
string osGetScriptEngineName()
```

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetScriptEngineName](https://opensimulator.org/wiki/osGetScriptEngineName)
