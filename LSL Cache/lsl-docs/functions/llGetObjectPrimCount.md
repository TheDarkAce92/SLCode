---
name: "llGetObjectPrimCount"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the total number of prims in the object that contains prim.

Avatars sitting on the object are not counted is not a prim.'
signature: "integer llGetObjectPrimCount(key object_id)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectPrimCount'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetobjectprimcount"]
---

Returns an integer that is the total number of prims in the object that contains prim.

Avatars sitting on the object are not counted is not a prim.


## Signature

```lsl
integer llGetObjectPrimCount(key object_id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `prim` | prim UUID that is in the same region |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectPrimCount)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectPrimCount) — scraped 2026-03-18_

Returns an integer that is the total number of prims in the object that contains prim.

## Caveats

- This cannot be used to detect if an avatar is seated (by checking for a non-zero return), use llGetAgentInfo instead.
- The prim count for attachments are not returned. If possible use llGetNumberOfPrims instead.

## Examples

```lsl
default
{
    touch_start(integer num)
    {
        integer prims = llGetObjectPrimCount(llGetKey());
        if (prims == 0)
        {
            // llGetObjectPrimCount returns zero for attachments.
            prims = llGetNumberOfPrims();
            // Avatars can't sit on attachments so this is ok.
        }
        llOwnerSay("This object has "
                    + (string)prims
                    + " prims and "
                    + (string)(llGetNumberOfPrims() - prims)
                    + " avatars.");
    }
}
```

## See Also

### Functions

- **llGetNumberOfPrims** — Returns the number of prims in the current object.
- **llGetObjectLinkKey** — Returns the key of the link in the linkset an object.

<!-- /wiki-source -->
