---
name: "llWorldPosToHUD"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector position in HUD frame that would place the center of the HUD object directly over world_pos as viewed by the current camera.

To run this function the script must request the PERMISSION_TRACK_CAMERA permission with llRequestPermissions.'
signature: "vector llWorldPosToHUD(vector pos)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llWorldPosToHUD'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a vector position in HUD frame that would place the center of the HUD object directly over world_pos as viewed by the current camera.

To run this function the script must request the PERMISSION_TRACK_CAMERA permission with llRequestPermissions.


## Signature

```lsl
vector llWorldPosToHUD(vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `world_pos` |  |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llWorldPosToHUD)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llWorldPosToHUD) — scraped 2026-03-18_

Returns a vector position in HUD frame that would place the center of the HUD object directly over world_pos as viewed by the current camera.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TRACK_CAMERA, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_TRACK_CAMERA permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |
Only works for HUD attachments.  The vector's X component will be 1.0 when **world_pos** is in front of camera and -1.0 when it is behind.  Returns zero vector when no permissions have been granted.

## Examples

```lsl
// llWorldPosToHUD() example
//
// Put this script on a HUD attachment (which attachment point doesn't matter).
// Touch to toggle 'tracking' on/off.
// Put an object at world_pos as reference for where the HUD should move when 'tracking'.

vector not_tracking_color = <1.0, 1.0, 1.0>; // white
vector tracking_front_color = <0.5, 0.0, 0.5>; // magenta
vector tracking_behind_color = <0.0, 0.5, 0.5>; // cyan

vector world_pos = <32,32,24>; // change this position as necessary, put a ref object here
integer tracking = FALSE;

default
{
    state_entry()
    {
        llOwnerSay("Touch HUD to toggle tracking");
        llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
        llSetAlpha(0.5, ALL_SIDES); // make object semi transparent
        llSetColor(not_tracking_color, ALL_SIDES);
    }

    touch_start(integer total_number)
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
        tracking = !tracking;
        if (tracking)
        {
            llSetTimerEvent(0.01);
            llSetColor(tracking_front_color, ALL_SIDES);
        }
        else
        {
            llSetTimerEvent(0.0);
            llSetPos(<0,0,0>);
            llSetColor(not_tracking_color, ALL_SIDES);
        }
    }

    attach(key id)
    {
        if (id != NULL_KEY)
        {
            llSetPos(<0,0,0>);
            tracking = FALSE;
            llSetTimerEvent(0.0);
        }
    }

    timer()
    {
        integer attachment_point = llGetAttached();
        if (attachment_point >= ATTACH_HUD_CENTER_2 && attachment_point <= ATTACH_HUD_BOTTOM_RIGHT)
        {
            vector hud_pos = llWorldPosToHUD(world_pos);
            if (hud_pos.x > 0.0)
            {
                // world-pos is in front of camera
                llSetColor(tracking_front_color, ALL_SIDES);
            }
            else
            {
                // world_pos is behind camera
                llSetColor(tracking_behind_color, ALL_SIDES);
            }
            // update HUD position
            llSetPos(hud_pos);
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
- llGetCameraFOV
- llGetCameraPos
- llGetCameraRot

### Articles

- Script permissions

<!-- /wiki-source -->
