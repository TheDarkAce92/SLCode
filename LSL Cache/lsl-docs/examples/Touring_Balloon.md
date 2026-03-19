---
name: "Touring Balloon"
category: "example"
type: "example"
language: "LSL"
description: "My touring hot air balloon..."
wiki_url: "https://wiki.secondlife.com/wiki/Touring_Balloon"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

My touring hot air balloon...

- 1 Hot Air Balloon "Engine"
- 2 MegaPrim/LargeMass Vehicles
- 3 Automated Tour
- 4 Destinations
- 5 Finder
- 6 ILS Navigation
- 7 Landmarks
- 8 Region
- 9 Settings
- 10 Voice Control
- 11 Sample Tour Notecard

## Hot Air Balloon "Engine"

```lsl
//Hot Air Touring Balloon
//by Hank Ramos

//=========
//Overview
//=========
//The Hot air balloon consists of a large number of scripts, working together.  The balloon will not function properly without all of the scripts.  The scripts are broken up by function, mainly for convenience but also because of the limitations of the LSL scripting memory.

//============================
//Scripts and their Function
//============================
//Hot Air Balloon:
//The main script and "engine" of the entire balloon.  All major functions are done here

//Automated Tour:
//Handles automatic tours given by a pre-set Tour notecard.  The script reads and follows the directions given in the script, and sends commands to the Hot Air Balloon script.

//Destination Script:
//Handles the file i/o of the tour notecards.  It converts the notecard information to a list of destinations for the Automated Tour script to handle.

//Finder Script:
//Handles notification of the owner of the balloon in case the balloon is lost.

//ILS Navigation:
//Handles reception of communications from ILS beacons. The owner manually activates the ILS beacon, which then communicates docking or nav info to this script.

//Landmark Script:
//Handles drag-and-dropped landmarks. Reads the landmark information, then passes it along to the Hot Air Balloon Script

//Region Script:
//Used to be a separate script along with another script that read world coordinates of various sims from a notecard.  Very slow, and required updating.
//Now, this script simply provides world coordinates from the llRequestSimulatorData function.

//Settings Script:
//Reads from the settings notecard and informs various scripts of their default settings.

//Voice Control:
//Provides centralized listen event to distribute voice commands to all of the scripts in the balloon.

//Air Bag Script (found in the invisible air bags and the bain air bag at the top):
//This script receives buoyancy values from the Hot Air Balloon script, and help make the balloon float and sink

//Display Script (found in the overhead display prim, invisible prim but visible text):
//Handles the display and timed request of information from the Hot Air Balloon Script.  When not receiving text to display, it automatically triggers the Hot Air Balloon script to send distance, destination, and altitude info back to this script.

//MasterFlameScript
//Receives Flame 911 info, and controls all other flames and sound.

//FlameScript
//Works in conjunction with the MasterFlameScript to show coordinated flames.

//==================================
//Constants Used with Link Messages
//==================================
//100   : Request Region World Coordinates
//102   : >>>Deprecated<<<
//110   : Request Landmark Information for a particular Tour Stop #.
//200   : Receive Region World Coordinates sent by the 100 command
//203   : >>>Deprecated<<<
//210   : Send Landmark Information to the Hot Air Balloon.
//211   : Send number of destinations in the loaded tour to the Automated Tour Script.
//237   : Broadcast current TravelForce, ArriveForce, DefaultZ settings from Settings Script.
//238   : Broadcast current Upforce, DownForce, Precision settings from Settings Script.
//240   : Send "API" command to all script.  Same as a voice command.
//411   : Text to display on the overhead display
//412   : Broadcast current Display Rate setting from Settings Script.
//482   : Broadcast current ChatChannel setting from Settings Script.
//487   : Send tour notecard name to the Destination Script.  Triggers automatic loading of that card as well.
//501   : Air Bag Buoyancy Information.
//555   : Send the current "Distance to Destination" to the Automated Tour script
//850   : Instructs Hot Air Balloon to send "Destination Name" info to the overhead display.
//851   : Instructs Hot Air Balloon to send "Distance to Destination" info to the overhead display.
//852   : Instructs Hot Air Balloon to send "Altitude" info to the overhead display.
//911   : Flame control
//999   : Broadcast reset to all scripts
//2658  : Manual Mode.  Informs the Automated Tour that we are currently in manual mode, and not following a tour notecard.
//95562 : Voice Command string broadcast by Voice Control Script. Each script processes their own particular commands.

vector  LPos;
vector  RPos;
vector  hovL;
vector  hovR;
string  dest;
string  region;
vector  destV;   //dock, undock, distance
integer hovering;
vector  forces;  //Upforce, DownForce, Precision
vector  defs;    //TravelForce, ArriveForce, DefaultZ
float   comp = 0;
float   mass;
vector  pos;
integer broadcastCounter;
float   currentFalseAlt;

string cap(string v)
{
    v = llToUpper(llGetSubString(v, 0, 0)) + llGetSubString(v, 1, llStringLength(v) - 1);
    return v;
}

disp(string message)
{
    llMessageLinked(LINK_ALL_CHILDREN, 411, message, NULL_KEY);
}

vector totarget(float gx, float gy, float lx, float ly)
{
    vector target;
    vector dir;
    vector corner = llGetRegionCorner();

    pos.x = pos.x + corner.x;
    pos.y = pos.y + corner.y;

    target.x = gx + lx;
    target.y = gy + ly;
    target.z = pos.z;

    dir = target - pos;
    destV.z = llVecMag(dir);

    dir = llVecNorm(dir);
    return dir;
}

turn(integer dock, float tau)
{
    return;
    vector vel;

    if(dock)
    {
        vel = <-0.00163, -0.00020, -1.00000>;
    }
    else
    {
        vel = llVecNorm(llGetVel());
    }
    vel.z = 0.0;
    vector fwd = llRot2Up(llGetRot());
    vector imp = fwd % vel;
    imp = (1/tau) * imp;
    vector omega = llGetOmega();
    imp = (mass * (imp - omega));
    llApplyRotationalImpulse(imp, FALSE);
}

push(vector direction, float speed)
{
    vector ivel = llGetVel();
    vector fvel = direction * speed;
    vector imp = (mass * (fvel - ivel))/10;

    llApplyImpulse(imp, FALSE);
}

alt(float tarz)
{
    float setFloatHeight;
    //float  zdiff = llFabs(pos.z - tarz);
    //
    //if (zdiff > 15)
    //{
    //    comp = 0.1 * ((zdiff - 15)/75);
    //    llOwnerSay("Compensation is now: " + (string)comp);
    //}
    //else
    //{
    //    comp = 0;
    //}
    if(pos.z < tarz)
    {
        //llMessageLinked(LINK_ALL_CHILDREN, 501, (string)(forces.x + comp), "");
        //llMessageLinked(LINK_ALL_CHILDREN, 501, (string)(forces.x), "");
        llMessageLinked(LINK_ALL_CHILDREN, 911, (string)TRUE, NULL_KEY);
        if (currentFalseAlt < tarz - 50) currentFalseAlt = tarz - 50 - forces.x;
        currentFalseAlt += forces.x;
        if (currentFalseAlt > tarz + 10) currentFalseAlt = tarz + 10;
        //llOwnerSay("Decrementing currentFalseAlt by " + (string)forces.x);
        //llSetBuoyancy(forces.x);
        //llOwnerSay("Buoyance Set to = " + (string)forces.x);
    }
    else
    {
        //llMessageLinked(LINK_ALL_CHILDREN, 501, (string)(forces.y - comp), "");
        //llMessageLinked(LINK_ALL_CHILDREN, 501, (string)(forces.y), "");
        llMessageLinked(LINK_ALL_CHILDREN, 911, (string)FALSE, NULL_KEY);
        if (currentFalseAlt > tarz + 50) currentFalseAlt = tarz + 50 + forces.y;
        currentFalseAlt -= forces.y;
        if (currentFalseAlt < tarz - 10) currentFalseAlt = tarz - 10;
        //llOwnerSay("Decrementing currentFalseAlt by " + (string)forces.y);
        //llSetBuoyancy(forces.y);
        //llOwnerSay("Buoyance Set to = " + (string)forces.y);
    }

    setFloatHeight = currentFalseAlt - llGround( <0.0, 0.0, 0.0> );
    if (pos.z < tarz)
    {
        if (setFloatHeight > 100) setFloatHeight = -100;
    }
    //if (setFloatHeight > 100) setFloatHeight = -(2147483648 - setFloatHeight);
    llSetVehicleFloatParam( VEHICLE_HOVER_HEIGHT, setFloatHeight);
    //llOwnerSay((string)setFloatHeight);
    //llSetVehicleFloatParam( VEHICLE_HOVER_HEIGHT, currentFalseAlt);
}

vect(integer hovering)
{
    //Update Global Info
    //mass = llGetMass();
    pos = llGetPos();

    //The "engine" of the balloon...
    vector dir = totarget(RPos.x, RPos.y, LPos.x, LPos.y);
    if(destV.z > 15)
    {
        push(dir, defs.x);
    }
    else
    {
        push(dir, defs.y);
    }
    turn(0, 3.0);
    alt(LPos.z);
    broadcastCounter++;
    if (broadcastCounter == 10)
    {
        if (!hovering){llMessageLinked(llGetLinkNumber(), 555, (string)destV.z, NULL_KEY);};
        broadcastCounter = 0;
    }
    //currentFalseAlt -= 0.01;
}

checkC(string m, key id)
{
    m = llToLower(m);
    if (m == "reset scripts")
    {
        disp("Resetting Scripts...");
        llResetScript();
    }
    if (m == "startup")
    {
        state startup;
    }
    if (m == "shutdown")
    {
        state shutdown;
    }
    if (m == "hover")
    {
        state hover;
    }
    if ((m == "resume") && (hovering))
    {
        LPos = hovL;
        RPos = hovR;
        state travel;
    }
}

checkTC(string msg, key id)
{
    float checkN;
    integer listLength;
    msg = llToLower(msg);
    if (llSubStringIndex(msg, "landmark ") == 0)
    {
        llMessageLinked(LINK_SET, 2658, "", NULL_KEY);//Manual Mode

        list tempList = llCSV2List(llGetSubString(msg,9,llStringLength(msg)));
        listLength = llGetListLength(tempList);
        region = llList2String(tempList, 0);
        dest   = "Manual Landmark";
        if (listLength >= 1)
        {
            if (defs.z >= 1)
            {
                LPos = <128,128,defs.z>;
            }
            else
            {
                LPos = <128,128,LPos.z>;
            }
        }
        if (listLength == 4)
        {
            LPos.z = llList2Float(tempList, 3);
        }
        if ((listLength == 4) || (listLength == 3))
        {
            LPos.x = llList2Float(tempList, 1);
            LPos.y = llList2Float(tempList, 2);
        }
        llMessageLinked(LINK_SET, 100, region, NULL_KEY);
        return;
    }
    if (llSubStringIndex(msg, "altitude ") == 0)
    {
        checkN = (float)llGetSubString(msg,9,18);
        if (checkN > 0.001)
        {
            LPos.z = checkN;
            disp("Altitude Set to " + (string)((integer)LPos.z) + " meters");
        }
        return;
    }
    if (llSubStringIndex(msg, "bump ") == 0)
    {
        checkN = (float)llGetSubString(msg,5,18);
        LPos.z += checkN;
        disp("Altitude bumped by " + (string)((integer)checkN) + " meters to " + (string)((integer)LPos.z) + " meters");
        return;
    }
    if (msg == "dock")
    {
        LPos.z = destV.x;
        disp("Docking at " + (string)((integer)LPos.z) +  " meters");
        return;
    }
    if (msg == "undock")
    {
        LPos.z = destV.y;
        disp("Heading for " + (string)((integer)LPos.z) +  " meters");
        return;
    }
}

checkM(integer n, string m, key id)
{
    vector position = llGetPos();
    list   L;

    //Destination Name = 850
    if ((n == 850) && (dest != "None"))
    {
        disp("Destination: " + cap(dest) + ", " + cap(region) + "(" + (string)((integer)LPos.x) + "," + (string)((integer)LPos.y)  + ")");
        return;
    }

    //Distance To Destination = 851
    if ((n == 851) && (dest != "None"))
    {
        disp("Distance To Destination: " + (string)((integer)destV.z) + " meters");
        return;
    }

    //Altitude = 852
    if (n == 852)
    {
        disp("Altitude: " + (string)((integer)position.z) + " meters");
        return;
    }

    //Process Return of Landmark Info Retrieval
    if (n == 210)
    {
        L = llCSV2List(m);

        dest    = llList2String(L, 0);
        region  = llList2String(L, 1);
        LPos.x  = llList2Float (L, 2);
        LPos.y  = llList2Float (L, 3);
        destV.x = llList2Float (L, 4);
        destV.y = llList2Float (L, 5);
        LPos.z  = destV.y;

        if (region != "")
        {
            llMessageLinked(LINK_SET, 100, region, NULL_KEY);
        }
        return;
    }
    //Process API Commands
    if (n == 240)
    {
        checkC(m, id);
        checkTC(m, id);
        return;
    }
    //Process API Forces Commands
    if (n == 238)
    {
        forces = (vector)m;
        return;
    }
    //Process API Other Commands
    if (n == 237)
    {
        defs = (vector)m;
        return;
    }

    //Process Return of Region Vector Determination
    if (n == 200)
    {
        RPos = (vector)m;
        state travel;
    }
}

reset()
{
    integer scriptCount = llGetInventoryNumber(INVENTORY_SCRIPT);
    integer x;
    string  scriptName;

    for (x=0; x < scriptCount ; x++)
    {
        scriptName = llGetInventoryName(INVENTORY_SCRIPT, x);
        if (scriptName != llGetScriptName())
        {
            llResetOtherScript(scriptName);
        }
    }
    llOwnerSay("To use the Touring Hot Air Balloon, simply sit on the balloon and say \"help\".");
}

init()
{
    dest  = "None";
    llMessageLinked(LINK_SET, 102, "", "");
    llSetStatus(STATUS_PHYSICS, FALSE);
    llSetStatus(STATUS_PHANTOM, FALSE);
    llMessageLinked(LINK_ALL_CHILDREN, 911, (string)FALSE, NULL_KEY); //Turn off Flames
    llSetVehicleType(VEHICLE_TYPE_BALLOON);
    //llSetVehicleFlags(VEHICLE_FLAG_HOVER_GLOBAL_HEIGHT);
    llSetVehicleFlags(VEHICLE_FLAG_HOVER_TERRAIN_ONLY);
    //llSetVehicleFloatParam(VEHICLE_VERTICAL_ATTRACTION_TIMESCALE, 1.0);
    //llSetVehicleFloatParam(VEHICLE_VERTICAL_ATTRACTION_TIMESCALE, 3.0);
    //llSetVehicleFloatParam(VEHICLE_VERTICAL_ATTRACTION_EFFICIENCY, 0.8);

    //llSetVehicleFloatParam(VEHICLE_HOVER_TIMESCALE, 1.0);
    //llSetVehicleFloatParam(VEHICLE_HOVER_TIMESCALE, 3.0);
    //llSetVehicleFloatParam(VEHICLE_HOVER_EFFICIENCY, 0.8);
}
//STATES
default
{
    state_entry()
    {
        reset();
        init();
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    link_message(integer sn, integer n, string m, key id)
    {
        //Process Listen Commands
        if (n == 95562)
        {
            checkC(m, id);
            return;
        }
        checkM(n, m, id);
    }
}
state startup
{
    state_entry()
    {
        vector cpos = llGetPos();

        disp("Starting up...");
        dest = "None";
        llSetBuoyancy(1.0);
        llSetStatus(STATUS_ROTATE_X | STATUS_ROTATE_Y, FALSE);
        llSetStatus(STATUS_ROTATE_Z | STATUS_PHYSICS | STATUS_BLOCK_GRAB, TRUE);
        llSetStatus(STATUS_PHYSICS, TRUE);
        //llMessageLinked(LINK_ALL_CHILDREN, 501, (string)forces.y, "");
            mass = llGetMass();
        state hover;
    }
    on_rez(integer start_param)
    {
        llResetScript();
    }
}
state shutdown
{
    state_entry()
    {
        disp("Shutting Down...");
        llMessageLinked(LINK_ALL_CHILDREN, 911, (string)FALSE, NULL_KEY);
        llSetStatus(STATUS_PHYSICS, FALSE);
        llSetTimerEvent(1);
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    link_message(integer sender_num, integer n, string m, key id)
    {
        //Process Listen Commands
        if (n == 95562)
        {
            checkC(m, id);
            return;
        }
        checkM(n, m, id);
    }

    timer()
    {
        if (llGetStatus(STATUS_PHYSICS))
        {
            llSetStatus(STATUS_PHYSICS, FALSE);
        }
        else
        {
            llSetTimerEvent(0);
            disp("Successfully Shut Down");
        };
    }
}
state hover
{
    state_entry()
    {
        hovering = TRUE;
        hovL     = LPos;
        hovR     = RPos;
        LPos     = llGetPos();
        RPos     = llGetRegionCorner();
        disp("Hovering at " + (string)((integer)LPos.z) + " meters");
        currentFalseAlt = LPos.z;
        llSetTimerEvent(forces.z);
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    link_message(integer sn, integer n, string m, key id)
    {
        //Process Listen Commands
        if (n == 95562)
        {
            checkTC(m, id);
            checkC(m, id);
            return;
        }
        checkM(n, m, id);
    }

    timer()
    {
        vect(TRUE);
    }

    state_exit()
    {
        hovering = FALSE;
    }
}
state travel
{
    state_entry()
    {
        disp("Heading for " + (string)((integer)LPos.z) + " meters");
        llSetTimerEvent(forces.z);
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    link_message(integer sender_number, integer number, string message, key id)
    {
        //Process Listen Commands
        if (number == 95562)
        {
            checkTC(message, id);
            checkC(message, id);
            return;
        }
        checkM(number, message, id);
    }

    timer()
    {
        vect(FALSE);
    }
}
```

