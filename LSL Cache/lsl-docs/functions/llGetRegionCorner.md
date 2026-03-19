---
name: "llGetRegionCorner"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector in meters that is the global location of the south-west corner of the region the object is in. The z component is 0.0

Divide the returned value by 256 to get the region offset.'
signature: "vector llGetRegionCorner()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionCorner'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetregioncorner"]
---

Returns a vector in meters that is the global location of the south-west corner of the region the object is in. The z component is 0.0

Divide the returned value by 256 to get the region offset.


## Signature

```lsl
vector llGetRegionCorner();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionCorner)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionCorner) — scraped 2026-03-18_

Returns a vector in meters that is the global location of the south-west corner of the region the object is in. The z component is 0.0

## Examples

```lsl
// Calculates your position relative to <0,0,0> of 'Da Boom' in meters when you touch it
vector vecrel; //a sum of llgetpos and llgetregioncorner (and another vector). Saving time doing vector math.

default
{
    state_entry()
    {
        llSetText("Touch me to get your position", <1.0,1.0,1.0>, 1.0);
    }

    touch_start(integer total_number)
    {
        vecrel = llGetRegionCorner() + llDetectedPos(0);
        llWhisper(0, "llGetRegionCorner() is:"+(string)vecrel); //for debugging before vector addition

        vecrel -= <256000.0, 256000.0, 0.0>;//Da Boom's region corner is at <256000.0, 256000.0, 0.0>
        llWhisper (0, "Position relative to <0,0,0> of 'Da Boom': " +
        (string)llRound(vecrel.x) + ", " + (string)llRound(vecrel.y) + ", " + (string)llRound(vecrel.z) + ".");

        llWhisper(0, "Position relative to <0,0,0> of 'Da Boom':" +(string)vecrel); //faster but unformatted output
    }
}
```

## Notes

The great zero is at region offset <1000,1000>, [Great Zero](http://slurl.com/secondlife/Da+Boom/0/0/0/?&title=Great+Zero)

<!-- /wiki-source -->
