---
name: "llBase64ToString"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the Base64 str decoded into a conventional string, interpreting the Base64-encoded bytes as UTF-8 character sequence."
signature: "string llBase64ToString(string str)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llBase64ToString'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llbase64tostring"]
---

Returns a string that is the Base64 str decoded into a conventional string, interpreting the Base64-encoded bytes as UTF-8 character sequence.


## Signature

```lsl
string llBase64ToString(string str);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `str` | Base64 string |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llBase64ToString)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llBase64ToString) — scraped 2026-03-18_

Returns a string that is the Base64 str decoded into a conventional string, interpreting the Base64-encoded bytes as UTF-8 character sequence.

## Caveats

- If the conversion creates any unprintable characters, they are converted to spaces.
- Converts invalid characters into question marks ('?').

## Examples

```lsl
default {
    state_entry()
    {
        string test = llBase64ToString("U2VjcmV0Ok9wZW4=");
        llSay(0,test );
    }
}
```

This can be used in  [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication), such as this login:

```lsl
GET / HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)
Host: www.example.com
Authorization: Basic U2VjcmV0Ok9wZW4=
```

```lsl
llBase64ToString("U2VjcmV0Ok9wZW4="); //will return the string "Secret:Open"
```

## See Also

### Functions

- **llXorBase64** — Article also discusses xor based Cryptography.
- llStringToBase64
- llBase64ToInteger

### Articles

- Base64

<!-- /wiki-source -->
