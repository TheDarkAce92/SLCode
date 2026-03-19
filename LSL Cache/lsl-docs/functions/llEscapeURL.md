---
name: "llEscapeURL"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the escaped/encoded version of url, replacing spaces with '%20' etc. The function will escape any character not in [a-zA-Z0-9] to '%xx' where 'xx' is the hexadecimal value of the character in UTF-8 byte form.

To clarify, numbers and ASCII7 alphabetical characters are NOT es'
signature: "string llEscapeURL(string url)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llEscapeURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llescapeurl"]
---

Returns a string that is the escaped/encoded version of url, replacing spaces with "%20" etc. The function will escape any character not in [a-zA-Z0-9] to "%xx" where "xx" is the hexadecimal value of the character in UTF-8 byte form.

To clarify, numbers and ASCII7 alphabetical characters are NOT escaped. If a character requires more then one byte in UTF-8 byte form then it returns multiple "%xx" sequences chained together.

This function is similar to functions (e.g. rawurlencode, encodeURIComponent) found in many other languages


## Signature

```lsl
string llEscapeURL(string url);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `url` | A (preferably valid and unescaped URL) string. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llEscapeURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llEscapeURL) — scraped 2026-03-18_

Returns a string that is the escaped/encoded version of url, replacing spaces with "%20" etc. The function will escape any character not in [a-zA-Z0-9] to "%xx" where "xx" is the  hexadecimal value of the character in  UTF-8  byte form.

## Caveats

The function is not appropriate for escaping a url all at once, because the `":"` after the protocol, and all of the `"/"` characters delimiting the various parts, will be escaped. Instead, build the url in parts; escaping parts of the path and query string arguments as needed.

Sample URL: [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/foo/bar?arg=gra](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/foo/bar?arg=gra)

| URL part | example |
| --- | --- |
| base URL | https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322 |
| trailing path | /foo/bar |
| query string past the first "?" in the URL | arg=gra |

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

## Notes

- The SL viewer pretty prints URLs when converting them to clickable links in chat and dialogs. To confirm that a URL was escaped as intended, right-click the URL and copy, then paste to inspect it in the chat bar; or wrap it between "..."; or examine your chat log in an external editor; or display the string with an alternative function like llSetText.

## See Also

### Functions

| • llUnescapeURL |  |  |  |  |
| --- | --- | --- | --- | --- |

### Articles

| • UTF-8 |  |  |  |  |
| --- | --- | --- | --- | --- |
| • Base64 |  |  |  |  |

<!-- /wiki-source -->
