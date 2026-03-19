---
name: "Hierarchics"
category: "example"
type: "example"
language: "LSL"
description: "This is a script that has been painstakingly crafted by Nexii Malthus to create a highly efficient and advanced system of controlling a large linkset of prims in a parametric fashion of a mechanical structure or robotic limb. I am giving out this script to the people now, to me it is a huge contribution to the community as I have spent many weeks designing the plans and debugging the script as well as studying and researching efficient script design. This can be used in your product under the condition you put credit in a visible location to the consumer that you used my work or derived from my work."
wiki_url: "https://wiki.secondlife.com/wiki/Hierarchics"
author: "Nexii Malthus"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a script that has been painstakingly crafted by Nexii Malthus to create a highly efficient and advanced system of controlling a large linkset of prims in a parametric fashion of a mechanical structure or robotic limb. I am giving out this script to the people now, to me it is a huge contribution to the community as I have spent many weeks designing the plans and debugging the script as well as studying and researching efficient script design. This can be used in your product under the condition you put credit in a visible location to the consumer that you used my work or derived from my work.

**Simple Example:**
Create a prim and shift-drag to create a tower of 4 prims.
Name 3 of them as following, from top to bottom

```lsl
A.B.C
A.B
A
```

Link them all up so the 4th unnamed prim is the root object, which should be the last prim on the bottom as a base.

Drop the Hierarchics script into each of the named prims.

Create a new script in the root object. Put the following constants as globals.

```lsl
integer Link_HierarchicsRot     = 660333;
rotation LastQuatA;
rotation LastQuatB;
```

In the touch_start event, put the following.

```lsl
    rotation QuatA = llEuler2Rot( < 0, 0, 15 > * DEG_TO_RAD ) * LastQuatA;
    rotation QuatB = llEuler2Rot( < 5, 0, 0 > * DEG_TO_RAD ) * LastQuatB;
    llMessageLinked(LINK_SET, Link_HierarchicsRot, (string)QuatA+";"+(string)QuatB, "A;A.B" );
    LastQuatA = QuatA;
    LastQuatB = QuatB;
```

Keep touching and observe the prims following their commanded rotations.





Script Hierarchic.40.lsl

