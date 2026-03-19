---
name: "llGetInventoryCreator"
category: "function"
type: "function"
language: "LSL"
description: "Returns a key of the creator of the inventory item."
signature: "key llGetInventoryCreator(string item)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryCreator'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetinventorycreator"]
---

Returns a key of the creator of the inventory item.


## Signature

```lsl
key llGetInventoryCreator(string item);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `item` | an item in the inventory of the prim this script is in |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryCreator)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryCreator) — scraped 2026-03-18_

Returns a key of the creator of the inventory item.

## Caveats

- If item is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.
- If item has multiple creators, then this function will return NULL_KEY. (e.g. if an object created by Lex contained a script created by Strife). See [SVC-6985](https://jira.secondlife.com/browse/SVC-6985) and [SVC-6820](https://jira.secondlife.com/browse/SVC-6820) for more information.

## Examples

Add an object to a prims inventory, as well as this script, in order to get the name of the creator.

```lsl
default{
    state_entry(){
        llRequestAgentData(llGetInventoryCreator(llGetInventoryName( INVENTORY_OBJECT, 0)),DATA_NAME);
    }

    dataserver(key qid, string data){
        llOwnerSay(data);
    }
}
```

## See Also

### Functions

- **llGetInventoryAcquireTime** — Returns the time the item was added to the prim's inventory
- **llGetInventoryName** — Returns the inventory item's name
- **llGetInventoryType** — Tests to see if an inventory item exists and returns its type
- **llGetInventoryNumber** — Returns the number of items of a specific type in inventory
- **llGetInventoryPermMask** — Returns the inventory item's permissions
- **llGetInventoryKey** — UUID

<!-- /wiki-source -->
