---
name: "llDetachFromAvatar"
category: "function"
type: "function"
language: "LSL"
description: 'Detach object from avatar.

To run this function the script must request the PERMISSION_ATTACH permission with llRequestPermissions and it must be granted by the owner.

The detached object is no longer present in the sim. There is no lsl equivilent of the 'Drop' command that moves an attachment ont'
signature: "void llDetachFromAvatar()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetachFromAvatar'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetachfromavatar"]
---

Detach object from avatar.

To run this function the script must request the PERMISSION_ATTACH permission with llRequestPermissions and it must be granted by the owner.

The detached object is no longer present in the sim. There is no lsl equivilent of the "Drop" command that moves an attachment onto the ground. Use llRezObject if you need similar behavior


## Signature

```lsl
void llDetachFromAvatar();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetachFromAvatar)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetachFromAvatar) — scraped 2026-03-18_

Detach object from avatar.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_ATTACH, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_ATTACH is granted by anyone other than the owner, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_ATTACH permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- Only works in the root prim of the attachment; calling it from a script in a child prim will cause it to fail silently.
- If the attachment was attached using llAttachToAvatarTemp, the attach() event will *not* be called because the object will be destroyed before the event gets processed.

## Examples

```lsl
default
{
    attach(key AvatarKey)
    {//give instructions for use and prevent item from being attached to avatar
        if(AvatarKey)
        {//event is called on both attach and detatch, but Key is only valid on attach
            llOwnerSay ("
            We hope you will enjoy your purchase,
            but if you really want to use this item properly, you should:
            1) drag it from your inventory to the ground
            2) Right click on it and select \"open\"
            3) copy its contents to inventory.");

            llRequestPermissions(AvatarKey, PERMISSION_ATTACH );
        }
    }
    run_time_permissions(integer perm)
    {
        if(perm & PERMISSION_ATTACH)
        {
            llDetachFromAvatar( );
        }
    }
}
```

## Notes

There is no way to delete an attachment with a script or to drop it to the ground.

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- attach

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llAttachToAvatar
- llGetAttached

### Articles

- Script permissions

<!-- /wiki-source -->
