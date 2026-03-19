---
name: "llSetCameraParams"
category: "function"
type: "function"
language: "LSL"
description: 'Sets multiple camera parameters at once.

To run this function the script must request the PERMISSION_CONTROL_CAMERA permission with llRequestPermissions.'
signature: "void llSetCameraParams(list rules)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetCameraParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetcameraparams"]
---

Sets multiple camera parameters at once.

To run this function the script must request the PERMISSION_CONTROL_CAMERA permission with llRequestPermissions.


## Signature

```lsl
void llSetCameraParams(list rules);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list (instructions)` | `rules` | Format is [ rule1, data1, rule2, data2 . . . rulen, datan ] |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetCameraParams)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetCameraParams) — scraped 2026-03-18_

Sets multiple camera parameters at once.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_CONTROL_CAMERA, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - The PERMISSION_CONTROL_CAMERA permission is automatically revoked when the avatar stands up from or detaches the object, and any scripted camera parameters are automatically cleared. |

- Camera control currently (server 1.38) only supported for attachments and objects on which you are sitting. An attempt otherwise will result in an error being shouted on DEBUG_CHANNEL.
- Scripted camera parameters are overriden for agents who are in Free Camera mode *(Alt + Click)*. **No error is returned if this is the case**; however when the agent returns to regular camera mode, their camera will go to the scripted camera position.
- When CAMERA_FOCUS is not defined, it is advised that CAMERA_FOCUS_THRESHOLD is set to 0.0 - this is because when left at it's default value, it may prevent the camera from focusing on the correct point, instead focusing just to the side of the intended point.
- A CAMERA_FOCUS_OFFSET of ZERO_VECTOR will always look at the same position as returned by llGetPos() for the avatar

  - When seated, this is also the position of "Avatar Center" when hover height is 0
  - When standing, this has a shape-dependent z-offset from "Avatar Center". (currently investigating Tapple Gao (talk))
- Cannot be used to control the camera in Mouselook.

## Examples

You can either set the camera in region relative coordinates or you can make the camera follow your avatar.

**Region relative coordinates, an example:**

```lsl
lookAtMe( integer perms )
{
    if ( perms & PERMISSION_CONTROL_CAMERA )
    {
        vector camPos = llGetPos() + (relCamP * llGetRot() * turnOnChair) ;
        vector camFocus = llGetPos() ;
        llClearCameraParams(); // reset camera to default
        llSetCameraParams([
            CAMERA_ACTIVE, 1, // 1 is active, 0 is inactive
            CAMERA_FOCUS, camFocus, // region relative position
            CAMERA_FOCUS_LOCKED, TRUE, // (TRUE or FALSE)
            CAMERA_POSITION, camPos, // region relative position
            CAMERA_POSITION_LOCKED, TRUE // (TRUE or FALSE)
        ]);
    }
}
```

Note that Focus and Position are both locked. This first example makes the camera look at *camFocus* from *camPos*.

**Camera follow avatar, an example:**

```lsl
lookAtMe( integer perms )
{
    if ( perms & PERMISSION_CONTROL_CAMERA )
    {
        llClearCameraParams(); // reset camera to default
        llSetCameraParams([
            CAMERA_ACTIVE, 1, // 1 is active, 0 is inactive
            CAMERA_BEHINDNESS_ANGLE, 30.0, // (0 to 180) degrees
            CAMERA_BEHINDNESS_LAG, 0.0, // (0 to 3) seconds
            CAMERA_DISTANCE, 10.0, // ( 0.5 to 10) meters
          //CAMERA_FOCUS, <0,0,5>, // region relative position
            CAMERA_FOCUS_LAG, 0.05 , // (0 to 3) seconds
            CAMERA_FOCUS_LOCKED, FALSE, // (TRUE or FALSE)
            CAMERA_FOCUS_THRESHOLD, 0.0, // (0 to 4) meters
            CAMERA_PITCH, 10.0, // (-45 to 80) degrees
          //CAMERA_POSITION, <0,0,0>, // region relative position
            CAMERA_POSITION_LAG, 0.0, // (0 to 3) seconds
            CAMERA_POSITION_LOCKED, FALSE, // (TRUE or FALSE)
            CAMERA_POSITION_THRESHOLD, 0.0, // (0 to 4) meters
            CAMERA_FOCUS_OFFSET, <2.0, 0.0, 0.0> // <-10,-10,-10> to <10,10,10> meters
        ]);
    }
}
```

Note that in this second example Focus and Position are NOT locked and not even set. This is appropriate for making the camera follow a pilot on a vehicle.

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llClearCameraParams
- llGetCameraPos
- llGetCameraRot
- llSetLinkCamera
- llSetCameraEyeOffset
- llSetCameraAtOffset

### Articles

- Script permissions
- FollowCam

<!-- /wiki-source -->
