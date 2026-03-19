---
name: "llGetVisualParams"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list of the details for agentid requested in params.

An empty list if agentid is not found.
An empty string, '', is returned in the place of any invalid or unknown visual parameter.'
signature: "list llGetVisualParams(key id, list params)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetVisualParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a list of the details for agentid requested in params.

An empty list if agentid is not found.
An empty string, "", is returned in the place of any invalid or unknown visual parameter.


## Signature

```lsl
list llGetVisualParams(key id, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agentid` | Avatar ID in the same region. |
| `list` | `params` | List of visual param ids or names. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetVisualParams)

