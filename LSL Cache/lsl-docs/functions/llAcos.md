---
name: "llAcos"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the arccosine in radians of val

The returned value is in the range [0.0, PI]'
signature: "float llAcos(float val)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAcos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llacos"]
---

Returns a float that is the arccosine in radians of val

The returned value is in the range [0.0, PI]


## Signature

```lsl
float llAcos(float val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `val` | must fall in the range [-1.0, 1.0] |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAcos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAcos) — scraped 2026-03-18_

Returns a float that is the arccosine in radians of val

## Caveats

- Triggers a Math Error for complex results if not compiled in Mono.

## Examples

```lsl
//  This example exercises the full valid range of argument from -1.0 to +1.0

default
{
    touch_start(integer num_detected)
    {
        float random = llFrand(2.0) - 1.0;

        llOwnerSay("The arccosine of " + (string)random + " is " + (string)llAcos(random));
    }
}
```

```lsl
//An example for the Law of Cosines to calculate any angle of a triangle from 3 known side lengths.

default
{
    touch_start(integer num_detected)
    {
        vector t=< llFrand(9.0)+1.0 , llFrand(9.0)+1.0 , llFrand(9.0)+1.0 >; //the 3 values of this vector are used to set the lengths of 3 sides of a triangle.

        float anglexy=llAcos( (t.x*t.x+t.y*t.y-(t.z*t.z)) / ( 2*t.x*t.y) ) //Law Of Cosines

        llOwnerSay("Using the Law Of Cosines, the angle of a triangle between side a="+(string)t.x+"and side b="+(string)t.y+"is = "+(string)anglexy+" radians="+(string)(anglexy*RAD_TO_DEG)+"° and that angle is not on side c="+(string)t.z);
    }
}
```

## See Also

### Functions

| • llSin | llAsin | – | sine & inverse Sine |  |
| --- | --- | --- | --- | --- |
| • llCos |  | – | cosine |  |
| • llTan | llAtan2 | – | tangent & inverse tangent |  |

### Articles

<!-- /wiki-source -->
