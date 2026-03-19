---
name: "llCeil"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the integer value of val rounded towards positive infinity (return >= val)."
signature: "integer llCeil(float val)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCeil'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llceil"]
---

Returns an integer that is the integer value of val rounded towards positive infinity (return >= val).


## Signature

```lsl
integer llCeil(float val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `val` | Any valid float value |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCeil)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCeil) — scraped 2026-03-18_

Returns an integer that is the integer value of val rounded towards positive infinity (return >= val).

## Caveats

- The returned value is -2147483648 (0x80000000) if the arithmetic result is outside of the range of valid integers (-2147483648 to 2147483647)

## Examples

```lsl
default
{
   state_entry()
   {
       llSay(0, "The ceil value of -4.5 is: " + (string)llCeil(-4.5));
//              "The ceil value of -4.5 is: -4"

       llSay(0, "The ceil value of -4.9 is: " + (string)llCeil(-4.9));
//              "The ceil value of -4.9 is: -4"

       llSay(0, "The ceil value of -4.1 is: " + (string)llCeil(-4.1));
//              "The ceil value of -4.1 is: -4"

       llSay(0, "The ceil value of 4.5 is: " + (string)llCeil(4.5));
//              "The ceil value of 4.5 is: 5"

       llSay(0, "The ceil value of 4.9 is: " + (string)llCeil(4.9));
//              "The ceil value of 4.9 is: 5"

       llSay(0, "The ceil value of 4.1 is: " + (string)llCeil(4.1));
//              "The ceil value of 4.1 is: 5"
    }
}
```

## See Also

### Functions

- **llRound** — Rounds the float to an integer towards the closest integer
- **llFloor** — Rounds the float to an integer towards negative infinity

<!-- /wiki-source -->
