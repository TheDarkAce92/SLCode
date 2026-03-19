---
name: "llGiveAgentInventory"
category: "function"
type: "function"
language: "LSL"
description: "Give the specified items to the destination agent in a folder. If a folder with that name already exists, a new one will still be created. If the options specify a root path, that root path will be created if it does not exists, but it won't be recreated if it exists. Returns TRANSFER_OK on success,"
signature: "integer llGiveAgentInventory(key agent, string folder, list items, list options)"
parameters:
  - name: "agent"
    type: "key"
    description: ""
  - name: "folder"
    type: "string"
    description: ""
  - name: "items"
    type: "list"
    description: ""
  - name: "options"
    type: "list"
    description: ""
return_type: "integer"
sleep_time: "0.0"
energy_cost: ""
wiki_url: "https://wiki.secondlife.com/wiki/llGiveAgentInventory"
deprecated: "false"
first_fetched: "2026-03-19"
last_updated: "2026-03-19"
---

Give the specified items to the destination agent in a folder. If a folder with that name already exists, a new one will still be created. If the options specify a root path, that root path will be created if it does not exists, but it won't be recreated if it exists. Returns TRANSFER_OK on success, or one of the TRANSFER_xxxx error constants on failure.

## Signature

```lsl
integer llGiveAgentInventory(key agent, string folder, list items, list options)
```

## Parameters

| Type | Name | Description |
|------|------|-------------|
| `key` | `agent` |  |
| `string` | `folder` |  |
| `list` | `items` |  |
| `list` | `options` |  |

## Return Value

Returns `integer`.

## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGiveAgentInventory)

