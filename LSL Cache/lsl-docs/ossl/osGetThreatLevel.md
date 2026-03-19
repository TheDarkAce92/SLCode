---
name: "osGetThreatLevel"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the configured threat-level label for the supplied OSSL function name."
signature: "string osGetThreatLevel(string id)"
return_type: "string"
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetThreatLevel"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the configured threat-level label for the supplied OSSL function name.

## Syntax

```lsl
string osGetThreatLevel(string id)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `id` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- See: [https://opensimulator.org/wiki/osGetThreatLevel](https://opensimulator.org/wiki/osGetThreatLevel)
