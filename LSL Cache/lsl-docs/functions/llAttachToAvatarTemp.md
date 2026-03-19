---
name: "llAttachToAvatarTemp"
category: "function"
type: "function"
language: "LSL"
description: "Follows the same convention as llAttachToAvatar, with the exception that the object will not create new inventory for the user, and will disappear on detach or disconnect. Also, this function can be used on avatars other than the owner (if granted permission) in which case the ownership is changed t"
signature: "void llAttachToAvatarTemp(integer attach_point)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llAttachToAvatarTemp'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llattachtoavatartemp"]
---

Follows the same convention as llAttachToAvatar, with the exception that the object will not create new inventory for the user, and will disappear on detach or disconnect. Also, this function can be used on avatars other than the owner (if granted permission) in which case the ownership is changed to the new wearer.

To run this function the script must request the PERMISSION_ATTACH permission with llRequestPermissions.
It should be noted that when an object is attached temporarily, a user cannot 'take' or 'drop' the object that is attached to them.

The user does not have to be the owner of the object in advance; this function transfers ownership automatically (the usual permissions required to transfer objects apply).
If attach_point is zero, then the object attaches to the attach point it was most recently attached to.


## Signature

```lsl
void llAttachToAvatarTemp(integer attach_point);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (attach_point)` | `attach_point` | ATTACH_* constant or valid value (see the tables below) |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAttachToAvatarTemp)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAttachToAvatarTemp) — scraped 2026-03-18_

Follows the same convention as llAttachToAvatar, with the exception that the object will not create new inventory for the user, and will disappear on detach or disconnect. Also, this function can be used on avatars other than the owner (if granted permission) in which case the ownership is changed to the new wearer.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_ATTACH, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_ATTACH permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- When object ownership changes, any granted permissions are reset. After a successful attach, you will need a fresh call to llRequestPermissions to allow llDetachFromAvatar and other permission-required functions to work.

  - Until successful attachment via this method, previously granted permissions are retained as normal.
- The attach step is not guaranteed to succeed, and this function should not be relied on as a security measure. Use the same permission and script precautions you would use with conventional inventory transfers.
- If you use llAttachToAvatarTemp in an object that you do not have permission to transfer, the function will fail with a script error *No permission to transfer*, even if you are trying to attach it to yourself.
- Temporary attachments cannot request the permission PERMISSION_TELEPORT, the following error will be returned: *"Temporary attachments cannot request runtime permissions to teleport"*
- Attach points can be occupied by multiple attachments.

  - This was not always the case, previously if attach_point was occupied, the existing object was detached and the new attachment took it's place.
- Objects attached to the head (and any attachment position within the head) will not be visible in First Person view (aka Mouselook) if "show attachments in mouselook" is disabled.
- If attach_point is zero but the object was never previously attached, it defaults to the right hand (ATTACH_RHAND).
- If the object is already attached the function fails silently, regardless of the attach_point being a different attach point.
- If attached via a Land Scope Experience script, the object will be force-detached by the server if the owner enters a parcel that does not have the Experience allowed.
- If the target agent is already wearing the maximum number of attachments, the object will remain on the ground with the target agent as owner. Scripters may wish to do one or more workarounds:

  - check for successful attachment and llDie() after a timeout or if the object is manipulated while unattached
  - check llGetObjectDetails(avatarKey, [OBJECT_ATTACHED_SLOTS_AVAILABLE]) beforehand, and avoid attaching if zero slots available

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
        if( vBitPermissions & PERMISSION_ATTACH )
        {
            llAttachToAvatarTemp( ATTACH_LHAND );
        }
        else
        {
            llOwnerSay( "Permission to attach denied" );
        }
    }

    on_rez(integer rez)
    {
        if(!llGetAttached())
        { //reset the script if it's not attached.
            llResetScript();
        }
    }

    attach(key AvatarKey)
    {
        if(AvatarKey)
        {//event is called on both attach and detach, but Key is only valid on attach
            integer test = llGetAttached();
            if (test) {
                llOwnerSay( "The object is attached" );
            } else {
                llOwnerSay( "The object is not attached");
            }
        }
    }
}
```

```lsl
//-- This example can demonstrate ownership transfer of an object on a temporary basis using llAttachToAvatarTemp()
//-- Whoever touches will be asked for permission to attach, and upon granting permission will have the item attach,
//-- But not appear in Inventory.
default
{
    touch_start(integer num_touches)
    {
        llRequestPermissions( llDetectedKey(0), PERMISSION_ATTACH );
    }

    run_time_permissions( integer vBitPermissions )
    {
        if( vBitPermissions & PERMISSION_ATTACH )
        {
            llAttachToAvatarTemp( ATTACH_LHAND );
        }
        else
        {
            llOwnerSay( "Permission to attach denied" );
        }
    }

    on_rez(integer rez)
    {
        if(!llGetAttached())
        { //reset the script if it's not attached.
            llResetScript();
        }
    }
}
```

```lsl
// This example illustrates how to handle permissions before and after llAttachToAvatarTemp has been called. Because ownership
// changes when the object is attached, the initial PERMISSION_ATTACH is revoked, and new permissions need to be requested.

integer gAttach = TRUE;

default
{

    touch_start(integer num)
    {
        if (gAttach)  // Object has not been attached yet
        {
            llRequestPermissions(llDetectedKey(0),PERMISSION_ATTACH);
            gAttach = FALSE;
        }
        else   // Object has been attached, but you still need PERMISSION_ATTACH in order to detach the object
        {
            if (llGetPermissions() & PERMISSION_TRIGGER_ANIMATION | PERMISSION_ATTACH)
            {
                llDetachFromAvatar();  // Note that the object vanishes when detached, so there is no need to set gAttach = TRUE again
            }
        }
    }

    attach(key id)
    {
        if (id)  // Object has been attached, so request permissions again
        {
            llRequestPermissions(id,PERMISSION_ATTACH | PERMISSION_TRIGGER_ANIMATION);
        }
    }

    run_time_permissions (integer perm)
    {
        if (!gAttach)  //First time
        {
            if (perm & PERMISSION_ATTACH)
            {
                gAttach = TRUE;
                llAttachToAvatarTemp(ATTACH_HEAD);  // Initial PERMISSION_ATTACH is revoked at this point
            }
        }
        else  // Second time
        {
            if (perm & PERMISSION_ATTACH | PERMISSION_TRIGGER_ANIMATION)
            {
                llStartAnimation(llGetInventoryName(INVENTORY_ANIMATION,0));
            }
        }
    }
}
```

An alternative solution:

```lsl
// Because ownership changes when the object is attached, the initial PERMISSION_ATTACH is revoked, and new permissions need to be requested.

default
{
    touch_start(integer num)
    {
        if (!llGetAttached()) llRequestPermissions( llDetectedKey(0), PERMISSION_ATTACH);
        else if ( llGetPermissions() & PERMISSION_ATTACH) llDetachFromAvatar();
    }
    attach(key id)
    {
        if (id) llRequestPermissions( id, PERMISSION_ATTACH | PERMISSION_TRIGGER_ANIMATION);
    }
    run_time_permissions (integer perm)
    {
        if (!llGetAttached() && (perm & PERMISSION_ATTACH)) llAttachToAvatarTemp( ATTACH_NOSE);
        if (perm & PERMISSION_TRIGGER_ANIMATION) llStartAnimation( llGetInventoryName( INVENTORY_ANIMATION, 0));
    }
}
```

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llDetachFromAvatar** — Detaches the object from the avatar
- **llGetAttached** — Gets the attach point number

### Articles

- Script permissions

<!-- /wiki-source -->
