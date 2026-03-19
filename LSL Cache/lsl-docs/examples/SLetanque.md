---
name: "SLetanque"
category: "example"
type: "example"
language: "LSL"
description: "default { touch_start(integer total_number) { rotation avatar_rotation = llGetRot(); vector direction = llRot2Fwd(avatar_rotation); direction += <0,0,1>; float power = 2 + llFrand(8.0); llRezObject..."
wiki_url: "https://wiki.secondlife.com/wiki/SLetanque"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Jack Launcher

```lsl
// SLetanque Jack Launcher by Babbage Linden
//
// Part of SLetanque
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

default
{
    touch_start(integer total_number)
    {
        rotation avatar_rotation = llGetRot();
        vector direction = llRot2Fwd(avatar_rotation);
        direction += <0,0,1>;
        float power = 2 + llFrand(8.0);
        llRezObject("SLetanque Jack", llGetPos() + direction, direction * power, <0,0,0,1>, 0);
    }
}
```

## Boule Launcher

```lsl
// SLetanque Boule Launcher by Babbage Linden
//
// Part of SLetanque
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

integer gPower = 0;
integer gMaxPower = 5;
float gPowerFactor = 3.0;

reset()
{
    llSetTimerEvent(1.0);
}

default
{
    state_entry()
    {
        reset();
    }

    on_rez(integer param)
    {
        reset();
    }

    touch_start(integer total_number)
    {
        rotation avatar_rotation = llGetRot();
        vector direction = llRot2Fwd(avatar_rotation);
        direction += <0,0,0.95 + llFrand(0.1)>;
        float power = 2 + llFrand(0.2) + gPower * (gPowerFactor + llFrand(0.1));
        llRezObject("SLetanque", llGetPos() + direction, direction * power, <0,0,0,1>, 0);
    }

    timer()
    {
        ++gPower;
        gPower %= gMaxPower;
        llSetTexture("Power" + (string)gPower, 4);
    }
}
```