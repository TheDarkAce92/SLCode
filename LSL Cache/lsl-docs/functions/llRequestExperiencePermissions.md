---
name: "llRequestExperiencePermissions"
category: "function"
type: "function"
language: "LSL"
description: 'Asks the agent for permission to participate in the script's Experience.

This request is similar to llRequestPermissions with all the following permissions: PERMISSION_TAKE_CONTROLS, PERMISSION_TRIGGER_ANIMATION, PERMISSION_ATTACH, PERMISSION_TRACK_CAMERA, PERMISSION_CONTROL_CAMERA and PERMISSION_T'
signature: "void llRequestExperiencePermissions(key agent, string name)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestExperiencePermissions'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llrequestexperiencepermissions"]
---

Asks the agent for permission to participate in the script's Experience.

This request is similar to llRequestPermissions with all the following permissions: PERMISSION_TAKE_CONTROLS, PERMISSION_TRIGGER_ANIMATION, PERMISSION_ATTACH, PERMISSION_TRACK_CAMERA, PERMISSION_CONTROL_CAMERA and PERMISSION_TELEPORT. However, unlike llRequestPermissions, the decision to allow or block the request is persistent and applies to all scripts using the experience grid-wide.

Subsequent calls to llRequestExperiencePermissions from scripts in the experience will receive the same response automatically with no user interaction.

Either experience_permissions or experience_permissions_denied will be generated in response to this call. If no response is given by the agent, the request will time out after at least 5 minutes. Multiple requests by the same script can be made during this time out though the script can only have permission for one agent at a time.

Agents in god mode will always see the permission dialog even if the experience has been previously approved.

Outstanding permission requests will be lost if the script is de-rezzed, moved to another region, or reset.

For this function to work, the script must be compiled into an Experience.


## Signature

```lsl
void llRequestExperiencePermissions(key agent, string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent` | Key of the agent to request permissions from |
| `string` | `name` | Deprecated, no longer used |


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestExperiencePermissions)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestExperiencePermissions) — scraped 2026-03-18_

Asks the agent for permission to participate in the script's Experience.

## Caveats

- If you recompile a script that was previously associated with an Experience but do so with a client that lacks the ability to compile scripts into an experience the script will lose the associated Experience.

## Examples

This is a shell for a HUD Dispenser.  It detects an avatar by the collision event, then rezzes an object that will request experience permissions and attach to the avatar:

```lsl
default
{
    state_entry()
    {
        llVolumeDetect(TRUE);
    }

    collision_start(integer NumberOfCollisions)
    {
        integer i = 0;
        for(; i < NumberOfCollisions; i++)
        {
            integer channel = llRound(llFrand(-1000));
            key give_to = llDetectedKey(i);
            llSay(0, "Rezzing HUD for " + (string)give_to + " using channel " + (string)channel);
            llRezObject(llGetInventoryName(INVENTORY_OBJECT, 0), llGetPos(), ZERO_VECTOR, ZERO_ROTATION, channel);
            llRegionSay(channel, "ATTACH|" + (string)give_to);
        }
    }
}
```

This script is for the object that is rezzed.  It requests experience permissions and then attaches itself to the avatar.   It must check for various failures such as denied permissions and failure to attach, and deletes itself when there is an error.

```lsl
// Example script for LSL Experience Tools attachment

// This script runs on an object that is rezzed in-world which gets
// an Experience permissions and then attaches to an AV.

integer listener;
integer msg_channel;

integer log_spam_channel = 0;       // Change this or remove llSay() commands

default
{
    on_rez(integer start_parameter)
    {   // Start listening for a message from rezzer
        msg_channel = start_parameter;
        llSay(log_spam_channel, "Test HUD has been rezzed");
        listener = llListen(start_parameter, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string text)
    {   // Listen for the message from the rezzer with the target agent key
        if (channel == msg_channel)
        {   // Ask for the experience permission
            list msg = llParseString2List(text, ["|"], []);
            llSay(log_spam_channel, "Trying experience permissions request to " + llList2String(msg, 1));
            llRequestExperiencePermissions((key)llList2String(msg, 1), "");
            llListenRemove(listener);
            llSetTimerEvent(60.0);
        }
    }

    experience_permissions(key target_id)
    {   // Permissions granted, so attach to the AV
        llSay(log_spam_channel, "Trying llAttachToAvatarTemp()");
        llAttachToAvatarTemp(ATTACH_HUD_CENTER_1);
        llSay(log_spam_channel, "After llAttachToAvatarTemp() with llGetAttached() returning " + (string)llGetAttached());
        llSetTimerEvent(0.0);
        if (llGetAttached() == 0)
        {   // Attaching failed
            llDie();
        }
    }

    experience_permissions_denied( key agent_id, integer reason )
    {   // Permissions denied, so go away
        llSay(log_spam_channel, "Denied experience permissions for " + (string)agent_id + " due to reason #" + (string) reason);
        llDie();
    }

    attach( key id )
    {   // Attached or detached from the avatar
        if (id)
        {
            llSetTimerEvent(0.0);
            llSay(log_spam_channel, "Now attached with a key " + (string)id + " and llGetAttached() returning " + (string)llGetAttached());
            // From this point, the object can start doing whatever it needs to do.
            state running;
        }
        else
        {
            llSay(log_spam_channel, "No longer attached");
            llDie();
        }
    }

    timer()
    {   // Use a timer to catch no permissions response
        llSay(log_spam_channel, "Permissions timer expired");
        llDie();
    }
}

// This state starts when permissions are granted, and the object is properly attached
state running
{
    state_entry()
    {
        llSay(log_spam_channel, "off and running!");
    }

    attach(key id)
    {
        if (id == NULL_KEY)
        {   // if the object ever un-attaches, make sure it deletes itself
            llSay(log_spam_channel, "No longer attached");
            llDie();
        }
    }
}
```

## Notes

#### Compiling

For a script to be associated with an Experience...

- It must be compiled with a client that is Experience aware,
- The "Use Experience" checkbox must be checked,
- And one of the users Experience keys selected.

|  | Important: Not all TPVs have this functionality. |
| --- | --- |

## See Also

### Events

- experience_permissions
- experience_permissions_denied

<!-- /wiki-source -->
