---
name: "Pointing Stick"
category: "example"
type: "example"
language: "LSL"
description: "Made this to point at folk when its their turn at games lolz right. the useful tidbit is how it goes in the direction of what ever angle its pointing in."
wiki_url: "https://wiki.secondlife.com/wiki/Pointing_Stick"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Made this to point at folk when its their turn at games lolz right. the useful tidbit is how it  goes in the direction of what ever angle its pointing in.





<source lang="lsl2">
integer switch = TRUE;
key user;

default
{

```lsl
   state_entry()
   {
       vector goal = <90, 0, 90>;
       llSetRot(llEuler2Rot(goal*DEG_TO_RAD));
       llSetText("Touch to activate", <0,1,0>, 1);
   }
   on_rez(integer x)
   {
       llResetScript();
   }
   touch_start(integer y)
   {
       if (switch)
       {
           user = llDetectedKey(0);
           llRequestPermissions(user, PERMISSION_TAKE_CONTROLS);
           llSetText("Touch to Release Controls", <1,0,0>, 1);
       }
       else
       {
           if (llDetectedKey(0) != user)     return;
           llReleaseControls();
           llRegionSayTo(user, 0, "Controls Released");
           llSetText("Touch to activate", <0,1,0>, 1);
       }
       switch = !switch;
   }
   run_time_permissions(integer perm)
   {
       if (perm & PERMISSION_TAKE_CONTROLS)
       {
           llTakeControls( CONTROL_FWD|CONTROL_BACK|CONTROL_ROT_LEFT|CONTROL_ROT_RIGHT|CONTROL_UP|CONTROL_DOWN,TRUE,FALSE);
       }
   }
   control(key id, integer level, integer edge)
   {
       if (level & CONTROL_UP)
       {
           llSetLinkPrimitiveParamsFast(-4,[ PRIM_POSITION, llGetPos() +<0,0,0.20> ]);
       }
       if (level & CONTROL_DOWN)
       {
           llSetLinkPrimitiveParamsFast(-4,[ PRIM_POSITION, llGetPos() +<0,0,-0.20> ]);
       }
       if (level & CONTROL_FWD)
       {
           llSetLinkPrimitiveParamsFast(-4,[ PRIM_POSITION, llGetPos() +<0,0,0.20> * llGetLocalRot()]);
       }
       if (level & CONTROL_BACK)
       {
           llSetLinkPrimitiveParamsFast(-4,[ PRIM_POSITION, llGetPos() +<0,0,-0.20> * llGetLocalRot()]);
       }
       if(level & CONTROL_ROT_LEFT)
       {
           llSetLinkPrimitiveParamsFast(-4,[PRIM_ROT_LOCAL, llGetLocalRot() * llEuler2Rot(<0,0,4>*DEG_TO_RAD)]);
       }
       if (level& CONTROL_ROT_RIGHT)
       {
           llSetLinkPrimitiveParamsFast(-4,[PRIM_ROT_LOCAL, llGetLocalRot() * llEuler2Rot(<0,0,-4>*DEG_TO_RAD)]);
       }
   }
```

}