---
name: "llAsin"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the arcsine in radians of val

The returned value is in the range [-PI_BY_TWO, PI_BY_TWO]'
signature: "float llAsin(float val)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAsin'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llasin"]
---

Returns a float that is the arcsine in radians of val

The returned value is in the range [-PI_BY_TWO, PI_BY_TWO]


## Signature

```lsl
float llAsin(float val);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llAsin)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAsin) — scraped 2026-03-18_

Returns a float that is the arcsine in radians of val

## Caveats

- Triggers a Math Error for complex results if not compiled in Mono.

## Examples

```lsl
// Touch the object with this script in it to see the arcsine of random numbers!
default
{
    touch_start(integer num)
    {
        float r = llFrand(2) - 1.0;
        llOwnerSay("The arcsine of " + (string)r + " is " + (string)llAsin(r));
    }
}
```

## See Also

### Functions

| • llSin |  | – | sine |  |
| --- | --- | --- | --- | --- |
| • llCos | llAcos | – | cosine & inverse cosine |  |
| • llTan | llAtan2 | – | tangent & inverse tangent |  |

### Articles

<!-- /wiki-source -->
