---
name: "InverseKinematics2D"
category: "example"
type: "example"
language: "LSL"
description: "Inverse Kinematics is something that is always being over complicated. With this script I attempt to simplify it for a broader audience to see the cool things they can do with it. This is a simple crane driven by IK to give an example of what is possible."
wiki_url: "https://wiki.secondlife.com/wiki/InverseKinematics2D"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Introduction

Inverse Kinematics is something that is always being over complicated. With this script I attempt to simplify it for a broader audience to see the cool things they can do with it. This is a simple crane driven by IK to give an example of what is possible.

Usage

To use this script, first create a root prim, then create a swivel joint for the bottom of the boom. After that make a lower and upper arm prim and then create a prim box for the end of it to represent the target point.

Name the arm closest to the base lowerLeg0 and make its size <2.0,0.1336,0.1336> set its Path Cut to B:0.125 E:0.625.

Name the arm furthest from the base upperLeg0 and make its size <2.0,0.1336,0.1336> set its Path Cut to B:0.125 E:0.625.

Name the end point foot0.

Name the swivel base hipHinge0.

Link all the parts to the original root prim.

Save the script.

Move the final point with the build menu's edit linked parts to see it in action.

The Code

This version is solving an entire IK solution at once building the mid point backwards from the foot point using the lengths of the legs, and the angles are being generated through the laws of cosines.
You may do anything you like with this code, without limitation. It's for educational purposes only and will need modification to be used in large projects.

```lsl
//  written by To-mos Codewarrior (tomos.halsey)
//  2D IK crane example using law of cosines
//  This version gives you TONS more memory when used to solve many limbs

//LINKS
integer LINK_hipHinge0;integer LINK_upperLeg0;
integer LINK_lowerLeg0;integer LINK_foot0;
float IK_cosAngle(float num1, float num2, float num3)
{
    if(num2>(num1+num3))
        return 0.0;
    if(num1>(num2+num3))
        return PI;
    else
    {
        float ang=llAcos((num2 * num2 + num3 * num3 - num1 * num1) / (2 * num2 * num3));
        if(ang>PI)
            return ang;
        else
            return -ang;
    }
}
list IK_solveLeg(integer linkHingeLink,integer linkUpperLeg,integer linkLowerLeg,integer linkFoot,vector posRay)
{
    vector hip0=llList2Vector(llGetLinkPrimitiveParams(linkHingeLink,[PRIM_POS_LOCAL]),0);
    //start IK
    vector temp0=posRay-hip0;
    rotation hingeRot0=llEuler2Rot(<0.0,0.0,llAtan2(temp0.y,temp0.x)>);
    temp0/=hingeRot0;
    float angle= IK_cosAngle(llVecMag(temp0),0.75,1.0);
    rotation upperLeg=llEuler2Rot(<0.0,(IK_cosAngle(0.75,llVecMag(temp0),1.0)-llAtan2(temp0.z, temp0.x)),0.0>);
    //end IK
    return [
        PRIM_LINK_TARGET,linkHingeLink,PRIM_ROT_LOCAL,hingeRot0,
        PRIM_LINK_TARGET,linkFoot,PRIM_ROT_LOCAL,hingeRot0,
        PRIM_LINK_TARGET,linkUpperLeg,PRIM_POS_LOCAL,hip0,PRIM_ROT_LOCAL,upperLeg*hingeRot0,
        PRIM_LINK_TARGET,linkLowerLeg,PRIM_POS_LOCAL,hip0+<1.0,0.0,0.0>*upperLeg*hingeRot0,PRIM_ROT_LOCAL,llEuler2Rot(<0,angle+PI,0>)*upperLeg*hingeRot0
    ];
}
default
{
    state_entry()
    {
        //SETUP LINKS
        integer total=llGetNumberOfPrims()+1;
        while((total--)-1)
        {
            string name=llGetLinkName(total);
            if(name=="hipHinge0")LINK_hipHinge0=total;if(name=="upperLeg0")LINK_upperLeg0=total;
            if(name=="lowerLeg0")LINK_lowerLeg0=total;if(name=="foot0")    LINK_foot0    =total;
        }
        llSetTimerEvent(1.0);
    }

    timer()
    {
        llSetText((string)(llGetFreeMemory()*0.000977)+"KB",<1.0,1.0,1.0>,1.0);//debug
        llSetLinkPrimitiveParams(0,
            IK_solveLeg(LINK_hipHinge0,LINK_upperLeg0,LINK_lowerLeg0,LINK_foot0,llList2Vector(llGetLinkPrimitiveParams(LINK_foot0,[PRIM_POS_LOCAL]),0))
        );
    }
}
```