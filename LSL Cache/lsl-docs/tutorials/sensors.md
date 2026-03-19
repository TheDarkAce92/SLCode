---
name: "Sensors"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Detecting nearby objects and avatars using llSensor, llSensorRepeat, the sensor and no_sensor events, and practical alternatives for full-region scans"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# Sensors

LSL scripts can scan nearby space for avatars and objects using `llSensor` (one-shot) and `llSensorRepeat` (repeating). Results arrive via the `sensor` event; if nothing is found, `no_sensor` fires instead.

## Function Signatures

```lsl
llSensor(string name, key id, integer type, float range, float arc);
llSensorRepeat(string name, key id, integer type, float range, float arc, float rate);
llSensorRemove();
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `name` | string | Filter by object or avatar name. `""` matches any name. |
| `id` | key | Filter by specific UUID. `NULL_KEY` matches any UUID. |
| `type` | integer | Bitmask of entity types to detect (see below). |
| `range` | float | Detection radius in metres, 0.0 to 96.0. |
| `arc` | float | Half-angle of the detection cone in radians, 0.0 to `PI`. Use `PI` for a full sphere. |

### Type Constants

| Constant | Value | Detects |
|---|---|---|
| `AGENT` | 1 | Avatars, matched by legacy name. Also available as `AGENT_BY_LEGACY_NAME` (same value). |
| `AGENT_BY_USERNAME` | 0x10 | Avatars, matched by username (the `name` parameter matches the account username, not the display name). |
| `ACTIVE` | 2 | Physically active or moving scripted objects (includes NPCs in motion). Does **not** include physical objects that are stationary. |
| `PASSIVE` | 4 | Non-physical objects, or physical objects that are stationary and inactive. |
| `SCRIPTED` | 8 | Objects that contain scripts |

Combine with `|` to detect multiple types:

```lsl
llSensor("", NULL_KEY, AGENT | ACTIVE, 20.0, PI);  // avatars and physical objects
```

## One-Shot Scan with llSensor

`llSensor` triggers a single scan. The `sensor` or `no_sensor` event fires once.

```lsl
default
{
    touch_end(integer num_detected)
    {
        llSensor("", NULL_KEY, AGENT, 10.0, PI);
    }

    sensor(integer num_detected)
    {
        integer i;
        for (i = 0; i < num_detected; i++)
        {
            llSay(0, "Found: " + llDetectedName(i) + " at " +
                  (string)llDetectedPos(i));
        }
    }

    no_sensor()
    {
        llSay(0, "Nothing detected.");
    }
}
```

## Repeating Scan with llSensorRepeat

`llSensorRepeat` runs scans automatically every `rate` seconds. **The first scan does not happen immediately — it fires after the first `rate`-second interval has elapsed.**

```lsl
default
{
    state_entry()
    {
        // Scan every 5 seconds, full sphere, 20 m radius
        llSensorRepeat("", NULL_KEY, AGENT, 20.0, PI, 5.0);
    }

    sensor(integer num_detected)
    {
        llSay(0, (string)num_detected + " avatar(s) nearby.");
    }

    no_sensor()
    {
        llSay(0, "Area clear.");
    }
}
```

Call `llSensorRemove()` to stop a repeating sensor:

```lsl
touch_end(integer num_detected)
{
    llSensorRemove();
    llSay(0, "Sensor stopped.");
}
```

## Maximum Detections

The `sensor` event receives a maximum of **32 detections** per scan, even if more entities are in range. Results are ordered nearest to furthest. If more than 32 entities match, only the 32 closest are reported.

## Detection Functions

Inside the `sensor` event, use these functions with an index from `0` to `num_detected - 1`:

| Function | Returns |
|---|---|
| `llDetectedName(i)` | Name of the detected entity |
| `llDetectedKey(i)` | UUID |
| `llDetectedPos(i)` | Position as a vector |
| `llDetectedVel(i)` | Velocity as a vector |
| `llDetectedRot(i)` | Rotation |
| `llDetectedType(i)` | Type bitmask (AGENT, ACTIVE, etc.) |
| `llDetectedDist(i)` | Distance from sensor origin in metres |
| `llDetectedOwner(i)` | UUID of the object's owner |

These functions are valid inside any **detection event** — `sensor`, `collision`, `collision_start`, `collision_end`, `touch`, `touch_start`, and `touch_end`. They return valid data only while that event handler is executing; storing the index and calling them later from a timer or other event will not work.

## Arc Parameter

The `arc` parameter is a **half-angle** in radians defining a cone pointing in the forward direction of the object (positive local X axis).

| Arc value | Coverage |
|---|---|
| `0.0` | Effectively a ray directly forward — almost nothing detected |
| `PI / 4` | 45° cone (90° total spread) |
| `PI / 2` | 90° half-angle (180° spread — a hemisphere in front) |
| `PI` | Full sphere (360° in all directions) |

Use `PI` for general proximity detection unless directional sensing is specifically needed.

## Scanning for Agents Region-Wide

`llSensor` is limited to a 96-metre range. For scanning all avatars across an entire region, the wiki recommends `llGetAgentList` instead:

```lsl
default
{
    touch_end(integer num_detected)
    {
        list agents = llGetAgentList(AGENT_LIST_REGION, []);
        integer count = llGetListLength(agents);
        llSay(0, "Agents in region: " + (string)count);
    }
}
```

`llGetAgentList` returns a list of avatar UUIDs with no range limit and no 32-entity cap. It does not return object data — only avatars.

## State Changes and Sensor

A state change cancels any active `llSensorRepeat`. If you want sensing to continue in a new state, call `llSensorRepeat` again in that state's `state_entry`.

## Caveats

- `llSensorRepeat` is **not** equivalent to an immediate scan followed by repeating — the first scan fires after the first interval.
- Detections are capped at **32** per scan. For dense scenes, the furthest entities are silently dropped.
- `llSensor` and `llSensorRepeat` do not detect the prim containing the script itself, nor can attachments detect their wearers.
- Only one sensor can be active at a time per script. Calling `llSensorRepeat` or `llSensor` while one is running replaces it.
- The detection functions (`llDetectedName`, `llDetectedKey`, etc.) are valid inside any detection event (`sensor`, `collision`, `touch_start`, etc.) but must be called during that event handler — not stored for later use in a timer or other event.
- `SCRIPTED` is not inclusive on its own — it filters to scripted objects but does not add any entities. Combine it with `ACTIVE` or `PASSIVE` to detect scripted objects of those types.
