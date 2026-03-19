---
name: "Give random object"
category: "example"
type: "example"
language: "LSL"
description: "Place this in an object with a big inventory (well, doesn't have to have LOTS in it) and touch to receive a random object."
wiki_url: "https://wiki.secondlife.com/wiki/Give_random_object"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Yes, the random object giver

Place this in an object with a big inventory (well, doesn't have to have LOTS in it) and touch to receive a random object.

```lsl
//Emmas Seetan

default
{
    touch_start(integer num_detected)
    {
    //  the key of the avatar touching
        key id = llDetectedKey(0);

        integer randomIndex = llGetInventoryNumber(INVENTORY_OBJECT);
    //  random >> [0.0, max)
        randomIndex = (integer)llFrand(randomIndex);

        string itemName = llGetInventoryName(INVENTORY_OBJECT, randomIndex);

        llGiveInventory(id, itemName);
    }
}
```