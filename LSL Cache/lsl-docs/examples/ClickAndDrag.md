---
name: "ClickAndDrag"
category: "example"
type: "example"
language: "LSL"
description: "Setup: Rez prim (A), apply script, Rez another prim (B) and put it slightly below it, link it up so B is a child and A is the root."
wiki_url: "https://wiki.secondlife.com/wiki/ClickAndDrag"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Setup: Rez prim (A), apply script, Rez another prim (B) and put it slightly below it, link it up so B is a child and A is the root.

This is exactly the same code on my aRTS project that the landscape uses for handling interface touches, such as clicking on a point or dragging a rectangle which the HUD can in return use for sending out commands to units and/or unit selection.

This is quite a cool and unique script which can be used to draw rectangles dynamically dragged by a user on an interface. For example one could use this on a sculpted miniature simulator map and designate an area for some specific purpose. This gives dynamic feedback invaluable to such interfaces.

```lsl
// ClickAndDrag made by Nexii Malthus
// Public Domain

// Protocol:
    //    Types   Data
    //      Click,  Player Key | Type | World Coords | Normal | Bi-Normal
    //      Drag,   Player Key | Type | WC-A | N-A | BN-A | WC-B | N-B | BN-B
// Type -  0 = Click, 1 = Drag

integer ch = 1; // Channel to send commands on

key kTextureClick = "5d431ade-24f3-2390-f1ba-ca404cad2864";
key kTextureDrag = "efc411bc-2005-10ff-da0c-3dda972f6e70";

list tData1;
list tData2;
vector ST1;

default{
    state_entry(){
        llMinEventDelay( 0.21 );
    }

    touch_start( integer d ){
        if( llDetectedTouchFace( 0 ) == -1 ) return;
        tData1 = [ llDetectedTouchPos(0), llDetectedTouchNormal(0), llDetectedTouchBinormal(0) ];
        ST1 = llDetectedTouchST( 0 );
    }

    touch( integer dn ){
        vector ST2 = llDetectedTouchST( 0 );

        if( ST1 == <-1,-1,0> || ST2 == <-1,-1,0> ) return;

        if( llVecDist( ST1, ST2 ) > 0.01 ){
            llSetColor( < 0.0, 0.0, 1.0 >, 0 ); llSetAlpha( 0.2, 0 );
            float relSize = 0.08;//0.084;
            vector selCentre = <1,1,0> - ((ST2+ST1)/2);
            vector selSize = (ST1-ST2); selSize = ;

            vector Scale = ;//selSize;//< selSize.x/relSize.x, selSize.y/relSize.y, 0>;
            vector Offset = (selCentre-<0.5,0.5,0>);Offset = ;
            llSetPrimitiveParams([ PRIM_TEXTURE, 0, kTextureDrag, Scale, Offset, 0 ]);
        }
    }

    touch_end( integer d ){
        key nKey = llDetectedKey( 0 );
        vector tPos = llDetectedTouchPos( 0 );
        tData2 = [ tPos, llDetectedTouchNormal( 0 ), llDetectedTouchBinormal( 0 ) ];
        vector ST2 = llDetectedTouchST( 0 );

        if( ST1 == <-1,-1,0> || ST2 == <-1,-1,0> ){
            if( llVecDist( ST1, ST2 ) > 0.01 )
                llSetAlpha( 0.0, 0 );
            return;
        }

        if( llVecDist( ST1, ST2 ) < 0.01 ){
            llSetColor( < 0.0, 1.0, 0.0 >, 0 ); llSetAlpha( 1.0, 0 );
            vector Scale = < 1.0, 1.0, 0>;
            vector Offset = < 1.0, 1.0, 0 > - ST1;
            llSetPrimitiveParams([ PRIM_TEXTURE, 0, kTextureClick, Scale, Offset, 0 ]);
            llSetAlpha( 0.0, 0 );
            llSay( ch, llDumpList2String( [nKey,0] + tData1, "|" ) );
        } else {
            llSetColor( < 0.0, 0.0, 1.0 >, 0 ); llSetAlpha( 0.2, 0 );
            float relSize = 0.08;
            vector selCentre = <1,1,0> - ((ST2+ST1)/2);
            vector selSize = (ST1-ST2); selSize = ;

            vector Scale = ;//selSize;//< selSize.x/relSize.x, selSize.y/relSize.y, 0>;
            vector Offset = (selCentre-<0.5,0.5,0>);Offset = ;
            llSetPrimitiveParams([ PRIM_TEXTURE, 0, kTextureDrag, Scale, Offset, 0 ]);
            llSay( ch, llDumpList2String( [nKey,1] + tData1 + tData2, "|" ) );
            llSetAlpha( 0.0, 0 );
        }
    }
}
```