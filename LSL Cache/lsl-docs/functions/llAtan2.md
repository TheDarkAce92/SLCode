---
name: "llAtan2"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the arctangent2 of y, x.

Similar to the arctangent(y/x) except it utilizes the signs of x & y to determine the quadrant and avoids division by zero.'
signature: "float llAtan2(float y, float x)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAtan2'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llatan2"]
---

Returns a float that is the arctangent2 of y, x.

Similar to the arctangent(y/x) except it utilizes the signs of x & y to determine the quadrant and avoids division by zero.


## Signature

```lsl
float llAtan2(float y, float x);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `y` |  |
| `float` | `x` |  |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAtan2)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAtan2) — scraped 2026-03-18_

Returns a float that is the  arctangent2 of y, x.

## Examples

```lsl
default
{
  state_entry()
  {
    float num1 = llFrand(100.0);
    float num2 = llFrand(100.0);

    llOwnerSay("y = " + (string)num1);
    llOwnerSay("x = " + (string)num2);

    llOwnerSay("The arctangent of y divided by x is " + (string)llAtan2(num1, num2));
  }
}
```

```lsl
//Function with input of a vector determining the position of a target and returning
//a string with the literal compass-direction of that target towards your position
//by Ramana Sweetwater 2009/01, any use allowed license :-)
//corrected by Patrick Muggins

string compass (vector target)
{
    vector source = llGetPos();
    list DIRS =["W","NW","N","NE","E","SE","S","SW","W"];
    integer index = llCeil(3.5 - (4 * llAtan2(target.y - source.y, target.x - source.x) / PI));
    return llList2String(DIRS, index);
}
```

/Compass QA

## See Also

### Functions

| • llSin | llAsin | – | sine & inverse Sine |  |
| --- | --- | --- | --- | --- |
| • llCos | llAcos | – | cosine & inverse cosine |  |
| • llTan |  | – | tangent |  |

### Articles

<!-- /wiki-source -->
