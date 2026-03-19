---
name: "llAngleBetween"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the angle in radians between rotation a and rotation b."
signature: "float llAngleBetween(rotation a, rotation b)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAngleBetween'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llanglebetween"]
---

Returns a float that is the angle in radians between rotation a and rotation b.


## Signature

```lsl
float llAngleBetween(rotation a, rotation b);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `a` | start rotation |
| `rotation` | `b` | end rotation |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAngleBetween)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAngleBetween) — scraped 2026-03-18_

Returns a float that is the angle in radians between rotation a and rotation b.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        rotation currentRootRotation = llGetRootRotation();
        float angle = llAngleBetween(ZERO_ROTATION, currentRootRotation);

        // PUBLIC_CHANNEL has the integer value 0
        llSay(PUBLIC_CHANNEL,
            "llAngleBetween(ZERO_ROTATION, " + (string)currentRootRotation + ") = " + (string)angle);
    }
}
```

## See Also

### Functions

- llRotBetween
- **llRot2Angle** — Similar functionality used for the Axis-Angle format

<!-- /wiki-source -->
