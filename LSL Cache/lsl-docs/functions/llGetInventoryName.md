---
name: "llGetInventoryName"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the name of the inventory item number of type. Returns an empty string if no item of the specified type is found in the prim's inventory (or there are less than or equal to number items of the type).

number does not support negative indexes.
Inventory items are sorted in al'
signature: "string llGetInventoryName(integer type, integer number)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetinventoryname"]
---

Returns a string that is the name of the inventory item number of type. Returns an empty string if no item of the specified type is found in the prim's inventory (or there are less than or equal to number items of the type).

number does not support negative indexes.
Inventory items are sorted in alphabetical order (not chronological order).


## Signature

```lsl
string llGetInventoryName(integer type, integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `type` | INVENTORY_* flag |
| `integer` | `number` | Beginning from 0 |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryName) — scraped 2026-03-18_

Returns a string that is the name of the inventory item number of type. Returns an empty string if no item of the specified type is found in the prim's inventory (or there are less than or equal to number items of the type).

## Caveats

- If number is out of bounds  the script continues to execute without an error message.

## Examples

Box Unpacker

```lsl
// Give all prim contents to anyone touching this object,
// But don't give this script itself.

default
{
    touch_start(integer num_detected)
    {
        list    InventoryList;
        integer count = llGetInventoryNumber(INVENTORY_ALL);  // Count of all items in prim's contents
        string  ItemName;
        while (count--)
        {
            ItemName = llGetInventoryName(INVENTORY_ALL, count);
            if (ItemName != llGetScriptName() )
                InventoryList += ItemName;   // add all contents except this script, to a list
        }
        // Give all the items to the toucher, in a folder named as per this prim's name
        llGiveInventoryList(llDetectedKey(0), llGetObjectName(), InventoryList);
    }
}
```

## Notes

The maximum number of characters for an object inventory item is currently 63 characters.

## See Also

### Functions

- **llGetInventoryAcquireTime** — Returns the time the item was added to the prim's inventory
- **llGetInventoryNumber** — Returns the number of items of a specific type in inventory
- **llGetInventoryType** — Tests to see if an inventory item exists and returns its type.
- **llGetInventoryCreator** — Returns the inventory item's creator
- **llGetInventoryPermMask** — Returns the inventory item's permissions
- **llGetInventoryKey** — UUID

<!-- /wiki-source -->
