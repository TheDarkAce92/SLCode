---
name: "HUD Dots Radar"
category: "example"
type: "example"
language: "LSL"
description: "Here is a simple example of drawing points on the HUD that cover a point in the region. It is based on Babbage's SLateIt, with the HUD drawing parts extracted for easier reuse."
wiki_url: "https://wiki.secondlife.com/wiki/HUD_Dots_Radar"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Here is a simple example of drawing points on the HUD that cover a point in the region. It is based on Babbage's SLateIt, with the HUD drawing parts extracted for easier reuse.

- 1 build script
- 2 radar script

## build script

First you will need to create a suitable HUD object. Use this first script to do that. It will ask for link permission, grant it.

```lsl
/**************************************************
    This is the script that creates the HUD dots radar object.

    1. Rez a cube and take it to your inventory.
    2. Drag the cube from your inventory back on to the ground.
    3. Go back to your inventory, this time ctrl+drag the same cube to inside the one you just rezzed.
    4. Edit the first cube, create a new script, paste in this code, and save.
    5. Touch to create the object.
    6. Edit the radar object again, create a new script, paste in the second script (the actual radar), and save.
    7. Take the result to your inventory, it should be ready.

    To use, attach it to your HUD on the Center or Center 2 point.
 **************************************************/

float gPrimSize = .02;

string gWorkPrim;
integer gNewChild;
integer gWorking = FALSE;

default
{
    state_entry()
    {
        llSetText("Rez a generic cube, take it to your inventory,\n"
                  + "Ctrl+drag it to inside this prim, then touch to begin", <1, 1, 1>, 1);
    }

    touch_start(integer num)
    {
        if (gWorking)
            return;

        if (llDetectedKey(0) != llGetOwner())
            return;

        gWorkPrim = llGetInventoryName(INVENTORY_OBJECT, 0);
        if (gWorkPrim == "")
        {
            llSetText("No object found in object inventory. Rez a generic cube, take it to your\n"
                      + "inventory, Ctrl+drag it to inside this prim, then touch to try again.", <1, 1, 0>, 1);
            return;
        }
        llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
    }

    run_time_permissions(integer perm)
    {
        if (gWorking)
            return;

        if (perm & PERMISSION_CHANGE_LINKS)
        {
            gWorking = TRUE;
            llSetText("Working...", <1, 1, 0>, 1);
            llSetLinkPrimitiveParamsFast(LINK_THIS, [
                PRIM_NAME,
                    "HUD dots radar",
                PRIM_ROTATION,
                    ZERO_ROTATION,
                PRIM_SIZE,
                    ,
                PRIM_TEXTURE,
                    ALL_SIDES,
                    TEXTURE_BLANK,
                    <1, 1, 0>,      // repeats
                    ZERO_VECTOR,    // offsets
                    0,              // rotation in rads
                PRIM_COLOR,
                    ALL_SIDES,
                    <1, 1, 0>,     // color
                    1,             // alpha
                PRIM_FULLBRIGHT,
                    ALL_SIDES,
                    TRUE
            ]);
            gNewChild = 0;
            llRezObject(gWorkPrim, llGetPos() + <.5, 0, 0>, ZERO_VECTOR, ZERO_ROTATION, 0);
        }
    }

    object_rez(key id)
    {
        llCreateLink(id, LINK_ROOT);
        llSetLinkPrimitiveParamsFast(2, [
            PRIM_TYPE,
                PRIM_TYPE_SPHERE,
                    PRIM_HOLE_DEFAULT,  // hole shape
                    <0, 1, 0>,          // cut
                    0,                  // hollow
                    <0, 0, 0>,          // twist
                    <0, 1, 0>,          // dimple
            PRIM_POSITION,
                ,
            PRIM_ROTATION,
                ZERO_ROTATION,
            PRIM_SIZE,
                ,
            PRIM_TEXTURE,
                ALL_SIDES,
                TEXTURE_BLANK,
                <1, 1, 0>,      // repeats
                ZERO_VECTOR,    // offsets
                0,              // rotation in rads
            PRIM_COLOR,
                ALL_SIDES,
                <1, 1, 0>,      // color
                .5,             // alpha
            PRIM_FULLBRIGHT,
                ALL_SIDES,
                TRUE,
            PRIM_DESC,
                (string)gNewChild
        ]);

        gNewChild++;
        if (gNewChild < 16)
        {
            llRezObject(gWorkPrim, llGetPos() + <.5, 0, 0>, ZERO_VECTOR, ZERO_ROTATION, 0);
        }
        else
        {
            llRemoveInventory(gWorkPrim);
            llSetText("Object created, you can drag in the radar script now.", <0, 1, 0>, 1);
            llRemoveInventory(llGetScriptName());
        }
    }
}
```

