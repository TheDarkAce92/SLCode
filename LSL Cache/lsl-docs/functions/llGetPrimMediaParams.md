---
name: "llGetPrimMediaParams"
category: "function"
type: "function"
language: "LSL"
description: 'Get the media params for a particular face on an object, given the desired list of names.

Returns a parameter list (a list) of values in the order requested.

Returns an empty list if no media exists on the face.'
signature: "list llGetPrimMediaParams(integer face, list params)"
return_type: "list"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetPrimMediaParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetprimmediaparams"]
---

Get the media params for a particular face on an object, given the desired list of names.

Returns a parameter list (a list) of values in the order requested.

Returns an empty list if no media exists on the face.


## Signature

```lsl
list llGetPrimMediaParams(integer face, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number |
| `list (instructions)` | `params` | a set of name (in no particular order) |


## Return Value

Returns `list`.


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetPrimMediaParams)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetPrimMediaParams) — scraped 2026-03-18_

Get the media params for a particular face on an object, given the desired list of names.Returns a parameter list (a list) of values in the order requested.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- If face indicates a face that does not exist the  return is an empty list.

## See Also

### Functions

- llGetLinkMedia
- llSetPrimMediaParams
- llSetLinkMedia
- llClearPrimMedia
- llClearLinkMedia

<!-- /wiki-source -->
