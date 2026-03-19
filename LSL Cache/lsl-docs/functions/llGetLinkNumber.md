---
name: "llGetLinkNumber"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the link number of the prim containing the script.

0 means the prim is not linked, 1 the prim is the root, 2 the prim is the first child, etc. Links are numbered in the reverse order in which they were linked -- if you select a box, a sphere and a cylinder in that order, '
signature: "integer llGetLinkNumber()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetLinkNumber'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetlinknumber"]
---

Returns an integer that is the link number of the prim containing the script.

0 means the prim is not linked, 1 the prim is the root, 2 the prim is the first child, etc. Links are numbered in the reverse order in which they were linked -- if you select a box, a sphere and a cylinder in that order, then link them, the cylinder is 1, the sphere is 2 and the box is 3. The last selected prim has the lowest link number.


## Signature

```lsl
integer llGetLinkNumber();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetLinkNumber)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetLinkNumber) — scraped 2026-03-18_

Returns an integer that is the link number of the prim containing the script.

## Caveats

- By design may equal llGetNumberOfPrims, *e.g.*, when prim is last, object contains multiple prims, and no sitting avatars

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay((string) llGetLinkNumber());
        llOwnerSay((string) llGetNumberOfPrims());
    }
}
```

A non-obvious feature is using double-negation to obtain a link number zero (for an unlinked prim) or one (for the root of a linkset). Unlike constants like LINK_ROOT, this number can be used directly with functions like llGetLinkPrimitiveParams without first determining whether a prim is part of a linkset:

```lsl
default
{
    state_entry()
    {
        integer rootLinkNum = !!llGetLinkNumber();
        // returns 0 in an unlinked prim, 1 in a linkset

        integer isFullBright = llList2Integer(llGetLinkPrimitiveParams(rootLinkNum,[PRIM_FULLBRIGHT, ALL_SIDES]),0);
        // TRUE if all sides of an unlinked prim or the root of a linkset are set to full bright, FALSE otherwise
    }
}
```

## See Also

### Functions

- llGetKey
- llGetNumberOfPrims

<!-- /wiki-source -->
