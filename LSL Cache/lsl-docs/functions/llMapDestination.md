---
name: "llMapDestination"
category: "function"
type: "function"
language: "LSL"
description: 'Opens world map centered on simname with pos highlighted.
Only works for scripts attached to avatar, or during touch events.

(NOTE: look_at currently does nothing)'
signature: "void llMapDestination(string simname, vector pos, vector look_at)"
return_type: "void"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llMapDestination'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llmapdestination"]
---

Opens world map centered on simname with pos highlighted.
Only works for scripts attached to avatar, or during touch events.

(NOTE: look_at currently does nothing)


## Signature

```lsl
void llMapDestination(string simname, vector pos, vector look_at);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `simname` | Region name |
| `vector` | `pos` | position in region coordinates |
| `vector` | `look_at` | position in local coordinates (not used) |


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llMapDestination)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llMapDestination) — scraped 2026-03-18_

Opens world map centered on simname with pos highlighted.Only works for scripts attached to avatar, or during touch events.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- if simname is omitted or invalid, the map will open centered on object, but pos will not be highlighted. Since this function requests the client to perform a task, there is no way for script to know if it has failed.

## Examples

```lsl
string simName = "Help Island Public";
vector tpDest = <128.0, 128.0, 24.0>;
vector lookAt = ZERO_VECTOR;

default
{
    state_entry()
    {
        // set white, opaque floattext with teleport destination
        llSetText("click to teleport\nto '" + simName + "'", <1.0, 1.0, 1.0>, (float)TRUE);
    }

    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);

        string oldSlurlPrefix = "http://slurl.com/secondlife/";
        string newSlurlPrefix = "http://maps.secondlife.com/secondlife/";
        string slurlSuffix = llEscapeURL(simName)
            + "/" + (string)llRound(tpDest.x)
            + "/" + (string)llRound(tpDest.y)
            + "/" + (string)llRound(tpDest.z);

        llInstantMessage(id, oldSlurlPrefix + slurlSuffix);
        llInstantMessage(id, newSlurlPrefix + slurlSuffix);

        llMapDestination(simName, tpDest, lookAt);
    }
}
```

## Notes

- pos will work with Region coordinates not inside simname. (like those returned by llRequestInventoryData)
- if called from non touch events, it only works for the owner.
- if called from touch, it may only work for the first or last touch in the event queue (example: num_touched > 1)
- if called inside an attachment, it only works for the owner.

## See Also

### Functions

- llRequestInventoryData
- llMapBeacon

<!-- /wiki-source -->
