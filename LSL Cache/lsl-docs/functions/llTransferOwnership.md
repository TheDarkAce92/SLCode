---
name: "llTransferOwnership"
category: "function"
type: "function"
language: "LSL"
description: "Transfer the ownership of the object to the agent, assuming it's inworld and not an attachment. - When flags = 0, ownership of the object will change in place. - When flags = TRANSFER_FLAG_TAKE, the object will go to the destination agent's inventory and derezzed from inworld. - When flags = TRANSFE"
signature: "integer llTransferOwnership(key agent, integer flags, list options)"
parameters:
  - name: "agent"
    type: "key"
    description: ""
  - name: "flags"
    type: "integer"
    description: ""
  - name: "options"
    type: "list"
    description: ""
return_type: "integer"
sleep_time: "0.0"
energy_cost: ""
wiki_url: "https://wiki.secondlife.com/wiki/llTransferOwnership"
deprecated: "false"
first_fetched: "2026-03-19"
last_updated: "2026-03-19"
---

Transfer the ownership of the object to the agent, assuming it's inworld and not an attachment. - When flags = 0, ownership of the object will change in place. - When flags = TRANSFER_FLAG_TAKE, the object will go to the destination agent's inventory and derezzed from inworld. - When flags = TRANSFER_FLAG_COPY, a copy of the object will go to the destination agent's inventory, and the original object will remain in place and owned by its original owner. Returns TRANSFER_OK on success, or one of the TRANSFER_xxxx error constants on failure.

## Signature

```lsl
integer llTransferOwnership(key agent, integer flags, list options)
```

## Parameters

| Type | Name | Description |
|------|------|-------------|
| `key` | `agent` |  |
| `integer` | `flags` |  |
| `list` | `options` |  |

## Return Value

Returns `integer`.

## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTransferOwnership)

