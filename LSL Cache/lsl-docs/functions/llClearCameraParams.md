---
name: "llClearCameraParams"
category: "function"
type: "function"
language: "LSL"
description: 'Resets all camera parameters to default values and turns off scripted camera control.

To run this function the script must request the PERMISSION_CONTROL_CAMERA permission with llRequestPermissions.'
signature: "void llClearCameraParams()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llClearCameraParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llclearcameraparams"]
---

Resets all camera parameters to default values and turns off scripted camera control.

To run this function the script must request the PERMISSION_CONTROL_CAMERA permission with llRequestPermissions.


## Signature

```lsl
void llClearCameraParams();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llClearCameraParams)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llClearCameraParams) — scraped 2026-03-18_

Resets all camera parameters to default values and turns off scripted camera control.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_CONTROL_CAMERA, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - The PERMISSION_CONTROL_CAMERA permission is automatically revoked when the avatar stands up from or detaches the object, and any scripted camera parameters are automatically cleared. |

## Examples

```lsl
integer gEnabled;

askForPermissions()
{
    llRequestPermissions(llGetOwner(), PERMISSION_CONTROL_CAMERA);
}

default
{

    on_rez(integer sp)
    {
        llResetScript();
    }

    state_entry()
    {
        askForPermissions();
    }

    touch_start(integer total_number)
    {

        if (llDetectedKey(0) != llGetOwner())
        {
            return;
        }
        else if (!llGetPermissions() & PERMISSION_CONTROL_CAMERA)
        {
            llOwnerSay("I need permissions to control your camera.");
            askForPermissions();
            return;
        }

        gEnabled = !gEnabled;
        if (gEnabled)
        {
            llOwnerSay("Enabled.");
            llSetCameraParams([
                CAMERA_ACTIVE, 1,
                CAMERA_DISTANCE, 50.0
            ]);
        }
        else
        {
            llOwnerSay("Disabled.");
            llClearCameraParams();
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
- llSetCameraParams

### Articles

- Script permissions

<!-- /wiki-source -->
