---
name: "no_sensor"
category: "event"
type: "event"
language: "LSL"
description: "Result of a call to llSensor or llSensorRepeat."
signature: "no_sensor()"
wiki_url: 'https://wiki.secondlife.com/wiki/no_sensor'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Result of a call to llSensor or llSensorRepeat.


## Signature

```lsl
no_sensor()
{
    // your code here
}
```


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/no_sensor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/no_sensor) — scraped 2026-03-18_

## Caveats

- sensor/no_sensor are not always the best solution:

  - To determine if something is in/out of range is overkill. For this situation use: llGetObjectDetails as you will see in the Useful Snippets section.
  - To determine if an avatar is in the region, try llGetAgentSize

## Examples

```lsl
//List all avatars in range.
default
{
     on_rez(integer i)
     {
          llSensor("", "", AGENT_BY_LEGACY_NAME, 96.0, PI);   // Detect any avatars within a 96 metre radius sphere
     }
     sensor(integer number_detected)
     {
          integer i = 0;
          do
          {
               llOwnerSay(llDetectedName(i) + " is " + (string) llVecDist(llGetPos(), llDetectedPos(i) ) + "m away.");
          }
          while(++i < number_detected);
     }
     no_sensor()
     {
          llOwnerSay("No avatars in range.");
     }
}
```

## See Also

### Functions

- llSensor
- llSensorRepeat

<!-- /wiki-source -->
