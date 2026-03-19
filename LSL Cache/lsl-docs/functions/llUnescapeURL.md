---
name: "llUnescapeURL"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is an unescaped/unencoded version of url, replacing '%20' with spaces etc.

This function is similar to functions (e.g. urldecode, decodeURIComponent) found in many other languages'
signature: "string llUnescapeURL(string url)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llUnescapeURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llunescapeurl"]
---

Returns a string that is an unescaped/unencoded version of url, replacing "%20" with spaces etc.

This function is similar to functions (e.g. urldecode, decodeURIComponent) found in many other languages


## Signature

```lsl
string llUnescapeURL(string url);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `url` | A (preferably valid and escaped URL) string. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llUnescapeURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llUnescapeURL) — scraped 2026-03-18_

Returns a string that is an unescaped/unencoded version of url, replacing "%20" with spaces etc.

## Caveats

- The  [hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal) encoded representation of  [UTF-8](https://en.wikipedia.org/wiki/UTF-8)  [byte](https://en.wikipedia.org/wiki/Byte) encoding is the only supported means of access to non ASCII7 characters (Unicode characters).

  - Decoding of Unicode as `"%u####"` is not supported.
- The `"+"` character is not decoded as a space.

## Examples

```lsl
string str = "http://wiki.secondlife.com/wiki/LSL Portal";

default
{
    state_entry()
    {
        llOwnerSay("Plain string:\n\t" + str);
        // output: "http://wiki.secondlife.com/wiki/LSL Portal"

        llOwnerSay("Escaped string:\n\t" + llEscapeURL(str));
        // output: "http%3A%2F%2Fwiki%2Esecondlife%2Ecom%2Fwiki%2FLSL%20Portal"

        llOwnerSay("Escaped string unescaped again:\n\t" + llUnescapeURL( llEscapeURL(str) ));
        // output: "http://wiki.secondlife.com/wiki/LSL Portal"

        // because escaping and unescaping are exact opposite
        // and unescaping an escaped string returns the original

        //  For readability's sake it would make more sense to do:
        llOwnerSay("For readability's sake:\n\t" + "http://wiki.secondlife.com/wiki/" + llEscapeURL("LSL Portal"));
        // output: "http://wiki.secondlife.com/wiki/LSL%20Portal"
    }
}
```

## See Also

### Functions

- **llEscapeURL** — Opposite of llUnescapeURL

### Articles

- UTF-8
- Base64
- **Combined Library: UnicodeIntegerToUTF8** — Easily convert unicode character codes to string form.

<!-- /wiki-source -->
