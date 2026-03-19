---
name: "sensor"
category: "event"
type: "event"
language: "LSL"
description: "Fires when llSensor or llSensorRepeat detects objects or avatars within range"
wiki_url: "https://wiki.secondlife.com/wiki/Sensor"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "sensor(integer num_detected)"
parameters:
  - name: "num_detected"
    type: "integer"
    description: "Number of objects or avatars found (always > 0)"
deprecated: "false"
---

# sensor

```lsl
sensor(integer num_detected)
{
    // process detections
}
```

Fires in response to `llSensor` or `llSensorRepeat`. `num_detected` is always greater than zero — if nothing is found, `no_sensor` fires instead.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_detected` | integer | Number of detected objects/avatars (≥ 1) |

## Detection Data

Use `llDetected*` functions with index 0 through `num_detected - 1`:
- Results are ordered nearest to furthest.
- `llDetectedKey(i)` — UUID
- `llDetectedName(i)` — name
- `llDetectedPos(i)` — position
- `llDetectedType(i)` — type flags (AGENT, ACTIVE, PASSIVE, SCRIPTED)
- `llDetectedVel(i)` — velocity

## Caveats

- Maximum 32 detections per sensor scan.
- Lindens in administrative mode cannot be sensed.
- Sensors in attachments use the avatar's facing as the forward vector.
- An attachment sensor will not detect the avatar wearing it.
- Avatars logging out temporarily appear as "Ghost" objects.

## Example

```lsl
default
{
    touch_start(integer n)
    {
        llSensor("", NULL_KEY, AGENT_BY_LEGACY_NAME, 10.0, PI);
    }

    sensor(integer num_detected)
    {
        string msg = "Detected " + (string)num_detected + " avatar(s): ";
        integer i = 0;
        while (i < num_detected)
        {
            if (i > 0) msg += ", ";
            msg += llDetectedName(i);
            ++i;
        }
        llWhisper(0, msg);
    }

    no_sensor()
    {
        llWhisper(0, "Nobody nearby.");
    }
}
```

## See Also

- `no_sensor` — fires when sensor finds nothing
- `llSensor` — single sensor scan
- `llSensorRepeat` — repeating sensor scan
- `llSensorRemove` — stop repeating sensor


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/sensor) — scraped 2026-03-18_

## Caveats

- Lindens in administrative mode cannot be sensed by sensors in the same region as the Linden.
- Sensors placed in attachments will use the direction the avatar is facing as their forward vector. In mouselook, this means that it will be wherever the avatar is looking, while out of mouselook, this means whichever way the avatar is pointing. This does not include where the avatar's head is pointing, or what animation the avatar is doing, just the direction the avatar would move in if you walked forward. This is the case, regardless of where the object is attached.
- A sensor running in an attachment will not detect the avatar wearing it.
- Only 32 objects will be scanned each time. (Increased from 16 with Release 2024-03-18.8333615376 on Tuesday, March 19, 2024)
- This event is not executed when nothing is detected, means, you never get the result 0 returned. Use no_sensor for that.
- on logout all avatars leave a Ghost for a few moments, this results in Failures in llDetected functions in sensor events.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
    //  do a 10m spherical sweep
        llSensor("", NULL_KEY, AGENT_BY_LEGACY_NAME, 10.0, PI);
    }

    sensor (integer num_detected)
    {
        string message = "Detected " + (string)num_detected + " avatar(s): " + llDetectedName(0);

    //  we already added the first avatar above, so continue from index 1
        integer index = 1;
        while (index < num_detected)
            message += ", " + llDetectedName(index++);

        llWhisper(PUBLIC_CHANNEL, message);
    }

    no_sensor()
    {
        llWhisper(PUBLIC_CHANNEL, "Nobody is near me at present.");
    }
}
```

## Notes

|  | Important: You might want to use llGetAgentList instead of using sensors to get a list of all avatars within the same parcel or region. |
| --- | --- |

## See Also

### Functions

- llSensor
- llSensorRepeat

### Articles

- Detected

<!-- /wiki-source -->
