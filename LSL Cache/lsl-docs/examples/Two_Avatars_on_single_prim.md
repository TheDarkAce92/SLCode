---
name: "Two Avatars on single prim"
category: "example"
type: "example"
language: "LSL"
description: "Ever wondered how to make two or more avatars to sit on single prim, to save prim amount on a furniture?"
wiki_url: "https://wiki.secondlife.com/wiki/Two_Avatars_on_single_prim"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Ever wondered how to make two or more avatars to sit on single prim, to save prim amount on a furniture?

You need two kinds of scripts; the master (which calculates avatars sitting down and standing up)
and a slave script for each additional avatar.

This is a modification of Pale Janus's script, originally posted here: [OsGrid](http://forums.osgrid.org/viewtopic.php?f=5&t=4799)



```lsl
DISCLAIMER:
    Do note, that in a linkset other child prims may move if you are not careful when setting this up.
    That means you have to tell the script how many prims is normal for your linkset and reset all scripts before testing.
```



Here are the basic scripts: modified for two avatars on single prim



### MASTER SCRIPT:

```lsl
//  October 5th 2013 Pale Janus & Cay Trudeau

//  NOTE:
//      An avatar counts as a child prim within a linkset, if you wish to move
//      it after it has sat down, you need to know what her prim number is and
//      use llSetLinkPrimitiveParamsFast to move her

integer lastnum;

key     firstavatar;
key     secondavatar;

string  animation;

integer num;

integer firstnum;
integer secondnum;

integer originalprims;

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        animation = llGetInventoryName(INVENTORY_ANIMATION, 0);

//      do not remove the position offset of the sit target
        llSitTarget(<1.0, 1.0, 1.0>, llEuler2Rot(ZERO_VECTOR*DEG_TO_RAD));

        llSetSitText("Sit");
        llSetClickAction(CLICK_ACTION_SIT);

        lastnum       = llGetNumberOfPrims();
        originalprims = llGetNumberOfPrims();//  you can set this value to your unsitted object

        llSetCameraEyeOffset(<-1.0, 0.0, 1.0> * ZERO_ROTATION);
        llSetCameraAtOffset(< 3.0, 0.0, 1.0> * ZERO_ROTATION);
    }

    changed(integer change)
    {
        if (change &  CHANGED_REGION_START)
        {
            llResetScript();
            return;
        }

        if (change & CHANGED_LINK)
        {
            num = llGetNumberOfPrims();

//          below is where all the magic happens
            if (num > originalprims)//  New avatar sitting down
            {
//              1st avatar sitting
                if (num > originalprims && num < (originalprims + 2))
                {
                    firstnum    = llGetNumberOfPrims();
//                  the avatar's UUID (cannot use llGetKey(llAvatarOnSitTarget) because two avatars)
                    firstavatar = llGetLinkKey(firstnum);

                    llRequestPermissions(firstavatar, PERMISSION_TRIGGER_ANIMATION);

//                  this is where we determine the avatar's sitting position
                    llSetLinkPrimitiveParamsFast(firstnum, [
                        PRIM_POS_LOCAL, <0.0,-0.8, 0.2>,//  < -front + back , -right + left, -down + up >
                        PRIM_ROT_LOCAL, ZERO_ROTATION]);

                    llSitTarget(ZERO_VECTOR, ZERO_ROTATION);//  releasing the sit target for next avatar

                    lastnum = llGetNumberOfPrims();
                }
//              2nd avatar sitting
                if ( num > (originalprims + 1) )
                {
                    secondnum = llGetNumberOfPrims();
                    lastnum = llGetNumberOfPrims();

                    llMessageLinked(LINK_THIS, 200, (string)secondnum, "");//  sends key
                 }
            }
//          standing up (I think this requires change upon the lastnum when the avatar sits, although it is mentioned at the bottom)
            else if (num < lastnum)
            {
                llStopAnimation(animation);

                if ( num > originalprims && num < originalprims + 2 )
                {
                    llSitTarget(<0.8, -1.05, -0.2>, llEuler2Rot(ZERO_VECTOR*DEG_TO_RAD));

//                  next line is a hint for how to make an edition for multiple avatars ;) 1111 being a channel to all slaves
//                  llMessageLinked(LINK_THIS, 1111, "whostoodup", "");
                }
            }

            lastnum = llGetNumberOfPrims();
        }
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            llStopAnimation("sit");
            llSleep(0.1);
            llStartAnimation(animation);
        }
    }
}
```

### SLAVE SCRIPT:

```lsl
//  October 5th 2013 Pale Janus & Cay Trudeau

integer lastnum;
integer avatarcount;
key     coavatar;
string  animation;
string  whostoodup;

key     secondavatar;
integer secondnum;

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        llSitTarget(<1.0, 1.0, 1.0>, llEuler2Rot(ZERO_VECTOR*DEG_TO_RAD));
        animation = llGetInventoryName(INVENTORY_ANIMATION, 0);
        lastnum   = llGetNumberOfPrims();
    }

    link_message(integer sender_num, integer num, string str, key id)
    {
//      someone just stood up
        if(num == 1111)
        {
            whostoodup = str;
        }

//      when making multiple avatar sit arrangements,
//      a new slave will have different num for each,
//      third script would have num == 300, fourth script would have num ==400 etc.

//      received 2nd avatar key
        if (num == 200)
        {
            secondnum    = (integer)str;
            secondavatar = llGetLinkKey(secondnum);

            llRequestPermissions(secondavatar, PERMISSION_TRIGGER_ANIMATION);

//          this is where we determine the avatar's sitting position
            llSetLinkPrimitiveParamsFast(secondnum, [
                PRIM_POS_LOCAL, <0.0, 0.8, 0.2>,//  < -front + back , -right + left, -down + up >
                PRIM_ROT_LOCAL, ZERO_ROTATION]);

//          releasing the sit target for next avatar
            llSitTarget(ZERO_VECTOR, ZERO_ROTATION);

//          we message the third script
//          llMessageLinked(LINK_THIS, 300, "2nd avatar sat down", "");
        }
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            llStopAnimation("sit");
            llSleep(0.1);
            llStartAnimation(animation);
        }
    }
}
```