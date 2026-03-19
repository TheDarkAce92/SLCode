---
name: "InverseKinematics3D"
category: "example"
type: "example"
language: "LSL"
description: "Inverse Kinematics is something that is always being over complicated. With this script I attempt to simplify it for a broader audience to see the cool things they can do with it. This is a simple crane driven by IK to give an example of what is possible."
wiki_url: "https://wiki.secondlife.com/wiki/InverseKinematics3D"
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

This version is solving a 3D point for the knee using the Doom 3 IK function.
You may do anything you like with this code, without limitation. It's for educational purposes only and will need modification to be used in large projects.

```lsl
//written by To-mos Codewarrior (tomos.halsey)
//3D IK crane exmple using doom3 Source conversion

//LINKS
integer LINK_hipHinge0;integer LINK_upperLeg0;
integer LINK_lowerLeg0;integer LINK_foot0;
float IK_angle(vector offset)
{return  llAtan2(offset.z,-offset.x);}
//compressed doom 3 IK ported by To-mos Codewarrior on (6/22/2012)
vector IK_bones(vector startPos,vector endPos, vector dirNorm, float upperLeg, float lowerLeg)
{
    vector offsetEnd=endPos-startPos;float lengthTemp=llPow(llVecMag(offsetEnd),2);
    float lengthTemp2=llPow(lengthTemp,-0.5);lengthTemp*=lengthTemp2;
    if(lengthTemp>upperLeg+lowerLeg||lengthTemp,1.0);//debug
        vector foot0=llList2Vector(llGetLinkPrimitiveParams(LINK_foot0,[PRIM_POS_LOCAL]),0);
        vector hip0=llList2Vector(llGetLinkPrimitiveParams(LINK_hipHinge0,[PRIM_POS_LOCAL]),0);
        vector temp0=hip0-foot0;rotation hingeRot0=llEuler2Rot(<0.0,0.0,llAtan2(-temp0.x,temp0.y)-1.57>);
        temp0=IK_bones(hip0,foot0,<-1.0,0.0,1.0>*hingeRot0,1.0,0.75);
        llSetLinkPrimitiveParams(LINK_hipHinge0,[
            PRIM_ROT_LOCAL,hingeRot0,
            PRIM_LINK_TARGET,LINK_foot0,PRIM_ROT_LOCAL,hingeRot0,
            PRIM_LINK_TARGET,LINK_upperLeg0,PRIM_POS_LOCAL,hip0,PRIM_ROT_LOCAL,llEuler2Rot(<0.0,IK_angle((hip0-temp0)/hingeRot0),0.0>)*hingeRot0,
            PRIM_LINK_TARGET,LINK_lowerLeg0,PRIM_POS_LOCAL,temp0,PRIM_ROT_LOCAL,llEuler2Rot(<0.0,IK_angle((temp0-foot0)/hingeRot0),0.0>)*hingeRot0
        ]);
    }
}
```

Warning: Solving IK points in 3D space using this method is really memory heavy for multiple legs. It is recommended to use a 2D method with the laws of cosines for many legs.