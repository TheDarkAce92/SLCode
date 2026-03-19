---
name: "Phantom Child"
category: "example"
type: "example"
language: "LSL"
description: "Phantom Child"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Phantom_Child/Phantom_Child/Object/Phantom_Child_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Phantom_Child"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Phantom_Child/Phantom_Child/Object/Phantom_Child_1.lsl"
source_project: "Phantom_Child"
source_part_total: "3"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-phantom-child-2026-03-19"
---

```lsl
// === Part 1/3 ===
// :CATEGORY:Phantom
// :NAME:Phantom_Child
// :AUTHOR:Aeron Kohime
// :CREATED:2010-12-27 12:28:17.673
// :EDITED:2013-09-18 15:38:59
// :ID:623
// :NUM:848
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Phantom Child
// 
// This easy to use code when put into a child prim of a linkset will make that child and only that child phantom, even when taken into inventory and re-rezzed. You can use multiple copies of this script to make multiple children of a linkset phantom.
// 
// This code relies on a bug in Second Life and may not function in later versions (Currently working in server 1.36). This script was created in part by Aeron Kohime and documents this useful bug (which like invis-prims, has countless applications).
// 
// You may use the following script in any manner you like, excluding claiming you made it and individually reselling it without change in function (its on the Wiki silly). Otherwise you can sell it as part of a product, modify it, remove my comments, etc etc.
// 
// It needs to be reset on sim restarts. A reliable solution is included in all these scripts. Checking llGetTime and a timer could be used but, is a more "expensive" method. 
// :CODE:
// Basic

//Phantom Child Script by Aeron Kohime

//WARNING: When used on the root prim it makes the entire object phantom, it

//         also does not function correctly on tortured prims. (Sorry.)

//Reset on Sim restart added by Void Singer

//Strife Onizuka was here doing simplification

//Reset on collision added by Taff Nouvelle (my stairs kept reverting)

//Psi Merlin updated CHANGED_REGION_START (live as of Server 1.27)

 

default {

    state_entry() {

        llSetPrimitiveParams([PRIM_TYPE, PRIM_TYPE_BOX,

            0, <0,1,0>, 0, <0,0,0>, <1,1,0>, <0,0,0>,

            PRIM_FLEXIBLE, TRUE, 0, 0, 0, 0, 0, <0,0,0>,

            PRIM_TYPE] + llGetPrimitiveParams([PRIM_TYPE]));

    }

 

    on_rez(integer s) {

        llResetScript();

    }

 

    //-- This event/test will reset the script on sim restart.

    changed (integer vBitChanges){

        if (CHANGED_REGION_START & vBitChanges){

            llResetScript();

        }

    }

    collision_start(integer num_detected){

        llResetScript();

 

    }

}

// === Part 2/3 ===
// :CATEGORY:Phantom
// :NAME:Phantom_Child
// :AUTHOR:Aeron Kohime
// :CREATED:2010-12-27 12:28:17.673
// :EDITED:2013-09-18 15:38:59
// :ID:623
// :NUM:849
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Switchable
// 
// Addition to the above script, a switchable version that could be useful for a phantom door. 
// :CODE:
//Phantom Child Script by Aeron Kohime

//WARNING: When used on the root prim it makes the entire object phantom, it

//         also does not function correctly on tortured prims. (Sorry.)

//Reset on Sim restart added by Void Singer

//Strife Onizuka was here doing simplification

//Phantom door idea added by Taff Nouvelle

//Psi Merlin updated CHANGED_REGION_START (live as of Server 1.27)

 

integer a = 1;

 

default

 {

    state_entry()

    {

    }

    touch_start(integer total_number)

    {

    a*=-1;

    if(a == 1)

    {

        llSetPrimitiveParams([PRIM_TYPE, PRIM_TYPE_BOX,

            0, <0,1,0>, 0, <0,0,0>, <1,1,0>, <0,0,0>,

            PRIM_FLEXIBLE, TRUE, 0, 0, 0, 0, 0, <0,0,0>,

            PRIM_TYPE] + llGetPrimitiveParams([PRIM_TYPE])); 

            llOwnerSay ("Phantom");

    }

    else

    {

        llSetPrimitiveParams([PRIM_PHANTOM, FALSE]);

        llOwnerSay ("Solid");

    }

}

    on_rez(integer s) {

        llResetScript();

    }

    changed (integer vBitChanges){

        if (CHANGED_REGION_START & vBitChanges){

            llResetScript();

        }

    }

}

// === Part 3/3 ===
// :CATEGORY:Phantom
// :NAME:Phantom_Child
// :AUTHOR:Aeron Kohime
// :CREATED:2010-12-27 12:28:17.673
// :EDITED:2013-09-18 15:38:59
// :ID:623
// :NUM:850
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Advanced
// 
// Unlike the versions above, this version will work with ANY prim type (torus, tube, box, sculpt etc.) with ANY shaping parameters (twist, hollow, taper, slice, dimple etc.) and ANY texturing applied (glow, texture, fullbright, color etc.) without changing those parameters. In other words... This version works in ALL cases without error (At least I'm pretty sure it does). The downside being a greater memory use and slower run time (Although this is negligible) for complex (tortured) prims. Should only be used on child prims. 
// :CODE:
list PRIM_PHANTOM_HACK = [

    PRIM_FLEXIBLE, 1, 0, 0.0, 0.0, 0.0, 0.0, <0,0,0>,

    PRIM_FLEXIBLE, 0, 0, 0.0, 0.0, 0.0, 0.0, <0,0,0>];

 

list Params()

{

    list result = [];

    integer i = 0;

    integer face = 0;

    list src = llGetPrimitiveParams([PRIM_TEXTURE, ALL_SIDES]);

    integer len = llGetListLength(src);

    do

    {

        result += [PRIM_TEXTURE, face] + llList2List(src, i, (i + 3));

        face++;

        i += 4;

    }

    while(i < len);

 

    i = 0;

    face = 0;

    src = llGetPrimitiveParams([PRIM_COLOR, ALL_SIDES]);

    len = llGetListLength(src);

    do

    {

        result += [PRIM_COLOR, face] + llList2List(src, i, (i + 1));

        face++;

        i += 2;

    }

    while(i < len);

 

    i = 0;

    face = 0;

    src = llGetPrimitiveParams([PRIM_BUMP_SHINY, ALL_SIDES]);

    len = llGetListLength(src);

    do

    {

        result += [PRIM_BUMP_SHINY, face] + llList2List(src, i, (i + 1));

        face++;

        i += 2;

    }

    while(i < len);

 

    i = 0;

    face = 0;

    src = llGetPrimitiveParams([PRIM_FULLBRIGHT, ALL_SIDES]);

    len = llGetListLength(src);

    do

    {

        result += [PRIM_FULLBRIGHT, face] + llList2List(src, i, i);

        face++;

        i++;

    }

    while(i < len);

    i = 0;

    face = 0;

    src = llGetPrimitiveParams([PRIM_TEXGEN, ALL_SIDES]);

    len = llGetListLength(src);

    do

    {

        result += [PRIM_TEXGEN, face] + llList2List(src, i, i);

        face++;

        i++;

    }

    while(i < len);

 

    i = 0;

    face = 0;

    src = llGetPrimitiveParams([PRIM_GLOW, ALL_SIDES]);

    len = llGetListLength(src);

    do

    {

        result += [PRIM_GLOW, face] + llList2List(src, i, i);

        face++;

        i++;

    }

    while(i < len);

 

    return result;

}

 

default

{

    state_entry()

    {

        list type_params = llGetPrimitiveParams([PRIM_TYPE]);

        integer type = llList2Integer(type_params, 0);

        if(type > PRIM_TYPE_PRISM)

        {

            // After prism comes sphere, torus, tube, ring and sculpt.

            if(type != PRIM_TYPE_SCULPT)

                type_params += Params();

 

            llSetPrimitiveParams([PRIM_TYPE, PRIM_TYPE_BOX, PRIM_HOLE_DEFAULT, <0,1,0>, 0, <0,0,0>, <1,1,0>, <0,0,0>]

                                  + PRIM_PHANTOM_HACK

                                  + [PRIM_TYPE] + type_params);

        }

        else

        {

            llSetPrimitiveParams(PRIM_PHANTOM_HACK);

        }

    }

    changed(integer change)

    {

        if(change & CHANGED_REGION_START)

            llResetScript();

    }

    on_rez(integer param)

    {

        llResetScript();

    }

    collision_start(integer nd)

    {

        llResetScript();

    }

}
```
