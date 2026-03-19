---
name: "llListStatistics"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the result of performing statistical aggregate function operation on src.

If a list entry type is not a float or an integer it is silently ignored.'
signature: "float llListStatistics(integer operation, list src)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListStatistics'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llliststatistics"]
---

Returns a float that is the result of performing statistical aggregate function operation on src.

If a list entry type is not a float or an integer it is silently ignored.


## Signature

```lsl
float llListStatistics(integer operation, list src);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `operation` | a LIST_STAT_* flag |
| `list` | `src` |  |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListStatistics)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListStatistics) — scraped 2026-03-18_

Returns a float that is the result of performing statistical aggregate function operation on src.

## Examples

```lsl
// Show results for each operation for a sample list
default
{
    state_entry()
    {
        list LX = [-1, 3.33, 17, "object", -4.5, 0.8675 ];

        llSay(0, "G.Mean= " + (string) llListStatistics(LIST_STAT_GEOMETRIC_MEAN, LX) );           // 0. 000000
        llSay(0, "Max= " + (string) llListStatistics(LIST_STAT_MAX, LX) );                         // 17.000000
        llSay(0, "Min= " + (string) llListStatistics(LIST_STAT_MIN, LX) );                         // -4.500000
        llSay(0, "Mean= " + (string) llListStatistics(LIST_STAT_MEAN, LX) );                       // 3.139500
        llSay(0, "Median= " + (string) llListStatistics(LIST_STAT_MEDIAN, LX) );                   // 0.867500
        llSay(0, "Count= " + (string) llListStatistics(LIST_STAT_NUM_COUNT, LX) );                 // 5.000000
        llSay(0, "Range= " + (string) llListStatistics(LIST_STAT_RANGE, LX) );                     // 21.500000
        llSay(0, "Std.Dev= " + (string) llListStatistics(LIST_STAT_STD_DEV, LX) );                 // 8.258468
        llSay(0, "Sum= " + (string) llListStatistics(LIST_STAT_SUM, LX) );                         // 15.697500
        llSay(0, "Sum of squares= " + (string) llListStatistics(LIST_STAT_SUM_SQUARES, LX) );      // 322.091500

    }
}
// Note that LSLEditor produces "NaN" (Not A Number) for the geometric mean above. Geometric mean applies only to numbers of the same sign.
```

```lsl
// shows just how bad SL is behaving and demonstrates the use of llListStatistics()
list dil_s;
list fps_s;
integer ticks = 0;

default
{
    state_entry()
    {
        llSetTimerEvent(1.0);
    }

    on_rez (integer parm)
    {
        llResetScript();
    }

    timer()
    {
        dil_s = llList2List(dil_s + llGetRegionTimeDilation(), -60, -1);
        fps_s = llList2List(fps_s + llGetRegionFPS(), -60, -1);
        if(3 <= ++ticks)
        {
            llSetText(
                "Dilation: min="+(string) llListStatistics(LIST_STAT_MIN, dil_s) + ", mean=" +
                    (string) llListStatistics(LIST_STAT_MEAN, dil_s) + ", max=" +
                    (string) llListStatistics(LIST_STAT_MAX, dil_s) + ", std.dev=" +
                    (string) llListStatistics(LIST_STAT_STD_DEV, dil_s) + "\n" +
                    "FPS: min="+(string) llListStatistics(LIST_STAT_MIN, fps_s) + ", mean=" +
                    (string) llListStatistics(LIST_STAT_MEAN, fps_s) + ", max=" +
                    (string) llListStatistics(LIST_STAT_MAX, fps_s) + ", std.dev=" +
                    (string) llListStatistics(LIST_STAT_STD_DEV, fps_s),
                <1.0, 1.0, 0.0>, //yellow
                1.0);
        }
    }

    changed(integer change)
    {
        if(change & CHANGED_REGION)
        {
            llResetScript();
        }
    }
}
```

## Notes

Given that this operation ignores any non-numbers in a list, it can be used to tell you, in a mixed list, how many of the elements in a list are numbers (when used with the LIST_STAT_NUM_COUNT parameter.)

## See Also

### Functions

- llGetListEntryType

<!-- /wiki-source -->
