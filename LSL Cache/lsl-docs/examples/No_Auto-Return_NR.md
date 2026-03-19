---
name: "No Auto-Return NR"
category: "example"
type: "example"
language: "LSL"
description: "This script is released under DNSIOIWKU License, Free and Open for anyone..."
wiki_url: "https://wiki.secondlife.com/wiki/No_Auto-Return_NR"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script is released under DNSIOIWKU License, Free and Open for anyone...

```lsl
//  anti return created by Jor3l Boa
//==================================================
//  (works on blue and rausch combat region),
//  NOTE: for red, change -5 to 5 and + 5 to -5 :)
//  this anti return needs a nearby region
//  with entry perms to work.
//==================================================
// NOTE: USE IT AT YOUR OWN RISK! <------YOUR OWN RISK!
//version 0.1

//Change log:
//  - 0.1 initial release

warpPos(vector destpos)
{
   llSetPrimitiveParams([PRIM_POSITION, <1.304382E+19, 1.304382E+19, 0.0>, PRIM_POSITION,destpos]);
}
integer time;

default
{
    state_entry()
    {
        llSetTimerEvent(10);
    }

    timer()
    {
        llSetTimerEvent(0);
        llSetColor(<1,0,0>,ALL_SIDES);
        vector pos = llGetPos();
            warpPos(<-5,pos.y,pos.z>);
        vector tpos = llGetPos();
            warpPos();
        llSetColor(<1,1,0>,ALL_SIDES);
            llSetTimerEvent(60);
        time++;
        //llSetText((string)time+" minutes\nin this region.",<1,0,0>,1.0);
    }
}
```

NOTE: I am not responsible for the use you give to this code, you are free to use it at your OWN risk

Another version... better :)

```lsl
float TIMER_SIM_JUMP = 600.0;

safe_posJump( vector target_pos )
{
    // An alternative to the warpPos trick without all the overhead.
    // Trickery discovered by Uchi Desmoulins and Gonta Maltz. More exact value provided by Fake Fitzgerald.
    // Safe movement modification provided by Alias Turbo.
    vector start_pos = llGetPos();
    llSetPrimitiveParams( [ PRIM_POSITION , < 1.304382E+19 , 1.304382E+19 , 0.0 > , PRIM_POSITION , target_pos ,
                            PRIM_POSITION , start_pos , PRIM_POSITION , target_pos ] );
}

vector get_another_region()
{
    list test = [ < 1.0 , 0.0 , 0.0 > , < -1.0 , 0.0 , 0.0 > , < 0.0 , 1.0 , 0.0 > , < 0.0 , -1.0 , 0.0 > ];
    integer i;
    vector off;
    for ( ; i < 4 ; i += 1 )
    {
        off = llList2Vector( test , i );
        if ( !llEdgeOfWorld( < 128.0 , 128.0 , 100.0 > , off ) ) jump found;
    }
    return ZERO_VECTOR;
    @found;
    vector m_pos = llGetPos();
    return off * 254.0;
}

default
{
    on_rez( integer start_param )
    {
        llResetScript();
    }

    state_entry()
    {
        vector another_region = get_another_region();
        if ( another_region )
        {
            llOwnerSay( "NR: Activated." );
            llSetTimerEvent( TIMER_SIM_JUMP );
        } else llOwnerSay( "NR: This will not work in the current region." );
    }

    timer()
    {
        vector another_region = get_another_region();
        if ( another_region )
        {
            safe_posJump( llGetPos() + another_region );
            llSleep( 2.0 );
            safe_posJump( llGetPos() - another_region );
        }
    }
}
```