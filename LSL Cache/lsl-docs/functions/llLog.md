---
name: "llLog"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the natural logarithm of val.
If val <= 0 return 0.0 instead.

To get the base 10 logarithm use llLog10.'
signature: "float llLog(float val)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLog'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllog"]
---

Returns a float that is the natural logarithm of val.
If val <= 0 return 0.0 instead.

To get the base 10 logarithm use llLog10.


## Signature

```lsl
float llLog(float val);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llLog)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLog) — scraped 2026-03-18_

Returns a float that is the  natural logarithm of val.If val <= 0 return 0.0 instead.

## Examples

```lsl
default
{
  state_entry()
  {
    float num1 = llFrand(100.0);

    llOwnerSay("The natural logarithm of " + (string)num1 + " is " + (string)llLog(num1));
  }
}
```

```lsl
float findexp(float result, float base)
{
    return llLog(result)/llLog(base);
}
default
{
    touch_start(integer total_number)
    {
        llSay(0, (string)findexp(8.0,2.0));
        //returns 3.0
    }
}
```

## Notes

There are only two log functions llLog and llLog10. Errors introduced as a result of floating-point arithmetic are most noticable when working with logarithms. llLog should be used instead of llLog10 when converting the base of the logarithm.

```lsl
float LogBaseN = llLog(value) / llLog(Base); //This technique introduces errors but is the only way
```

If Base is a constant, your script will run faster if you calculate it's log and divide by that constant instead.



| Number | logarithm |
| --- | --- |
| 2 | {{#ln:2}} |
| 4 | {{#ln:4}} |
| 8 | {{#ln:8}} |
| 10 | {{#ln:10}} |
| 16 | {{#ln:16}} |
| 32 | {{#ln:32}} |
| 64 | {{#ln:64}} |
| 128 | {{#ln:128}} |
| 256 | {{#ln:256}} |

## See Also

### Functions

- llLog10
- llPow
- llSqrt

### Articles

<!-- /wiki-source -->
