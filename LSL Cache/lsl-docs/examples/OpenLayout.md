---
name: "OpenLayout"
category: "example"
type: "example"
language: "LSL"
description: "This is a script in the root prim of a HUD that allows it to be dragged and dropped."
wiki_url: "https://wiki.secondlife.com/wiki/OpenLayout"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a script in the root prim of a HUD that allows it to be dragged and dropped.

Two child prims named 'Reference' and 'Gizmo' are searched for on script reset.

- Root prim is used as the 'draggable' surface, you can imagine it as the surface handle. This has to be the root, due to a limitation with llDetectedGrab.
- 'Reference' is used to compute a bounding box for edge snapping. You can hardcode these values in Scale and Offset and comment out lines with Reference however if you prefer.
- 'Gizmo' is used for the visual effects during dragging.



Note that the HUD requires being able to estimate screen width to support screen edge snapping for the left and right edges. This means it needs to be attached to one of the HUD attachment points to the left or the right of the screen. The HUD will warn about this and use a placeholder value otherwise.

The example scripted linkset is available from: [https://marketplace.secondlife.com/p/openLayout-DragDrop-HUD-and-edge-snapping-with-ease/4542777](https://marketplace.secondlife.com/p/openLayout-DragDrop-HUD-and-edge-snapping-with-ease/4542777)

Example video at: [https://www.youtube.com/watch?v=ZAP-PZJC7v4](https://www.youtube.com/watch?v=ZAP-PZJC7v4)

```lsl
// Textures
key txtFree = "161cb352-8ef0-a792-02f2-b038e88b9262";
key txtScreenEdge = "02cbd01a-96bb-90aa-d9ea-f1d7d64c5a94";
key txtScreenCorner = "56f705e9-b9e9-bee2-32f3-ead14c29911b";
key txtSnapEdge = "10b9d2f6-574a-53e3-4698-5bc730770e34";
key txtSnapCorner = "9bcbe0f1-8a78-f8ea-5588-06bf6f8908c5";
key txtScreenSnap = "8a819c74-6ae5-9cc6-c7d7-35e9a808e690";

// States
integer LeftRight; // [Left, Center, Right] = [-1, 0, 1]
integer TopBottom; // [Top, Center, Bottom] = [-1, 0, 1]
integer Header;
integer Drag; // Being dragged?
integer Checking;
integer Snap; // Snapped to anything
integer ScreenV; // Snapped to edge of screen, [Top, Bottom] = [-1, 1]
integer ScreenH; // Snapped to edge of screen, [Left, Right] = [-1, 1]
integer SnapV; // Snapped to edge of a box, [Top, Bottom] = [-1, 1]
integer SnapH; // Snapped to edge of a box, [Left, Right] = [-1, 1]

// Temporary
vector Last;
vector OriginalHeaderScale;

// Config
vector Location;
vector Offset;
vector Scale;
float ScreenWidth;
float screenDist = 0.02; // How close to start snapping to screen
float SnapDist = 0.03; // How close to start snapping to edges of boxes

// Other
integer Point;
integer LastPoint;
integer Gizmo;
integer Linked(string Needle) {
    integer Prims = llGetNumberOfPrims()+1;
    while(--Prims) if(llGetLinkName(Prims) == Needle) return Prims;
    return 0;
} // https://wiki.secondlife.com/wiki/LinksetIndexing

integer OpenLayouts;
list OpenLayoutsKey;
list OpenLayoutsPos;
list OpenLayoutsScl;

// Converts screen to local coordinates
vector ScreenLocal(vector Coordinate)
{
    if(Point == ATTACH_HUD_TOP_RIGHT) Coordinate.z = Coordinate.z - 1;
    else if(Point == ATTACH_HUD_TOP_LEFT) Coordinate = ;
    else if(Point == ATTACH_HUD_BOTTOM_LEFT) Coordinate.y = Coordinate.y - ScreenWidth;
    // ATTACH_HUD_BOTTOM_RIGHT is <0,0,0> origin
    return Coordinate;
}

// Converts local to screen coordinates
vector LocalScreen(vector Coordinate)
{
    if(Point == ATTACH_HUD_TOP_RIGHT) Coordinate.z = 1 + Coordinate.z;
    else if(Point == ATTACH_HUD_TOP_LEFT) Coordinate = ;
    else if(Point == ATTACH_HUD_BOTTOM_LEFT) Coordinate.y = ScreenWidth + Coordinate.y;
    // ATTACH_HUD_BOTTOM_RIGHT is <0,0,0> origin
    return Coordinate;
}

string Output()
{
    vector Coordinate = LocalScreen(llGetLocalPos() + Offset);
    return (string)Coordinate+"|"+(string)Scale;
}

default
{
    state_entry()
    {
        Point = llGetAttached();
        if(Point == ATTACH_HUD_TOP_RIGHT) { LeftRight = 1; TopBottom = -1; /*llSetObjectDesc("TOP RIGHT");*/ } else
        if(Point == ATTACH_HUD_BOTTOM_RIGHT) { LeftRight = 1; TopBottom = 1; /*llSetObjectDesc("BOTTOM RIGHT");*/ } else
        if(Point == ATTACH_HUD_TOP_LEFT) { LeftRight = -1; TopBottom = -1; /*llSetObjectDesc("TOP LEFT");*/ } else
        if(Point == ATTACH_HUD_BOTTOM_LEFT) { LeftRight = -1; TopBottom = 1; /*llSetObjectDesc("BOTTOM LEFT");*/ }
        else {
            LeftRight = 0; // We won't be able to detect screen edges. (TODO: Have other HUDs communicate screen width?)
            TopBottom = 0;
        }
        LastPoint = Point;

        if(llGetLinkNumber() != 1) {
            llOwnerSay("This script needs to be in the root prim to correctly interpret touch drags.");
            return;
        }

        // llSetObjectDesc((string)llGetLocalPos());
        Location = llGetLocalPos();
        OriginalHeaderScale = llList2Vector(llGetLinkPrimitiveParams(LINK_THIS, [PRIM_SIZE]), 0);

        integer Reference = Linked("Reference");
        Gizmo = Linked("Gizmo");
        if(Reference && Gizmo) {
            Scale = llList2Vector(llGetLinkPrimitiveParams(Reference, [PRIM_SIZE]), 0);
            Offset = llList2Vector(llGetLinkPrimitiveParams(Reference, [PRIM_POS_LOCAL]), 0);

            llSetLinkPrimitiveParamsFast(Gizmo, [
                PRIM_SIZE, Scale
            ]);
        } else {
            if(!Reference)
                llOwnerSay("No prim found by name of 'Reference' in linkset, please set one so we know what dimensions the HUD is.");
            else if(!Gizmo)
                llOwnerSay("No prim found by name of 'Gizmo' in linkset, please add one so that we can show the layout modification visual.");
            return;
        }


        llListen(-42000000, "", "", "");
        string temp = llGetObjectName();
        llSetObjectName("openLayout.new");
        Checking = TRUE;
        llRegionSayTo(llGetOwner(), -42000000, Output());
        llSetObjectName(temp);

        llOwnerSay("Init");
    }

    listen(integer ch, string nm, key k, string msg)
    {
        if(llGetOwnerKey(k) != llGetOwner()) return;

        if(nm == "openLayout.new" || (Checking && nm == "openLayout.reply"))
        {
            OpenLayouts++;
            OpenLayoutsKey += k;
            integer Pipe = llSubStringIndex(msg, "|");
            vector Pos = (vector)llGetSubString(msg, 0, Pipe-1 );
            vector Scl = (vector)llGetSubString(msg, Pipe+1, -1);
            OpenLayoutsPos += Pos;
            OpenLayoutsScl += Scl;

            if(nm == "openLayout.new") {
                string temp = llGetObjectName();
                llSetObjectName("openLayout.reply");
                llRegionSayTo(llGetOwner(), -42000000, Output());
                llSetObjectName(temp);
            } else {
                llSetTimerEvent(0);
                llSetTimerEvent(1);
            }
        }
        else if(nm == "openLayout.moved")
        {
            integer Pointer = llListFindList(OpenLayoutsKey, [k]);
            if(~Pointer) {
                integer Pipe = llSubStringIndex(msg, "|");
                vector Pos = (vector)llGetSubString(msg, 0, Pipe-1 );
                vector Scl = (vector)llGetSubString(msg, Pipe+1, -1);

                OpenLayoutsPos = llListReplaceList(OpenLayoutsPos, [Pos], Pointer, Pointer);
                OpenLayoutsScl = llListReplaceList(OpenLayoutsScl, [Scl], Pointer, Pointer);
            }
        }
    }

    timer()
    {
        llSetTimerEvent(0);
        Checking = FALSE;
    }

    touch_start(integer d)
    {
        llResetTime();

        integer Link = llDetectedLinkNumber(0);

        // Clicked Root?
        Header = (Link == 1);
    }

    touch(integer d)
    {
        if(Drag)
        {
            vector Touch = llDetectedTouchPos(0);
            if(Last == ZERO_VECTOR) { Last = Touch; return; }
            if(Touch == ZERO_VECTOR) return;

            vector Delta = Touch - Last;
            Last = Touch;

            Location.y += Delta.y;
            Location.z += Delta.z;

            vector Pos = Location;
            Pos += Offset;
            vector Half = Scale * .5;
            vector GizmoPos = Offset; Offset.x - 0.5;
            Delta = ZERO_VECTOR;

            ScreenV = 0;
            ScreenH = 0;
            float screenTop = 1.0 - Half.z;
            float screenBottom = 0.0 + Half.z;
            float screenLeft = ScreenWidth - Half.y;
            float screenRight = 0.0 + Half.y;
            if(TopBottom == -1) {
                screenTop = 0.0 - Half.z;
                screenBottom = -1.0 + Half.z;
            }
            if(LeftRight == -1) {
                screenLeft = 0.0 - Half.y;
                screenRight = -ScreenWidth + Half.y;
            }

            if(Pos.z < screenBottom+screenDist) {
                Delta.z = screenBottom - Pos.z;
                ScreenV = 1;
            } else if(Pos.z > screenTop-screenDist) {
                Delta.z = screenTop - Pos.z;
                ScreenV = -1;
            }

            if(Pos.y > screenLeft-screenDist) {
                Delta.y = screenLeft - Pos.y;
                ScreenH = -1;
            } else if(Pos.y < screenRight+screenDist) {
                Delta.y = screenRight - Pos.y;
                ScreenH = 1;
            }


            SnapV = 0; float closestV = 31337;
            SnapH = 0; float closestH = 31337;
            float myTop = Delta.z + Pos.z + Half.z;
            float myBottom = Delta.z + Pos.z - Half.z;
            float myLeft = Delta.y + Pos.y + Half.y;
            float myRight = Delta.y + Pos.y - Half.y;

            integer x = OpenLayouts;
            while(x--) {
                vector v = ScreenLocal(llList2Vector(OpenLayoutsPos, x));
                vector s = llList2Vector(OpenLayoutsScl, x) * .5;
                float theirTop = v.z + s.z;
                float theirBottom = v.z - s.z;
                float theirLeft = v.y + s.y;
                float theirRight = v.y - s.y;

                float d = theirTop - myBottom;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestV)) {
                        closestV = d;
                        SnapV = 1;
                    }
                }
                d = theirBottom - myBottom;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestV)) {
                        closestV = d;
                        SnapV = 1;
                    }
                }
                d = theirBottom - myTop;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestV)) {
                        closestV = d;
                        SnapV = -1;
                    }
                }
                d = theirTop - myTop;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestV)) {
                        closestV = d;
                        SnapV = -1;
                    }
                }
                d = theirLeft - myRight;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestH)) {
                        closestH = d;
                        SnapH = 1;
                    }
                }
                d = theirRight - myRight;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestH)) {
                        closestH = d;
                        SnapH = 1;
                    }
                }
                d = theirRight - myLeft;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestH)) {
                        closestH = d;
                        SnapH = -1;
                    }
                }
                d = theirLeft - myLeft;
                if(d < SnapDist && d > -SnapDist) {
                    if(llFabs(d) < llFabs(closestH)) {
                        closestH = d;
                        SnapH = -1;
                    }
                }
            }

            if(SnapV) Delta.z += closestV;
            if(SnapH) Delta.y += closestH;

            Pos -= Offset;

            key Texture = txtFree;
            Snap = FALSE;
            float Angle;
            if(ScreenH || ScreenV || SnapV || SnapH)
            {
                Snap = TRUE;

                if(ScreenH && ScreenV)
                {
                    Texture = txtScreenCorner;
                }
                else if(ScreenH)
                {
                    Angle = PI_BY_TWO;
                    if(SnapV) {
                        Texture = txtScreenSnap;
                        if(SnapV == -1) Angle = -Angle;
                    } else {
                        Texture = txtScreenEdge;
                    }
                }
                else if(ScreenV)
                {
                    if(SnapH) {
                        Texture = txtScreenSnap;
                        if(SnapH == 1) Angle = PI;
                    } else Texture = txtScreenEdge;
                }
                else if(SnapH && SnapV)
                {
                    Texture = txtSnapCorner;
                    if(SnapH ==  1 && SnapV ==  1) Angle = PI_BY_TWO; else
                    if(SnapH == -1 && SnapV ==  1) Angle = 0; else
                    if(SnapH == -1 && SnapV == -1) Angle = -PI_BY_TWO; else
                    if(SnapH ==  1 && SnapV == -1) Angle = PI;
                }
                else if(SnapH)
                {
                    Texture = txtSnapEdge;
                    if(SnapH ==  1) Angle = PI;
                }
                else if(SnapV)
                {
                    Texture = txtSnapEdge;
                    Angle = PI_BY_TWO * SnapV;
                }
            }

            list Params = [PRIM_LINK_TARGET, Gizmo,
                PRIM_TEXTURE, 4, Texture, <1,1,0>, <0,0,0>, Angle,
                PRIM_POS_LOCAL, Offset + <.5, Delta.y, Delta.z>
            ];

            llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_POS_LOCAL, Pos] + Params);
        }
        else if(Header && LeftRight && llGetTime() > 0.3)
        {
            Drag = TRUE;
            Location = llGetLocalPos();
            Last = llDetectedTouchPos(0);
            vector ST = llDetectedTouchST(0);
            ScreenWidth = ((ST.x - .5) * Scale.y - Location.y + Last.y) * 2;
            if(ScreenWidth < 0) ScreenWidth = -ScreenWidth;

            llSetLinkPrimitiveParamsFast(LINK_THIS, [
                PRIM_SIZE, <.01,4,4>,
                PRIM_COLOR, 4, <0,0,0>, 0.3,
                PRIM_LINK_TARGET, Gizmo,
                PRIM_SIZE, <0.01, Scale.y * 2, Scale.z * 2>,
                PRIM_POS_LOCAL, Offset + <.5,0,0>
            ]);
        }
    }

    touch_end(integer d)
    {
        if(Drag)
        {
            Drag = FALSE;

            vector GizmoPos = llList2Vector(llGetLinkPrimitiveParams(Gizmo, [PRIM_POS_LOCAL]), 0);
            vector Delta = <0, GizmoPos.y - Offset.y, GizmoPos.z - Offset.z>;
            llSetLinkPrimitiveParamsFast(LINK_THIS, [
                PRIM_SIZE, OriginalHeaderScale,
                PRIM_POS_LOCAL, Location + Delta,
                PRIM_COLOR, 4, <0,0,0>, 0.01,
                PRIM_LINK_TARGET, Gizmo,
                PRIM_SIZE, Scale,
                PRIM_POS_LOCAL, Offset + <.5,0,0>
            ]);

            string temp = llGetObjectName();
            llSetObjectName("openLayout.moved");
            llRegionSayTo(llGetOwner(), -42000000, Output());
            llSetObjectName(temp);

            llMessageLinked(LINK_SET, -42000000, llList2CSV([Snap, ScreenWidth, ScreenH, ScreenV, SnapH, SnapV]), Output());
        }
        else
        {
            // Normal click
        }
    }


    changed(integer c) { if(c & CHANGED_LINK) llResetScript(); }
    attach(key k) {
        Point = llGetAttached();
        if(Point && LastPoint && Point != LastPoint) {
            llOwnerSay("Attempting to restore screen position after switching HUD attachment points");
            if(ScreenWidth == 0.0) {
                llOwnerSay("Missing screen width; Calculation will be estimated");
                ScreenWidth = 1.7777777777777777777777777777778;
            }
            Point = LastPoint;
            vector Pos = LocalScreen(llGetLocalPos());
            Point = llGetAttached();
            Pos = ScreenLocal(Pos);

            llSetLinkPrimitiveParamsFast(LINK_THIS, [
                PRIM_POS_LOCAL, Pos
            ]);
        }
        if(Point) {
            llResetScript();
        }
    }
}
```