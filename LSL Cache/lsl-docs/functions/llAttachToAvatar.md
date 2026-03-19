---
name: "llAttachToAvatar"
category: "function"
type: "function"
language: "LSL"
description: 'Attaches the object to the avatar who has granted permission to the script. The object is taken into the users inventory and attached to attach_point.

To run this function the script must request the PERMISSION_ATTACH permission with llRequestPermissions and it must be granted by the owner.
If atta'
signature: "void llAttachToAvatar(integer attach_point)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAttachToAvatar'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llattachtoavatar"]
---

Attaches the object to the avatar who has granted permission to the script. The object is taken into the users inventory and attached to attach_point.

To run this function the script must request the PERMISSION_ATTACH permission with llRequestPermissions and it must be granted by the owner.
If attach_point is zero, then the object attaches to the attach point it was most recently attached to.


## Signature

```lsl
void llAttachToAvatar(integer attach_point);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (attach_point)` | `attach_point` | ATTACH_* constant or valid value (see the tables below) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAttachToAvatar)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAttachToAvatar) — scraped 2026-03-18_

Attaches the object to the avatar who has granted permission to the script. The object is taken into the users inventory and attached to attach_point.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_ATTACH, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_ATTACH is granted by anyone other than the owner, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_ATTACH permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- Attach points can be occupied by multiple attachments.

  - This was not always the case, previously if attach_point was occupied, the existing object was detached and the new attachment took it's place.
- Objects attached to the head (and any attachment position within the head) will not be visible in First Person view (aka Mouselook) if "show attachments in mouselook" is disable.
- If attach_point is zero but the object was never previously attached, it defaults to the right hand (ATTACH_RHAND).
- If the object is already attached the function fails silently, regardless if the attach_point is a different attach point. -- SCR-137

## Examples

```lsl
//-- rez object on ground, drop in this script, it will request permissions to attach,
//-- and then attach to the left hand if permission is granted. if permission is denied,
//-- then the script complains.
default
{
    state_entry()
    {
        llRequestPermissions( llGetOwner(), PERMISSION_ATTACH );
    }

    run_time_permissions( integer vBitPermissions )
    {
        if ( vBitPermissions & PERMISSION_ATTACH )
            llAttachToAvatar( ATTACH_LHAND );
        else
            llOwnerSay( "Permission to attach denied" );
    }

    on_rez(integer rez)
    {
        if (!llGetAttached() )        //reset the script if it's not attached.
            llResetScript();
    }

    attach(key id)
    {
        // The attach event is called on both attach and detach, but 'id' is only valid on attach
        if (id)
            llOwnerSay( "The object is attached to " + llKey2Name(id) );
        else
            llOwnerSay( "The object is not attached");
    }
}
```

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- attach

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llAttachToAvatarTemp** — Attach an object to any avatar but only temporarily
- **llDetachFromAvatar** — Detaches the object from the avatar
- **llGetAttached** — Gets the attach point number (that the object is attached to)

### Articles

- Script permissions

<!-- /wiki-source -->
