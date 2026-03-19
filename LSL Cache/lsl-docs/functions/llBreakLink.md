---
name: "llBreakLink"
category: "function"
type: "function"
language: "LSL"
description: 'Delinks the prim with the given link number in a linked object set

To run this function the script must request the PERMISSION_CHANGE_LINKS permission with llRequestPermissions and it must be granted by the owner.'
signature: "void llBreakLink(integer linknum)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llBreakLink'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llbreaklink"]
---

Delinks the prim with the given link number in a linked object set

To run this function the script must request the PERMISSION_CHANGE_LINKS permission with llRequestPermissions and it must be granted by the owner.


## Signature

```lsl
void llBreakLink(integer linknum);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llBreakLink)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llBreakLink) — scraped 2026-03-18_

Delinks the prim with the given link number in a linked object set

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_CHANGE_LINKS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_CHANGE_LINKS is granted by anyone other than the owner, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_CHANGE_LINKS permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- This function removes sitting avatars from the object, even if not sitting on the unlinked prim.
- This function silently fails if called from a script inside an attachment.
- This function fails if the owner does not have edit permissions on the object containing the script, the system message "*Delink failed because you do not have edit permission*" is received by the owner.
- A prim with PERMISSION_CHANGE_LINKS can delink any prim in the linked object set even itself or the root
- The only LINK_* flag that link currently supports is LINK_ROOT. SVC-3510

  - Use llGetLinkNumber() as the parameter to unlink the script's prim, not LINK_THIS.
  - Use llBreakAllLinks() instead of using LINK_SET, LINK_ALL_CHILDREN, or LINK_ALL_OTHERS as the parameter for llBreakLink.

## Examples

```lsl
//-- requests permission to change links, then breaks the link
//-- between the prim and the rest of the object, on touch.
default
{
    touch_start(integer vIntTouched)
    {
        llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_CHANGE_LINKS)
        {
            llBreakLink(llGetLinkNumber());
        }
    }
}
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- **changed** — CHANGED_LINK

### Functions

- **llGetLinkNumber** — prim
- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llBreakAllLinks** — Break all links
- **llCreateLink** — Link to another object

### Articles

- Script permissions

<!-- /wiki-source -->
