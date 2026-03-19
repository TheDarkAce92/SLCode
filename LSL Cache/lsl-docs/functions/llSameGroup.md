---
name: "llSameGroup"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a boolean (an integer) that is TRUE if uuid and the prim the script is in are of the same group, otherwise FALSE.

This function compares the of what uuid describes.
It answers these two questions:
*'Is the script's prim in the same group as uuid?'
*'Is the of the script's prim equal to uuid'
signature: "integer llSameGroup(key id)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSameGroup'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsamegroup"]
---

Returns a boolean (an integer) that is TRUE if uuid and the prim the script is in are of the same group, otherwise FALSE.

This function compares the of what uuid describes.
It answers these two questions:
*"Is the script's prim in the same group as uuid?"
*"Is the of the script's prim equal to uuid?"


## Signature

```lsl
integer llSameGroup(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `uuid` | group, avatar or prim UUID that is in the same region |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSameGroup)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSameGroup) — scraped 2026-03-18_

Returns a boolean (an integer) that is TRUE if uuid and the prim the script is in are of the same group, otherwise FALSE.

## Caveats

- Not so obvious is that it returns TRUE if the object is not set to a group (i.e. "(none)") and either the AV with the given key has no group active or the function is called with a NULL_KEY.

## Examples

```lsl
// Gives inventory object only to agents with the same active group

default
{
    touch_start(integer total_number)
    {
        key id = llDetectedKey(0);

        integer sameGroup = llSameGroup(id);
//      same as llDetectedGroup(i) (with llDetectedGroup, detected does not need to be in the sim)

        if (sameGroup)
        {
            integer numberOfObjectsInPrim = llGetInventoryNumber(INVENTORY_OBJECT);

            if (numberOfObjectsInPrim)
                llGiveInventory(id, llGetInventoryName(INVENTORY_OBJECT, 0));
        }
        else
        {
            llRegionSayTo(id, 0, "Wrong active group!");
        }
    }
}
```

## Notes

#### Child Prims

It is possible for the group of a child prim to differ from that of the root prim. To build such an object it must first be unlinked, the groups set, and then relinked. Rezzing an object resets the group of the object to that of the group that the user currently has activated. Changing the group of an object changes the group for the entire object. This may only be an artifact or manifestation of VWR-5044.

## See Also

### Functions

- **llDetectedGroup** — detection
- **llGetAttachedList** — llGetObjectDetails

<!-- /wiki-source -->
