---
name: "llGetForce"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the force (if the script is physical)"
signature: "vector llGetForce()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetForce'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetforce"]
---

Returns a vector that is the force (if the script is physical)


## Signature

```lsl
vector llGetForce();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetForce)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetForce) — scraped 2026-03-18_

Returns a vector that is the force (if the script is physical)

## Examples

```lsl
default
{
    state_entry()
    {
        llSetForce(<0,llFrand(10),0>,FALSE); //Sets the force in a frand of 10 in Y axis.
        llSetTimerEvent(1); //Resets the force every second.
    }
    touch_start(integer total_num)
    {
        llOwnerSay((string)llGetForce()); //Says the force.
    }
    timer()
    {
        llResetScript();
    }
}
```

## See Also

### Functions

- llGetOmega
- llGetVel
- llGetTorque
- llGetMass
- llGetAccel
- llSetForce
- llSetTorque
- llSetForceAndTorque

<!-- /wiki-source -->
