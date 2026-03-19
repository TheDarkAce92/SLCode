---
name: "llSetRegionPos"
category: "function"
type: "function"
language: "LSL"
description: 'Tries to move the entire object so that the root prim is within 0.1m of position.

Returns an integer boolean, TRUE if the object is successfully placed within 0.1 m of position, FALSE otherwise. See #Specification for details.

Only if TRUE is returned does the object move, if FALSE is returned, th'
signature: "integer llSetRegionPos(vector pos)"
return_type: "integer"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llSetRegionPos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetregionpos"]
---

Tries to move the entire object so that the root prim is within 0.1m of position.

Returns an integer boolean, TRUE if the object is successfully placed within 0.1 m of position, FALSE otherwise. See #Specification for details.

Only if TRUE is returned does the object move, if FALSE is returned, the object does not change position.


## Signature

```lsl
integer llSetRegionPos(vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `position` | position in region coordinates |


## Return Value

Returns `integer`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetRegionPos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetRegionPos) — scraped 2026-03-18_

Tries to move the entire object so that the root prim is within 0.1m of position.Returns a boolean (an integer) , TRUE if the object is successfully placed within 0.1 m of position, FALSE otherwise. See #Specification for details.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        vector currentPosition = llGetPos();

        // check whether the object has successfully been moved
        // to the center of the sim at the same height
        integer hasMoved = llSetRegionPos(<128.0, 128.0, currentPosition.z>);

        if (hasMoved)
        {
            llOwnerSay("My new position is now:\n"
                + "http://maps.secondlife.com/secondlife/" + llEscapeURL(llGetRegionName())
                + "/128/128/" + (string)llRound(currentPosition.z) + "/");
        }
        else if ( currentPosition.z < llGround(ZERO_VECTOR) )
        {
            llOwnerSay("My new position is now:\n"
                + "http://maps.secondlife.com/secondlife/" + llEscapeURL(llGetRegionName())
                + "/128/128/" + (string)llCeil(llGround(ZERO_VECTOR)) + "/");
        }
        else
            llOwnerSay("Move was not possible!");
    }
}
```

## Notes

This function is intended to replace WarpPos.

## See Also

### Functions

- **llGetLocalPos** — Returns the prim's local position if it is attached or non-root (otherwise it returns the global position)
- **llGetRootPosition** — Gets the root prims position
- **llGetPos** — Returns the prim's global position, even if it is attached or non-root
- llSetPos
- llEdgeOfWorld

<!-- /wiki-source -->
