---
name: "llGetAttached"
category: "function"
type: "function"
language: "LSL"
description: "Returns the attach_point (an integer) the object is attached to or zero if it is either not attached or is pending detachment."
signature: "integer llGetAttached()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAttached'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetattached"]
---

Returns the attach_point (an integer) the object is attached to or zero if it is either not attached or is pending detachment.


## Signature

```lsl
integer llGetAttached();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAttached)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAttached) — scraped 2026-03-18_

Returns the attach_point (an integer) the object is attached to or zero if it is either not attached or is pending detachment.

## Examples

```lsl
default
{
    attach(key id)
    {
        if(id)//it's attached
        {
            if(llGetAttached() != ATTACH_LHAND)
            {
                llOwnerSay("Please attach me only to the left hand");
                llRequestPermissions(id, PERMISSION_ATTACH);
            }
        }
    }
    run_time_permissions(integer a)
    {
        if(a & PERMISSION_ATTACH)
            llDetachFromAvatar();
    }
}
```

This snippet will make a prim invisible when attached, but visible when rezzed unattached

```lsl
    on_rez(integer p)
    {
        // !llGetAttached() has the value 0 when attached, and 1 when unattached
        llSetAlpha( !llGetAttached(), ALL_SIDES);
    }
```

## See Also

### Events

- attach

### Functions

- llAttachToAvatar
- llDetachFromAvatar
- llGetAttachedList
- llGetAttachedListFiltered
- **llGetObjectDetails** — OBJECT_ATTACHED_POINT

<!-- /wiki-source -->
