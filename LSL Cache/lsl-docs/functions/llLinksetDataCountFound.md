---
name: "llLinksetDataCountFound"
category: "function"
type: "function"
language: "LSL"
description: 'The llLinksetDataCountFound function returns the number of keys in the linkset datastore that match the pattern supplied in the pattern.

Returns an integer Count of the keys in the datastore that match the supplied pattern.'
signature: "integer llLinksetDataCountFound(string pattern)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataCountFound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

The llLinksetDataCountFound function returns the number of keys in the linkset datastore that match the pattern supplied in the pattern.

Returns an integer Count of the keys in the datastore that match the supplied pattern.


## Signature

```lsl
integer llLinksetDataCountFound(string pattern);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `pattern` | A regular expression describing which keys to return. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataCountFound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataCountFound) — scraped 2026-03-18_

The llLinksetDataCountFound function returns the number of keys in the linkset datastore that match the pattern supplied in the pattern.Returns an integer Count of the keys in the datastore that match the supplied pattern.

## Examples

The following regular expression code can be used to count UUID keys. (Such as those use to identify user UUID)

```lsl
        integer numKeysFound = llLinksetDataCountFound("(?i)^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$",  0, 0);
```

The following code can also be used to count UUID keys in LinksetData memory.

```lsl
        integer numKeysFound = llLinksetDataCountFound("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",  0, 0);
```

## Notes

### Regular Expression Cheat Sheet

| Wildcard |  |  |
| --- | --- | --- |
| . | Matches any character |  |
| Anchors |  |  |
| ^ | Matches the beginning of the string. |  |
| $ | Matches the end of the string. |  |
| Expression Prefixes |  |  |
| (?i) | Makes search string case insensitive. | This must be the first thing that appears in the search string. "(?i)apple" will match "apple", "APPLE", "ApPlE", and any other combination of upper and lower case characters. |
| $ | Matches the end of the string. |  |
| Repeats |  |  |
| * | Matches the preceding atom 0 or more times. |  |
| + | Matches the preceding atom 1 or more times. |  |
| ? | Matches the preceding atom 0 or 1 times. |  |
| {n} {n,} {n, m} | Matches the preceding atom n, n or more, or between n and m times. |  |
| Sub-expressions |  |  |
| (expression) | Text enclosed in parentheses is a marked sub-expression. Text matched as part of a sub-expressions is split out and may be repeated. |  |
| Alternation |  |  |
| a \| b | Match either a or b. |  |
| Character Sets |  |  |
| [abc] | Matches any one of the enumerated characters. |  |
| [a-c] | Matches any character in the specified range. |  |
| [^abc] | Matches any character other than the enumerated characters. |  |
| [[:name:]] | Matches any character of the named class. |  |
|  | Any of the above character set definitions may be combined. |  |
| Escape Sequences |  |  |
|  | Specific Characters |  |
| \e | ASCII 0x1B, ESC |  |
| \n | New line |  |
| \r | Carriage return |  |
| \t | Tab |  |
| \xdd | Matches an ASCII character with the code dd |  |
|  | Single character classes |  |
| \d \D | Any decimal digit. | - **\d** → [[:digit:]] or [0-9] - **\D** → [^[:digit:]] or [^0-9] |
| \l \L | Any lower case character. | - **\l** → [[:lower:]] or [a-z] - **\L** → [^[:lower:]] or [^a-z] |
| \s \S | Any whitespace character. | - **\s** → [[:space:]] or [ \t\r\n] - **\S** → [^[:space:]] or [^ \t\r\n] |
| \u \U | Any upper case character. | - **\u** → [[:upper:]] or [A-Z] - **\U** → [^[:upper:]] or [^A-Z] |
| \w \W | Any "word" character. Alphanumeric plus underscore | - **\w** → [[:upper:][:lower:][:digit:]_] or [A-Za-z0-9_] - **\W** → [^[:upper:][:lower:][:digit:]_] or [^A-Za-z0-9_] |
|  | Word boundaries |  |
| \< | Start of word. |  |
| \> | End of word |  |
| \b |  |  |
| \B | Not a word boundary. |  |
| *Note* LSL uses '\' as an escape character in strings. The escape characters above must be double escaped. So "\d" needs to be written in LSL as "\\d" Please see LSL Strings, Escape Codes |  |  |
| Named Character Classes |  |  |
| alnum | Any alpha-numeric character. | - [[:alnum:]] → [0-9a-zA-Z] - [^[:alnum:]] → [^0-9a-zA-Z] |
| alpha | Any alphabetic character. | - [[:alpha:]] → [a-zA-Z] - [^[:alpha:]] → [^a-zA-Z] |
| blank | Any whitespace character that is not a line separator. |  |
| cntrl | Any control character | - [[:cntrl:]] → [\x01-\x31] - [^[:cntrl:]] → [^\x01-\x31] |
| digit d | Any decimal digit | - [[:digit:]] → [0-9] - [^[:digit:]] → [^0-9] |
| lower l | Any lower case character. | - [[:lower:]] → [a-z] - [^[:lower:]] → [^a-z] |
| print | Any printable character. |  |
| punct | Any punctiation character. |  |
| space s | Any whitespace character. |  |
| upper u | Any upper case character. | - [[:upper:]] → [A-Z] - [^[:upper:]] → [^A-Z] |
| word w | Any control character | - [[:word:]] → [0-9a-zA-Z_] - [^[:word:]] → [^0-9a-zA-Z_] |
| xdigit | Any hexadecimal digit character | - [[:xdigit:]] → [0-9a-fA-F] - [^[:xdigit:]] → [^0-9a-fA-F] |

## See Also

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataDelete
- llLinksetDataDeleteProtected
- llLinksetDataListKeys
- llLinksetDataRead
- llLinksetDataReadProtected
- llLinksetDataReset
- llLinksetDataWrite
- llLinksetDataWriteProtected

<!-- /wiki-source -->
