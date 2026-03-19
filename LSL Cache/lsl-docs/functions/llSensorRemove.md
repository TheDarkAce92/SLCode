---
name: "llSensorRemove"
category: "function"
type: "function"
language: "LSL"
description: 'Removes the sensor setup by llSensorRepeat.

There are no parameters or return value for this function, as only one llSensorRepeat can be specified per script.'
signature: "void llSensorRemove()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSensorRemove'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsensorremove"]
---

Removes the sensor setup by llSensorRepeat.

There are no parameters or return value for this function, as only one llSensorRepeat can be specified per script.


## Signature

```lsl
void llSensorRemove();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSensorRemove)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSensorRemove) — scraped 2026-03-18_

Removes the sensor setup by llSensorRepeat.

## Caveats

- If called within the sensor event then it also removes all of the sensor data that is accessed by the detection functions.

## Examples

The following basic example shows an object that when touched starts scanning for avatars in 10m every 30 seconds, and stops as soon as at least one is found, and returns their name.

```lsl
default {
    touch_start(integer x) {
        llSensorRepeat("", NULL_KEY, AGENT, 10.0, PI, 30.0);
    }

    sensor(integer x) {
        llSay(0, llDetectedName(0) + " was found first!");
        llSensorRemove();
    }
}
```

## See Also

### Events

- **sensor** — Triggered when a sensor detects something
- **no_sensor** — Triggered when a sensor detects nothing

### Functions

- **llSensorRepeat** — Scans for agents or objects every time period
- **llSensor** — Runs a sensor once

<!-- /wiki-source -->
