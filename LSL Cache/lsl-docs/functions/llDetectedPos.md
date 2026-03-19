---
name: "llDetectedPos"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the position (in region coordinates) of detected object number.

number does not support negative indexes.
Returns ZERO_VECTOR if number is not valid sensed object.'
signature: "vector llDetectedPos(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedPos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedpos"]
---

Returns a vector that is the position (in region coordinates) of detected object number.

number does not support negative indexes.
Returns ZERO_VECTOR if number is not valid sensed object.


## Signature

```lsl
vector llDetectedPos(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` |  |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedPos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedPos) — scraped 2026-03-18_

Returns a vector that is the position (in region coordinates) of detected object number.

## Caveats

- If number is out of bounds this function returns <0.0, 0.0, 0.0> and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
// Get position and distance of toucher

default
{
    touch_start(integer total_number)
    {
	// get the position of the avatar touching this prim
	vector pos = llDetectedPos(0);

	// compute how far away they are
	float dist = llVecDist(pos, llGetPos() );

	llSay(0, "You are " + (string) dist + " metres from me, at coordinates " + (string) pos);
    }
}
```

```lsl
// get name and sim position of Avatars within "say" range

default
{
    state_entry()
    {
        llOwnerSay( "Touch me to get the positions of avatars in 'Say' range" );
    }

    touch_start( integer vIntTouchCount )
    {
        // Do a one-off sensor sweep over a 20m radius sphere for avatars
        llSensor( "", "", AGENT, 20, PI );
    }

    sensor( integer vIntFound )
    {
        integer vIntCounter = 0;
        //-- loop through all avatars found
        do
        {
            llOwnerSay( llDetectedName( vIntCounter )
                // get the position of this detected avatar
                + (string) llDetectedPos( vIntCounter ) );
        } while (++vIntCounter < vIntFound);
    }

    // sensor does not detect owner if it's attached
    no_sensor()
    {
        llOwnerSay( "I couldn't find anybody" );
    }
}
```

## See Also

### Articles

- Detected

<!-- /wiki-source -->
