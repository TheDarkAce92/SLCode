---
name: "llSqrt"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the square root of val.

For imaginary results (val < 0.0), a Math Error is triggered under LSO, or 'NaN' (Not A Number) is returned under Mono'
signature: "float llSqrt(float val)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSqrt'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsqrt"]
---

Returns a float that is the square root of val.

For imaginary results (val < 0.0), a Math Error is triggered under LSO, or 'NaN' (Not A Number) is returned under Mono


## Signature

```lsl
float llSqrt(float val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `val` | positive number (val >= 0.0) |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSqrt)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSqrt) — scraped 2026-03-18_

Returns a float that is the square root of val.

## Caveats

- Crashes the script if passed a negative number.

## Examples

```lsl
default
{
  state_entry()
  {
    float num1 = llFrand(100.0);

    llOwnerSay("The square root of " + (string)num1 + " is " + (string)llSqrt(num1));
  }
}
```

## Notes

- If you need the square root of two, you can use the constant SQRT2.
- Other roots can be computed by llPow(**val**, 1.0/**root**).

## See Also

### Functions

- llLog
- llLog10
- llPow

<!-- /wiki-source -->
