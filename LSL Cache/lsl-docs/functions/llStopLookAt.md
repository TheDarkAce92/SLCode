---
name: "llStopLookAt"
category: "function"
type: "function"
language: "LSL"
description: 'Stop causing object to point at a target

Use in conjunction llLookAt or llRotLookAt.'
signature: "void llStopLookAt()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStopLookAt'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstoplookat"]
---

Stop causing object to point at a target

Use in conjunction llLookAt or llRotLookAt.


## Signature

```lsl
void llStopLookAt();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStopLookAt)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStopLookAt) — scraped 2026-03-18_

Stop causing object to point at a target

## Examples

```lsl
default
{
    state_entry()
    {
        llSensorRepeat("", "", AGENT, 20.0, PI, 0.2);
        //Detects avatars
    }

    sensor(integer total_number)
    {
        llLookAt( llDetectedPos(0) + <0.0, 0.0, 1.0>, 3.0, 1.0 );
        //Looks at the nearest avatar.
    }

    touch_start(integer total_number)
    {
        llStopLookAt();
        llSensorRemove();
        //Stops looking at any avatar and removes the sensor.
    }
}
```

## See Also

### Functions

- llLookAt
- llRotLookAt

<!-- /wiki-source -->
