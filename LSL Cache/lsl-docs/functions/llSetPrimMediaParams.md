---
name: "llSetPrimMediaParams"
category: "function"
type: "function"
language: "LSL"
description: 'Set the media params for a particular face.

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation(s).'
signature: "integer llSetPrimMediaParams(integer face, list params)"
return_type: "integer"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetPrimMediaParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetprimmediaparams"]
---

Set the media params for a particular face.

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation(s).


## Signature

```lsl
integer llSetPrimMediaParams(integer face, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number |
| `list (instructions)` | `params` | a set of name/value pairs (in no particular order) |


## Return Value

Returns `integer`.


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetPrimMediaParams)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetPrimMediaParams) — scraped 2026-03-18_

Set the media params for a particular face.Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation(s).

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- The function silently fails if its face value indicates a face that does not exist.
- If prim-media is not already on this object, add it.
- Params not specified are unchanged, or if new media is added set to the default specified.
- Both width and height must be specified together to work, and they narrow the texture space while inversely widening the aperture.

  - width and height scaled larger than 1024pixels will require the texture backdrop to be resized to fit(see Useful Snippets)

  - if resized to fit, the resulting view will cut off scrolled content outside the bounds making it impossible to be viewed
- Face needs to be a single face. If you want the media on multiple faces (e. g. opposing sides of an object), you have to call the function multiple times with different face numbers. Bitwise AND for face numbers does not work.

## See Also

### Functions

- llSetLinkMedia
- llGetPrimMediaParams
- llClearPrimMedia

### Articles

- /Tricks

<!-- /wiki-source -->
