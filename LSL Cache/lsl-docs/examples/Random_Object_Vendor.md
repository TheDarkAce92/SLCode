---
name: "Random Object Vendor"
category: "example"
type: "example"
language: "LSL"
description: "This script is a simple object vendor that gives out random items when you pay the fixed price. Just drop it in a prim, add items, and change the prices list variable to whatever price you want to sell the items. It will give out the item in a folder named like the container prim."
wiki_url: "https://wiki.secondlife.com/wiki/Random_Object_Vendor"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script is a simple object vendor that gives out random items when you pay the fixed price. Just drop it in a prim, add items, and change the prices list variable to whatever price you want to sell the items. It will give out the item in a folder named like the container prim.

```lsl
//  Random object vendor by CodeBastard Redgrave
//  Drop items in the prim containing this script
//  Pay the set price amount and it will give you a random object

//  Pieces stolen from:
//      Give inventory to whoever touches the prim, written by Sasun Steinbeck

integer price = 10;

list inventory_list()
{
    string thisScript = llGetScriptName();
    integer numberOfItems = llGetInventoryNumber(INVENTORY_ALL);

    list listToBeReturned;
    string itemName;

    integer index;
    do
    {
        itemName = llGetInventoryName(INVENTORY_ALL, index);
        if (itemName != thisScript)
            listToBeReturned += [itemName];
    }
    while (++index < numberOfItems);

    return
        listToBeReturned;
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    state_entry()
    {
        key owner = llGetOwner();

        llRequestPermissions(owner, PERMISSION_DEBIT);
        llSetPayPrice(PAY_HIDE, [price, PAY_HIDE, PAY_HIDE, PAY_HIDE]);
    }

    money(key id, integer amount)
    {
        if (amount == price)
        {
            list listOfItems = inventory_list();

            integer numberOfItems = llGetListLength(listOfItems);
            integer randomIndex = (integer)llFrand(numberOfItems);

            if (numberOfItems)
            {
                string nameOfThisPrim = llGetObjectName();
                llGiveInventoryList(id, nameOfThisPrim, [llList2String(listOfItems, randomIndex)]);
                llInstantMessage(id, "Your item is in a folder named '" + nameOfThisPrim + "'. Thank you!");
            }
            else
            {
                llInstantMessage(id, "No items to offer.");
                llGiveMoney(id, amount);
            }
        }
        else
        {
            llInstantMessage(id, "Sorry that is the wrong amount for this item.");
            llGiveMoney(id, amount);
        }
    }
}
```