---
name: "Curtain script"
category: "example"
type: "example"
language: "LSL"
description: "Drop this script into the prim you want to use as a curtain etc. The script will change the length of the prim on one or more axes. Use sliced or path-cut prims to keep an edge stationary, e.g. in a blind. For a Mesh prim, arrange for the pivot point to be on one edge. You can use these scripts with any prim type."
wiki_url: "https://wiki.secondlife.com/wiki/Curtain_script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## About this script:

```lsl
Drop this script into the prim you want to use as a curtain etc.
The script will change the length of the prim on one or more axes.
Use sliced or path-cut prims to keep an edge stationary, e.g. in a blind.
For a Mesh prim, arrange for the pivot point to be on one edge.
```

You can use these scripts with any prim type.

```lsl
// Prim Resizer (shrink/expand) by Omei Qunhua
// e.g. Roll a blind from the top. (use a prim with slice end = 50%)

// Note: This script can rescale a prim on any or all axes

// Define the large and small sizes of the prim here:-
// (if the prim is sliced or path cut, it will appear to be half size on the affected dimension)
vector  gScaleLarge = <0.1, 3.0, 6.0>;
vector  gScaleSmall = <0.1, 3.0, 1.2>;

integer gSteps  = 20;   	// Number of steps in the shrink/expand process
float   gSwitch = 1.0;  	// Action on first touch. +1.0 = shrink, -1.0 = expand

default
{
    state_entry()
    {
	llSetScale(gScaleLarge);
    }

    on_rez(integer x)
    {
	llResetScript();
    }

    touch_start(integer total_number)
    {
	vector ScaleStep = (gScaleLarge - gScaleSmall) / gSteps;  // Compute the scale augment per step
	vector wscale = llGetScale();
	gSwitch *= -1;   	// Switch between stretch and contract
	integer i;
	for ( ; i < gSteps; ++i )
	{
	    // It is more lag-friendly to incorporate a sleep per step
	    // Rather than greatly increasing the number of steps
	    llSleep(0.1);
	    llSetScale(wscale + ScaleStep * (float) i * gSwitch);
	}
    }
}
```