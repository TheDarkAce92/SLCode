---
name: "llDetectedVel"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the vector velocity of detected object or avatar number.

number does not support negative indexes.
Returns <0.0, 0.0, 0.0> if number is not valid sensed object or avatar.'
signature: "vector llDetectedVel(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedVel'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedvel"]
---

Returns the vector velocity of detected object or avatar number.

number does not support negative indexes.
Returns <0.0, 0.0, 0.0> if number is not valid sensed object or avatar.


## Signature

```lsl
vector llDetectedVel(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedVel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedVel) — scraped 2026-03-18_

Returns the vector velocity of detected object or avatar number.

## Caveats

- If number is out of bounds this function returns <0.0, 0.0, 0.0> and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
//Tells the name and velocity of all near-by avatars.
default
{
    state_entry()
    {
        // Scan once for avatars within a 96 metre radius sphere
        llSensor("", "", AGENT, 96, PI);
    }
    sensor(integer num)
    {
        // num will initially be 1 or more. When num is 1, the index of the detected avatar will be zero
        while(num--)
        {
            llOwnerSay(llDetectedName(num) + " is moving at " + (string)llVecMag(llDetectedVel(num)) + " m/s.");
        }
    }
}
```

## See Also

### Articles

- Detected

<!-- /wiki-source -->
