---
name: "Display Names Radar"
category: "example"
type: "example"
language: "LSL"
description: "Here is a simple HUD type avatar radar that can show display names. This can be useful while some viewers support them and others do not."
wiki_url: "https://wiki.secondlife.com/wiki/Display_Names_Radar"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Here is a simple HUD type avatar radar that can show display names. This can be useful while some viewers support them and others do not.

It has a few commands you can use:

- /44 range 42 will change the radar distance to 42 meters (maximum 96).
- /44 interval 3 will change the scan poll to 3 seconds (minimum 1).
- /44 scripts on will show script count and memory if the region supports it.

First you will need to create a suitable HUD object. Use this first script to do that. It will ask for link permission, grant it.

### build script

```lsl
/**************************************************
    This is the script that creates the radar object.

    1. Rez a cube and take it to your inventory.
    2. Drag the cube from your inventory back on to the ground.
    3. Go back to your inventory, this time ctrl+drag the same cube to inside the one you just rezzed.
    4. Edit the first cube, create a new script, paste in this code, and save.
    5. Touch to create the object.
    6. Edit the radar object again, create a new script, paste in the second script (the actual radar), and save.
    7. Take the result to your inventory, it should be ready.

    To use, attach it to your HUD. By default it expects to be worn on the bottom. If you want to
    wear it near the top of the screen, it will be good to flip the object 180 degrees.

    The text spacing could be too big or small, resize the object with the editor
    until it looks how you want.
**************************************************/

string gWorkPrim;
integer gNewChild;
float gCubeSize = .02;

default
{
    state_entry()
    {
        llSetText("Rez a generic cube, take it to your inventory,\n"
            + "ctrl+drag it to inside this prim, then touch to begin", <1., 1., 1.>, 1.);
    }

    touch_start(integer num)
    {
        if (llDetectedKey(0) != llGetOwner())
            return;

        gWorkPrim = llGetInventoryName(INVENTORY_OBJECT, 0);
        if (gWorkPrim == "")
        {
            llSetText("No object found in object inventory. Rez a generic cube, take it to your\n"
                + "inventory, ctrl+drag it to inside this prim, then touch to try again.", <1., 1., 0.>, 1.);
            return;
        }
        llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_CHANGE_LINKS)
        {
            llSetText("Working...", <1., 1., 0.>, 1.);
            llSetLinkPrimitiveParamsFast(LINK_THIS, [
                PRIM_NAME,
                    "display names radar",
                PRIM_ROTATION,
                    ZERO_ROTATION,
                PRIM_SIZE,
                    ,
                PRIM_TEXTURE,
                    ALL_SIDES,
                    TEXTURE_BLANK,
                    <1., 1., 0.>,
                    ZERO_VECTOR,
                    .5,
                PRIM_COLOR,
                    ALL_SIDES,
                    ZERO_VECTOR,
                    .5
            ]);
            gNewChild = 0;
            llRezObject(gWorkPrim, llGetPos() + <.5, 0., 0.>, ZERO_VECTOR, ZERO_ROTATION, 0);
        }
    }

    object_rez(key id)
    {
        llCreateLink(id, LINK_ROOT);
        llSetLinkPrimitiveParamsFast(2, [
            PRIM_POSITION,
                <0., 0., gCubeSize * (gNewChild + 1)>,
            PRIM_ROTATION,
                ZERO_ROTATION,
            PRIM_SIZE,
                ,
            PRIM_TEXTURE,
                ALL_SIDES,
                TEXTURE_BLANK,
                <1., 1., 0.>,
                ZERO_VECTOR,
                0.,
            PRIM_COLOR,
                ALL_SIDES,
                ZERO_VECTOR,
                0.,
            PRIM_DESC,
                (string)gNewChild
        ]);

        gNewChild++;
        if (gNewChild < 16)
        {
            llRezObject(gWorkPrim, llGetPos() + <.5, 0., 0.>, ZERO_VECTOR, ZERO_ROTATION, 0);
        }
        else
        {
            llRemoveInventory(gWorkPrim);
            llSetText("Object created, you can drag in the radar script now.", <0., 1., 0.>, 1.);
            llRemoveInventory(llGetScriptName());
        }
    }
}
```

When the object is created, here is the radar script that will do the real work.

To use, attach it to your HUD. By default it expects to be worn on the bottom. If you want to wear it near the top of the screen, it will be good to flip the object 180 degrees.

The text spacing could be too big or small, resize the object with the editor until it looks how you want.

Have fun,
--Cerise Sorbet 00:30, 6 November 2010 (UTC)

### radar script

