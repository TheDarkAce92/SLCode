---
name: "Kilt / Skirt Editor"
category: "example"
type: "example"
language: "LSL"
description: "Having spent too many hours editing the parameters of 35 flexi-prims on a kilt, and still not being pleased with the result, and starting all over again, it finally occured to me to write this little guy."
wiki_url: "https://wiki.secondlife.com/wiki/Kilt_Editor"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Having spent too many hours editing the parameters of 35 flexi-prims on a kilt, and still not being pleased with the result, and starting all over again, it finally occured to me to write this little guy.



```lsl
// This sets all flexis in your link set to the parameters you program here.
// Note this will chage the params of EVERY flexi in your link set - so if you add
// tassles and junk, do that after you are happy with the basic skirt!
// You only need to put this into the root prim, and touch the link set,
// or save or reset the script -Brangus Weir

integer gSoftness = 1;
float gGravity =    0.3;
float gDrag =       1.0;
float gWind =       0.0;
float gTension =    0.6;
float gForceX =     0.0;
float gForceY =     0.0;
float gForceZ =     0.0;

// DO NOT EDIT BELOW HERE

setParams() {
    llOwnerSay("soft: " + (string) gSoftness + " grav: " + (string) gGravity
        + " drag: " + (string) gDrag + " wind: " + (string) gWind
        + " tens: " + (string) gTension + " Force: <" + (string) gForceX + ","
        + (string) gForceY + "," + (string) gForceZ + ">");
    list primparam = [];
    integer i = llGetNumberOfPrims();
    integer prims = 0;
    for (; i >= 0; --i) { // test each prim in link set
        primparam = llGetLinkPrimitiveParams(i,[PRIM_FLEXIBLE]);
        if (llList2Integer(primparam,0)) { // this is a flexi
            llSetLinkPrimitiveParams( i,
                [PRIM_FLEXIBLE, TRUE, gSoftness, gGravity, gDrag, gWind, gTension,
                < gForceX, gForceY, gForceZ > ]);
            prims++;  // count the prims changed
        }
    }
    llOwnerSay( (string) prims + " prims were set.");
}

default {
    on_rez(integer x) {
        setParams();
    }
    state_entry() {
        setParams();
    }
    touch_start(integer total_number) {
        setParams();
    }
}
```