```lsl
///////////////////////////////////
/// Hierarchy Script            //
/// Creator:    Nexii Malthus  //
/// Revision:   v0.4.0        //
///////////////////////////////
// Public Domain
///////////////////////////
// Tweaked by Strife Onizuka

list hNm  = [];
list hLnk = [];
list hPos = [];
list hRot = [];
//list hRef = [];

vector   lastPos;
rotation lastRot;
rotation mRef;

integer Link_HierarchicsRot     = 660333;   //0xA136D
integer Link_HierarchicsPos     = 660334;   //0xA136E
integer Link_HierarchicsPR      = 660335;   //0xA136F
integer Link_HierarchicsReset   = 660336;   //0xA1370
integer Link_HierarchicsReport  = 660337;   //0xA1371
integer Link_HierarchicsEdit    = 660338;   //0xA1372
integer Link_HierarchicsGet     = 660339;   //0xA1373

integer Commanded = FALSE;
integer Report = FALSE;
integer EditMode = FALSE;

float   CheckTimer = 0.3;

Update(){
    vector Pos = llList2Vector( hPos, 0 );
    rotation Rot;

    integer x = ( hNm != [] ) - 0; integer y;
    for( y = 1; y < x; ++y ){
        Rot = llList2Rot( hRot, y - 1) * Rot;
        Pos += llList2Vector( hPos, y ) * Rot;
    }

    Rot = mRef * llList2Rot( hRot, -1 ) * Rot;
    Commanded = TRUE;
    llSetPrimitiveParams([ PRIM_POSITION, Pos, PRIM_ROTATION, Rot / llGetRootRotation() ]);
}

rotation RefAndRot(string RefString, rotation CurrentRot){
    rotation Rot = ZERO_ROTATION;
    rotation Ref = (rotation)RefString;
    if(Ref == Rot){//it might not be a quaternion
        vector v = (vector)RefString;
        if(v){
            Ref = llEuler2Rot(v * DEG_TO_RAD);
        } else { //it might not even be a vector
            integer index = llSubStringIndex(RefString, "<");
            if(~index){//"<" was found, now insert "-"
                RefString = llGetSubString(RefString, 0, index) + "-" +
                    llStringTrim(llDeleteSubString(RefString, 0, index), STRING_TRIM_HEAD);
                if((string)((vector)RefString) == (string)v)
                    Rot = CurrentRot;//Ref couldn't be parsed
            } else {
                Rot = CurrentRot;//Ref couldn't be parsed
            }
        }
    }
    hRot += Rot;
    //hRef += Ref;
    return Ref;
}//Strife Onizuka was here

default{
    state_entry(){
        vector rPos; rotation rRot;
        if( llGetLinkNumber() == LINK_ROOT ){
            rPos = llGetPos(); rRot = llGetRot();
        } else {
            rPos = llGetRootPosition(); rRot = llGetRootRotation();
        }
        string a = llGetObjectName();
        list b = llParseString2List( a, ["."], []);

        integer y;integer z = (b!=[]) - 1;string txt;
        for(y = 0;y < z;++y){
            integer x = llGetNumberOfPrims();
            while(x){
                list c = llGetObjectDetails(llGetLinkKey(x),
                            [OBJECT_NAME,OBJECT_DESC,OBJECT_POS,OBJECT_ROT]);
                list d = llParseString2List( llList2String(c,0), ["."], []);
                if( (d!=[]) - 1 <= y )
                {
                    if(llList2String(d,y) == llList2String(b,y)){
                        txt += ( llList2String(d,y) +", " );
                        hNm  += llList2List(c,0,0);
                        hLnk += [x];
                        hPos += (llList2Vector(c,2)-rPos)/rRot;
                        RefAndRot(llList2String(c,1), llList2Rot( c,3 )/rRot);
                    }
                }
                --x;
            }
        }
        integer f;integer g = (hPos!=[]);list temp = hPos;
        if(g > 1){
            for(f = 1;f < g;++f){
                hPos = llListReplaceList(hPos, [llList2Vector(temp,f)-llList2Vector(temp,f - 1)], f, f);
            }
        }
        hNm  += llGetObjectName();
        if(g) hPos += llGetLocalPos()-llList2Vector(temp,(hPos!=[]) - 1);
        else  hPos += llGetLocalPos();
        mRef = RefAndRot(llGetObjectDesc(), llGetLocalRot());
        state Main;
    }
}

state Main{
    state_entry(){
        integer x;string txt;
        for(x = 0;x < (hNm!=[]);++x)
            txt += ( llList2String( hNm, x ) + ", " );
        lastPos = llGetLocalPos(); lastRot = llGetLocalRot();
        if( EditMode || Report ) llSetTimerEvent( CheckTimer );
    }

    link_message(integer sn,integer n,string s,key k){
        if( n == Link_HierarchicsRot ){
            integer Update;
            list sl = llParseString2List(s,[";"],[]);// Values
            list kl = llParseString2List(k,[";"],[]);// Keys
            integer si = (sl!=[]);
            integer x;
            for(x = 0;x < si;++x){
                if( llList2String(kl,x) == llGetObjectName() ){
                    integer y = (hPos!=[]) - 1;
                    hRot = llListReplaceList( hRot, [(rotation)llList2String(sl,x)], y, y);
                    Update = TRUE;
                } else {
                    integer Find = llListFindList( hNm, [llList2String(kl,x)] );
                    if( ~Find ){
                        hRot = llListReplaceList( hRot, [(rotation)llList2String(sl,x)], Find, Find);
                        Update = TRUE;
                    }
                }
            }
            if(Update) Update();
        } else if( n == Link_HierarchicsPos ){
            integer Update;
            list sl = llParseString2List(s,[";"],[]);// Values
            list kl = llParseString2List(k,[";"],[]);// Keys
            integer si = (sl!=[]);
            integer x;
            for(x = 0;x < si;++x){
                if( llList2String(kl,x) == llGetObjectName() ){
                    integer y = (hPos!=[]) - 1;
                    hPos = llListReplaceList( hPos, [(vector)llList2String(sl,x)], y, y);
                    Update = TRUE;
                } else {
                    integer Find = llListFindList( hNm, [llList2String(kl,x)] );
                    if( ~Find ){
                        hPos = llListReplaceList( hPos, [(vector)llList2String(sl,x)], Find, Find);
                        Update = TRUE;
                    }
                }
            }
            if(Update) Update();
        } else if( n == Link_HierarchicsPR ){
            integer Update;
            list sl = llParseString2List(s,[";"],[]);// Values
            list kl = llParseString2List(k,[";"],[]);// Keys
            integer ki = (kl!=[]);
            integer x; integer z;
            for(x = 0;x < ki;++x){
                if( llList2String(kl,x) == llGetObjectName() ){
                    integer y = (hPos!=[]) - 1;
                    hPos = llListReplaceList( hPos, [(vector)llList2String(sl,z)], y, y);
                    hRot = llListReplaceList( hRot, [(rotation)llList2String(sl,z+1)], y, y);
                    Update = TRUE;
                } else {
                    integer Find = llListFindList( hNm, [llList2String(kl,x)] );
                    if( ~Find ){
                        hPos = llListReplaceList( hPos, [(vector)llList2String(sl,z)], Find, Find);
                        hRot = llListReplaceList( hRot, [(rotation)llList2String(sl,z+1)], Find, Find);
                        Update = TRUE;
                    }
                }
                z += 2;
            }
            if(Update) Update();
        } else if( n == Link_HierarchicsEdit ){
            if( s == "all" ){
                EditMode = (integer)((string)k);
            } else {
                list sl = llParseString2List(s,[";"],[]);
                if( ~llListFindList( sl, [llGetObjectName()]) )
                    EditMode = (integer)((string)k);
            }
            if( EditMode ) llSetTimerEvent( CheckTimer );
            else if( !Report ) llSetTimerEvent( FALSE );
        } else if( n == Link_HierarchicsReset ){
            llResetScript();
        } else if( n == Link_HierarchicsReport ){
            if( s == "all" ) Report = (integer)((string)k);
            else {
                list sl = llParseString2List(s,[";"],[]);
                if( ~llListFindList( sl, [llGetObjectName()]) )
                    Report = (integer)((string)k);
            }
            if( Report ) llSetTimerEvent( CheckTimer );
            else if( !Report && !EditMode ) llSetTimerEvent( FALSE );
        } else if( n == Link_HierarchicsGet ){
            if( s == "all" ){
                llMessageLinked( LINK_ROOT, Link_HierarchicsGet,
                    llDumpList2String([llGetLocalPos(),llGetLocalRot()],";"),
                    llDumpList2String([],";") );
            } else {
                 list sl = llParseString2List(s,[";"],[]);
                 if( ~llListFindList( sl, [llGetObjectName()]) )
                    llMessageLinked( LINK_ROOT, Link_HierarchicsGet,
                        llDumpList2String([llGetLocalPos(),llGetLocalRot()],";"),
                        llDumpList2String([],";") );
            }
        }
    }

    timer(){
        integer ChangedRot = ( lastRot != llGetLocalRot() );
        integer ChangedPos = ( lastPos != llGetLocalPos() );
        if( ChangedRot || ChangedPos ){
            if( Commanded ){
                Commanded = FALSE;
                lastPos = llGetLocalPos(); lastRot = llGetLocalRot();
                return;
            }

            if( Report ){
                llMessageLinked( LINK_ROOT, Link_HierarchicsReport,
                    (string)llGetLocalPos(), (string)llGetLocalRot() );

            }
            if( EditMode ){
                if( ChangedRot && ChangedPos ){
                    vector newPos = (llGetLocalPos() - lastPos);
                    if( (hRot!=[]) > 1 ) newPos /= llList2Rot( hRot, -2 );
                    newPos = llList2Vector(hPos,-1) + newPos;
                    rotation diffRot = (llGetLocalRot() / lastRot) * llList2Rot(hRot,-1);
                    hPos = llListReplaceList(hPos,[newPos],-1,-1);
                    hRot = llListReplaceList(hRot,[diffRot],-1,-1);
                    llMessageLinked( LINK_ALL_OTHERS, Link_HierarchicsPR,
                            (string)newPos+";"+(string)diffRot, llGetObjectName() );
                } else if( ChangedRot ){
                    rotation diffRot = (llGetLocalRot() / lastRot) * llList2Rot(hRot,-1);
                    hRot = llListReplaceList(hRot,[diffRot],-1,-1);
                    llMessageLinked( LINK_ALL_OTHERS, Link_HierarchicsRot,
                            (string)diffRot, llGetObjectName() );
                } else if( ChangedPos ){
                    vector newPos = (llGetLocalPos() - lastPos);
                    if( (hRot!=[]) > 1 ) newPos /= llList2Rot( hRot, -2 );
                    newPos = llList2Vector(hPos,-1) + newPos;
                    hPos = llListReplaceList(hPos,[newPos],-1,-1);
                    llMessageLinked( LINK_ALL_OTHERS, Link_HierarchicsPos,
                            (string)newPos, llGetObjectName() );
                }
            }
            lastPos = llGetLocalPos(); lastRot = llGetLocalRot();
        }
    }
}
```