---
name: "llGiveInventoryList"
category: "function"
type: "function"
language: "LSL"
description: "Gives inventory items to target, creating a new folder to put them in."
signature: "void llGiveInventoryList(key target, string folder, list inventory)"
return_type: "void"
sleep_time: "3.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGiveInventoryList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgiveinventorylist"]
---

Gives inventory items to target, creating a new folder to put them in.


## Signature

```lsl
void llGiveInventoryList(key target, string folder, list inventory);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | avatar or prim UUID that is in the same region |
| `string` | `folder` | folder name to use |
| `list` | `inventory` | a list of items in the inventory of the prim this script is in |


## Caveats

- Forced delay: **3.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGiveInventoryList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGiveInventoryList) — scraped 2026-03-18_

Gives inventory items to target, creating a new folder to put them in.

## Caveats

- This function causes the script to sleep for 3.0 seconds.
- If **target** is not the owner nor shares the same owner,  and **inventory** does not have transfer permissions, an error is shouted on DEBUG_CHANNEL.
- If **inventory** permissions do not allow copy, the transfer fails and an error is shouted on DEBUG_CHANNEL.
- If **target** is a prim that is not in the same region an error is shouted on DEBUG_CHANNEL.
- When scripts are copied or moved between inventories, their state does not survive the transfer. Memory, event queue and execution position are all discarded.
- If inventory is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.

## Examples

```lsl
default
{
    touch_start(integer n)
    {
        key toucher = llDetectedKey(0);
        string folder = "Item Folder";
        list inventory = ["item", "another item"];
        llGiveInventoryList(toucher, folder, inventory);
    }
}
```

```lsl
//  when the prim is touched, the script checks all other inventory items whether or not they're copiable
//  copiable items are added to a list, if the list is not empty when all items have been checked
//  the prim gives them to the touching avatar within a single folder

default
{
    touch_start(integer num_detected)
    {
        string thisScript = llGetScriptName();
        list inventoryItems;
        integer inventoryNumber = llGetInventoryNumber(INVENTORY_ALL);

        integer index;
        for ( ; index < inventoryNumber; ++index )
        {
            string itemName = llGetInventoryName(INVENTORY_ALL, index);

            if (itemName != thisScript)
            {
                if (llGetInventoryPermMask(itemName, MASK_OWNER) & PERM_COPY)
                {
                    inventoryItems += itemName;
                }
                else
                {
                    llSay(0, "Unable to copy the item named '" + itemName + "'.");
                }
            }
        }

        if (inventoryItems == [] )
        {
            llSay(0, "No copiable items found, sorry.");
        }
        else
        {
            llGiveInventoryList(llDetectedKey(0), llGetObjectName(), inventoryItems);    // 3.0 seconds delay
        }
    }
}
```

```lsl
//  script gives items to owner only
//  all copiable items are given within a single folder
//  all no-copy items are transferred separately (only one time, right? right!)

default
{
    touch_start(integer num_detected)
    {
        key owner = llGetOwner();
        if (llDetectedKey(0) != owner)
            return;

        list inventoryItems;
        integer inventoryNumber = llGetInventoryNumber(INVENTORY_ALL);

        integer index;
        for ( ; index < inventoryNumber; ++index )
        {
            string itemName = llGetInventoryName(INVENTORY_ALL, index);
            if (itemName != llGetScriptName() )
            {
                if (llGetInventoryPermMask(itemName, MASK_OWNER) & PERM_COPY)
                {
                    inventoryItems += itemName;
                }
                else
                {
                    llGiveInventory(owner, itemName);    // 2.0 seconds delay
                }
            }
        }

        if (inventoryItems != [] )
            llGiveInventoryList(owner, llGetObjectName(), inventoryItems);    // 3.0 seconds delay
    }
}
```

## See Also

### Events

- changed

### Functions

- llGiveInventory
- llGiveAgentInventory

<!-- /wiki-source -->