## radar script

When you have created the object, put this script in its root prim.

```lsl
// HUD dots radar

// This is a simple example of drawing a dot son the HUD covering a point
// in the region.
//
// Based by Cerise Sorbet on Babbage Linden's SLateIt, with the HUD drawing part
// extracted to make it easier to follow and reuse.
//
// This little example does only simple things for demnstration. The HUD has 16
// pointer prims that it moves over avatars in radar range. Only avatars within the
// HUD square get dots, the rest are skipped. The floating text will be a distraction
// in a real application, but it helps to see how things work.

vector gHomePosition = <0.0, 0.0, -1.1>; // puts the root prim off screen
// vector gHomePosition = <0.0, 0.0, -0.2>; // puts the root prim on the screen for debugging

float gPrimSize = .01; // make this match the build script. it is only for tidiness

float gSensorRange = 96.0; // up to 96 meters
float gSensorInterval = 3.0; // scan every gSensorInterval seconds

integer gLastNumDetected;

// Here is the function that does the interesting part.

// convert region coordinates to a spot on the center or center2 HUD position.
// returns gOffScreen if the coordinates are off screen
//
// Derived from Babbage Linden's SlateIt, http://wiki.secondlife.com/wiki/SLateIt
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

// precalculated stuff for perspective, FOV is 60 degrees,
// gFOV is 1./ llTan(((60. * DEG_TO_RAD) / 2.))
float gFOV = 1.7320508075688774;

vector gOffScreen = <-1000.0, -1000.0, -1000.0>; // an "invalid" return value for Region2Hud

vector Region2HUD(vector objectPos, vector cameraPos, rotation cameraRot)
{
//    vector cameraPos = llGetCameraPos();
//    rotation cameraRot = llGetCameraRot();

    // Translate object in to camera space.
    objectPos = (objectPos - cameraPos)
        // Rotate object in camera space.
        * (ZERO_ROTATION / cameraRot);

    // Switch axes from Z = up to RHS (X = left, Y = up, Z = forward)
    objectPos = <-objectPos.y, objectPos.z, objectPos.x>;

    // Apply perspective distortion and clip object to HUD
    float xHUD = (objectPos.x * gFOV) / objectPos.z;

    // remove xHUD check, or expand (say, to > -3 && < 3) for a non-square target field spanning the window
    //if (xHUD > -1.0 && xHUD < 1.0)
    if (xHUD > -3.0 && xHUD < 3.0)
    {
        float yHUD = (objectPos.y * gFOV) / objectPos.z;
        if (yHUD > -1.0 && yHUD < 1.0)
        {
            // Set front clipping plane to 1m and back clipping plane to infinity.
            float zHUD = (objectPos.z - 2) / objectPos.z;
            if (zHUD > -1.0 && zHUD < 1.0)
                return <0.0, -xHUD / 2.0, yHUD / 2.0>;
        }
    }

    return gOffScreen;
}

// Move uninteresting prims out of the way behind the root
ResetChildPositions(integer startPrim, integer endPrim)
{
    if (endPrim > 1)
    {
        for (; endPrim >= startPrim; endPrim--)
            llSetLinkPrimitiveParamsFast(endPrim, [
                PRIM_POSITION,
                    ,
                PRIM_SIZE,
                    ,
                PRIM_FULLBRIGHT,
                    ALL_SIDES,
                    TRUE,
                PRIM_TEXT,
                    "",
                    ZERO_VECTOR,
                    0.0
            ]);
    }
}

Setup()
{
    ResetChildPositions(2, llGetNumberOfPrims());

    // make sure the object is attached to one of the center HUD points
    integer attachPoint = llGetAttached();
    if (attachPoint != ATTACH_HUD_CENTER_1 && attachPoint != ATTACH_HUD_CENTER_2)
    {
        llOwnerSay("Attach me to the Center or Center 2 HUD position.");
        // some floating text to make the object easier to find
        llSetText ("HUD dots radar\n|\n|\nV", <1.,1.,0.>, 1.);
        return;
    }

    // put the root where it belongs
    llSetRot(ZERO_ROTATION);
    llSetPos(gHomePosition);

    llSetText("", ZERO_VECTOR, 0.0);

    llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA|PERMISSION_TAKE_CONTROLS);
}

default
{
    state_entry()
    {
        Setup();
    }

    attach(key id)
    {
        if (id)
            Setup();
    }

    on_rez(integer p)
    {
        Setup();
    }


    run_time_permissions(integer p)
    {
        // keep-running hack
        if (p & PERMISSION_TAKE_CONTROLS)
            llTakeControls(CONTROL_LBUTTON, TRUE, TRUE);

        if (p & PERMISSION_TRACK_CAMERA)
            llSetTimerEvent(gSensorInterval);
        else
            llOwnerSay("Something went wrong, did not get PERMISSION_TRACK_CAMERA!");
    }

    timer()
    {
        llSensor("", "", AGENT, gSensorRange, PI);
    }

    no_sensor()
    {
        // clean up if there were visible dots before
        if (gLastNumDetected) {
            ResetChildPositions(2, gLastNumDetected + 1);
            gLastNumDetected = 0;
        }
    }

    sensor(integer num)
    {
        vector cameraPos = llGetCameraPos();
        rotation cameraRot = llGetCameraRot();
        vector myPos = llGetPos();

        integer i;
        for (i = 0; i < num; i++)
        {
            vector dPos = llDetectedPos(i);
            float dist = llVecDist(myPos, dPos);

            // z += .5 to get dots off crotches :p
            vector childPos = Region2HUD(dPos + <0.0, 0.0, .5>, cameraPos, cameraRot);
            if (childPos != gOffScreen)
            { // only show avatars in the hud square
                key k = llDetectedKey(i);
                string legName = llDetectedName(i);
                list nameParts = llParseString2List(legName, [" "], []);
                if (llList2String(nameParts, 1) == "Resident")
                    legName = llList2String(nameParts, 0);
                string showName = legName;
                string dispName = llGetDisplayName(k);
                if (dispName)
                    if (llToLower(dispName) != llToLower(legName))
                        showName = dispName + " (" + llGetUsername(k) + ")";

                llSetLinkPrimitiveParamsFast(i + 2, [
                    PRIM_POSITION,
                        childPos - llGetLocalPos(),
                    PRIM_COLOR,
                        ALL_SIDES,
                        llVecNorm(),
                        1.0,
                    PRIM_TEXT,
                        showName,
                        <1.0,1.0,1.0>,
                        1.0
                ]);
            }
            else
            { // off screen, put the dot away
                llSetLinkPrimitiveParamsFast(i + 2, [
                    PRIM_POSITION,
                        ,
                    PRIM_TEXT,
                        "",
                        ZERO_VECTOR,
                        0.0
                ]);
            }
        }
        if (gLastNumDetected > num)
            ResetChildPositions(i + 2, gLastNumDetected + 1);
        gLastNumDetected = num;
    }
}
```