---
name: "llGetExperienceErrorMessage"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a text description of a particular Experience LSL error constant.

Returns a string describing the error code passed or the string corresponding to error. Returns XP_ERROR_UNKNOWN_ERROR if the error is not a valid error code.'
signature: "string llGetExperienceErrorMessage(integer value)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetExperienceErrorMessage'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llgetexperienceerrormessage"]
---

Returns a text description of a particular Experience LSL error constant.

Returns a string describing the error code passed or the string corresponding to error. Returns XP_ERROR_UNKNOWN_ERROR if the error is not a valid error code.


## Signature

```lsl
string llGetExperienceErrorMessage(integer value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (experience_error)` | `error` | The error code constant to translate. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetExperienceErrorMessage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetExperienceErrorMessage) — scraped 2026-03-18_

Returns a text description of a particular Experience LSL error constant.Returns a string describing the error code passed or the string corresponding to error. Returns XP_ERROR_UNKNOWN_ERROR if the error is not a valid error code.

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay(llGetExperienceErrorMessage(XP_ERROR_NONE));
    }
}
```

## Notes

#### Compiling

For a script to be associated with an Experience...

- It must be compiled with a client that is Experience aware,
- The "Use Experience" checkbox must be checked,
- And one of the users Experience keys selected.

|  | Important: Not all TPVs have this functionality. |
| --- | --- |

## See Also

### Events

- experience permissions_denied

### Functions

- llCreateKeyValue
- llReadKeyValue
- llUpdateKeyValue
- llDeleteKeyValue
- llDataSizeKeyValue
- llKeyCountKeyValue
- llKeysKeyValue

<!-- /wiki-source -->
