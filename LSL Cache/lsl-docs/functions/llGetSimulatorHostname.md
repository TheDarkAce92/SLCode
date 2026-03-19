---
name: "llGetSimulatorHostname"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the hostname of the machine the script is running on (same as string in viewer Help dialog)"
signature: "string llGetSimulatorHostname()"
return_type: "string"
sleep_time: "10.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetSimulatorHostname'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetsimulatorhostname"]
---

Returns a string that is the hostname of the machine the script is running on (same as string in viewer Help dialog)


## Signature

```lsl
string llGetSimulatorHostname();
```


## Return Value

Returns `string`.


## Caveats

- Forced delay: **10.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetSimulatorHostname)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetSimulatorHostname) — scraped 2026-03-18_

Returns a string that is the hostname of the machine the script is running on (same as string in viewer Help dialog)

## Caveats

- This function causes the script to sleep for 10.0 seconds.

## Examples

```lsl
// The beginnings of a region-info script.
string region;
string sim;

default
{
    state_entry()
    {
        llSetTimerEvent(1.0);
    }
    timer()
    {
        string here = llGetRegionName();
        if(region != here)
        {
            sim = llGetSimulatorHostname();
            region = here;
        }
        llSetText(
                "   REGION NAME : " + region +
              "\n  SIM HOSTNAME : " + sim +
              "\nTIME DIALATION : " + (string)llGetRegionTimeDilation() +
              "\n    REGION FPS : " + (string)llGetRegionFPS(),
            <0,1,0>, 1.0);
    }
}
```

```lsl
// llGetEnv now offers an equivalent function without the 10 second delay.
SaySimulatorHostname()
{
    llOwnerSay("Simulator Hostname: " + llGetEnv("simulator_hostname") );
}

default
{
    on_rez(integer start_param)
    {
        SaySimulatorHostname();
    }

    changed(integer iChange)
    {
        if (iChange & (CHANGED_REGION_START|CHANGED_REGION))
            SaySimulatorHostname();
    }

    state_entry()
    {
        SaySimulatorHostname();
    }
}
```

## See Also

### Functions

- **llGetRegionFPS** — Gets the region FPS
- **llGetRegionTimeDilation** — Gets the region time dilation
- **llGetEnv** — Equivalent function without the script delay

### Articles

- Simulator IP Addresses

<!-- /wiki-source -->