## MegaPrim/LargeMass Vehicles

I've found that large mass vehicles pose a problem as llApplyImpulse uses energy faster than most megaprims, even those of smaller dimensions such as <11,11,.5>, can replenish. I've had success changing the following code.

Change the push function in the ATB Engine from:

```lsl
push(vector direction, float speed)
{
    vector ivel = llGetVel();
    vector fvel = direction * speed;
    vector imp = (mass * (fvel - ivel))/10;

    llApplyImpulse(imp, FALSE);
}
```

To the following code which applies a constant force:

```lsl
push(vector direction, float speed)
{
    vector ivel = llGetVel();
    vector fvel = direction * speed;
    vector imp = (mass * (fvel - ivel))/10;

    llSetForce(imp, FALSE);
}
```

- Cydkne Chronowire

## Automated Tour

```lsl
//Automated Tour
//by Hank Ramos
//June 22, 2004

integer ListenAPI = 95562;
string  destName = "None";
string  region; //regionName
integer stop;
integer dests; //destionationsCount
integer regions;
integer wp = FALSE; //waypoint
integer pa; //pause
integer ar = TRUE; //arrived
vector  localP; //localPosition
float   distance;
integer distRecv; //distanceReceived
float   time;

disp(string m)
{
    llMessageLinked(LINK_SET, 411, m, NULL_KEY);
}

string cap(string v)
{
    v = llToUpper(llGetSubString(v, 0, 0)) + llGetSubString(v, 1, llStringLength(v) - 1);
    return v;
}

next()
{
    if (stop > 0)
    {
        disp("Continuing to Next Stop.");
        if(stop < dests)
        {
            stop += 1;
        }
        else
        {
            stop = 1;
        }
        llMessageLinked(LINK_SET, 110, (string)((integer)stop), NULL_KEY); //Process Landmark
        state idle;
    }
}

checkTC(string m, key id)
{
    integer newStop;

    m = llToLower(m);
    if (llSubStringIndex(m, "goto ") == 0)
    {
        newStop = (integer)llGetSubString(m, 5,8);
        if ((newStop <= dests) && (newStop > 0))
        {
            stop = newStop;
            llMessageLinked(LINK_SET, 110, (string)((integer)stop), NULL_KEY); //Process Landmark
            state idle;
        }
        else
        {
            disp("Stop #" +  (string)newStop + " is Invalid.");
        }
        return;
    }
    if (llSubStringIndex(m, "timeout ") == 0)
    {
        pa = (integer)llGetSubString(m, 8,12);
        return;
    }
    if (llSubStringIndex(m, "extend ") == 0)
    {
        pa += (integer)llGetSubString(m, 7,12);
        return;
    }
    if (m == "next")
    {
        next();
        return;
    }
    if (m == "shutdown")
    {
        stop = 0;
        state idle;
    }
}

checkM(integer n, string m, key id)
{
    if (n == 210)
    {
        string tempS;
        list L = llCSV2List(m);

        destName = llList2String (L, 0);
        region   = llList2String (L, 1);
        localP.x = llList2Float  (L, 2);
        localP.y = llList2Float  (L, 3);
        wp       = llList2Integer(L, 6); //Waypont
        pa       = llList2Integer(L, 7); //Pause

        //llMessageLinked(LINK_SET, 100, regionName, NULL_KEY); //This is done in the balloon script
        if (stop > 0)
        {
            tempS ="Destination set to Landmark #" + (string)stop + ", ";
        }
        else
        {
            tempS ="Destination set to ";
        }
        disp(tempS + destName + ", " + region +  \
                     "(" + (string)((integer)localP.x) + "," + (string)((integer)localP.y) + ").");
        state enroute;
    }
    if (n == 555)
    {
        distance = (float)m;
        distRecv = TRUE;
        return;
    }
    if (n == 211)
    {
        dests = (integer)m;
        return;
    }
    if (n == 2658)
    {
        stop = 0;
        wp = FALSE;
        pa = 0;
        if (m == "reset")
        {
            state loading;
        }
        else
        {
            state idle;
        }
    }
}

//STATES
default
{
    state_entry()
    {
        disp("Initializing Automated Tour...");
        state loading;
    }
}

state loading
{
    link_message(integer sn, integer n, string m, key id)
    {
        if (n == 95562)
        {
            checkTC(m, id);
            return;
        }
        if (n == 211)
        {
            dests = (integer)m;
            state idle;
        }
        checkM(n, m, id);
    }
}

state enroute
{
    state_entry()
    {
        distRecv = FALSE;
        distance = 999999999;
        disp("Enroute to Destination...");
    }

    on_rez(integer sp)
    {
        state idle;
    }

    link_message(integer sn, integer n, string m, key id)
    {
        if (n == 95562)
        {
            checkTC(m, id);
            return;
        }
        checkM(n, m, id);
        if (distRecv)
        {
            if (distance < 20)
            {
                state arrive;
            }
        }
    }
}

state arrive
{
    state_entry()
    {
        string tempS;

        if (stop > 0)
        {
            tempS = "Arrived at Landmark #" + (string)stop+ ", ";
        }
        else
        {
            tempS = "Arrived at ";
        }

        disp(tempS + destName + ", " + cap(region) +  \
                       "(" + (string)((integer)localP.x) + "," + (string)((integer)localP.y) + ").");
        if (pa > 0)
        {
            llGetAndResetTime();
            llSetTimerEvent(5);
        }
        if (wp)
        {
            next();
        }
    }

    on_rez(integer sp)
    {
        state idle;
    }

    link_message(integer sn, integer n, string m, key id)
    {
        if (n == 95562)
        {
            checkTC(m, id);
            return;
        }
        checkM(n, m, id);
    }

    timer()
    {
        time = llGetTime();
        float calcTime = pa - time;

        if (pa > 0)
        {
            if (calcTime <= 0)
            {
                next();
            }
            else if ((calcTime > 1) && (calcTime < 60))
            {
                disp("Leaving in " + (string)((integer)calcTime)  + " seconds.");
            }
            else if ((calcTime >= 60)&& (calcTime < 120))
            {
                disp("Leaving in approximately 1 minute.");
            }
            else if (calcTime >= 120)
            {
                disp("Leaving in " + (string)((integer)(calcTime / 60))  + " minutes.");
            }
        }
    }
}

state idle
{
    link_message(integer sn, integer n, string m, key id)
    {
        if (n == 95562)
        {
            checkTC(m, id);
            return;
        }
        checkM(n, m, id);
    }
}
```

