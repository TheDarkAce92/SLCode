---
name: "llTakeControls"
category: "function"
type: "function"
language: "LSL"
description: 'Allows for intercepting of keyboard and mouse clicks, specifically those specified by controls, from the agent the script has permissions for.

To run this function the script must request the PERMISSION_TAKE_CONTROLS permission with llRequestPermissions.
If accept is FALSE and pass_on is FALSE, the'
signature: "void llTakeControls(integer controls, integer accept, integer pass_on)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTakeControls'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltakecontrols"]
---

Allows for intercepting of keyboard and mouse clicks, specifically those specified by controls, from the agent the script has permissions for.

To run this function the script must request the PERMISSION_TAKE_CONTROLS permission with llRequestPermissions.
If accept is FALSE and pass_on is FALSE, the behavior is not intuitive. In this case, the complement of the specified controls do not generate events and do not perform their normal functions. They are effectively disabled. Certain control bits (e.g. CONTROL_ROT_LEFT) are also disabled when specified, in this case.
If accept is FALSE and pass_on is TRUE, then the specified controls do not generate events but perform their normal functions.
If accept is TRUE and pass_on is FALSE, then the specified controls generate events but do not perform their normal functions.
If accept is TRUE and pass_on is TRUE, then the specified controls generate events and perform their normal functions.


## Signature

```lsl
void llTakeControls(integer controls, integer accept, integer pass_on);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `controls` | bitfield of CONTROL_* flags |
| `integer (boolean)` | `accept` | boolean, determines whether control events are generated |
| `integer (boolean)` | `pass_on` | boolean, determines whether controls perform their normal functions |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTakeControls)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTakeControls) — scraped 2026-03-18_

Allows for intercepting of keyboard and mouse clicks, specifically those specified by controls, from the agent the script has permissions for.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TAKE_CONTROLS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_TAKE_CONTROLS permission is granted, it can be revoked from inside the script (with llReleaseControls or a new llRequestPermissions call), or if the user chooses Release Keys from the viewer. The script will also lose this permission on reset, or if the object is deleted, detached, or dropped. |

- There appears to be no penalty for using accept = TRUE, pass_on = TRUE when there is no control event in the script (such as is used in AO's to ensure they work on no-script land)

  - There is a bug in some permissions that prevents left clicks from working in mouselook if they are set to accept = FALSE, pass_on = TRUE
- If you sit/are sitting on the object that has taken your controls using accept = TRUE and pass_on = TRUE, then CONTROL_FWD, CONTROL_BACK, CONTROL_ROT_LEFT, and CONTROL_ROT_RIGHT will never generate events; instead these controls will only perform their normal functions.
- if the undocumented controls 0x02000000 or 0x04000000 are taken with pass_on = FALSE, then llGetAnimation will never be "Turning Left" or "Turning Right", respectively, and those animations set by llSetAnimationOverride will never play

  - all control flags documented in [libopenmetaverse](https://github.com/openmetaversefoundation/libopenmetaverse/blob/master/OpenMetaverse/AgentManagerMovement.cs#L42) [secondlife viewer](https://github.com/secondlife/viewer/blob/c7053a6928fd5eafdc935453742e92951ae4e0c1/indra/llcommon/indra_constants.h#L255)
- If your viewer's 'Single click on land' setting is set to 'Move to clicked point', then CONTROL_LBUTTON might not be sent to the server when taken by llTakeControls().

## Examples

```lsl
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);
    }
    run_time_permissions(integer perm)
    {
        if(PERMISSION_TAKE_CONTROLS & perm)
        {
            llTakeControls(
                            CONTROL_FWD |
                            CONTROL_BACK |
                            CONTROL_LEFT |
                            CONTROL_RIGHT |
                            CONTROL_ROT_LEFT |
                            CONTROL_ROT_RIGHT |
                            CONTROL_UP |
                            CONTROL_DOWN |
                            CONTROL_LBUTTON |
                            CONTROL_ML_LBUTTON ,
                            TRUE, TRUE);

        }
    }
    control(key id, integer level, integer edge)
    {
        integer start = level & edge;
        integer end = ~level & edge;
        integer held = level & ~edge;
        integer untouched = ~(level | edge);
        llOwnerSay(llList2CSV([level, edge, start, end, held, untouched]));
    }
}
```

## Notes

If a script has taken controls, it and other scripts in the same prim will not be stopped if the Agent enters a "No Outside Scripts" parcel. This is done to keep vehicle control alive and AOs functional. This is an intentional feature. This only applies to the object containing the script - child objects in a linkset (wheels, particle emitters, in vehicles, child objects in huds, etc) will not inherit this immunity. To preserve functionality in child objects, llTakeControls must be issued in each scripted child as well.

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- control

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llReleaseControls

### Articles

- Script permissions

<!-- /wiki-source -->
