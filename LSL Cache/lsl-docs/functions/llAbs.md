---
name: "llAbs"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the positive version of val.

This function is similar to functions (e.g. abs) found in many other languages'
signature: "integer llAbs(integer val)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAbs'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llabs"]
---

Returns an integer that is the positive version of val.

This function is similar to functions (e.g. abs) found in many other languages


## Signature

```lsl
integer llAbs(integer val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `val` | Any integer value |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAbs)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAbs) — scraped 2026-03-18_

Returns an integer that is the positive version of val.

## Caveats

- The llAbs of -2147483648 is -2147483648. This is because the positive integer 2147483648 is outside the range of allowed LSL integer values.

## Examples

```lsl
default
{
    state_entry()
    {
//      returns: "The absolute value of -4 is: 4"
        llSay(PUBLIC_CHANNEL, "The absolute value of -4 is: "+(string)llAbs(-4) );
    }
}
```

```lsl
// Here's a more elaborate example.

ShowAbsolute(integer inputInteger)
{
    string output = "llAbs(" + (string)inputInteger + ") --> " + (string)llAbs(inputInteger);

    llSay(PUBLIC_CHANNEL, output);
}

default
{
    state_entry()
    {
        ShowAbsolute(-3);   //  llAbs(-3)  --> 3
        ShowAbsolute(5);    //  llAbs(5)   --> 5
        ShowAbsolute(-20);  //  llAbs(-20) --> 20
        ShowAbsolute(0);    //  llAbs(0)   --> 0
    }
}
```

## Notes

- Using `val-(val<<1)*(val<0)` is roughly two times faster than llAbs, as it avoids a function call and produces identical results.

## See Also

### Functions

- **llFabs** — float

### Articles

<!-- /wiki-source -->
