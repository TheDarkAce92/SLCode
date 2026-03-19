---
name: "Taper Door (minimalistic)"
category: "example"
type: "example"
language: "LSL"
description: "Example prim settings for these types of doors:"
wiki_url: "https://wiki.secondlife.com/wiki/Taper_Door_(minimalistic)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Example prim settings for these types of doors:

- Type: Box
- Size: <2.5, 3.75, 0.01>
- Rotation: <270, 0, 0>
- Hollow: 0.90
- Taper-x: -1
- Taper-y: 0

```lsl
// Created by Kopilo Hallard
// Creative Commons - Attribute only
// http://creativecommons.org/licenses/by/3.0/

//to alter script, see touch start,
//first value is magnitude (how much to change by, larger is 'faster')
//second value is rate of change (smaller is faster)
//Example DecreaseTaper(0.01, 0.02)
//0.01 = change by 0.01,
//0.02 = pause for 20ms between each change

//time to keep door open defined here:
float openpause = 2.0; //2.0 = 2 seconds

// Area not to touch starts here (scroll down to make changes)
list baseObject;
integer indexLoc;

vector getCurrentTaper() {
    integer objectType = llList2Integer(baseObject, 0);
    if(objectType < 3) {
        //box, cylinder, prism, index 5
        indexLoc = 5;
        return llList2Vector(baseObject, 5);
    }
    else if(objectType > 3 && objectType != 7) {
        //ring tube torus, index 8
        indexLoc = 8;
        return llList2Vector(baseObject, 8);
    }
    return <-42,-42,-42>;

}

DecreaseTaper(float mag, float speed) {
    baseObject = llGetPrimitiveParams([PRIM_TYPE]);
    vector tmp = getCurrentTaper();
    if(tmp.z != -42) { //safety check

        while (tmp.x > 1) {
            tmp.x -= mag;
            baseObject = llListReplaceList(baseObject, [tmp], indexLoc, indexLoc);
            llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_TYPE] + baseObject);
            llSleep(speed);
        }
        llSleep(openpause);
        IncreaseTaper(mag, speed);
    }
}

IncreaseTaper(float mag, float speed) {
    vector tmp = getCurrentTaper();
    if(tmp.z != -42) { //safety check

        while (tmp.x < 2) {
            tmp.x += mag;
            baseObject = llListReplaceList(baseObject, [tmp], indexLoc, indexLoc);
            llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_TYPE] + baseObject);
            llSleep(speed);
        }

    }
}

default
{
    state_entry()
    {
      baseObject = llGetPrimitiveParams([PRIM_TYPE, PRIM_POSITION]);
    }

    touch_start(integer total_number)
    {
        //Alter values here
        DecreaseTaper(0.01, 0.02);
        //That's all
    }
}
```