---
name: "llDetectedGroup"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is TRUE if the detected object or agent has the same active group as the prim containing the script. Otherwise FALSE is returned.

number does not support negative indexes.
Returns FALSE if number is out of range.'
signature: "integer llDetectedGroup(integer number)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedGroup'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedgroup"]
---

Returns an integer that is TRUE if the detected object or agent has the same active group as the prim containing the script. Otherwise FALSE is returned.

number does not support negative indexes.
Returns FALSE if number is out of range.


## Signature

```lsl
integer llDetectedGroup(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedGroup)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedGroup) — scraped 2026-03-18_

Returns a boolean (an integer) that is TRUE if the detected object or agent has the same active group as the prim containing the script. Otherwise FALSE is returned.

## Caveats

- If number is out of bounds this function returns FALSE and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.
- There is no way to detect if the prim is in the same group as one of the agent's inactive groups.

## Examples

```lsl
//Gives inventory only to agents with the same active group
default
{
    touch_start(integer total_number)
    {
        if (llDetectedGroup(0) )     //same as llSameGroup(llDetectedKey(0) ) (with llSameGroup, detected must be in the sim)
            llGiveInventory(llDetectedKey(0), llGetInventoryName(INVENTORY_OBJECT, 0) );
        else
            llSay(0, "Wrong active group!");
    }
}
```

## Notes

#### Child Prims

It is possible for the group of a child prim to differ from that of the root prim. To build such an object it must first be unlinked, the groups set, and then relinked. Rezzing an object resets the group of the object to that of the group that the user currently has activated. Changing the group of an object changes the group for the entire object. This may only be an artifact or manifestation of VWR-5044.

## See Also

### Functions

- llSameGroup

### Articles

- Detected

<!-- /wiki-source -->
