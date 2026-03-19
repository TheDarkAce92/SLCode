---
name: "Basic Sim Status Button Indicator HUD"
category: "example"
type: "example"
language: "LSL"
description: "string homeregion; SimStutusButtonColor(string data) { vector simstatuscolor; if (data==\"\") simstatuscolor = <0.0,0.0,0.0>; // set color to black else { if ( data == \"up\" ) simstatuscolor = <0.0,1...."
wiki_url: "https://wiki.secondlife.com/wiki/Basic_Sim_Status_Button_Indicator_HUD"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Generic Sim Status Button Indicator
// HUD / 1 prim
// by Ackley Bing
//
// A HUD button for remote monitoring of sims.
// Color indicates the sim status
// Green = SIM available
// When the sim goes down it turns red/black
//
// To use:  Put this in a prim and attach to your preferred HUD location.
// Go to the sim you want to monitor and and click the prim
// Click and HOLD the hud button (5 seconds) to choose another sim.
//
// Modify // Attach / Connect this to your HUD/Vehicle/etc any way you like.

string homeregion;
SimStutusButtonColor(string data)
{
    vector simstatuscolor;
    if (data=="") simstatuscolor = <0.0,0.0,0.0>;  // set color to black
    else
    {
        if ( data == "up" ) simstatuscolor = <0.0,1.0,0.0>;  // set color to green
        else if ( data == "down" ) simstatuscolor = <1.0,0.0,0.0>;  // set color to red
        else if ( data == "starting" || data == "stopping" ) simstatuscolor = <1.0,1.0,0.0>;  // set color to yellow
        // if (homeregion!="") llOwnerSay(": http://maps.secondlife.com/secondlife/"+(llEscapeURL(homeregion))+" is "+data+"."); // uncomment if you want constant chat notifications
    }
    if (homeregion=="") simstatuscolor = <0.0,0.0,0.0>;
    llSetPrimitiveParams( [ PRIM_COLOR, 4, simstatuscolor, 1.0 ] );
    llSetText(homeregion, simstatuscolor, 1.0*(homeregion!="") );
}
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);
        SimStutusButtonColor("");
    }
    touch_start(integer n)
    {
        llResetTime();
    }
    touch_end(integer n)
    {
        if(llGetTime()<5.0 && homeregion != "") llRequestSimulatorData(homeregion,DATA_SIM_STATUS);
        else
        {
            llSetTimerEvent(30.0);
            llListenRemove(1);
            llListen(1, "", llGetOwner(), "");
            llDialog(llGetOwner(), "Monitor Sim Status for "+llGetRegionName()+"?", ["Yes","No","Reset"], 1);
        }
    }
    listen(integer channel, string name, key id, string message)
    {
        if (message!="Yes" && message!="No")
        {
            if (message=="Reset") llResetScript();
            return;
        }
        else
        {
            if (message=="No")
            {
                if (homeregion=="") return;
                llSetTimerEvent(0.0);
                homeregion="";
            }
            else homeregion=llGetRegionName();
            llRequestSimulatorData(homeregion,DATA_SIM_STATUS);
            llSetPrimitiveParams( [ PRIM_NAME, homeregion+" Sim Status" ] );
        }
    }
    timer()
    {
        llListenRemove(1);
        if (homeregion!="") llRequestSimulatorData(homeregion,DATA_SIM_STATUS);
        else llSetTimerEvent(0.0);
    }
    dataserver(key requested, string data)
    {
        SimStutusButtonColor(data);
    }
    run_time_permissions(integer perms)
    {
        llTakeControls((perms && PERMISSION_TAKE_CONTROLS)*CONTROL_BACK, TRUE, TRUE);
    }
}
```