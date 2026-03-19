---
name: "Recent Avatar Scanner"
category: "example"
type: "example"
language: "LSL"
description: "Recent Avatar Scanner by Ackley Bing. Put this script in a prim. Wear the object as a HUD. Touch it to see a list of recently collected names. Stores up to 100 names. Adjust 100 to 1000 or whatever you want, just beware of script memory use or you will get a Stack Heap Collision. Modify it to suit your particular use in another Hud, weapon, or whatever you want. <3 --Ackley Bing"
wiki_url: "https://wiki.secondlife.com/wiki/Recent_Avatar_Scanner"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Recent Avatar Scanner by Ackley Bing.  Put this script in a prim.  Wear the object as a HUD.  Touch it to see a list of recently collected names.  Stores up to 100 names.  Adjust 100 to 1000 or whatever you want, just beware of script memory use or you will get a Stack Heap Collision. Modify it to suit your particular use in another Hud, weapon, or whatever you want. <3 --Ackley Bing

```lsl
list RecentAgents;
integer MaxRecent=100;
Process_Region_Agents()
{
    list RegionAgents=llGetAgentList(AGENT_LIST_REGION,[]);
    integer TotalAgentsInRegion=llGetListLength(RegionAgents);
    integer i;
    for(i=0;iMaxRecent) RecentAgents=llDeleteSubList(RecentAgents,0,0);
            llSleep(0.03);
        }
    }
    llSetTimerEvent((float)llGetListLength(RecentAgents)/8.0);
}
default
{
    state_entry()
    {
        llSetTexture("6a571ff9-efba-7327-7bc3-0cf3b98bae37",4);
        llSetTimerEvent(5.0);
    }
    timer()
    {
        llSetTimerEvent(0.0);
        Process_Region_Agents();
    }
    touch_start(integer index)
    {
        integer TotalRecentAgents=llGetListLength(RecentAgents);
        llOwnerSay ((string)TotalRecentAgents+" recent avatars:");
        llSleep(0.03);
        if (TotalRecentAgents)
        {
            integer i=0;
            for (i;i