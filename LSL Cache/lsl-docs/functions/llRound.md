---
name: "llRound"
category: "function"
type: "function"
language: "LSL"
description: "Rounds a float to the nearest integer (rounds half away from zero)"
wiki_url: "https://wiki.secondlife.com/wiki/llRound"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llRound(float val)"
parameters:
  - name: "val"
    type: "float"
    description: "The float to round"
return_type: "integer"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llround"]
deprecated: "false"
---

# llRound

```lsl
integer llRound(float val)
```

Returns `val` rounded to the nearest integer. Rounds half away from zero (0.5 → 1, -0.5 → -1).

## Examples

```lsl
llRound(1.4)  // 1
llRound(1.5)  // 2
llRound(1.6)  // 2
llRound(-1.5) // -2 (away from zero)
```

## See Also

- `llFloor` — round down to integer
- `llCeil` — round up to integer
- `llFabs` — absolute value of float
- `llAbs` — absolute value of integer


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRound) — scraped 2026-03-18_

Returns the integer that val is closest to.

## Caveats

- The returned value is -2147483648 (0x80000000) if the arithmetic result is outside of the range of valid integers (-2147483648 to 2147483647 inclusive).

## Examples

```lsl
default
{
   state_entry()
   {
       llSay(0,  "The rounded value of -4.9 is: "+(string)llRound(-4.9) );
       //Returns "The rounded value of -4.9 is: -5"

       llSay(0,  "The rounded value of -4.1 is: "+(string)llRound(-4.1) );
       //Returns "The rounded value of -4.1 is: -4"

       llSay(0,  "The rounded value of 4.5 is: "+(string)llRound(4.5) );
       //Returns "The rounded value of 4.5 is: 5"

       llSay(0,  "The rounded value of 4.9 is: "+(string)llRound(4.9) );
       //Returns "The rounded value of 4.9 is: 5"

       llSay(0,  "The rounded value of 4.1 is: "+(string)llRound(4.1) );
       //Returns "The rounded value of 4.1 is: 4"

       llSay(0,  "The rounded value of -4.5 is: "+(string)llRound(-4.5) );
       //Returns "The rounded value of -4.5 is: -4"
    }
}
```

## Notes

- For positive values, it is quicker to add 0.5 to the value and cast to an integer. i=(integer)(f+0.5) produces less bytecode than i=llRound(f) and is about 5 times faster in execution, while giving the same result.

## See Also

### Functions

- **llCeil** — Rounds the float to an integer towards positive infinity
- **llFloor** — Rounds the float to an integer towards negative infinity

<!-- /wiki-source -->
