---
name: "llModPow"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is a raised to the b power, mod c. ( (a**b)%c )"
signature: "integer llModPow(integer a, integer b, integer c)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llModPow'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llmodpow"]
---

Returns an integer that is a raised to the b power, mod c. ( (a**b)%c )


## Signature

```lsl
integer llModPow(integer a, integer b, integer c);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `a` |  |
| `integer` | `b` |  |
| `integer` | `c` |  |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.
- **No forced delay** — the 1.0-second delay was removed in the January 2025 update.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llModPow)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llModPow) — scraped 2026-03-18_

Returns an integer that is a raised to the b power, mod c. ( (a**b)%c )

## Examples

```lsl
integer x = llModPow(13743, 14200, 10000); // = 1
integer y = llModPow(0xc734abfa, 0x8371b314, 0xffffffff); // = -1481328730, corresponding to unsigned value of 2813638566
```

## Notes

- Internally, the parameters are considered unsigned integers. This means it's possible to get extra range by using negative values or hexadecimal, and interpreting the result as such as well.
- This function used to have a forced delay of 1.0 and precision issues before an update in January 2025.

<!-- /wiki-source -->
