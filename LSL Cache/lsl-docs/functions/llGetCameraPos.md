---
name: "llGetCameraPos"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the current camera position for the agent the task has permissions for."
signature: "vector llGetCameraPos()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetCameraPos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetcamerapos"]
---

Returns a vector that is the current camera position for the agent the task has permissions for.


## Signature

```lsl
vector llGetCameraPos();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetCameraPos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetCameraPos) — scraped 2026-03-18_

Returns a vector that is the current camera position for the agent the task has permissions for.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TRACK_CAMERA, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_TRACK_CAMERA permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- Seems to act weird when the camera gets too far from the agent.

## Examples

```lsl
//Camera Follower Script
//llGetCameraPos & llGetCameraRot Example
//By Nika Rugani

integer perm_track = 0x400;
float second_check = 0.1;

vector object_offset = <2,0,0>; //Offset of the cameras position where the object will set itself

integer die_channel = 0;
string die_command = "/die";

quickPosRot(vector pos, rotation rot)
{//This way you don't have the 0.2 second sleeps from llSetPos and llSetRot
    llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_POSITION, pos, PRIM_ROTATION, rot]);
}

default
{
    on_rez(integer a)
    {
        llResetScript();
    }
    state_entry()
    {
        llRequestPermissions(llGetOwner(), perm_track);
    }
    run_time_permissions(integer permission)
    {
        if(permission == perm_track)
        {
            llSetTimerEvent(second_check);
            llListen(die_channel, "", llGetOwner(), "");
        }
        else
        {
            //llResetScript(); //Remove comment to loop the process of requesting permissions if user deny's permission
            //llDie(); //Remove comment to kill the object if user deny's it
        }
    }
    listen(integer channel, string name, key id, string str)
    {
        str = llToLower(str);
        if(str == die_command)
        {
            llDie();
        }
    }
    timer()
    {
        vector c_pos = llGetCameraPos(); //Get Users Camera Position
        rotation c_rot = llGetCameraRot(); //Get Users Camera Rotation
        c_pos = (c_pos+object_offset*c_rot); //Apply the offset to the position
        quickPosRot(c_pos, c_rot); //EXECUTE ORDER!
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
- llGetCameraRot
- llSetCameraParams
- llSetCameraAtOffset
- llSetCameraEyeOffset

### Articles

- Script permissions

<!-- /wiki-source -->
