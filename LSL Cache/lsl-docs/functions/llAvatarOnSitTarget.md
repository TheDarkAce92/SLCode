---
name: "llAvatarOnSitTarget"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a key that is the UUID of the user seated on the prim.

If the prim lacks a sit target or there is no avatar sitting on the prim, then NULL_KEY is returned.'
signature: "key llAvatarOnSitTarget()"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAvatarOnSitTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llavataronsittarget"]
---

Returns a key that is the UUID of the user seated on the prim.

If the prim lacks a sit target or there is no avatar sitting on the prim, then NULL_KEY is returned.


## Signature

```lsl
key llAvatarOnSitTarget();
```


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAvatarOnSitTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAvatarOnSitTarget) — scraped 2026-03-18_

Returns a key that is the UUID of the user seated on the prim.

## Caveats

- A prim does not have a sit target unless llSitTarget has been called with a **nonzero** vector as the first argument.
- If the prim lacks a sit target or the avatar is seated upon a different prim, the only way to determine how many and which avatars are seated upon the object is to scan the link set (for an example of this, see llGetNumberOfPrims).

## Examples

```lsl
default
{
    state_entry()
    {
        // set sit target, otherwise this will not work
        llSitTarget(<0.0, 0.0, 0.1>, ZERO_ROTATION);
    }

    changed(integer change)
    {
        if (change & CHANGED_LINK)
        {
            key av = llAvatarOnSitTarget();
            if (av) // evaluated as true if key is valid and not NULL_KEY
            {
                llSay(0, "Hello " + llKey2Name(av) + ", thank you for sitting down");
            }
        }
    }
}
```

## Notes

The position of an avatar on a sit target can be determined with the use of llGetObjectDetails (see llSitTarget for an example).

## See Also

### Events

- changed

### Functions

- llAvatarOnLinkSitTarget
- llSitTarget
- llLinkSitTarget
- llGetLinkKey

### Articles

- CHANGED_LINK

<!-- /wiki-source -->
