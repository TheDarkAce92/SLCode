---
name: "osGetLinkColor"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the color vector of a given link and face."
signature: "vector osGetLinkColor(integer linknum, integer face)"
return_type: "vector"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetLinkColor"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns the color vector of a given link and face.

## Syntax

```lsl
vector osGetLinkColor(integer linknum, integer face)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linknum` |
| `integer` | `face` |

## Return Value

`vector`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkColor](https://opensimulator.org/wiki/osGetLinkColor)
