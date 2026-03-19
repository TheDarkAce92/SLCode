---
name: "llFabs"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the positive version of val."
signature: "float llFabs(float val)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llFabs'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llfabs"]
---

Returns a float that is the positive version of val.


## Signature

```lsl
float llFabs(float val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `val` | Any valid float value |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llFabs)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llFabs) — scraped 2026-03-18_

Returns a float that is the positive version of val.

## Examples

```lsl
default
{
    state_entry()
    {
        llSay(0,"The (Float)absolute value of -4.5 is: "+(string)llFabs(-4.5) );
    }
}
// returns :
// The (Float)absolute value of -4.5 is: 4.500000
```

## Notes

- Using `val-2*val*(val<0)` is roughly 60% faster than llFabs as it avoids a function call, though it produces NaN if given an infinite value and (correctly) returns 0.0 instead of -0.0 when taking the absolute value of negative zero.

## See Also

### Functions

- **llAbs** — integer

### Articles

<!-- /wiki-source -->
