---
name: "llHash"
category: "function"
type: "function"
language: "LSL"
description: "Returns a 32bit hash for the provided string. Returns 0 if the input string is empty."
signature: "integer llHash(string val)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llHash'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a 32bit hash for the provided string. Returns 0 if the input string is empty.


## Signature

```lsl
integer llHash(string val);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `val` | String to hash. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llHash)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llHash) — scraped 2026-03-18_

Returns a 32bit hash for the provided string. Returns 0 if the input string is empty.Returns an integer

## Caveats

This hash value is not cryptographically secure and should not be used as part of any security protocol.
SDBM provides a good distribution of hash values across its range, however with only
32 bits the chance of a collision is unacceptably high.(with 1000 entries, the odds for a collision are about 1 in 10000.)

## Examples

Given the combination of the object name and the owner's key generate a unique number.  This number could be used for things
like selecting a chat channel that has a low probability of colliding with another object.

```lsl
integer pickIDForObject()
{
    /* Generate an arbitrary integer ID for the combination of the
     * object name and the ower's key.  This value could be used
     * for selecting a chat/listen channel.
     */
    string obj_name = llGetObjectName();
    key obj_owner = llGetOwner();

    integer hash = llHash(obj_name + (string)obj_owner);

    return hash;
}
```

## See Also

### Functions

| • llOrd | Convert a character into an ordinal |  |  |  |
| --- | --- | --- | --- | --- |
| • llChar | Convert an ordinal into a character |  |  |  |

### Articles

- Hash Collision Probabilities

<!-- /wiki-source -->
