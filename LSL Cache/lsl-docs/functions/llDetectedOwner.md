---
name: "llDetectedOwner"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the key (UUID) of the owner of the object.

number does not support negative indexes.
Returns an empty key if number does not relate to a valid sensed object'
signature: "key llDetectedOwner(integer number)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedOwner'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedowner"]
---

Returns the key (UUID) of the owner of the object.

number does not support negative indexes.
Returns an empty key if number does not relate to a valid sensed object


## Signature

```lsl
key llDetectedOwner(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedOwner)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedOwner) — scraped 2026-03-18_

Returns the key (UUID) of the owner of the object.

## Caveats

- If number is out of bounds  the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
default
{
    collision_start(integer num_detected)
    {
        string output =
            "\nkey of colliding object's owner ... or the colliding avatar: " + (string)llDetectedOwner(0)
            + "\nkey of this object's owner: " + (string)llGetOwner()
            + "\nname of colliding object/avatar: " + llDetectedName(0)
            + "\nkey of colliding object/avatar: " + (string)llDetectedKey(0)
            + "\nkey of the prim containing this script: " + (string)llGetKey()
            + "\nkey of this object's root prim: " + (string)llGetLinkKey(LINK_ROOT);
        llSay(0, output);
    }
}
```

## Notes

If the detected type is an avatar the key of that avatar is returned. Avatars are owned by themselves. llGetOwnerKey works the same way with regards to avatar UUIDs.

## See Also

### Functions

- **llGetOwnerKey** — llGetOwnerKey(llDetectedKey(number)) is the same as llDetectedOwner(number) only if the detected object is in the same region.
- llGetOwner

### Articles

- Detected

<!-- /wiki-source -->
