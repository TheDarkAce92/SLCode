---
name: "LINK constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Constants for targeting linked prims in llMessageLinked, llSetLinkPrimitiveParamsFast, and related functions"
wiki_url: "https://wiki.secondlife.com/wiki/LINK_ROOT"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# LINK_* Constants

Used to specify which prim(s) to target in link-related functions.

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `LINK_ROOT` | 1 | The root prim of the linkset |
| `LINK_SET` | -1 | All prims in the linkset |
| `LINK_ALL_OTHERS` | -2 | All prims except the one containing this script |
| `LINK_ALL_CHILDREN` | -3 | All child prims (not the root) |
| `LINK_THIS` | -4 | The prim containing this script |

## Notes

- Link numbers 1 and above refer to specific prims: 1 = root, 2+ = child prims.
- `LINK_ROOT` (1) is equivalent to using the literal integer 1.
- An unlinked single prim: `llGetLinkNumber()` returns 0.
- Use `llGetNumberOfPrims()` to count prims in the linkset.

## Usage

```lsl
// Send message to all prims
llMessageLinked(LINK_SET, 1, "activate", NULL_KEY);

// Send to all except sending prim
llMessageLinked(LINK_ALL_OTHERS, 0, "ping", NULL_KEY);

// Set colour on root prim only
llSetLinkPrimitiveParamsFast(LINK_ROOT,
    [PRIM_COLOR, ALL_SIDES, <1.0, 0.0, 0.0>, 1.0]);

// Set colour on all children
llSetLinkPrimitiveParamsFast(LINK_ALL_CHILDREN,
    [PRIM_COLOR, ALL_SIDES, <0.0, 1.0, 0.0>, 1.0]);
```

## See Also

- `llMessageLinked` — send inter-script messages
- `llSetLinkPrimitiveParamsFast` — set prim parameters on linked prims
- `llGetLinkNumber` — get the current prim's link number
- `llGetNumberOfPrims` — count prims in linkset
- `llGetLinkName` — get name of a specific linked prim
- `llGetLinkKey` — get UUID of a specific linked prim
