---
name: "llGetRegionFlags"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the region flags (REGION_FLAG_*) for the region the object is in.

Only a small number of flags are actually used; the rest (shown below in strike-through) are always zero.  In particular, it is not possible to detect the status of 'Allow Land Resell', 'Allow Land Join/Div'
signature: "integer llGetRegionFlags()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionFlags'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetregionflags"]
---

Returns an integer that is the region flags (REGION_FLAG_*) for the region the object is in.

Only a small number of flags are actually used; the rest (shown below in strike-through) are always zero.  In particular, it is not possible to detect the status of "Allow Land Resell", "Allow Land Join/Divide", or "Block Land Show in Search"; nor, obviously, it is possible for a script to detect that "Disable Scripts" has been set.


## Signature

```lsl
integer llGetRegionFlags();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionFlags)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionFlags) — scraped 2026-03-18_

Returns an integer that is the region flags (REGION_FLAG_*) for the region the object is in.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        if( llGetRegionFlags() & REGION_FLAG_SANDBOX )
        {
            llOwnerSay("Region is a sandbox.");
        }
        else
        {
            llOwnerSay("Region is not a sandbox.");
        }
    }
}
```

## See Also

### Functions

- **llGetEnv** — for region settings that don't fit in a flag
- llGetParcelFlags
- llRequestSimulatorData

<!-- /wiki-source -->