## Destinations

```lsl
integer count;
list    dests;
string  notecard;
integer lineCount;
key     readKey;

displayMessage(string m)
{
    llMessageLinked(LINK_SET, 411, m, NULL_KEY);
}
loadLandmarks()
{
    displayMessage("Loading " + notecard + "...");
    dests = [];
    count = 0;
    lineCount = 0;
    readKey = llGetNotecardLine(notecard, lineCount);
}

checkC(string m, key id)
{
    integer index;
    list    landmarkInfo;
    string  testM;

    testM = llToLower(m);

    if (llSubStringIndex(testM, "destination notecard ") == 0)
    {
        notecard =llGetSubString(m, 21, 100);
        displayMessage("Destination Notecard Changed To: " + notecard + ".");
        llMessageLinked(LINK_SET, 2658, "reset", NULL_KEY);
        loadLandmarks();
        return;
    }
    if (llSubStringIndex(testM, "notecard ") == 0)
    {
        notecard =llGetSubString(m, 9, 100);
        displayMessage("Destination Notecard Changed To: " + notecard + ".");
        llMessageLinked(LINK_SET, 2658, m, NULL_KEY);
        loadLandmarks();
        return;
    }
    if ((testM == "reset destinations") || (testM == "reset notecards"))
    {
        loadLandmarks();
        return;
    }
    if (testM == "say destinations")
    {
        //Get Landmark Info
        for (index = 0;index < count;index += 1)
        {
            landmarkInfo = llCSV2List(llList2String(dests, index));

            llWhisper(0, "Destination #" + (string)(index +1) + ": " + llList2String(landmarkInfo,0));
        }
        return;
    }
}

string getLandmark(integer index)
{
    index -= 1;
    return llList2String(dests, index);
}

default
{
    state_entry()
    {
    }
    link_message(integer sn, integer n, string m, key id)
    {
        if (n == 95562)
        {
            checkC(m, id);
            return;
        }
        if (n == 487)
        {
            notecard = m;
            loadLandmarks();
            return;
        }
        if (n == 110)
        {
            //Get Landmark Info
            llMessageLinked(LINK_SET, 210, getLandmark((integer)m), NULL_KEY);
        }
    }

    dataserver(key requested, string data)
    {
        list L;

        //Process Landmarks
        if (requested == readKey)
        {
            L = llCSV2List(data);
            if (data != EOF)
            {
                if ((llSubStringIndex(data, "#") != 0) && (llGetListLength(L) == 8))
                {
                    dests += data;
                    count += 1;
                }
                lineCount += 1;
                readKey = llGetNotecardLine(notecard, lineCount);
            }
            else
            {
                displayMessage("There are " + (string)(count) + " destinations loaded.");
                llMessageLinked(LINK_SET, 211, (string)count, NULL_KEY);
            }
        }
    }
}
```

