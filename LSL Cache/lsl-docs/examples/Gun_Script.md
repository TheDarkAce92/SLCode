---
name: "Gun Script"
category: "example"
type: "example"
language: "LSL"
description: "Gun Script.lsl"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Gun_Script/Gun_Script/Object/Gun_Script_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Gun_Script"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Gun_Script/Gun_Script/Object/Gun_Script_1.lsl"
source_doc_kind: "script"
source_project: "Gun_Script"
source_project_dir: "Gun_Script"
source_project_confidence: "medium"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-gun-script-2026-03-19"
---

```lsl
// :CATEGORY:Weapons
// :NAME:Gun_Script
// :AUTHOR:Anonymous
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:54
// :ID:368
// :NUM:501
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Gun Script.lsl
// :CODE:

//
//  This basic script acts as a gun, by doing the following: 
//
//  Attach gun to right hand so that aiming animation is correct.
//
//   
vector pos; 
rotation rot;
vector offset; 

float BULLET_VELOCITY = 30.0;
float REPEAT_DELAY = 0.15;

default
{
    run_time_permissions(integer perm)
    {
        if (perm)
        {
            llAttachToAvatar(ATTACH_LHAND);
            llTakeControls(CONTROL_ML_LBUTTON, TRUE, FALSE);
            llStartAnimation("hold_R_bazooka");
        }
    }
    
    touch_start(integer tnum)
    {
        
        integer perm = llGetPermissions();
        key on = llDetectedKey(0);
        key avatar = llDetectedKey(0);
        key owner = llGetOwner();
        if (owner == avatar)
        {
            llWhisper(0, "Attach me to your right hand, and enter mouselook to fire!");
            //if (perm != (PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION | PERMISSION_ATTACH))
   //         {
     //           llRequestPermissions(on, PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION | PERMISSION_ATTACH);
       //     }
         //   else
           // {
            //    llAttachToAvatar(ATTACH_RHAND);
             //   llTakeControls(CONTROL_ML_LBUTTON, TRUE, FALSE);
             //   llStartAnimation("hold_R_handgun");
           // }
        }
        else
        {
            llWhisper(0, "Buy a copy and rez from your inventory and attach to your right hand to use.");
        }
    }
    
    attach(key on)
    {
        if (on != NULL_KEY)
        {
            integer perm = llGetPermissions();
            
            if (perm != (PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION | PERMISSION_ATTACH))
            {
                llRequestPermissions(on, PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION | PERMISSION_ATTACH);
            }
            else
            {
                llTakeControls(CONTROL_ML_LBUTTON, TRUE, FALSE);
                llStartAnimation("hold_R_bazooka");
            }
            
        }
        else
        {
            llTakeControls(FALSE, TRUE, FALSE);
            llStopAnimation("hold_R_bazooka");
        }
    }
        
    control(key owner, integer level, integer edge)
    {
        if ((level & CONTROL_ML_LBUTTON) == CONTROL_ML_LBUTTON)
        {
            //  Mouse down
            if ((edge & CONTROL_ML_LBUTTON) == CONTROL_ML_LBUTTON)
            { 
                // First Press - start sound loop and point
                //llSay(0, "Start");
                llLoopSound("gun", 2.0);
                pos = llGetPos();
                rot = llGetRot();
                offset = <1.0, 0.0, 0.0>;
                offset *= rot;
                pos += offset;
                llPointAt(pos); 
            } 
            //  Fire 1 bullet  
            pos = llGetPos();
            rot = llGetRot();
            offset = <1.0, 0.0, 0.0>;
            offset *= rot;
            pos += offset;
            llPointAt(pos); 
            vector fwd = llRot2Fwd(rot);
            fwd *= BULLET_VELOCITY; 
            integer i = 5;
            rot *= llEuler2Rot(<0, PI_BY_TWO, 0>);
            llRezObject("Bullet 1.0", pos, fwd, rot, 1);
            llSleep(REPEAT_DELAY);
        }
        else
        {
            if ((edge & CONTROL_ML_LBUTTON) == CONTROL_ML_LBUTTON)
            { 
                // Stopped
                //llSay(0, "Stop");
                llLoopSound("gun", 0.0);
                llStopPointAt();
            }  
        }
    
    }
}
// END //
```