```lsl
//  display names avatar radar

integer gCommandChannel = 44;           // Listen for commands on this channel
float gMaxSensorRange = 96.0;           // Default maximum scanner range
float gInterval = 5.0;                  // Default seconds between checks
integer gScriptVoyeur = FALSE;          // show script count amd memory?

integer gCommandListener;               // llListen results go here
float gSensorRange = gMaxSensorRange;   // sensor range in use right now

integer gLastNumDetected = 16;          // how many (if any) seen on last scan

list gTextLines;
list gPrims;
float gTextAlpha = 1.;

Setup() {
    list prims;
    integer i;
    for (i = 2; i <= llGetNumberOfPrims(); i++)
    {
        prims += llList2Integer(llGetLinkPrimitiveParams(i, [PRIM_DESC]), 0);
    }

    gPrims = [];
    for (i = 0; i < 16; i++)
    {
        integer index = llListFindList(prims, [i]);
        if (index == -1)
        {
            llOwnerSay("no prim with description \"" + (string)i + "\", display will be incomplete");
            gPrims += "";
        }
        else
        {
            gPrims += index + 2;
        }
    }

    llListenRemove(gCommandListener);
    gCommandListener = llListen(gCommandChannel, "", llGetOwner(), "");
    if (llGetAttached())
        llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);

    llSetTimerEvent(gInterval);
}


default
{
    state_entry()
    {
        Setup();
    }

    on_rez(integer start_param)
    {
        Setup();
    }

    attach(key id)
    {
        Setup();
    }

    changed(integer change)
    {
        if (change & CHANGED_TELEPORT)
            llSensor("", "", AGENT, gSensorRange, PI);
        else if (change & CHANGED_OWNER)
            Setup();
    }

    // Terrible handy no script area hack.
    run_time_permissions (integer perm)
    {
        if (perm & PERMISSION_TAKE_CONTROLS)
        {
            // Take all the controls ALL the scripts in the same
            // object want to use or SVC-3187 will break them.
            llTakeControls(CONTROL_FWD, TRUE, TRUE);
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        list command = llParseString2List(message, [" "], []);

        if (llGetListLength(command) != 2)
            return;

        string verb = llList2String(command, 0);
        string argument = llList2String(command, 1);

        if (verb == "range")
        {
            gSensorRange = llListStatistics(LIST_STAT_MIN, [(float)argument, gMaxSensorRange]);
            llOwnerSay("The sensor range is " + (string)gSensorRange + " meters now.");
        }
        else if (verb == "interval")
        {
            gInterval = llListStatistics(LIST_STAT_MAX, [(float)argument, 1.0]);
            llOwnerSay("The sensor poll interval is " + (string)gInterval + " seconds now.");
            llSetTimerEvent(gInterval);
        }
        else if (verb == "scripts")
        {
            if (argument == "on")
            {
                llOwnerSay("Script usage is on");
                gScriptVoyeur = TRUE;
            }
            else
            {
                llOwnerSay("Script usage is off");
                gScriptVoyeur = FALSE;
            }

        }
    }


    no_sensor()
    {
        if (gLastNumDetected)
        {
            llSetText("0 in " + (string)((integer) gSensorRange) + "m", <0.,0.,0.>, gTextAlpha);
            llSetLinkPrimitiveParamsFast(LINK_ALL_CHILDREN, [
                PRIM_TEXT,
                "",
                <1., 1., 1.>,
                1.
            ]);
            gLastNumDetected = 0;
        }

    }

    timer()
    {
        llSensor("", "", AGENT, gSensorRange, PI);
    }

    sensor(integer num)
    {
        list statList = [];
        vector myPos = llGetPos();
        list status;
        integer i;
        for (i = 0; i < num; i++)
        {
            if (i > 15)
                jump endloop;
            float theirDistance = llVecDist(myPos, llDetectedPos(i));
            if (theirDistance <= gSensorRange) {
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
                status = [showName, " ", (integer)theirDistance , "m"];

                if (gScriptVoyeur)
                {
                    list scrStats = llGetObjectDetails(k, [OBJECT_RUNNING_SCRIPT_COUNT, OBJECT_SCRIPT_MEMORY]);
                    integer scrBytes = llList2Integer(scrStats, 1);
                    integer scrMB = scrBytes >> 20;
                    if (scrMB)
                        status += [" • ", llList2Integer(scrStats, 0), " @ ", scrMB, "M"];
                    else
                        status += [" • ", llList2Integer(scrStats, 0), " @ ", scrBytes >> 10, "K"];
                }

                llSetLinkPrimitiveParamsFast(llList2Integer(gPrims, i), [
                    PRIM_TEXT,
                        llDumpList2String(status, ""),
                        <1., 1., 1.>,
                        gTextAlpha
                ]);
            }
        }
        @endloop;

        for (; i < gLastNumDetected; i++)
        {
            llSetLinkPrimitiveParamsFast(llList2Integer(gPrims, i), [
                PRIM_TEXT,
                    "", <1., 1., 1.>,
                    1.
            ]);
        }
        gLastNumDetected = num;
        llSetText("(" + (string)((integer)gSensorRange) + "m) " + (string)num,  <1.0, 1.0, 1.0>, gTextAlpha);
    }
}
```