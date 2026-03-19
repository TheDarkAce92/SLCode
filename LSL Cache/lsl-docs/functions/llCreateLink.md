---
name: "llCreateLink"
category: "function"
type: "function"
language: "LSL"
description: 'Attempt to link the script's object with target.

To run this function the script must request the PERMISSION_CHANGE_LINKS permission with llRequestPermissions and it must be granted by the owner.
target must be modifiable and have the same owner.
This object must also be modifiable.'
signature: "void llCreateLink(key target, integer parent)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCreateLink'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcreatelink"]
---

Attempt to link the script's object with target.

To run this function the script must request the PERMISSION_CHANGE_LINKS permission with llRequestPermissions and it must be granted by the owner.
target must be modifiable and have the same owner.
This object must also be modifiable.


## Signature

```lsl
void llCreateLink(key target, integer parent);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | prim UUID that is in the same region |
| `integer` | `parent` | If FALSE, then target becomes the root. If TRUE, then the script's object becomes the root. |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCreateLink)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCreateLink) — scraped 2026-03-18_

Attempt to link the script's object with target.

## Caveats

- This function causes the script to sleep for 0.1 seconds.

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_CHANGE_LINKS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_CHANGE_LINKS is granted by anyone other than the owner, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_CHANGE_LINKS permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- If target is not in the region, not a prim, or is attached to an avatar, an error is shouted on DEBUG_CHANNEL.
- If either the object or the target are not modifiable or of different owners, then an error is shouted on DEBUG_CHANNEL.
- If the the parent object and target are too far apart they will fail to link.

  - The maximum distance is further explained here: Linkability Rules
- This function silently fails if called from a script inside an attachment.

## Examples

```lsl
// Rez an object and link it as a child prim.
string ObjectName = "Object Name Here";
// NOTE: must be a name of an object in this object's inventory.

default
{
    touch_start(integer count)
    {
        // When the object is touched, make sure we can do this before trying.
        llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
    }
    run_time_permissions(integer perm)
    {
        // Only bother rezzing the object if will be able to link it.
        if (perm & PERMISSION_CHANGE_LINKS)
            llRezObject(ObjectName, llGetPos() + <0,0,0.5>, ZERO_VECTOR, llGetRot(), 0);
        else
            llOwnerSay("Sorry, we can't link.");
    }
    object_rez(key id)
    {
        // NOTE: under some conditions, this could fail to work.
        // This is the parent object.  Create a link to the newly-created child.
        llCreateLink(id, TRUE);
    }
}
```

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- **changed** — CHANGED_LINK

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llBreakLink** — Break a link
- **llBreakAllLinks** — Break all links

### Articles

- Script permissions
- Linkability Rules

<!-- /wiki-source -->