## Finder

```lsl
//Finder Script
//By Hank Ramos
//Portions originally by Eggy Lippmann
//===========================
//Configurable Options...
float sensorInterval = 1800; //Seconds between scans
float sensorDistance = 30.0; //Max distance owner can be from object, Max is 96 meters
//===========================
string  OwnerName;
integer dispOnce;
integer gotName;

disp(string message)
{
    llMessageLinked(LINK_ALL_CHILDREN, 411, message, NULL_KEY);
}

initialize()
{
    dispOnce = FALSE;
    gotName  = FALSE;
    llSensorRepeat("", llGetOwner(), AGENT, 96, TWO_PI, 1); //Get Name of Avatar, so use max diatance and min time
}

checkC(string message, key id)
{

    if ((llSameGroup(id)) || (id == llGetOwner()))
    {
        message = llToLower(message);
        if (llSubStringIndex(message, "finder rate ") == 0)
        {
            sensorInterval = (float)llGetSubString(message,12,18) * 60;
            disp("Finder Sensor Rate Set To " + (string)((integer)(sensorInterval/60)) + " minutes");
        }

        else if (llSubStringIndex(message, "finder distance ") == 0)
        {
            sensorDistance = (float)llGetSubString(message,16,22) * 60;
            disp("Finder Sensor Distance Set To " + (string)((integer)(sensorDistance/60)) + " meters");
        }

        else if ((message == "startup") || (message == "finder on"))
        {
            dispOnce = FALSE;
            disp("Finder is On.  If lost, will IM " + OwnerName);
        }

        else if ((message == "shutdown") || (message == "finder off"))
        {
            disp("Finder is Off. No lost notifications will be sent.");
            llSensorRemove();
        }
    }
}
default
{
    state_entry()
    {
        initialize();
    }
    on_rez(integer start_param)
    {
        llResetScript();
    }
    sensor(integer num_detected)
    {
        if (!gotName)
        {
            gotName   = TRUE;
            OwnerName = llDetectedName(0);
            llSensorRepeat("", "", AGENT, sensorDistance, TWO_PI, 5); //Get Name of Avatar, so use max diatance and min time
        }
        dispOnce = FALSE;
    }
    no_sensor()
    {
        if ((llGetTime() >= sensorInterval) || (!dispOnce))
        {
            llWhisper(0, OwnerName + " lost me! Tell them to come and get me at " + (string) llGetPos() + " in the " + llGetRegionName() + " region.");
            llInstantMessage(llGetOwner(), "I'm lost!  Come and get me at " + (string) llGetPos() + " in the " + llGetRegionName() + " region.");
            llResetTime();
        }
        if (!dispOnce)
        {
            dispOnce = TRUE;
            llResetTime();
        }
    }
    link_message(integer sender_number, integer number, string message, key id)
    {
        if (number == 95562)
        {
            checkC(message, id);
            return;
        }
        //Process API Commands
        if (number == 240)
        {
            checkC(message, id);
            return;
        }
    }

}
```

