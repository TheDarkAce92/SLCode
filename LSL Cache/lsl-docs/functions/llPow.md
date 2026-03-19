---
name: "llPow"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is base raised to the power exponent (base^exponent)

Returns NaN when base is negative and exponent is not an integer (an imaginary result, (exponent != (integer)exponent) && (base < 0.0)).'
signature: "float llPow(float base, float exponent)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llPow'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llpow"]
---

Returns a float that is base raised to the power exponent (base^exponent)

Returns NaN when base is negative and exponent is not an integer (an imaginary result, (exponent != (integer)exponent) && (base < 0.0)).


## Signature

```lsl
float llPow(float base, float exponent);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `base` |  |
| `float` | `exponent` |  |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPow)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPow) — scraped 2026-03-18_

Returns a float that is base raised to the power exponent (baseexponent)

## Caveats

- If exponent is a static integer and not a variable, llPow is dramatically slower than simple repeated multiplication, i.e. it's much faster to do `val = base*base*base` instead of `val = llPow(base, 3)`.
- Triggers a Math Error for imaginary results if not compiled in Mono.

## Examples

```lsl
default {
     state_entry() {
          llOwnerSay("llPow(5, .5) (" + (string)llPow(5, .5) + ") is equal to llSqrt(5) ("
                      + (string)llSqrt(5) + ").");
     }
}
```

## See Also

### Functions

- llLog
- llLog10
- llSqrt

<!-- /wiki-source -->
