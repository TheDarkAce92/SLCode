---
name: "llGetParcelFlags"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a bit field (an integer) of parcel flags (PARCEL_FLAG_*) for the parcel that includes the point pos.

Both x and y components of pos are clamped to the range [0.0, 256.0], the z component is ignored.'
signature: "integer llGetParcelFlags(vector pos)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetParcelFlags'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetparcelflags"]
---

Returns a bit field (an integer) of parcel flags (PARCEL_FLAG_*) for the parcel that includes the point pos.

Both x and y components of pos are clamped to the range [0.0, 256.0], the z component is ignored.


## Signature

```lsl
integer llGetParcelFlags(vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates (z component is ignored) |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelFlags)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelFlags) — scraped 2026-03-18_

Returns a bit field (an integer) of parcel flags (PARCEL_FLAG_*) for the parcel that includes the point pos.

## Examples

```lsl
if (!(llGetParcelFlags(llGetPos()) & PARCEL_FLAG_ALLOW_FLY))
    llSay(0,"You are not allowed to fly here!, Sorry!.");

// Answers TRUE if rezzing is permitted, FALSE if not.
// Rezzing can fail even if this returns TRUE due to parcel full or server errors.
// Rezzing will always fail if this returns FALSE
integer canRezAt(vector pos) {
    integer parcelFlags = llGetParcelFlags(pos);
    list parcelDetails = llGetParcelDetails(pos, [PARCEL_DETAILS_OWNER, PARCEL_DETAILS_GROUP]);
    key parcelOwner = llList2Key(parcelDetails, 0);
    key parcelGroup = llList2Key(parcelDetails, 1);

    if (parcelFlags & PARCEL_FLAG_ALLOW_CREATE_OBJECTS) return TRUE;
    if (parcelOwner == llGetOwner()) return TRUE;
    if (!llSameGroup(parcelGroup)) return FALSE;
    if (parcelFlags & PARCEL_FLAG_ALLOW_CREATE_GROUP_OBJECTS) return TRUE;
    return FALSE;
}

// Answers TRUE if running scripts is permitted, FALSE if not
integer canRunScriptsAt(vector pos) {
    integer parcelFlags = llGetParcelFlags(pos);
    list parcelDetails = llGetParcelDetails(pos, [PARCEL_DETAILS_OWNER, PARCEL_DETAILS_GROUP]);
    key parcelOwner = llList2Key(parcelDetails, 0);
    key parcelGroup = llList2Key(parcelDetails, 1);

    if (parcelFlags & PARCEL_FLAG_ALLOW_SCRIPTS) return TRUE;
    if (parcelOwner == llGetOwner()) return TRUE;
    if (!llSameGroup(parcelGroup)) return FALSE;
    if (parcelFlags & PARCEL_FLAG_ALLOW_GROUP_SCRIPTS) return TRUE;
    return FALSE;
}
```

## See Also

### Functions

- llGetParcelDetails
- llGetRegionFlags

<!-- /wiki-source -->