## ILS Navigation

```lsl
integer channel = 36658425;

default
{
    state_entry()
    {
        llListen(channel, "", NULL_KEY, "");
    }
    on_rez(integer startup_param)
    {
        llResetScript();
    }

    listen(integer channel, string name, key id, string message)
    {
        list packet;
        list navinfo;
        string owner;

        packet = llCSV2List(message);
        owner = llKey2Name(llGetOwner());

        if (owner == llList2String(packet, 1))
        {
            navinfo += llList2String(packet, 0);
            navinfo += llToLower(llList2String(packet, 2));
            navinfo += llList2Float(packet, 3);
            navinfo += llList2Float(packet, 4);
            navinfo += llList2Float(packet, 5);
            navinfo += llList2Float(packet, 6);

            llMessageLinked(llGetLinkNumber(), 210, llList2CSV(navinfo), NULL_KEY);
        }

     }
}
```

## Landmarks

```lsl
//Landmark Inventory Script
//supports reading of drag and dropped landmarks on this vehicle

string landmarkName;
key    reqID;

default
{
    changed(integer change)
    {
        if (change == CHANGED_INVENTORY)
        {
            if (llGetInventoryNumber(INVENTORY_LANDMARK) > 0)
            {
                landmarkName = llGetInventoryName(INVENTORY_LANDMARK, 0);
                if (llGetInventoryKey(landmarkName) != NULL_KEY)
                  reqID = llRequestInventoryData(landmarkName);
            }
        }
    }
    dataserver(key queryid, string data)
    {
        //vector localPos;
        vector regionPos;
        list   tempList;
        integer x;
        integer test;
        list navinfo;
        vector targetPos;
        vector targetRegionPos;

        if (queryid == reqID)
        {
            llRemoveInventory(landmarkName);

            test = llSubStringIndex(landmarkName, ",");
            if (test >= 0)
            {
                tempList = llCSV2List(landmarkName);
                landmarkName = llList2String(tempList, 0);
            }

            targetPos = (vector)data; //Get Offset to Local Position

            regionPos = llGetRegionCorner();

            targetPos = targetPos + regionPos;  //Convert targetPos to absolute world coordinates

            targetRegionPos = targetPos;
            targetRegionPos.x = ((integer)((targetRegionPos.x) / 256)) * 256;
            targetRegionPos.y = ((integer)((targetRegionPos.y) / 256)) * 256;

            vector localPos = llGetPos();
            navinfo += landmarkName;
            navinfo += "";
            navinfo += targetPos.x - targetRegionPos.x;
            navinfo += targetPos.y - targetRegionPos.y;
            navinfo += localPos.z;
            navinfo += localPos.z;

            llMessageLinked(llGetLinkNumber(), 210, llList2CSV(navinfo), NULL_KEY);
            llMessageLinked(llGetLinkNumber(), 200, (string)targetRegionPos, NULL_KEY);
        }
     }
}
```

