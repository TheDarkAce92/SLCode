---
name: "FastConeSpread"
category: "example"
type: "example"
language: "LSL"
description: "default{ state_entry(){ Spread *= DEG_TO_RAD; }"
wiki_url: "https://wiki.secondlife.com/wiki/FastConeSpread"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// 2009, Nexii Malthus
// Public Domain

float Spread = 15.0;

default{
    state_entry(){
        Spread *= DEG_TO_RAD;
    }

    touch_start( integer d ){
        float x = (llFrand(1)-0.5)*PI;
        float y = llFrand(0.5)*Spread;

        rotation rSpread = <0,llSin(y),0,llCos(y)> * ;
        llSetRot( rSpread );
        // Example with rezzing a bullet:
        // rSpread *= llGetRot();
        // llRezObject("b",llGetPos()+llRot2Fwd(rSpread), <60,0,0>*rSpread, rSpread, 1 );
    }
}
```

```lsl
// 2008-2009, Aeron Kohime
// Licensed under the Creative Commons Attribution 3.0 License
// http://creativecommons.org/licenses/by/3.0/

float spread = 15.0;

default{
    state_entry(){
        spread *= DEG_TO_RAD;
    }

    touch_start( integer d ){
        float y = spread*(llFrand(1)-0.5);
        float z = spread*(llFrand(1)-0.5);
        rotation rSpread = llEuler2Rot(<0,y,z>);
        llSetRot( rSpread );
    }
}
```