---
name: "llToLower"
category: "function"
type: "function"
language: "LSL"
description: "Returns a lowercase version of the string"
wiki_url: "https://wiki.secondlife.com/wiki/llToLower"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llToLower(string src)"
parameters:
  - name: "src"
    type: "string"
    description: "The string to convert"
return_type: "string"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["lltolower"]
deprecated: "false"
---

# llToLower

```lsl
string llToLower(string src)
```

Returns `src` with all ASCII uppercase letters converted to lowercase. Non-ASCII characters are unchanged.

## Example

```lsl
llOwnerSay(llToLower("Hello World"));  // "hello world"

// Case-insensitive comparison
if (llToLower(message) == "hello")
    llSay(0, "Hi there!");
```

## See Also

- `llToUpper` — convert to uppercase
- `llStringTrim` — trim whitespace
- `llSubStringIndex` — find substring (case-sensitive)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llToLower) — scraped 2026-03-18_

Returns a string that is src with all lower-case letters

## Caveats

- There is no Linden Library "llToProperCase", which would return *correctly* capitalized strings; However, there are user functions that do this: ToNormal
- The function also works for many characters outside the 7-bit ASCII range, especially latin, cyrillic and greek, but not all characters tagged as "uppercase" in the Unicode specification are converted.

## Examples

```lsl
string msg = "I like CANDY!";
string p = llToLower(msg);
llOwnerSay(p);//Will say "i like candy!"
```

## See Also

### Functions

- llToUpper

<!-- /wiki-source -->
