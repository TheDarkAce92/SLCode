---
name: "llSensor"
category: "example"
type: "example"
language: "LSL"
description: "Performs a single scan for name and id with type within radius meters and arc radians of forward vector."
wiki_url: "https://wiki.secondlife.com/wiki/LlSensor"
author: "legacy name"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


SensorllSensor

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Notes

  - 4.1 Loops & Repetition
- 5 See Also

  - 5.1 Events
  - 5.2 Functions
- 6 Deep Notes

  - 6.1 Footnotes
  - 6.2 Signature
  - 6.3 Haiku
- 7 Gallery

## Summary

 Function:  **llSensor**( string name, key id, integer type, float radius, float arc );

0.0

Forced Delay

10.0

Energy

Performs a single scan for name and id with type within radius meters and arc radians of forward vector.

Script execution continues immediately. When the scan is completed, a sensor or no_sensor event is put in the event queue.

• string

name

–

object or avatar name!

• key

id

–

group, avatar or object UUID that is in the same region

• integer

type

–

bit field (AGENT, AGENT_BY_LEGACY_NAME, AGENT_BY_USERNAME, ACTIVE, PASSIVE, and/or SCRIPTED)

• float

radius

–

distance in meters from center, [0.0, 96.0]

• float

arc

–

the max angle between the object's local X-axis and detectable objects, [0.0, PI]

If name and/or id are empty, they are ignored.**If id is an invalid key or NULL_KEY it is treated as empty.Depending upon which AGENT* flag is used determines the format requirements for name See: llSensor for an excellent explanation of arc. type Flag Mask**

**Description (llDetectedType())**

**Description (llSensor() and llSensorRepeat() mask)**

AGENT_BY_LEGACY_NAME

0x1

Agents

This is used to find agents by legacy name.

AGENT

0x1

Agents

This is also used to find agents by legacy name, and is functionally identical to AGENT_BY_LEGACY_NAME

AGENT_BY_USERNAME

0x10

*Reserved*

This is used to find agents by username.

ACTIVE

0x2

Physical tasks. (Physical objects & agents)

Physical objects that are moving or objects containing an active script. Thus, it is using SL server resources now.

PASSIVE

0x4

Non-physical objects.

Non-scripted or script is inactive and non-physical or, if physical, not moving. Thus, it is not using SL server resources now.

SCRIPTED

0x8

Objects containing any active script.

Objects that has any script, which is doing anything in simulator just now.

DAMAGEABLE

0x20

Objects & agents that are able to process damage.

Filter for objects in world that have a script with on_damage or a final_damage event (able to process damage)

llDetectedType()

Scripted

Not Scripted

Agent Standing

Agent Sitting

Physical Movement

10 (ACTIVE|SCRIPTED)

2 (ACTIVE)

3 (ACTIVE|AGENT)

3 (ACTIVE|AGENT)

Non-Physical

12 (PASSIVE|SCRIPTED)

4 (PASSIVE)

1 (AGENT)

5 (PASSIVE|AGENT)

Float Constants

Arc

PI_BY_TWO

A hemisphere scan

PI

A full sphere scan

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



      **Important:** You might want to use llGetAgentList instead of using sensors to get a list of all avatars within the same parcel or region.


#### Loops & Repetition

Using llSensor in a for loop is a beginners mistake, as events will not interrupt each other (the sensor event will not interrupt whatever event is currently being executed). To perform repeat sensor sweeps, llSensorRepeat is the better solution. While it is possible to call llSensor from a timer event, it is less efficient to do so; there is a limit to the number of events that can be processed in a second and using the timer just to call llSensor will result in your script getting less timeslice.

## See Also

### Events

•

sensor

–

Triggered when a sensor detects something

•

no_sensor

–

Triggered when a sensor detects nothing

### Functions

•

llSensorRepeat

–

Runs a sensor on a timer

•

llSensorRemove

–

Stops the llSensorRepeat timer

## Deep Notes

#### Footnotes

1. **^** The ranges in this article are written in [Interval Notation](http://en.wikipedia.org/wiki/Interval_(mathematics)#Notations_for_intervals).

#### Signature

```lsl
function void llSensor( string name, key id, integer type, float radius, float arc );
```

#### Haiku

The hounds are straining.


Elusive quarry sighted.


The game's afoot!



## Gallery

- arc = PI / 4
- arc = PI / 2
- arc = PI