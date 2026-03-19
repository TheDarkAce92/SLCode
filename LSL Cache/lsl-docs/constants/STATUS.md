---
name: "STATUS constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Bitmask constants for llSetStatus and llGetStatus controlling object physics, phantom, sandbox, and other behaviours"
wiki_url: "https://wiki.secondlife.com/wiki/STATUS_PHYSICS"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# STATUS_* Constants

Used with `llSetStatus` and `llGetStatus` to control and query object behaviour flags.

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `STATUS_PHYSICS` | 0x001 | Object is physical |
| `STATUS_ROTATE_X` | 0x002 | Object can rotate along X axis (physical only) |
| `STATUS_ROTATE_Y` | 0x004 | Object can rotate along Y axis (physical only) |
| `STATUS_ROTATE_Z` | 0x008 | Object can rotate along Z axis (physical only) |
| `STATUS_PHANTOM` | 0x010 | Object is phantom (passes through other objects) |
| `STATUS_SANDBOX` | 0x020 | Keep object within 10m and in same region |
| `STATUS_BLOCK_GRAB` | 0x040 | Prevent click-drag movement on root prim |
| `STATUS_DIE_AT_EDGE` | 0x080 | Delete (do not return) object if it leaves the region |
| `STATUS_RETURN_AT_EDGE` | 0x100 | Return to owner if object leaves the region |
| `STATUS_CAST_SHADOWS` | 0x200 | Reserved — not currently used |
| `STATUS_BLOCK_GRAB_OBJECT` | 0x400 | Prevent click-drag movement on all prims |
| `STATUS_DIE_AT_NO_ENTRY` | 0x800 | Delete (do not return) if object cannot enter a parcel |

## Usage

```lsl
// Enable physics
llSetStatus(STATUS_PHYSICS, TRUE);

// Enable phantom + block grab
llSetStatus(STATUS_PHANTOM | STATUS_BLOCK_GRAB, TRUE);

// Check if physical
if (llGetStatus(STATUS_PHYSICS))
    llOwnerSay("I'm physical");

// Restrict rotation to Z-axis only
llSetStatus(STATUS_ROTATE_X | STATUS_ROTATE_Y, FALSE);
llSetStatus(STATUS_ROTATE_Z, TRUE);
```

## See Also

- `llSetStatus` — set status flags
- `llGetStatus` — query status flags
- `STATUS_PHYSICS`, `STATUS_PHANTOM` (individual constant pages)