## Region

```lsl
//Region Database Script
//by Hank Ramos

key     RegionReadKey;

default
{
    state_entry()
    {
    }

    link_message(integer sn, integer n, string m, key id)
    {
        string tempString;
        vector tempVector;
        list   tempList;

        m = llToLower(m);
        if (n == 100)
        {
            //Convert Name to Vector
            RegionReadKey = llRequestSimulatorData(m, DATA_SIM_POS);
            return;
        }

        if (n == 999)
        {
            llResetScript();
        }
    }

    dataserver(key requested, string data)
    {
        if (requested == RegionReadKey)
        {
            llMessageLinked(llGetLinkNumber(), 200, data, NULL_KEY);
        }
    }
}
```

## Settings

```lsl
integer Count;
string  Notecard = "Settings";
integer LineCount;
key     ReadKey;
vector  forces;    //Upforce, DownForce, Precision
vector  defs;      //TravelForce, ArriveForce, DefaultZ
integer altChatCH; //Alternative Chat Channel
string  home;
integer distRecv;  //distanceReceived
float   distance;
float   dockZ;
integer docking;
float   dispRate;
integer chatChannel;
string  TourName;

disp(string m)
{
    llMessageLinked(LINK_SET, 411, m, NULL_KEY);
}
loadSettings()
{
    disp("Loading " + Notecard + "...");
    Count = 0;
    LineCount = 0;
    ReadKey = llGetNotecardLine(Notecard, LineCount);
}
checkC(string m, key id)
{
    integer Index;
    list    landmarkInfo;
    string  tempString;

    m = llToLower(m);
    if (m == "help")
    {
        llGiveInventory(id, "Touring Balloon Instructions");
        return;
    }
    if (m == "reset settings")
    {
        loadSettings();
        return;
    }
    if (m == "return home")
    {
        disp("Returning home...");
        docking = FALSE;
        landmarkInfo = llCSV2List(home);
        dockZ = llList2Float(landmarkInfo,3);
        tempString = "Home," + llList2String(landmarkInfo,0) + "," + llList2String(landmarkInfo,1) + "," + \
                     llList2String(landmarkInfo,2) + "," + llList2String(landmarkInfo,3) +"," + llList2String(landmarkInfo,4);
        llMessageLinked(LINK_SET, 210, tempString, NULL_KEY);
        llSetTimerEvent(10.0);
        return;
    }
    if (m == "say settings")
    {
        llWhisper(0, "Home        = " + home);
        llWhisper(0, "DefaultZ    = " + (string)defs.z);
        llWhisper(0, "Precision   = " + (string)forces.z);
        llWhisper(0, "UpForce     = " + (string)forces.x);
        llWhisper(0, "DownForce   = " + (string)forces.y);
        llWhisper(0, "TravelForce = " + (string)defs.x);
        llWhisper(0, "ArriveForce = " + (string)defs.y);
        llWhisper(0, "Alt Chat CH = " + (string)chatChannel);
        return;
    }
    if (llSubStringIndex(m, "speed ") == 0)
    {
        defs.x = (float)llGetSubString(m,6,18);
        llMessageLinked(LINK_SET, 237, (string)defs, llGetOwner());
        disp("Speed Set to " + (string)defs.x);
        return;
    }
    if (llSubStringIndex(m, "precision ") == 0)
    {
        forces.z = (float)llGetSubString(m,10,18);
        llMessageLinked(LINK_SET, 238, (string)forces, llGetOwner());
        disp("Timer Precision Set to " + (string)((integer)(forces.z*1000)) + " ms");
        return;
    }
    if (llSubStringIndex(m, "upforce ") == 0)
    {
        forces.x = forces.x + ((float)llGetSubString(m,8,18))/1000;
        llMessageLinked(LINK_SET, 238, (string)forces, llGetOwner());
        disp("Up Force " + (string)((integer)(forces.x*1000)));
        return;
    }
    if (llSubStringIndex(m, "downforce ") == 0)
    {
        forces.y = forces.y + ((float)llGetSubString(m,10,18))/1000;
        llMessageLinked(LINK_SET, 238, (string)forces, llGetOwner());
        disp("Down Force " + (string)((integer)(forces.y*1000)));
        return;
    }
    if (llSubStringIndex(m, "display rate ") == 0)
    {
        dispRate = (float)llGetSubString(m,13,18);
        llMessageLinked(LINK_SET, 412, (string)dispRate, llGetOwner());
        disp("Display Rate Set to " + (string)dispRate + " seconds");
        return;
    }
    if (llSubStringIndex(m, "chat channel ") == 0)
    {
        chatChannel = (integer)llGetSubString(m,13,18);
        llMessageLinked(LINK_SET, 482, (string)chatChannel, llGetOwner());
        disp("Chat Channel Set to " + (string)chatChannel);
        return;
    }
}
default
{
    state_entry()
    {
        loadSettings();
    }
    on_rez(integer startup_param)
    {
        llResetScript();
    }
    timer()
    {
        vector position = llGetPos();
        //Check to see if we have arrived, if so, dock and then shutdown
        if (docking)
        {
            disp("Waiting to finish docking...");
            if((position.z > (dockZ - 2)) && (position.z < (dockZ + 2)))
            {
                disp("Shutting Down...");
                llMessageLinked(LINK_SET, 240, "shutdown", llGetOwner());
                llSetTimerEvent(0);
            }
        }
        else if (distance < 5)
        {
            disp("Sending Docking Command...");
            llMessageLinked(LINK_SET, 240, "dock", llGetOwner());
            docking = TRUE;
        }

    }
    link_message(integer sn, integer n, string m, key id)
    {
        if (n == 555)
        {
            distance = (float)m;
            distRecv = TRUE;
            return;
        }
        //Process API Commands
        if (n == 240)
        {
            checkC(m, id);
            return;
        }
        if (n == 95562)
        {
            checkC(m, id);
            return;
        }
    }

    dataserver(key requested, string data)
    {
        //Process Settings
        if (requested == ReadKey)
        {
            if (data != EOF)
            {
                if ((llSubStringIndex(data, "#") != 0) && (data != ""))
                {
                    if (Count == 0)
                    {
                         home = data;
                    }
                    if (Count == 1)
                    {
                        defs.z = (float)data;  //TravelForce, ArriveForce, DefaultZ
                    }
                    if (Count == 2)
                    {
                        forces.z = (float)data;  //Upforce, DownForce, Precision
                    }
                    if (Count == 3)
                    {
                        forces.x = ((float)data)/1000;  //Upforce, DownForce, Precision
                    }
                    if (Count == 4)
                    {
                        forces.y = ((float)data)/1000;  //Upforce, DownForce, Precision
                    }
                    if (Count == 5)
                    {
                        defs.x = (float)data;   //TravelForce, ArriveForce, DefaultZ
                    }
                    if (Count == 6)
                    {
                        defs.y = (float)data;   //TravelForce, ArriveForce, DefaultZ
                    }
                    if (Count == 7)
                    {
                        dispRate = (float)data;   //Display Rate
                    }
                    if (Count == 8)
                    {
                        chatChannel = (integer)data;   //Chat Channel
                    }
                    if (Count == 9)
                    {
                        TourName = (string)data; //Default Tour Notecard Name
                    }
                    Count += 1;
                }
                LineCount += 1;
                ReadKey = llGetNotecardLine(Notecard, LineCount);
            }
            else
            {
                disp("Settings are loaded");
                //Send settings
                llMessageLinked(LINK_SET, 238, (string)forces, llGetOwner());
                llMessageLinked(LINK_SET, 237, (string)defs,   llGetOwner());
                llMessageLinked(LINK_SET, 412, (string)dispRate,   llGetOwner());
                llMessageLinked(LINK_SET, 482, (string)chatChannel,   llGetOwner());
                llMessageLinked(LINK_SET, 487, TourName,   llGetOwner());
            }
        }
    }
}
```

