---
name: "llSensor"
category: "function"
type: "function"
language: "LSL"
description: 'Performs a single scan for name and id with type within radius meters and arc radians of forward vector.

Script execution continues immediately. When the scan is completed, a sensor or no_sensor event is put in the event queue.

If name and/or id are empty, they are ignored.
If id is an invalid key'
signature: "void llSensor(string name, key id, integer type, float range, float arc)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSensor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsensor"]
---

Performs a single scan for name and id with type within radius meters and arc radians of forward vector.

Script execution continues immediately. When the scan is completed, a sensor or no_sensor event is put in the event queue.

If name and/or id are empty, they are ignored.
If id is an invalid key or NULL_KEY it is treated as empty.
Depending upon which AGENT* flag is used determines the format requirements for name

See: llSensor for an excellent explanation of arc.


## Signature

```lsl
void llSensor(string name, key id, integer type, float range, float arc);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | object or avatar name! |
| `key` | `id` | group, avatar or object UUID that is in the same region |
| `integer` | `type` | mask (AGENT, AGENT_BY_LEGACY_NAME, AGENT_BY_USERNAME, ACTIVE, PASSIVE, and/or SCRIPTED) |
| `float` | `radius` | distance in meters from center, [0.0, 96.0] |
| `float` | `arc` | the max angle between the object's local X-axis and detectable objects, [0.0, PI] |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSensor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSensor) — scraped 2026-03-18_

Performs a single scan for name and id with type within radius meters and arc radians of forward vector.

## Caveats

- When searching for an avatar but not by name, it doesn't matter which AGENT flag is used.
- AGENT, PASSIVE and ACTIVE behave inclusively. SCRIPTED is **not** inclusive and will exclude non-scripted targets (like avatars) from the detected set.
- Objects do not detect themselves, and attachments cannot detect their wearers (this includes HUD attachments).
- Attachments cannot be detected by llSensor.
- For an object to be detected, the center of its root prim (the same point it would report with llGetRootPosition) must be within the sensor beam.
- For an agent to be detected, a point near the pelvis must be inside the sensor beam (the same as llGetRootPosition would report in a script attached to that avatar). This point is indicated by red crosshairs when Advanced>Character>Display Agent Target is turned on.

  - If the agent is sitting on an object, the root prim of the sat upon object becomes a second sensor target for the agent (but not if the avatar is outside the sensor arc, see [SVC-5145](https://jira.secondlife.com/browse/SVC-5145)).
- Sensors placed in the root prim of attachments will use the direction the avatar is facing as their forward vector. In mouselook, this means that it will be wherever the avatar is looking, while out of mouselook, this means whichever way the avatar is pointing. This does not include where the avatar's head is pointing, or what animation the avatar is doing, just the direction the avatar would move in if you walked forward. This is the case, regardless of where the object is attached.
- Sensors placed in prims other than the root prim of an attachment will have their forward direction offset relative to the root prim's forward direction, e.g. a sensor in a prim whose +X direction is the reverse of the root +X will look backward.
- llSensor does not detect objects or agents across region boundaries
- If type is zero, the sensor will silently fail, neither sensor or no_sensor will be triggered.
- Only 32 objects will be scanned each time. (Increased from 16 with Release 2024-03-18.8333615376 on Tuesday, March 19, 2024)
- DAMAGEABLE is a filter flag; it cannot be used on its own. It must be combined with at least one other flag. For example, AGENT | ACTIVE | PASSIVE | DAMAGEABLE will return all damageable agents and objects, whether physical or not.

## Examples

This sensor scans a 45 degree cone about the x-axis (PI/2 or PI_BY_TWO scans a hemisphere; PI is a spherical scan). Also it will only match an agent with the legacy name "Governor Linden".

```lsl
llSensor( "Governor Linden", NULL_KEY, AGENT_BY_LEGACY_NAME, 96.0, PI/4 );
```

This sensor detects all prims and agents with a given name within 15m of the sensor.  (AGENT, PASSIVE and ACTIVE behave inclusively.  SCRIPTED is not inclusive and will exclude non-scripted targets (like avatars) from the detected set.)

```lsl
llSensor( "", NULL_KEY, ( AGENT | PASSIVE | ACTIVE ), 15.0, PI );
```

Basic example script that when touched executes a sensor scan of agents. When the sensor event is processed it spits out messages to the owner of each detected agents' name.

```lsl
default
{
    touch_start(integer total_number)
    {
        llSensor("", NULL_KEY, AGENT, 30.0, PI);
    }

    sensor( integer detected )
    {
        while(detected--)
        {
            llOwnerSay(llDetectedName(detected));
        }
    }
}
```

## Notes

|  | Important: You might want to use llGetAgentList instead of using sensors to get a list of all avatars within the same parcel or region. |
| --- | --- |

#### Loops & Repetition

Using llSensor in a for loop is a beginners mistake, as events will not interrupt each other (the sensor event will not interrupt whatever event is currently being executed). To perform repeat sensor sweeps, llSensorRepeat is the better solution. While it is possible to call llSensor from a timer event, it is less efficient to do so; there is a limit to the number of events that can be processed in a second and using the timer just to call llSensor will result in your script getting less timeslice.

## See Also

### Events

- **sensor** — Triggered when a sensor detects something
- **no_sensor** — Triggered when a sensor detects nothing

### Functions

- **llSensorRepeat** — Runs a sensor on a timer
- **llSensorRemove** — Stops the llSensorRepeat timer

<!-- /wiki-source -->
