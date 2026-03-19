---
name: "llSin"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the sine of theta."
signature: "float llSin(float theta)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSin'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsin"]
---

Returns a float that is the sine of theta.


## Signature

```lsl
float llSin(float theta);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llSin)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSin) — scraped 2026-03-18_

Returns a float that is the sine of theta.

## Caveats

Because of IEE754 on floats , llSin(PI) returns -8.742278E-8 ( hex : 0xB3BBBD2E ) and not 0.0 . The error is cumulative with multiples of PI : For instance  llSin(100000.0*PI) = 0.015890 when the result should be 0.0

## Examples

```lsl
// Touch the object with this script in it to see the sine of random numbers!
default
{
    touch_start(integer num)
    {
        float r = llFrand(TWO_PI);
        llOwnerSay("The sine of " + (string)r + " in radians or " + (string)(r * RAD_TO_DEG) + " in degrees is " + (string)llSin(r));
    }
}
```

## See Also

### Functions

- **llAsin** — inverse Sine
- **llCos** — llAcos
- **llTan** — llAtan2

<!-- /wiki-source -->
