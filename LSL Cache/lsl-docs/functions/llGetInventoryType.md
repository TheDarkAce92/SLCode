---
name: "llGetInventoryType"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the type of the inventory item name

If name does not exist, INVENTORY_NONE is returned (no errors or messages are generated), making this function ideal for testing the existence of a certain item in inventory.'
signature: "integer llGetInventoryType(string name)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryType'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetinventorytype"]
---

Returns an integer that is the type of the inventory item name

If name does not exist, INVENTORY_NONE is returned (no errors or messages are generated), making this function ideal for testing the existence of a certain item in inventory.


## Signature

```lsl
integer llGetInventoryType(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | name of an inventory item |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryType)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryType) — scraped 2026-03-18_

Returns an integer that is the type of the inventory item name

## Examples

```lsl
string get_type_info(integer inputInteger)
{
    if (inputInteger == INVENTORY_TEXTURE)
        return "INVENTORY_TEXTURE";

    else if (inputInteger == INVENTORY_SOUND)
        return "INVENTORY_SOUND";

    else if (inputInteger == INVENTORY_LANDMARK)
        return "INVENTORY_LANDMARK";

    else if (inputInteger == INVENTORY_CLOTHING)
        return "INVENTORY_CLOTHING";

    else if (inputInteger == INVENTORY_OBJECT)
        return "INVENTORY_OBJECT";

    else if (inputInteger == INVENTORY_NOTECARD)
        return "INVENTORY_NOTECARD";

    else if (inputInteger == INVENTORY_SCRIPT)
        return "INVENTORY_SCRIPT";

    else if (inputInteger == INVENTORY_BODYPART)
        return "INVENTORY_BODYPART";

    else if (inputInteger == INVENTORY_ANIMATION)
        return "INVENTORY_ANIMATION";

    else if (inputInteger == INVENTORY_GESTURE)
        return "INVENTORY_GESTURE";

    else if (inputInteger == INVENTORY_SETTING)
        return "INVENTORY_SETTING";

    else
        return "inventory type unknown";
}

default
{
    touch_start(integer num_detected)
    {
        integer totalItems = llGetInventoryNumber(INVENTORY_ALL);

        integer index;
        while (index < totalItems)
        {
            string itemName = llGetInventoryName(INVENTORY_ALL, index);
            integer type = llGetInventoryType(itemName);

            // PUBLIC_CHANNEL has the integer value 0
            llSay(PUBLIC_CHANNEL,
                "'" + itemName + "' (" + get_type_info(type) + ")");

            ++index;
        }
    }
}
```

## See Also

### Functions

- **llGetInventoryAcquireTime** — Returns the time the item was added to the prim's inventory
- **llGetInventoryName** — Returns the inventory item's name
- **llGetInventoryNumber** — Returns the number of items of a specific type in inventory
- **llGetInventoryCreator** — Returns the inventory item's creator
- **llGetInventoryPermMask** — Returns the inventory item's permissions
- **llGetInventoryKey** — UUID

<!-- /wiki-source -->
