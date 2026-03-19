---
name: "llGetPermissions"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer bitfield with the script permissions granted"
signature: "integer llGetPermissions()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetPermissions'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetpermissions"]
---

Returns an integer bitfield with the script permissions granted


## Signature

```lsl
integer llGetPermissions();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetPermissions)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetPermissions) — scraped 2026-03-18_

Returns an integer bitfield with the script permissions granted

## Examples

```lsl
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(),
        //Comment out any of the following lines for fun
            PERMISSION_DEBIT |
            PERMISSION_TAKE_CONTROLS |
            PERMISSION_TRIGGER_ANIMATION |
            PERMISSION_ATTACH |
            PERMISSION_CHANGE_LINKS |
            PERMISSION_TRACK_CAMERA |
            PERMISSION_CONTROL_CAMERA |
            0);
    }
    touch_start(integer a)
    {
        integer perm = llGetPermissions();
        if(perm & PERMISSION_DEBIT)
            llOwnerSay("Can use llGiveMoney");
        if(perm & PERMISSION_TAKE_CONTROLS)
            llOwnerSay("Can use llTakeControls");
        if(perm & PERMISSION_TRIGGER_ANIMATION)
            llOwnerSay("Can use llStartAnimation");
        if(perm & PERMISSION_ATTACH)
            llOwnerSay("Can use llAttachToAvatar");
        if(perm & PERMISSION_CHANGE_LINKS)
            llOwnerSay("Can use llCreateLink");
        if(perm & PERMISSION_TRACK_CAMERA)
            llOwnerSay("Can use llGetCameraPos");
        if(perm & PERMISSION_CONTROL_CAMERA)
            llOwnerSay("Can use llSetCameraParams");
    }
    run_time_permissions(integer perm)
    {
        if(perm & PERMISSION_DEBIT)
            llOwnerSay("Can use llGiveMoney");
        if(perm & PERMISSION_TAKE_CONTROLS)
            llOwnerSay("Can use llTakeControlls");
        if(perm & PERMISSION_TRIGGER_ANIMATION)
            llOwnerSay("Can use llStartAnimation");
        if(perm & PERMISSION_ATTACH)
            llOwnerSay("Can use llAttachToAvatar");
        if(perm & PERMISSION_CHANGE_LINKS)
            llOwnerSay("Can use llCreateLink");
        if(perm & PERMISSION_TRACK_CAMERA)
            llOwnerSay("Can use llGetCameraPos");
        if(perm & PERMISSION_CONTROL_CAMERA)
            llOwnerSay("Can use llSetCameraParams");
    }
}
```

## See Also

### Events

- **run_time_permissions** — Permission receiver event

### Functions

- **llGetPermissionsKey** — Get the avatar who granted permissions.
- **llRequestPermissions** — Request permissions

<!-- /wiki-source -->
