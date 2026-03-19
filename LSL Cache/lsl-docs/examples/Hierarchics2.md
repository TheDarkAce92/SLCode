---
name: "Hierarchics2"
category: "example"
type: "example"
language: "LSL"
description: "This is a script for creating parametrically driven hierarchies within a linked object."
wiki_url: "https://wiki.secondlife.com/wiki/Hierarchics2"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a script for creating parametrically driven hierarchies within a linked object.

The use-cases are varied and diverse, for example: User Interfaces (HUD/Vendor/Others..), Limbs (Robotic/Organic), Turrets, Machinery...

Scaling may be buggy, but position and rotation should work fine.

```lsl
/*/
        Hierarchics2
    created by Nexii
    Released into Public Domain
/*/

//////////////////////
// Hierarchics2
list hName;
list hLink;
list hPtrs;
list hPos;
list hRot;
list hScl;

BuildTree() {
    list Names; list Links; hName = hLink = hPtrs = hPos = hRot = hScl = [];
    integer x = llGetNumberOfPrims();
    do {
        string Name = llGetLinkName(x);
        if( llGetSubString(Name,0,0) == "h" ) {
            Names += Name; Links += x; }
    } while( --x > 1 );
    integer z = x = llGetListLength(Names); integer y;
    while( x-- ) {
        string   rootName = llList2String(Names,x);
        integer  rootLink = llList2Integer(Links,x);
        list     rootTier = llParseString2List(rootName, ["."], []);
        integer  rootTiers = llGetListLength(rootTier);

        integer PtrA; integer PtrB;
        integer Children; y = z;
        while( y-- ) {
                // Is the same? Skip.
            if(y == x) jump skip;
            string   childName = llList2String(Names,y);
            list     childTier = llParseString2List(childName, ["."], []);
            integer  childTiers = llGetListLength(childTier);
                // Isn't directly below? Skip.
            if(rootTiers+1 != childTiers) jump skip;
            integer lastTier = rootTiers-1;
                // Isn't same root? Skip.
            if(llList2String(rootTier,lastTier) != llList2String(childTier,lastTier)) jump skip;
                // Otherwise, add as child
            if(Children >= 4)
                 PtrB = PtrB | ( (y+1) << (Children-4)*8 );
            else PtrA = PtrA | ( (y+1) << Children*8 );
            ++Children;
            @skip;
        }
        hName   = [rootName] + hName;
        hLink   = [rootLink] + hLink;
        hPtrs   = [0,PtrA,PtrB] + hPtrs;
    }
    x = z;
    while( x-- ) {
        string Name = llList2String(hName,x);
        integer cLink = llList2Integer(hLink,x);
        list Tier = llParseString2List(Name,["."],[]);
        integer Tiers = llGetListLength(Tier);

        vector cPos = (llList2Vector(llGetLinkPrimitiveParams(cLink,[PRIM_POSITION]),0)-llGetRootPosition())/llGetRootRotation();
        rotation cRot = llList2Rot(llGetLinkPrimitiveParams(cLink,[PRIM_ROTATION]),0)/llGetRootRotation();
        if(Tiers > 1) {
            integer Find = llListFindList( hName, [llDumpList2String(llList2List(Tier,0,Tiers-2),".")] );
            hPtrs = llListReplaceList(hPtrs,[Find+1],x*3,x*3);
            integer rLink = llList2Integer(hLink,Find);
            vector rPos = (llList2Vector(llGetLinkPrimitiveParams(rLink,[PRIM_POSITION]),0)-llGetRootPosition())/llGetRootRotation();
            rotation rRot = llList2Rot(llGetLinkPrimitiveParams(rLink,[PRIM_ROTATION]),0)/llGetRootRotation();

            cPos = (cPos-rPos)/rRot; cRot /= rRot;
        }
        hPos    = [cPos] + hPos;
        hRot    = [cRot] + hRot;
        hScl    = llGetLinkPrimitiveParams(cLink,[PRIM_SIZE]) + hScl;
    }
}

// Usage: UpdateTree([PRIM_POSITION,"Turret",<1,2,3>]);
UpdateTree( list Input ) {
    integer Find; integer Root;
    integer Operation = llList2Integer(Input,0);
    if(llGetListEntryType(Input,1) == TYPE_STRING) {
        Root = TRUE;
        Find = llListFindList( hName, [llList2String(Input,1)]);
        if(Find == -1) return;
    } else Find = llList2Integer(Input,1);

    list Params;

    if(Root) {
        vector rPos; rotation rRot;
        list lPos; list lRot;
        integer Lookup = llList2Integer(hPtrs,Find*3);
        integer x; integer y;
        while( Lookup-- ) {
            lPos = [llList2Vector(hPos,Lookup)] + lPos;
            lRot = [llList2Rot(hRot,Lookup)] + lRot;
            Lookup = llList2Integer(hPtrs,Lookup*3); ++y;
        } rPos = llList2Vector( lPos,0);
        for( x = 1; x < y; ++x ) {
            rRot = llList2Rot(lRot, x-1) * rRot;
            rPos += llList2Vector(lPos,x) * rRot; }
        if(y>1) rRot = llList2Rot(lRot,-1) * rRot;

        if(Operation == PRIM_POSITION) {
            vector cPos = llList2Vector(hPos,Find);
            vector tPos = llList2Vector(Input,2);
            Params = [PRIM_POSITION, rPos+(tPos*rRot)];
            hPos = llListReplaceList(hPos,[tPos],Find,Find);
            Input = [rPos+(tPos*rRot), llList2Rot(hRot,Find)*rRot];
        } else if(Operation == PRIM_ROTATION) {
            rotation tRot = llList2Rot(Input,2);
            Params = [PRIM_ROTATION, (tRot*rRot)/llGetRootRotation()];
            hRot = llListReplaceList(hRot,[tRot],Find,Find);
            Input = [rPos+(llList2Vector(hPos,Find)*rRot), tRot*rRot];
        } else if(Operation == PRIM_SIZE) {
            vector cScl = llList2Vector(hScl,Find);
            vector tScl = llList2Vector(Input,2);
            Params = [PRIM_SIZE, tScl];
            hScl = llListReplaceList(hScl,[tScl],Find,Find);
            Input = [rPos+(llList2Vector(hPos,Find)*rRot), llList2Rot(hRot,Find)*rRot,
                     ];
        }
    } else {
        Root = llList2Integer(Input,2);
        vector rPos = llList2Vector(Input,3);
        rotation rRot = llList2Rot(Input,4);
        if(Operation == PRIM_POSITION) {
            vector cPos = llList2Vector(hPos,Find);
            Params = [PRIM_POSITION, rPos+(cPos*rRot)];
            Input = [rPos+(cPos*rRot),llList2Rot(hRot,Find)*rRot];
        } else if(Operation == PRIM_ROTATION) {
            rotation cRot = llList2Rot(hRot,Find);
            vector cPos = llList2Vector(hPos,Find);
            Params = [PRIM_POSITION, rPos+(cPos*rRot), PRIM_ROTATION, (cRot*rRot)/llGetRootRotation()];
            Input = [rPos+(cPos*rRot), cRot*rRot];
        } else if(Operation == PRIM_SIZE) {
            vector cScl = llList2Vector(hScl,Find);
            vector dScl = llList2Vector(Input,5);
            vector tScl = ;
            vector cPos = llList2Vector(hPos,Find);
                   cPos = ;
            Params = [PRIM_POSITION, rPos+(cPos*rRot), PRIM_SIZE, tScl];
            hPos = llListReplaceList(hPos,[cPos],Find,Find);
            hScl = llListReplaceList(hScl,[tScl],Find,Find);
            Input = [rPos+(cPos*rRot),llList2Rot(hRot,Find)*rRot]+llList2List(Input,5,5);
        }
    }

    integer PtrA = llList2Integer(hPtrs,(Find*3)+1);
    integer PtrB = llList2Integer(hPtrs,(Find*3)+2);
    integer Children; integer x = 4;
    while(x--) {
        integer ChildA = (PtrA >> (x*8))&0xFF;
        integer ChildB = (PtrB >> (x*8))&0xFF;
        if(ChildA) UpdateTree([Operation,--ChildA,Find]+ Input);
        if(ChildB) UpdateTree([Operation,--ChildB,Find]+ Input);
    }
    llSetLinkPrimitiveParamsFast( llList2Integer(hLink,Find), Params );
}

default {
    state_entry() {
        llOwnerSay("Building Tree..");
        BuildTree();
        llOwnerSay("Updating Tree..");
        vector Pos = <1.5,-.0,-.6>;
        float x;
        for( x = 0; x > -1.0; x -= .1 ) {
            UpdateTree([PRIM_POSITION,"hA",]);
            llSleep(.1);
        }

        UpdateTree([PRIM_ROTATION,"hA",llEuler2Rot(<0,0,11.25>*DEG_TO_RAD)]); llSleep( 1.0 );

        UpdateTree([PRIM_SIZE,"hA.A",<.5,.6,.3>]); llSleep( 1.0 );

        UpdateTree([PRIM_ROTATION,"hA.B.A",llEuler2Rot(<0,0,0>*DEG_TO_RAD)]); llSleep( 1.0 );

        UpdateTree([PRIM_ROTATION,"hA",llEuler2Rot(<0,0,0>*DEG_TO_RAD)]); llSleep( 1.0 );

        UpdateTree([PRIM_ROTATION,"hA.B.A",llEuler2Rot(<0,11.25,0>*DEG_TO_RAD)]); llSleep( 1.0 );

        UpdateTree([PRIM_SIZE,"hA.A",<.5,.5,.5>]); llSleep( 1.0 );
    }
}
```