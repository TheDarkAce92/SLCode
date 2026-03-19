---
name: "llGetInventoryNumber"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the number of items of a given type in the prims inventory."
signature: "integer llGetInventoryNumber(integer type)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryNumber'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetinventorynumber"]
---

Returns an integer that is the number of items of a given type in the prims inventory.


## Signature

```lsl
integer llGetInventoryNumber(integer type);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `type` | INVENTORY_* flag |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryNumber)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryNumber) — scraped 2026-03-18_

Returns an integer that is the number of items of a given type in the prims inventory.

## Examples

```lsl
//                             Item Counter
//                       By Apollia Pirandello
//                              9/19/2007
//
// Public domain.  Free to use and/or modify for any purpose,
// including commercial purposes.
//
// Once you drop this script in any prim, it will immediately
// tell you in an OwnerSay how many items are in that prim,
// minus 1, so the script itself isn't counted.
//
// It will also do that whenever the prim is touched.
//**SCRIPT BEGINS BELOW**

//VARIABLE

integer items_contained;

//END OF VARIABLE SECTION
//FUNCTIONS

CountItems()
{
  items_contained = llGetInventoryNumber( INVENTORY_ALL );
  --items_contained; //minus 1, the script itself isn't counted, since its used with the INVENTORY_ALL flag
}

SayCount()
{
  llOwnerSay( "This prim contains " + (string)items_contained + " items." );
}

//END OF FUNCTIONS
//DEFAULT STATE

default
{
  state_entry()
  {
    CountItems();
    SayCount();
  }

  touch_start(integer total_number)
  {
    CountItems();
    SayCount();
  }
}
```

```lsl
objects = llGetInventoryNumber(INVENTORY_OBJECT);
```

```lsl
// Inventory Statistic By Zep Palen.
// Here is another use of llGetInventoryNumber to show a statistic in a hovertext
// For this script to work you must add a showlist and an excludelist to the Description of the item this script is in.
// The description field must be filled like follows: [showlist];[Excludelist]
// Example: 0,1,3,5,6,7,10,13,20,21;3,7,10
// in the example all types are shown, but only types 3,7 and 10 are counted as total. You can see in the 2 lists below which number means which type
// -----------------
// This script is free to use and modify as you wish - Zep Palen
// --------------------------

list inv_types = [0, 1, 3, 5, 6, 7, 10, 13, 20, 21];
list inv_names = ["Textures", "Sounds", "Landmarks", "Clothings", "Objects", "Notecards", "Scripts", "Bodyparts", "Animations", "Gestures"];

processCountInventory()
{
    list objDesc = llParseString2List(llGetObjectDesc(), [";"], []);
    list showList = llParseString2List(llList2String(objDesc, 0), [","], []);
    list excludeFromCount = llParseString2List(llList2String(objDesc, 1), [","], []);

    string counted = "ITEM COUNTER";
    integer i = ~llGetListLength(showList);
    while (++i)
    {
        integer showItem = (integer)llList2String(showList, i);
        integer sIndex = llListFindList(inv_types, [showItem]);
        if (~sIndex)
            counted += "\n" + llList2String(inv_names, sIndex) + ": " + (string)llGetInventoryNumber(showItem);
    }
    integer totalCount = llGetInventoryNumber(INVENTORY_ALL);
    for (i = ~llGetListLength(excludeFromCount); ++i;)
    {
        integer exclItem = (integer)llList2String(excludeFromCount, i);
        integer cIndex = llListFindList(inv_types, [(string)exclItem]);
        if (~cIndex)
            totalCount = totalCount - llGetInventoryNumber(exclItem);
    }

    counted += "\n \n" + "Total: " + (string)totalCount;
    llSetText(counted, <1,1,0>, 1);
}

default
{
    state_entry()
    {
        processCountInventory();
    }

    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
        {
            processCountInventory();
        }
    }
}
```

## See Also

### Functions

- **llGetInventoryAcquireTime** — Returns the time the item was added to the prim's inventory
- **llGetInventoryName** — Returns the inventory item's name
- **llGetInventoryType** — Tests to see if an inventory item exists and returns its type.
- **llGetInventoryCreator** — Returns the inventory item's creator
- **llGetInventoryPermMask** — Returns the inventory item's permissions
- **llGetInventoryKey** — UUID

<!-- /wiki-source -->
