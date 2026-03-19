---
name: "llGetPermissionsKey"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the avatar (a key) of the avatar that last granted or declined permissions to the script.

Returns NULL_KEY if permissions were neither granted nor declined (e.g., the permissions dialog was cancelled or otherwise ignored).'
signature: "key llGetPermissionsKey()"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetPermissionsKey'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetpermissionskey"]
---

Returns the avatar (a key) of the avatar that last granted or declined permissions to the script.

Returns NULL_KEY if permissions were neither granted nor declined (e.g., the permissions dialog was cancelled or otherwise ignored).


## Signature

```lsl
key llGetPermissionsKey();
```


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetPermissionsKey)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetPermissionsKey) — scraped 2026-03-18_

Returns the avatar (a key) of the avatar that last granted or declined permissions to the script.

## Examples

```lsl
// 1. rez a cube
// 2. create a new script and paste this
// 3. save script
// 4. right-click the prim and choose attach
// 5. touch the prim

announce_permissions_key()
{
    key permissionsKey = llGetPermissionsKey();

    llSay(0, "key llGetPermissionsKey() = '" + (string)permissionsKey + "'");
}

default
{
    state_entry()
    {
        announce_permissions_key();

        key owner = llGetOwner();
        llRequestPermissions(owner, PERMISSION_ATTACH);
    }

    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);
        key owner = llGetOwner();
        key permissionsKey = llGetPermissionsKey();

        if (id == owner)
        {
            if (permissionsKey == owner)
                llDetachFromAvatar();
            else
                llSay(0, "Can't detach from you, you have not granted ATTACH perms.");
        }
        else
            llSay(0, "Sorry, you're not the owner!");
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_ATTACH)
            announce_permissions_key();
    }
}
```

## See Also

### Events

- run_time_permissions

### Functions

- llGetPermissions
- llRequestPermissions

<!-- /wiki-source -->
