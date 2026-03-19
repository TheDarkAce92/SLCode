---
name: "Grenade Script"
category: "example"
type: "example"
language: "LSL"
description: "Uses two methods within separate states to 'throw' objects at a velocity dependent on how long you hold the mouse button down."
wiki_url: "https://wiki.secondlife.com/wiki/Grenade_Script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Uses two methods within separate states to 'throw' objects at a velocity dependent on how long you hold the mouse button down.

<source lang="lsl2">
vector pos;
rotation rot;
vector offset;
vector fwd;
integer gPermFlags;
vector BULLET_VELOCITY = <2,0,1>;
float REPEAT_DELAY = 0.40;
string ammo =  "grenade";
string throwanim = "avatar_throw_R";
integer on=TRUE;



default
{

```lsl
  state_entry()
    {
         gPermFlags = PERMISSION_TRIGGER_ANIMATION | PERMISSION_TAKE_CONTROLS | PERMISSION_TRACK_CAMERA;
```

```lsl
         if ( llGetAttached() )
           llRequestPermissions(llGetOwner(), gPermFlags);
     }

   run_time_permissions(integer perm)
   {
       if ((perm & gPermFlags) == gPermFlags)
      {
          llTakeControls(CONTROL_ML_LBUTTON, TRUE, FALSE);
          llOwnerSay("First Person Mode. Click to change to Third Person Mode.");
      }
   }

    touch_end(integer nd)
   {

     key DetectedKey= llDetectedKey(0);
     key OwnerKey= llGetOwner();


        if (OwnerKey== DetectedKey)  //Ensures only the operator can change the mode.
        {
         state two;
        }
    }

   attach(key id)
   {
       if (id)
           llRequestPermissions(id, gPermFlags);

       else if(id== NULL_KEY)         // Things to do when detached.
       {
        llStopAnimation(throwanim);
        llReleaseControls();
        llResetScript();
        }
   }
   changed(integer change)
   {
        if(change &(CHANGED_OWNER | CHANGED_INVENTORY))
           llResetScript();
   }
```

```lsl
   control(key owner, integer level, integer edge)
   {
        if (edge  & CONTROL_ML_LBUTTON )
        {
            if(on==TRUE)
            {
             llResetTime();
             on=FALSE;
            }
       else if (on==FALSE)
        {
             float factor = llGetTime()+1*3;
             vector last=factor*BULLET_VELOCITY *llGetCameraRot();
             llStartAnimation(throwanim);
             llRezAtRoot(ammo,llGetCameraPos()+<1.0,0,1.0>*llGetCameraRot(),last ,llGetCameraRot(),10);
             llSleep(REPEAT_DELAY);
              on=TRUE;
        }
      }
   }
```

}

state two
{

```lsl
   state_entry()
    {
         gPermFlags = PERMISSION_TRIGGER_ANIMATION | PERMISSION_TAKE_CONTROLS | PERMISSION_TRACK_CAMERA;
         llRequestPermissions(llGetOwner(), gPermFlags);
    }

    run_time_permissions(integer perm)
    {
       if ( (perm & gPermFlags) == gPermFlags)
       {
           llTakeControls(CONTROL_LBUTTON, TRUE, FALSE);
           llOwnerSay("Third Person mode. Click to change to First Person Mode.");
       }
    }

    touch_end(integer nd)
    {
       key DetectedKey= llDetectedKey(0);
       key OwnerKey= llGetOwner();

        if (OwnerKey== DetectedKey)  //Ensures only the operator can change the mode.
        {
           state default;
        }
    }

   attach(key id)
   {
      if(id== NULL_KEY)            // Things to do when detached.
       {
          llStopAnimation(throwanim);
          llReleaseControls();
          llResetScript();
        }
   }
   changed(integer change)
   {
         if(change &(CHANGED_OWNER | CHANGED_INVENTORY) )
            llResetScript();
    }
```

```lsl
 control(key owner, integer level, integer edge)
   {

          if (edge  & CONTROL_LBUTTON )
        {
            if(on==TRUE)
            {
             llResetTime();
             on=FALSE;
            }
       else if (on==FALSE)
        {
           float factor = llGetTime()+1*3;
           llStartAnimation(throwanim);
           pos = llGetPos();
           rot = llGetRot();
           offset = <1.0,0.0, 2.0>;
           pos += offset*rot;
           offset *= rot;
           rot *= llEuler2Rot(<0, 0, 0>*DEG_TO_RAD);
           fwd = factor*BULLET_VELOCITY*rot;
           llRezAtRoot(ammo, pos, fwd, rot, 1);
           llSleep(REPEAT_DELAY);
           on=TRUE;
       }
     }
  }
```

}