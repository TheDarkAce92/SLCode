---
name: "llIntegerToBase64"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is a Base64 big endian encode of number"
signature: "string llIntegerToBase64(integer number)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llIntegerToBase64'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llintegertobase64"]
---

Returns a string that is a Base64 big endian encode of number


## Signature

```lsl
string llIntegerToBase64(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llIntegerToBase64)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llIntegerToBase64) — scraped 2026-03-18_

Returns a string that is a Base64 big endian encode of number

## Examples

```lsl
string ASCII7ToString(integer letter)
{
    if(letter >= 0x80 || letter < 0) return "";//Not valid ascii7 character
    return llBase64ToString(llIntegerToBase64(letter << 24));
}
```

```lsl
// Packs a 24-bit unsigned integer value (0-16777215) to only 4 Base64 characters.
string Int24ToBase64(integer value)
{
    return llGetSubString(llIntegerToBase64(value<<8), 0, 3);
}
// unpacks a 4-character Base64 value to a 24-bit unsigned integer
integer Base64ToInt24(string value)
{
    return (llBase64ToInteger(value)>>8)&0xffffff; // Masking required to remove sign extension from bit-shifting
}
```

If you are looking for full Unicode translation, not just ASCII7 see: Combined_Library

## Notes

- Only the first 6 of the 8 characters returned are needed to decoded it back into an integer. The padding "==" can be safely removed for storage.
- "Big-endian" refers to the fact that the most significant, i.e. highest byte of the integer is processed first: the first characters in the returned Base64 string correspond to this byte, and the last characters correspond to the least significant byte.

  - Combined with bit-shifting, removing characters from the Base64 string allows more efficient packing of small values. See llBase64ToInteger caveats for specifics.

## See Also

### Functions

- llBase64ToInteger
- llBase64ToString
- llStringToBase64

<!-- /wiki-source -->
