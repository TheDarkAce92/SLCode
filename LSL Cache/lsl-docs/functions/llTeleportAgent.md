---
name: "llTeleportAgent"
category: "function"
type: "function"
language: "LSL"
description: 'Teleports an agent to a landmark stored in the object's inventory.

If landmark is an empty string, the avatar is teleported to the location position in the current region.

If the destination is in the current region, the avatar will land facing look_at as a position within that region. Otherwise, '
signature: "void llTeleportAgent(key avatar, string landmark, vector position, vector look_at)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llTeleportAgent'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llteleportagent"]
---

Teleports an agent to a landmark stored in the object's inventory.

If landmark is an empty string, the avatar is teleported to the location position in the current region.

If the destination is in the current region, the avatar will land facing look_at as a position within that region. Otherwise, look_at is treated as a unit direction.

To run this function the script must request the PERMISSION_TELEPORT permission with llRequestPermissions and it must be granted by agent.


## Signature

```lsl
void llTeleportAgent(key avatar, string landmark, vector position, vector look_at);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent` | avatar UUID that is in the same region (the avatar to teleport, must be the owner) |
| `string` | `landmark` | a landmark in the inventory of the prim this script is in or an empty string (for teleporting within the same region) |
| `vector` | `position` | The position within the local region to teleport the avatar to if no landmark was provided. |
| `vector` | `look_at` | The position within the region that the avatar should be turned to face upon arrival. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTeleportAgent)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTeleportAgent) — scraped 2026-03-18_

Teleports an agent to a landmark stored in the object's inventory.

## Caveats

- If landmark is not an empty string and...

  - landmark is missing from the prim's inventory   or it is not a landmark then an error is shouted on DEBUG_CHANNEL.

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TELEPORT, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_TELEPORT is granted by anyone other than agent, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_TELEPORT permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- **This function can only teleport the owner of the object** (unless part of an Experience).
- Teleports are throttled (no more than 10 teleports within 15 seconds)
- Does not work in scripts within attached temp objects　llAttachToAvatarTemp.　Error Message is "Temporary attachments cannot request runtime permissions to teleport"
- Sitting avatars cannot be teleported using this function. You must llUnSit them first.
- This function does not override a parcel's teleport settings, i.e. if the parcel has a landing zone enabled the avatar will be teleported there.
- If the script is part of an experience that the avatar has granted permission, then this function may teleport them without being the owner and it will override parcel teleport routing. See the example below.
- When look_at is treated as a direction, a valid input should be .

  - In other words, it should be a **unit vector** corresponding to the avatar turning **angle** radians from north.

## Examples

Basic example with a landmark called **Destination** in the object's inventory:

```lsl
default
{
    touch_start(integer num_detected)
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TELEPORT);
    }

    run_time_permissions(integer perm)
    {
        if (PERMISSION_TELEPORT & perm)
        {
            llTeleportAgent(llGetPermissionsKey(), "Destination", ZERO_VECTOR, ZERO_VECTOR);
        }
    }
}
```

Basic example without a landmark in the object's inventory, while facing the avatar towards the center of the region:

```lsl
default
{
    touch_start(integer num_detected)
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TELEPORT);
    }

    run_time_permissions(integer perm)
    {
        if (PERMISSION_TELEPORT & perm)
        {
            vector region_pos = <100, 130, 40>;
            vector look_at = <128,128,40>;
            llTeleportAgent(llGetPermissionsKey(), "", region_pos, look_at);
        }
    }
}
```

**How to use this function in an Experience**

```lsl
// A SIMPLE SCRIPT that implements an Experience based teleport.
// Compile with the "Use Experience" box cnecked and an experience key you own selected.
// The prim containing this script must contain a landmark named "Landmark" in its contents
//
// If the person touching this box has not previously accepted an invitation to your experience,
// that person will be offered that opportunity when this prim is touched, and if the invitations
// is accepted, will be immediately teleported to the target of the landmark.
//
// If the toucher has previously accepted an invitation, the person will be immediately teleported
// with no interruption.
//
// The script has no safety features, e.g., will simply fail if the prim contains no landmark.
//
// Thanks to Rolig Loon for her help in figuring out how to do this
// See https://community.secondlife.com/t5/English-Knowledge-Base/Experiences-in-Second-Life/ta-p/2744686
// to read what the Lindens think is an adequate explanation of all this.

default
{
    touch_start(integer n)
    {
        llRequestExperiencePermissions(llDetectedKey(0), "");
    }

    experience_permissions(key agent)
    {
        llTeleportAgent(agent, "Landmark", ZERO_VECTOR, ZERO_VECTOR);
    }
}
```

Below is an example of properly handling the **look_at** value based on whether the destination is the current region or a different one. This ensures that the avatar will always be facing the same *direction* regardless of whether they're teleporting within the region or to another one.

The script keeps track of the landmark's destination coordinate in the **state_entry** and **changed** events, which is later used to calculate the total distance of the teleport.

```lsl
string landmark;
vector destination;

default
{
    state_entry()
    {
        // Get data about the first landmark in object inventory when script starts.
        if (llGetInventoryNumber(INVENTORY_LANDMARK) > 0) {
            landmark = llGetInventoryName(INVENTORY_LANDMARK, 0);
            llRequestInventoryData(landmark);
        }
    }

    changed(integer change)
    {
        if (!(change & (CHANGED_INVENTORY|CHANGED_REGION))) return;

        // Get data about the first landmark in object inventory when inventory changes.
        if (llGetInventoryNumber(INVENTORY_LANDMARK) > 0) {
            landmark = llGetInventoryName(INVENTORY_LANDMARK, 0);
            llRequestInventoryData(landmark);
        }
    }

    dataserver(key query, string data)
    {
        // Save llRequestInventoryData response.
        destination = (vector)data;
    }

    touch_start(integer num_detected)
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TELEPORT);
    }

    run_time_permissions(integer perm)
    {
        if (!(PERMISSION_TELEPORT & perm)) return;

        float angle = 45 * DEG_TO_RAD;

        // When teleporting to another region, we need a direction vector.
        vector look_at = ;

        float sim_size = llVecMag(<1,1,1>);
        float distance = llVecDist(<1,1,1>, destination / 256);

        if (distance < sim_size) {
            // When teleporting within the current region, we should use a position within the region instead.
            look_at = destination + look_at;
        }

        llTeleportAgent(llGetPermissionsKey(), landmark, ZERO_VECTOR, look_at);
    }
}
```

Another example, submitted by Jesse Barnett, shows how to use a list of landmarks inside a HUD to allow teleporting, even inside a no-script area: Teleport HUD.

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llTeleportAgentGlobalCoords** — Teleports an agent to a global position.

### Articles

- Script permissions

<!-- /wiki-source -->
