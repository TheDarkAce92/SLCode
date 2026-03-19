---
name: "llTriggerSoundLimited"
category: "function"
type: "function"
language: "LSL"
description: 'Plays sound at volume, centered at but not attached to the object, limited to the box defined by vectors top_north_east and bottom_south_west

If the object moves the sound does not move with it.
Use llPlaySound to play a sound attached to the object.'
signature: "void llTriggerSoundLimited(string sound, float volume, vector top_north_east, vector bottom_south_west)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTriggerSoundLimited'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltriggersoundlimited"]
---

Plays sound at volume, centered at but not attached to the object, limited to the box defined by vectors top_north_east and bottom_south_west

If the object moves the sound does not move with it.
Use llPlaySound to play a sound attached to the object.


## Signature

```lsl
void llTriggerSoundLimited(string sound, float volume, vector top_north_east, vector bottom_south_west);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |
| `vector` | `top_north_east` | position in region coordinates |
| `vector` | `bottom_south_west` | position in region coordinates |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTriggerSoundLimited)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTriggerSoundLimited) — scraped 2026-03-18_

Plays sound at volume, centered at but not attached to the object, limited to the box defined by vectors top_north_east and bottom_south_west

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- Unlike llSetSoundRadius, the sound audibility is determined by **avatar** position and not camera position.
- If the script is attached and the parcel has avatar sounds turned off, an error is shouted on DEBUG_CHANNEL: "Too many sound triggers."

## Examples

```lsl
/*
    Single Prim llTriggerSoundLimited Helper by Daemonika Nightfire.

    Just use this script in a single prim and make the prim as big as your room.
    If you then click on the prim, the sound will only be triggered inside and you will get a message with a finished LSL code.
    You can simply copy this code to the clipboard and use it in your actual script.

    Important:
    You cannot rotate the prim, the code needs global coordinates.
*/

string sound = "c704dbd8-53b1-246d-e197-b486e92da45b"; // use here your own sound uuid

////////// nothing to do below this line \\\\\\\\\\
default
{
    state_entry()
    {
        llSetStatus(STATUS_PHANTOM, TRUE);
        llSetRot(ZERO_ROTATION);
    }

    touch_start(integer total_number)
    {
        llSetRot(ZERO_ROTATION);
        vector my_pos = llGetPos();
        vector my_scale = llGetScale();

        float _X = my_scale.x/2;
        float _Y = my_scale.y/2;
        float _Z = my_scale.z/2;

        vector bottom_south_west = ;
        vector top_north_east    = ;

        llTriggerSoundLimited(sound, 1.0, top_north_east, bottom_south_west);

        llOwnerSay("\nllTriggerSoundLimited(\"" + sound + "\", 1.0, " + (string)top_north_east + ", " + (string)bottom_south_west + ");");
    }

    on_rez(integer Dae)
    {
        llResetScript();
    }
}
```

### Secret Collision Sound

This will play a sound on collision, only to the person who collided with it.
It can be used for haunted houses where you want to add confusion, since others wont hear!

```lsl
string sound = "a9da4612-5d4b-662a-050a-c821c394991f"; // squeaky toy

playSoundAt(key avatar, string sound, float volume)
{
    if (llGetAgentSize(avatar)) // Make sure theyre actually present
    {
        vector pos = (vector)llList2String(llGetObjectDetails(avatar, [OBJECT_POS]),0); // Their position
        list scale = llGetBoundingBox(avatar); // The corners of their bounding box
        vector corner2 = pos+llList2Vector(scale,1); // Top northeast corner of their bounding box
        vector corner1 = pos+llList2Vector(scale,0); // Bottom southwest corner of their bounding box
        llTriggerSoundLimited(sound, volume, corner2, corner1); // Play sound in their location only
    }
}
default
{
    collision_start(integer n)
    {
        key bumper = llDetectedKey(0);
        float volume = 1.0; // Volume is affected by distance like llPlaySound!
        playSoundAt(bumper, sound, volume);
    }
}
```

## See Also

### Functions

- llPlaySound
- llTriggerSound
- llSetSoundRadius

<!-- /wiki-source -->
