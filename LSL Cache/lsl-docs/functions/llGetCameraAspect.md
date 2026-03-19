---
name: "llGetCameraAspect"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float value for the current camera's aspect ratio (e.g. width/height) of the agent for which the task has permissions."
signature: "float llGetCameraAspect()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetCameraAspect'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a float value for the current camera's aspect ratio (e.g. width/height) of the agent for which the task has permissions.


## Signature

```lsl
float llGetCameraAspect();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetCameraAspect)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetCameraAspect) — scraped 2026-03-18_

Returns a float value for the current camera's aspect ratio (e.g. width/height) of the agent for which the task has permissions.

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

```lsl
// Scale an object to fit the aspect ratio of the viewer.
fit_to_screen()
{
    // The X axis from the left to  the right edge of the screen is 0.0 to width value.
    // The Y axis is always 1.
    float x = llGetCameraAspect();
    float y = 1;
    llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_SIZE, <0, x, y>]);
}
```

## Notes

The reported aspect ratio is based on values provided by the viewer to the simulator. This may cause visual oddities if there's a discrepancy between the viewer's reported camera and what the viewer actually displays to the user. For example: entering mouselook may cause portions of the viewer interface to disappear, which alters the amount of space available to the HUD, which can lead to misaligned positioning or slightly-off aspect ratio. (This is currently considered a viewer-bug.)

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llGetCameraFOV
- llGetCameraPos
- llGetCameraRot
- llSetCameraParams
- llSetCameraAtOffset
- llSetCameraEyeOffset

### Articles

- Script permissions

<!-- /wiki-source -->
