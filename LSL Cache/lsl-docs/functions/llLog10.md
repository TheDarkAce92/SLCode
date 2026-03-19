---
name: "llLog10"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the base 10 logarithm of val.
If val <= 0 return zero instead.

To get the natural logarithm use llLog.
llLog10 should only be used where the base 10 log is needed, all other applications should use llLog instead.'
signature: "float llLog10(float val)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLog10'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllog10"]
---

Returns a float that is the base 10 logarithm of val.
If val <= 0 return zero instead.

To get the natural logarithm use llLog.
llLog10 should only be used where the base 10 log is needed, all other applications should use llLog instead.


## Signature

```lsl
float llLog10(float val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `val` |  |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLog10)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLog10) — scraped 2026-03-18_

Returns a float that is the base 10  logarithm of val.If val <= 0 return zero instead.

## Examples

```lsl
default
{
  state_entry()
  {
    float num1 = llFrand(100.0);

    llOwnerSay("The base 10 logarithm of " + (string)num1 + " is " + (string)llLog10(num1));
  }
}
```

## Notes

There are only two log functions llLog and llLog10. Errors introduced as a result of floating-point arithmetic are most noticable when working with logarithms. llLog should be used instead of llLog10 when converting the base of the logarithm.

```lsl
float LogBaseN = llLog(value) / llLog(Base); //This technique introduces errors but is the only way
```

## See Also

### Functions

- llLog
- llPow
- llSqrt

### Articles

<!-- /wiki-source -->
