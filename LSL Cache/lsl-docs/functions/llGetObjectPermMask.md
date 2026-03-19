---
name: "llGetObjectPermMask"
category: "function"
type: "function"
language: "LSL"
description: "Returns a bit field (an integer) of the requested permission category for the object containing this script."
signature: "integer llGetObjectPermMask(integer mask)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectPermMask'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetobjectpermmask"]
---

Returns a bit field (an integer) of the requested permission category for the object containing this script.


## Signature

```lsl
integer llGetObjectPermMask(integer mask);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `category` | MASK_* flag |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectPermMask)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectPermMask) — scraped 2026-03-18_

Returns a bit field (an integer) of the requested permission category for the object containing this script.

## Examples

```lsl
if ((permsYouHave & permsYouWant) == permsYouWant)
    llSay(0, "You have the perms you want.");
else
    llSay(0, "You don't have the perms you want.");
```

```lsl
integer ownerPerms = llGetObjectPermMask(MASK_OWNER);
integer copyAndModPerms = PERM_COPY | PERM_MODIFY;

if ((ownerPerms & copyAndModPerms) == copyAndModPerms)
    llSay(0, "Owner has copy & modify perms.");
else
    llSay(0, "Owner does not have copy & modify perms.");
```

```lsl
string getPermsAsReadableString(integer perm)
{
    integer allPerms = PERM_ALL;
    integer fullPerms = PERM_COPY | PERM_MODIFY | PERM_TRANSFER;

    integer copyModMovePerms = PERM_COPY | PERM_MODIFY | PERM_MOVE;
    integer copyModPerms = PERM_COPY | PERM_MODIFY;

    integer copyTransMovePerms = PERM_COPY | PERM_TRANSFER | PERM_MOVE;
    integer copyTransPerms = PERM_COPY | PERM_TRANSFER;

    integer modTransMovePerms = PERM_MODIFY | PERM_TRANSFER | PERM_MOVE;
    integer modTransPerms = PERM_MODIFY | PERM_TRANSFER;

    integer copyMovePerms = PERM_COPY | PERM_MOVE;

    integer transMovePerms = PERM_TRANSFER | PERM_MOVE;

    string output = " perms: ";

    if ((perm & allPerms) == allPerms)
        output += "full and move";
    else if ((perm & fullPerms) == fullPerms)
        output += "full";
    else if ((perm & copyModMovePerms) == copyModMovePerms)
        output += "copy & modify & move";
    else if ((perm & copyModPerms) == copyModPerms)
        output += "copy & modify";
    else if ((perm & copyTransMovePerms) == copyTransMovePerms)
        output += "copy & transfer & move";
    else if ((perm & copyTransPerms) == copyTransPerms)
        output += "copy & transfer";
    else if ((perm & modTransMovePerms) == modTransMovePerms)
        output += "modify & transfer & move";
    else if ((perm & modTransPerms) == modTransPerms)
        output += "modify & transfer";
    else if ((perm & copyMovePerms) == copyMovePerms)
        output += "copy & move";
    else if ((perm & PERM_COPY) == PERM_COPY)
        output += "copy";
    else if ((perm & transMovePerms) == transMovePerms)
        output += "transfer & move";
    else if ((perm & PERM_TRANSFER) == PERM_TRANSFER)
        output += "transfer";
    else if ((perm & PERM_MOVE) == PERM_MOVE)
        output += "move";
    else
        output += "none";

    //  Remember, items in Second Life must have either
    //  PERM_COPY or PERM_TRANSFER when "talking about"
    //  owner perms or perms for next owner.

    return
        output;
}
default
{
    state_entry()
    {
        integer basePerms      = llGetObjectPermMask(MASK_BASE);
        integer ownerPerms     = llGetObjectPermMask(MASK_OWNER);
        integer nextOwnerPerms = llGetObjectPermMask(MASK_NEXT);
        integer groupPerms     = llGetObjectPermMask(MASK_GROUP);
        integer everyonePerms  = llGetObjectPermMask(MASK_EVERYONE);

        llSay(0, "base"       + getPermsAsReadableString(basePerms));
        llSay(0, "owner"      + getPermsAsReadableString(ownerPerms));
        llSay(0, "next owner" + getPermsAsReadableString(nextOwnerPerms));
        llSay(0, "group"      + getPermsAsReadableString(groupPerms));
        llSay(0, "everyone"   + getPermsAsReadableString(everyonePerms));
    }
}
```

```lsl
integer isLocked()
{
    return !(llGetObjectPermMask(MASK_OWNER) & PERM_MOVE);
}
```

## Notes

The perms of a newly created object are often:

```lsl
 Base = PERM_ALL
 Owner = PERM_ALL
 Next = PERM_MOVE or PERM_TRANSFER
 Group = 0 (none)
 Everyone = 0 (none)
```

## See Also

### Functions

- llGetInventoryPermMask

### Articles

- hex

<!-- /wiki-source -->
