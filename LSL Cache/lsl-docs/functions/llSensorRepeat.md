---
name: "llSensorRepeat"
category: "function"
type: "function"
language: "LSL"
description: 'Performs a scan for name and id with type within range meters and arc radians of forward vector and repeats every rate seconds. The first scan is not performed until rate seconds have passed.

Script execution continues immediately. Whenever a scan is completed, a sensor or no_sensor event is put in'
signature: "void llSensorRepeat(string name, key id, integer type, float range, float arc, float rate)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSensorRepeat'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsensorrepeat"]
---

Performs a scan for name and id with type within range meters and arc radians of forward vector and repeats every rate seconds. The first scan is not performed until rate seconds have passed.

Script execution continues immediately. Whenever a scan is completed, a sensor or no_sensor event is put in the event queue.

If name, id, and/or type are empty or 0, they are ignored.
If id is an invalid key or NULL_KEY it is treated as empty.
Depending upon which AGENT* flag is used determines the format requirements for name

See: llSensor for an excellent explanation of arc.


## Signature

```lsl
void llSensorRepeat(string name, key id, integer type, float range, float arc, float rate);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | Object or avatar name! |
| `key` | `id` | group, avatar or object UUID |
| `integer` | `type` | mask (AGENT_BY_LEGACY_NAME, AGENT_BY_USERNAME, ACTIVE, PASSIVE, and/or SCRIPTED) |
| `float` | `radius` | distance in meters from center, [0.0, 96.0] |
| `float` | `arc` | the max angle between the object's local X-axis and detectable objects, [0.0, PI] |
| `float` | `rate` | how often a scan is performed |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSensorRepeat)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSensorRepeat) — scraped 2026-03-18_

Performs a scan for name and id with type within range meters and arc radians of forward vector and repeats every rate seconds. The first scan is not performed until rate seconds have passed.

## Caveats

- When searching for an avatar but not by name, it doesn't matter which AGENT flag is used.
- The repeat of the sensor event is adversely affected by time dilation (lag).
- Sensors placed in the root prim of attachments will use the direction the avatar is facing as their forward vector. In mouselook, this means that it will be wherever the avatar is looking, while out of mouselook, this means whichever way the avatar is pointing. This does not include where the avatar's head is pointing, or what animation the avatar is doing, just the direction the avatar would move in if you walked forward. This is the case, regardless of where the object is attached.
- Sensors placed in prims other than the root prim of an attachment will have their forward direction offset relative to the root prim's forward direction, e.g. a sensor in a prim whose +X direction is the reverse of the root +X will look backward.
- Only the most recent sensor event is queued. Previous sensor events are replaced.
- A repeating sensor does not persist across a state change.
- llSensorRepeat can occasionally detect outside of it's specified range every few cycles when used near sim borders. llSensor in a timer does not.
- Only one or zero llSensorRepeats can be active per script. If llSensorRepeat is called a second time without calling llSensorRemove, the first llSensorRepeat is deactivated and the second one replaces it

## Examples

```lsl
// Written by Steamy Latte.
// Scans every 30 seconds for visitors within 10 meters.
// Reports new visitors to object owner when she is in range.

string AllAgents;

default
{
    state_entry()
    {
        // arc=PI is a sphere, you could look more narrowly in the direction object is facing with PI/2, PI/4 etc.
        // don't repeat this too often to avoid lag.
        llSensorRepeat("", "", AGENT_BY_LEGACY_NAME, 10.0, PI, 30.0);
    }
    sensor(integer num_detected)
    {
        string thisAgent;
        integer agentNum;
        for (agentNum=0; agentNum

## Notes

|  | Important: You might want to use llGetAgentList instead of using sensors to get a list of all avatars within the same parcel or region. |
| --- | --- |

## See Also

### Events

- **sensor** — Triggered when a sensor detects something
- **no_sensor** — Triggered when a sensor detects nothing

### Functions

- **llSensor** — Runs a sensor once
- **llSensorRemove** — Stops the llSensorRepeat timer
- **llOverMyLand** — What happens over owners land

<!-- /wiki-source -->
