---
name: "llFloor"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the integer value of val rounded towards negative infinity (return <= val)."
signature: "integer llFloor(float val)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llFloor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llfloor"]
---

Returns an integer that is the integer value of val rounded towards negative infinity (return <= val).


## Signature

```lsl
integer llFloor(float val);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llFloor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llFloor) — scraped 2026-03-18_

Returns an integer that is the integer value of val rounded towards negative infinity (return <= val).

## Caveats

- The returned value is -2147483648 (0x80000000) if the arithmetic result is outside of the range of valid integers (-2147483648 to 2147483647 inclusive).

## Examples

```lsl
default
{
   state_entry()
   {
       llSay(0,  "The floor value of -4.5 is: "+(string)llFloor(-4.5) );
       //Returns "The floor value of -4.5 is: -5"

       llSay(0,  "The floor value of -4.9 is: "+(string)llFloor(-4.9) );
       //Returns "The floor value of -4.9 is: -5"

       llSay(0,  "The floor value of -4.1 is: "+(string)llFloor(-4.1) );
       //Returns "The floor value of -4.1 is: -5"

       llSay(0,  "The floor value of 4.5 is: "+(string)llFloor(4.5) );
       //Returns "The floor value of 4.5 is: 4"

       llSay(0,  "The floor value of 4.9 is: "+(string)llFloor(4.9) );
       //Returns "The floor value of 4.9 is: 4"

       llSay(0,  "The floor value of 4.1 is: "+(string)llFloor(4.1) );
       //Returns "The floor value of 4.1 is: 4"
    }
}
```

## Notes

- For positive values, it is quicker and shorter to simply cast the float to an integer. i=(integer)f is 32 bytes shorter than i=llFloor(f) (in Byte Code) and about 30 times faster in execution, while giving the same result.

## See Also

### Functions

- **llRound** — Rounds the float to an integer towards the closest integer
- **llCeil** — Rounds the float to an integer towards positive infinity

<!-- /wiki-source -->
