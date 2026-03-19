---
name: "llFindNotecardTextCount"
category: "function"
type: "function"
language: "LSL"
description: "Counts the number of occurrences of the pattern (a regular expression) in the given notecard, returning the result through a dataserver event. Returns NULL_KEY if the regexp or the notecard were not valid, or the query ID for the dataserver event. The data parameter of the dataserver will contain a "
signature: "key llFindNotecardTextCount(string name, string pattern, list options)"
parameters:
  - name: "name"
    type: "string"
    description: ""
  - name: "pattern"
    type: "string"
    description: ""
  - name: "options"
    type: "list"
    description: ""
return_type: "key"
sleep_time: "0.0"
energy_cost: ""
wiki_url: "https://wiki.secondlife.com/wiki/llFindNotecardTextCount"
deprecated: "false"
first_fetched: "2026-03-19"
last_updated: "2026-03-19"
---

Counts the number of occurrences of the pattern (a regular expression) in the given notecard, returning the result through a dataserver event. Returns NULL_KEY if the regexp or the notecard were not valid, or the query ID for the dataserver event. The data parameter of the dataserver will contain a string representing an integer, which is the number of occurrences.

## Signature

```lsl
key llFindNotecardTextCount(string name, string pattern, list options)
```

## Parameters

| Type | Name | Description |
|------|------|-------------|
| `string` | `name` |  |
| `string` | `pattern` |  |
| `list` | `options` |  |

## Return Value

Returns `key`.

## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llFindNotecardTextCount)

