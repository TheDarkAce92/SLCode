---
name: "llGetInventoryAcquireTime"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string with the timestamp that the item was added to the prim's inventory.

The time is in the UTC time zone in the format 'YYYY-MM-DDThh:mm:ssZ'

Appears to be accurate to seconds.'
signature: "string llGetInventoryAcquireTime(string item)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryAcquireTime'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a string with the timestamp that the item was added to the prim's inventory.

The time is in the UTC time zone in the format "YYYY-MM-DDThh:mm:ssZ"

Appears to be accurate to seconds.


## Signature

```lsl
string llGetInventoryAcquireTime(string item);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `item` | an item in the inventory of the prim this script is in |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryAcquireTime)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryAcquireTime) — scraped 2026-03-18_

Returns a string with the timestamp that the item was added to the prim's inventory.

## Caveats

- If item is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.
- This function currently returns an ISO timestamp that is missing milliseconds. It is recommended that you code your applications in preparation of millisecond support being added at a later date.
- Using llListSort to sort a list of timestamps that both include and exclude milliseconds will have undesired results. ".000000" will first have to be inserted into timestamps missing milliseconds.
- Changing the contents of a script or notecard (or recompiling a script) does not change its acquire time.

## Examples

If there is no other item in the inventory, you get the timestamp from the script itself.

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }

    touch_start(integer total_number)
    {
        string item = llGetInventoryName(INVENTORY_ALL, 0); // 0 means the first item in prim's inventory.
        string timestamp = llGetInventoryAcquireTime(item);

        llSay(0, "Timestamp for: " + item + " - " + timestamp); // output
    }
}
```

## See Also

### Functions

- **llGetTimestamp** — Returns the current timestamp using the same format
- **llGetInventoryCreator** — Returns the inventory item's creator
- **llGetInventoryName** — Returns the inventory item's name
- **llGetInventoryType** — Tests to see if an inventory item exists and returns its type
- **llGetInventoryNumber** — Returns the number of items of a specific type in inventory
- **llGetInventoryPermMask** — Returns the inventory item's permissions
- **llGetInventoryKey** — UUID

<!-- /wiki-source -->
