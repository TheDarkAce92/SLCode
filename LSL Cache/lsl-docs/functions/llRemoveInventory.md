---
name: "llRemoveInventory"
category: "function"
type: "function"
language: "LSL"
description: "Remove the named inventory item"
signature: "void llRemoveInventory(string item)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRemoveInventory'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llremoveinventory"]
---

Remove the named inventory item


## Signature

```lsl
void llRemoveInventory(string item);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `item` | an item in the inventory of the prim this script is in |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRemoveInventory)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRemoveInventory) — scraped 2026-03-18_

Remove the named inventory item

## Caveats

- If item is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.
- If the current script is removed it will continue to run for a short period of time after this call.
- With multiple executions an llSleep(0.1) after llRemoveInventory will allow edit window contents to refresh correctly and avoid errors on phantom contents.
- llRemoveInventory will not trigger a changed event.

## Examples

```lsl
// Remove the current script from the object

default
{
    state_entry()
    {
        llRemoveInventory(llGetScriptName());
    }
}
```

```lsl
// user-function to include in your script
// deletes all other contents of any type except the script itself
delete_all_other_contents()
{
    string thisScript = llGetScriptName();
    string inventoryItemName;

    integer index = llGetInventoryNumber(INVENTORY_ALL);
    while (index)
    {
        --index;        // (faster than index--;)

        inventoryItemName = llGetInventoryName(INVENTORY_ALL, index);

        if (inventoryItemName != thisScript)
            llRemoveInventory(inventoryItemName);
    }
}

default
{
    state_entry()
    {
        delete_all_other_contents();
    }
}
```

<!-- /wiki-source -->
