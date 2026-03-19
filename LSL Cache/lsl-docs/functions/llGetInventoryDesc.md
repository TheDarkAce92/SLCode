---
name: "llGetInventoryDesc"
category: "function"
type: "function"
language: "LSL"
description: "Returns the description of the item named itemname which is in the contents of the prim the script is in. If itemname does not exist in the prim's inventory, an error is shouted in DEBUG_CHANNEL and the result is an empty string."
signature: "string llGetInventoryDesc(string itemname)"
parameters:
  - name: "itemname"
    type: "string"
    description: ""
return_type: "string"
sleep_time: "0.0"
energy_cost: ""
wiki_url: "https://wiki.secondlife.com/wiki/llGetInventoryDesc"
deprecated: "false"
first_fetched: "2026-03-19"
last_updated: "2026-03-19"
---

Returns the description of the item named itemname which is in the contents of the prim the script is in. If itemname does not exist in the prim's inventory, an error is shouted in DEBUG_CHANNEL and the result is an empty string.

## Signature

```lsl
string llGetInventoryDesc(string itemname)
```

## Parameters

| Type | Name | Description |
|------|------|-------------|
| `string` | `itemname` |  |

## Return Value

Returns `string`.

## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryDesc)

