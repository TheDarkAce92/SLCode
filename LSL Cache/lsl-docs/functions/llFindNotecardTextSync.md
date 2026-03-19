---
name: "llFindNotecardTextSync"
category: "function"
type: "function"
language: "LSL"
description: "Finds all occurrences of the pattern in a given notecard, which must be cached. Returns the list [NAK] if the notecard was not cached, otherwise a strided list with [integer line, integer column, integer length] triplets. The count parameter specifies the maximum amount of matches to return."
signature: "list llFindNotecardTextSync(string name, string pattern, integer start, integer count, list options)"
parameters:
  - name: "name"
    type: "string"
    description: ""
  - name: "pattern"
    type: "string"
    description: ""
  - name: "start"
    type: "integer"
    description: ""
  - name: "count"
    type: "integer"
    description: ""
  - name: "options"
    type: "list"
    description: ""
return_type: "list"
sleep_time: "0.0"
energy_cost: ""
wiki_url: "https://wiki.secondlife.com/wiki/llFindNotecardTextSync"
deprecated: "false"
first_fetched: "2026-03-19"
last_updated: "2026-03-19"
---

Finds all occurrences of the pattern in a given notecard, which must be cached. Returns the list [NAK] if the notecard was not cached, otherwise a strided list with [integer line, integer column, integer length] triplets. The count parameter specifies the maximum amount of matches to return.

## Signature

```lsl
list llFindNotecardTextSync(string name, string pattern, integer start, integer count, list options)
```

## Parameters

| Type | Name | Description |
|------|------|-------------|
| `string` | `name` |  |
| `string` | `pattern` |  |
| `integer` | `start` |  |
| `integer` | `count` |  |
| `list` | `options` |  |

## Return Value

Returns `list`.

## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llFindNotecardTextSync)