...and associated notecard...

```lsl
#Settings
#This file contains your default settings
#The order of entries in this file is important.
#Do not change the order!
#You may add comments with lines beginning with "#"
#
#Home
#Region,X,Y,DockZ,TravelZ
#The location used when you tell the balloon to go home
#The balloon will automatically go there at the TravelZ
#altitude, then goto the DockZ altitude, then shutdown
Grignano,98.0,98.0,30,160
#Default Travel Height
#The default travel hight used when not specified
#Value of 0 means to use the current travel height
0
#Precision
#Timer precision, lower is bettter but harder on server
#Range 0.1-infinite.  In seconds
0.15
#Upforce
#The amount of upward force applied when the flames are on
450
#DownForce
#The amount of downward force applied when the flames are off
650
#PushTravel
#The amount of push during flight
8.0
#PushArrive
#The amount of push when you are within 10 meters of your destination
1.0
#DisplayRate
#The time, in seconds, that an item will be displayed in the central display
2.75
#Alternate Command Chanel
#An additional chat channel that can be used to communicate with the
#balloon.  Use "/channel command" format to silently communicate commands
#to the balloon.  Use "//command" to repeat the last channel used.
#If value is 0, then only the public chat channel is used.
0
#Default Tour Notecard Name
Welcome Tour
```

