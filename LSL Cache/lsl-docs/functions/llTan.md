---
name: "llTan"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the tangent of theta."
signature: "float llTan(float theta)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTan'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltan"]
---

Returns a float that is the tangent of theta.


## Signature

```lsl
float llTan(float theta);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llTan)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTan) — scraped 2026-03-18_

Returns a float that is the tangent of theta.

## Caveats

Because of IEE754 on floats , llTan(PI_BY_TWO) returns -22877332 ( hex: 0xCBAE8A4A) and not infinity

## Examples

```lsl
// Touch the object with this script in it to see the tangent of random numbers!
default
{
    touch_start(integer num)
    {
        float r = llFrand(TWO_PI);
        llOwnerSay("The tangent of " + (string)r + " in radians or " + (string)(r * RAD_TO_DEG) + " in degrees is " + (string)llTan(r));
    }
}
```

## See Also

### Functions

| • llSin | llAsin | – | sine & inverse Sine |  |
| --- | --- | --- | --- | --- |
| • llCos | llAcos | – | cosine & inverse cosine |  |
| •  | llAtan2 | – | inverse tangent |  |

<!-- /wiki-source -->
