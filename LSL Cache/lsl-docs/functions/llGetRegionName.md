---
name: "llGetRegionName"
category: "function"
type: "function"
language: "LSL"
description: "Returns the name of the current region"
wiki_url: "https://wiki.secondlife.com/wiki/llGetRegionName"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llGetRegionName()"
parameters: []
return_type: "string"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llgetregionname"]
deprecated: "false"
---

# llGetRegionName

```lsl
string llGetRegionName()
```

Returns the name of the region this script is currently running in.

## Return Value

`string` — current region name.

## Example

```lsl
// Build a SLURL for the current position
string buildSLURL()
{
    string region = llGetRegionName();
    vector pos = llGetPos();
    return "http://maps.secondlife.com/secondlife/"
        + llEscapeURL(region) + "/"
        + (string)llRound(pos.x) + "/"
        + (string)llRound(pos.y) + "/"
        + (string)llRound(pos.z);
}

default
{
    state_entry()
    {
        llOwnerSay("Region: " + llGetRegionName());
        llOwnerSay("SLURL: " + buildSLURL());
    }
}
```

## See Also

- `llGetSimulatorHostname` — simulator host name
- `llGetEnv` — detailed region information
- `llGetRegionFlags` — region capability flags
- `llGetRegionFPS` — region frame rate
- `llGetRegionTimeDilation` — region time dilation


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionName) — scraped 2026-03-18_

Returns a string that is the current region name

## Examples

```lsl
// Say what would be said by "Copy SLURL to clipboard" in the Map of the standard client

string wwGetSLUrl()
{
    string globe = "http://maps.secondlife.com/secondlife";
    string region = llGetRegionName();
    vector pos = llGetPos();
    string posx = (string)llRound(pos.x);
    string posy = (string)llRound(pos.y);
    string posz = (string)llRound(pos.z);
    return (globe + "/" + llEscapeURL(region) +"/" + posx + "/" + posy + "/" + posz);
}

default
{
    state_entry()
    {
        llOwnerSay( wwGetSLUrl() );
    }
}
```

## See Also

### Functions

- llRequestSimulatorData
- llGetSimulatorHostname
- llGetParcelDetails
- llEscapeURL

<!-- /wiki-source -->
