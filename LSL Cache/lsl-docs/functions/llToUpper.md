---
name: "llToUpper"
category: "function"
type: "function"
language: "LSL"
description: "Returns an uppercase version of the string"
wiki_url: "https://wiki.secondlife.com/wiki/llToUpper"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llToUpper(string src)"
parameters:
  - name: "src"
    type: "string"
    description: "The string to convert"
return_type: "string"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["lltoupper"]
deprecated: "false"
---

# llToUpper

```lsl
string llToUpper(string src)
```

Returns `src` with all ASCII lowercase letters converted to uppercase.

## Example

```lsl
llOwnerSay(llToUpper("hello world"));  // "HELLO WORLD"
```

## See Also

- `llToLower` — convert to lowercase
- `llStringTrim` — trim whitespace


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llToUpper) — scraped 2026-03-18_

Returns a string that is src with all upper-case characters.

## Caveats

- There is no Linden Library "llToProperCase", which would return *correctly* capitalized strings; However, there are user functions that do this: ToNormal
- The function also works for many characters outside the 7-bit ASCII range, especially latin, cyrillic and greek, but not all characters tagged as "lowercase" in the Unicode specification are converted.

## Examples

```lsl
string msg = "I like candy!";
string p = llToUpper(msg);
llOwnerSay(p);//Will say "I LIKE CANDY!"
```

## See Also

### Functions

- llToLower

<!-- /wiki-source -->
