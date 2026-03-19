---
name: "llSetInventoryPermMask"
category: "function"
type: "function"
language: "LSL"
description: "Sets the given permission category to the new value on the inventory item."
signature: "void llSetInventoryPermMask(string item, integer mask, integer value)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetInventoryPermMask'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Sets the given permission category to the new value on the inventory item.


## Signature

```lsl
void llSetInventoryPermMask(string item, integer mask, integer value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `item` | an item in the inventory of the prim this script is in |
| `integer (mask)` | `category` | MASK_* flag |
| `integer (perm)` | `value` | Permission bit field (PERM_* flags) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetInventoryPermMask)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetInventoryPermMask) — scraped 2026-03-18_

Sets the given permission category to the new value on the inventory item.

## Caveats

- This function can only be executed in God Mode.
- If item is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.

## See Also

### Functions

- llGetInventoryPermMask

<!-- /wiki-source -->
