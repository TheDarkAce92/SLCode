---
name: "llCos"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the cosine of theta."
signature: "float llCos(float theta)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcos"]
---

Returns a float that is the cosine of theta.


## Signature

```lsl
float llCos(float theta);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `theta` | angle expressed in radians |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCos) — scraped 2026-03-18_

Returns a float that is the cosine of theta.

## Caveats

because of IEE754 on single floats, llCos(PI_BY_TWO) returns -4.371139E-8  (hex : 0xB33BBD2E ) and not 0 ; llCos(PI/3.0) returns 0.49999997 ( hex : 0x3EFFFFFF ) and not 0.5

## Examples

```lsl
// Touch the object with this script in it to see the cosine of random numbers!
default
{
    touch_start(integer num)
    {
        float r = llFrand(TWO_PI);
        llOwnerSay("The cosine of " + (string)r + " in radians or " + (string)(r * RAD_TO_DEG) + " in degrees is " + (string)llCos(r));
    }
}
```

## See Also

### Functions

| • llSin | llAsin | – | sine & inverse Sine |  |
| --- | --- | --- | --- | --- |
| •  | llAcos | – | inverse cosine |  |
| • llTan | llAtan2 | – | tangent & inverse tangent |  |

<!-- /wiki-source -->
