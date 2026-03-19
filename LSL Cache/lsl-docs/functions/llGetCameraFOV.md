---
name: "llGetCameraFOV"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float value for the current camera's field of view (FOV), in radians, of the agent for which the task has permissions."
signature: "float llGetCameraFOV()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetCameraFOV'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a float value for the current camera's field of view (FOV), in radians, of the agent for which the task has permissions.


## Signature

```lsl
float llGetCameraFOV();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetCameraFOV)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetCameraFOV) — scraped 2026-03-18_

Returns a float value for the current camera's field of view (FOV), in radians, of the agent for which the task has permissions.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TRACK_CAMERA, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_TRACK_CAMERA permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |
Returns zero when permissions have not been granted.

## Examples

```lsl
// say the camera aspect ratio and field of view (FOV)
integer has_perms = FALSE;
default
{
    on_rez(integer a)
    {
        llResetScript();
        has_perms = FALSE;
    }
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
    }
    run_time_permissions(integer permission)
    {
        has_perms = (permission == PERMISSION_TRACK_CAMERA);
    }
    touch_start(integer num_touches)
    {
        if (has_perms)
        {
            float aspect = llGetCameraAspect();
            float fov = llGetCameraFOV();
            llOwnerSay("aspect = " + (string)aspect + "  FOV = " + (string)fov);
        }
        else
        {
            llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
        }
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
- llGetCameraAspect
- llGetCameraPos
- llGetCameraRot
- llSetCameraParams
- llSetCameraAtOffset
- llSetCameraEyeOffset

### Articles

- Script permissions

<!-- /wiki-source -->
