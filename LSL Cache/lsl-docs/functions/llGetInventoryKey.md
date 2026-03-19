---
name: "llGetInventoryKey"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a key that is the UUID of the inventory name

If name is not copy, mod, trans then the return is NULL_KEY.
Use llGetInventoryType instead of this function to verify the existence of inventory.'
signature: "key llGetInventoryKey(string name)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryKey'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetinventorykey"]
---

Returns a key that is the UUID of the inventory name

If name is not copy, mod, trans then the return is NULL_KEY.
Use llGetInventoryType instead of this function to verify the existence of inventory.


## Signature

```lsl
key llGetInventoryKey(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | an item in the inventory of the prim this script is in |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryKey)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryKey) — scraped 2026-03-18_

Returns a key that is the UUID of the inventory name

## Caveats

- Inventory items are records that usually *point* to assets, but they are not the actual assets.

  - Multiple inventory items can point to the same asset and return the same key.
  - Some newly created inventory entries get default keys until they are edited and saved:

  - Newly created notecard entries use NULL_KEY at present, until they are edited and saved.
  - Newly created script entries point to the "Hello Avatar" script ("d0d40b7c-e32b-3bcb-3346-2be8470093c0" at this writing, not a guaranteed default) until they are edited and saved.
  - Most other inventory entries are given unique asset keys at creation time.
  - When an asset is "edited" a new asset key is assigned to the edit. The inventory item used to open the asset for editing is updated with the new asset key.

  - No other inventory items that share the original asset are updated with the new asset key.

## Examples

```lsl
// Put this script in an empty prim, and drag a full-perm texture into the prim's contents to find out its UUID
default
{
    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)    // if there has been a change to the prim's contents ...
        {
            string name = llGetInventoryName(INVENTORY_TEXTURE, 0);
            if (name)        // if a texture exists ...
            {
                key uuid = llGetInventoryKey(name);
                if (uuid)    // if the uuid is valid ...
                    llOwnerSay( "The UUID of '" + name + "' is " + (string) uuid);
                else         // texture was not full-perm
                    llOwnerSay( "The UUID of '" + name + "' could not be determined");
            }
        }
    }
}
```

```lsl
string item = "Default";

default
{
    state_entry()
    {
        llOwnerSay("Touch to get information about \"" + item + "\".");
    }

    touch_start(integer total_number)
    {
        integer type = llGetInventoryType(item);
        integer index = llListFindList([ INVENTORY_NONE,
            INVENTORY_TEXTURE, INVENTORY_SOUND, INVENTORY_LANDMARK, INVENTORY_CLOTHING,
            INVENTORY_OBJECT, INVENTORY_NOTECARD, INVENTORY_SCRIPT, INVENTORY_BODYPART,
            INVENTORY_ANIMATION, INVENTORY_GESTURE], [type]);
        string name = llList2String(["does not exist",
            "texture", "sound", "landmark", "clothing",
            "object", "notecard", "script", "body part",
            "animation", "gesture"], index);

        llOwnerSay("Type: " + name);

        if(type == INVENTORY_NONE)
            return;

        integer owner_perms = llGetInventoryPermMask(item, MASK_OWNER);
        list perms;
        if(owner_perms & PERM_COPY)
            perms += "Copy";

        if(owner_perms & PERM_MODIFY)
            perms += "Modify";

        if(owner_perms & PERM_TRANSFER)
            perms += "Transfer";

        if(owner_perms & PERM_MOVE)
            perms += "Move";

        llOwnerSay("Perms: " + llList2CSV(perms));

        integer temp = PERM_COPY | PERM_MODIFY | PERM_TRANSFER;
        if((owner_perms & temp) != temp)
            return;

        llOwnerSay("Key: " + (string)llGetInventoryKey(item));
    }
}
```

## Notes

- The UUID returned is that of the asset to which the inventory item points, it is not the UUID of the inventory item itself. The assets themselves are immutable (they never change, they are only ever created and deleted); this allows multiple inventory handles to refer to the same asset without having to duplicate the asset. When it appears an asset is being modified, it is saved as a new asset. The consequence of this is that multiple copies of items in inventory all share the same asset UUID.
- It is still possible to inspect the UUID of any animation in inventory by triggering it and using llGetAnimationList() like so:

```lsl
llStartAnimation("myAnim");
llOwnerSay("myAnim's UUID is " + llList2String(llGetAnimationList(llGetPermissionsKey()), -1));
```

## See Also

### Functions

- **llGetInventoryAcquireTime** — Returns the time the item was added to the prim's inventory
- **llGetInventoryName** — Returns the inventory item's name
- **llGetInventoryType** — Tests to see if an inventory item exists and returns its type
- **llGetInventoryNumber** — Returns the number of items of a specific type in inventory
- **llGetInventoryPermMask** — Returns the inventory item's permissions
- **llGetInventoryCreator** — Returns the inventory item's creator

<!-- /wiki-source -->