## Voice Control

```lsl
integer LISTEN_API   = 95562;
integer CHAT_CHANNEL = 482;

integer chatChannel = 0;
integer indexChat;

default
{
    state_entry()
    {
        indexChat = llListen(chatChannel, "", NULL_KEY, "");
    }
    on_rez(integer startup_param)
    {
        llResetScript();
    }
    listen(integer channel, string name, key id, string message)
    {
        if (name != "Display Panel")
        {
            if ((llSameGroup(id)) || (id == llGetOwner()))
            {
                llMessageLinked(LINK_SET, LISTEN_API, message, id);
            }
         }
    }
    link_message(integer sender_num, integer num, string str, key id)
    {
        if (num == CHAT_CHANNEL)
        {
            chatChannel = (integer)str;
            llListenRemove(indexChat);
            indexChat = llListen(chatChannel, "", NULL_KEY, "");
        }
    }

}
```

## Sample Tour Notecard

```lsl
#Welcome Tour
#
#There are 9 Parameters for each Destination
#Landmarks are accessed in the order they are in this file
#Starting with Destination #1
#1 = Title
#2 = Simulator Name
#3 = Local X
#4 = Local Y
#5 = Docking Z.  The docking altitude.
#6 = Travel Z.  The altitude used to travel to the destination.
#7 = Waypoint.  0=False, Any other value is TRUE.  If TRUE the the next landmark is automatically set when you are within 10 meters of the landmark.
#8= TimeToStay.  0=Disabled, Any other value waits at that position for the specified number of seconds and then selects next landmark.
#
#Note: any line beginning with "#" is a comment line, and is ignored
#
Vehicle Rezzing Area,Balance,194.0,226.0,24,53,0,60
Wild West Town,Oak Grove,67.8,48.0,12,35,0,60
Oak Grove,Oak Grove,109,168,40,50.0,1,0
Venice,bonifacio,24.5,150.5,28.0,115.0,0,120
Grignano,grignano,128,128,70,70,1,0
Sistiana,sistiana,235,17,70,70,1,0
Luna Oaks Galleria,Luna,53.0,53.0,33.0,50.0,0,60
Sistiana,sistiana,128,128,95,95,1,0
Grignano,grignano,170,250,95,95,1,0
Shangri-La,Dore,47.0,102.0,45.0,50.0,0,60
Bonifacio Waypoint,Bonifacio,110,43,60,60,1,0
Gibson Waypoint,Gibson,110,77,60,60,1,0
Oak Grove,Oak Grove,109,168,40,50.0,1,0
Vehicle Rezzing Area,Balance,194.0,226.0,24,53,0,60
```