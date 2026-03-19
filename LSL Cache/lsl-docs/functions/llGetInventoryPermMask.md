---
name: "llGetInventoryPermMask"
category: "function"
type: "function"
language: "LSL"
description: "Returns a bit field (an integer) of the requested permission category for the inventory item"
signature: "integer llGetInventoryPermMask(string item, integer mask)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetInventoryPermMask'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetinventorypermmask"]
---

Returns a bit field (an integer) of the requested permission category for the inventory item


## Signature

```lsl
integer llGetInventoryPermMask(string item, integer mask);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `item` | an item in the inventory of the prim this script is in |
| `integer` | `category` | MASK_* flag |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryPermMask)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetInventoryPermMask) — scraped 2026-03-18_

Returns a bit field (an integer) of the requested permission category for the inventory item

## Caveats

- If item is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.
- Note that including the MASK_COMBINED bit does not impact the output of this function, as the combined permissions are the only accessible permissions for inventory items.

## Examples

```lsl
if ((permsYouHave & permsYouWant) == permsYouWant)
    llSay(PUBLIC_CHANNEL, "You have the perms you want.");
else
    llSay(PUBLIC_CHANNEL, "You don't have the perms you want.");
```

```lsl
integer ownerPerms = llGetInventoryPermMask("inventory item name goes here", MASK_OWNER);
integer copyAndModPerms = PERM_COPY | PERM_MODIFY;

if ((ownerPerms & copyAndModPerms) == copyAndModPerms)
    llSay(PUBLIC_CHANNEL, "Owner has copy & modify perms.");
else
    llSay(PUBLIC_CHANNEL, "Owner does not have copy & modify perms.");
```

```lsl
string getPermsAsReadableString(integer perm)
{
    integer fullPerms = PERM_COPY | PERM_MODIFY | PERM_TRANSFER;
    integer copyModPerms = PERM_COPY | PERM_MODIFY;
    integer copyTransPerms = PERM_COPY | PERM_TRANSFER;
    integer modTransPerms = PERM_MODIFY | PERM_TRANSFER;

    string output = " perms: ";

    if ((perm & fullPerms) == fullPerms)
        output += "full";
    else if ((perm & copyModPerms) == copyModPerms)
        output += "copy & modify";
    else if ((perm & copyTransPerms) == copyTransPerms)
        output += "copy & transfer";
    else if ((perm & modTransPerms) == modTransPerms)
        output += "modify & transfer";
    else if ((perm & PERM_COPY) == PERM_COPY)
        output += "copy";
    else if ((perm & PERM_TRANSFER) == PERM_TRANSFER)
        output += "transfer";
    else
        output += "none";

    //  Remember, items in Second Life must have either
    //  PERM_COPY or PERM_TRANSFER when "talking about"
    //  owner perms or perms for next owner.

    return  output;
}

default
{
    state_entry()
    {
        string inventoryItemName = "inventory item name goes here";

        integer basePerms      = llGetInventoryPermMask(inventoryItemName, MASK_BASE);
        integer ownerPerms     = llGetInventoryPermMask(inventoryItemName, MASK_OWNER);
        integer nextOwnerPerms = llGetInventoryPermMask(inventoryItemName, MASK_NEXT);
        integer groupPerms     = llGetInventoryPermMask(inventoryItemName, MASK_GROUP);
        integer everyonePerms  = llGetInventoryPermMask(inventoryItemName, MASK_EVERYONE);

        llSay(0, "/me [" + inventoryItemName
            + "]: base" + getPermsAsReadableString(basePerms));
        llSay(0, "/me [" + inventoryItemName
            + "]: owner" + getPermsAsReadableString(ownerPerms));
        llSay(0, "/me [" + inventoryItemName
            + "]: next owner" + getPermsAsReadableString(nextOwnerPerms));
        llSay(0, "/me [" + inventoryItemName
            + "]: group" + getPermsAsReadableString(groupPerms));
        llSay(0, "/me [" + inventoryItemName
            + "]: everyone" + getPermsAsReadableString(everyonePerms));
    }
}
```

To test for the opposite (e.g. to see if something is NOT copy):

```lsl
    if (!(PERM_COPY & llGetInventoryPermMask(myitem, MASK_OWNER)))
        llSay(PUBLIC_CHANNEL, "/me [" + myitem + "]: owner doesn't have copy perms.");
```

To remind the next owner what permissions to set before selling on
choose which need to be set;

```lsl
CheckPerms()
{
    string item = llGetScriptName();
    integer nextOwnerPerms = llGetInventoryPermMask(item, MASK_NEXT);

    if(PERM_COPY & nextOwnerPerms)
        llOwnerSay("Set no copy");

    if(PERM_MODIFY & nextOwnerPerms)
        llOwnerSay("Set no mod");

    if(PERM_TRANSFER & nextOwnerPerms)
        llOwnerSay("Set no transfer");
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        if(llGetOwner() != llGetInventoryCreator(llGetScriptName()))
            CheckPerms();
    }
}
```

## Notes

- In effect, the perms for articles published on this Wiki are PERM_COPY and PERM_TRANSFER until you log in, then PERM_MODIFY, PERM_MOVE, PERM_COPY and PERM_TRANSFER.
- The default perms of a newly created script are: Base = PERM_ALL, Owner = PERM_ALL, Next = PERM_MOVE or PERM_TRANSFER, Group = 0 (none), Everyone = 0 (none). These perms are the same, no matter if the script is created in user inventory or in an object.

  - However, an option in the *Preferences > Advanced* menu allows to set the **Default Creation Permissions** of all items that can be created or uploaded in-world.

## See Also

### Functions

- llGetObjectPermMask
- **llGetInventoryAcquireTime** — Returns the time the item was added to the prim's inventory
- **llGetInventoryName** — Returns the inventory item's name
- **llGetInventoryType** — Tests to see if an inventory item exists and returns its type
- **llGetInventoryNumber** — Returns the number of items of a specific type in inventory
- **llGetInventoryKey** — UUID
- **llGetInventoryCreator** — Returns the inventory item's creator

### Articles

- hex

<!-- /wiki-source -->
