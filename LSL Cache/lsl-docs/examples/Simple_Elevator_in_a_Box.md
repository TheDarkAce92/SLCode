---
name: "Simple Elevator in a Box"
category: "example"
type: "example"
language: "LSL"
description: "This is a vary simple elevator script, and not the best one out there. It was developed back during SL 2003 and may or may not function well now..."
wiki_url: "https://wiki.secondlife.com/wiki/Simple_Elevator_in_a_Box"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a vary simple elevator script, and not the best one out there.  It was developed back during SL 2003 and may or may not function well now...

```lsl
vector  alignment;
vector  targetVector;
integer travelDistance;
integer numListen;
integer targetFloor = -1;
list    floorHeights = [26.1,36,46,56,66,76,86,96,106,116,126,136];
float   fixedFloorHeight = 10; //Set to floor heights, or set to -1 to use floorHeights list
float   speed = 0.25; //Valid values are 0.01 to 1.0, a Percentage of maxSpeed;
float   maxSpeed = 32;
float   precision = 0.5;
integer autoSpeed = TRUE;
integer initialDistance;
integer commChannel = 6538559;
integer numListenPrivate;
integer TTL = 5;
float   lastCommand;

elevate (vector end)
{
    vector current = llGetPos();
    travelDistance = llRound(current.z-end.z);
    travelDistance = llAbs(travelDistance);

    if (autoSpeed)
    {
        if (travelDistance < (initialDistance / 2))
        {
            speed -= (precision * 2 / 50);
            if (speed < 0.25)
              speed = 0.25;
        }
        else
        {
            speed += (precision / 25);
            if (speed > 1)
              speed = 1;
        }
    }
    if (travelDistance > 30)
    {
        travelDistance = 30;
        if (end.z > current.z)
        {
            end.z = current.z + 30;
        }
        else
        {
            end.z = current.z - 30;
        }
    }
    float i = travelDistance/(maxSpeed*speed);
    llMoveToTarget(end,i);
}

GotoFloor (integer floor, key id)
{
    if (targetFloor != floor)
    {
        llSetStatus(STATUS_PHYSICS, TRUE);
        llLoopSound("ElevatorNoises", 1);

        targetFloor = floor;

        if (fixedFloorHeight > 0)
        {
            targetVector = alignment;
            targetVector.z = alignment.z + (fixedFloorHeight * floor);
        }
        else
        {
            targetVector = alignment;
            targetVector.z = llList2Float(floorHeights, floor);
        }

        vector current = llGetPos();
        initialDistance = llRound(current.z-targetVector.z);
        initialDistance = llAbs(initialDistance);

        if (autoSpeed)
        {
            speed = 0.01;
        }

        llSay(0, "Heading for Floor # " + (string)targetFloor + "[" + (string)targetVector.z + "]");
        elevate(targetVector);
        llSetTimerEvent(precision);
    }
}

reset()
{
    llSay(0, "Resetting Elevator...");
    llSetStatus(STATUS_ROTATE_X| STATUS_ROTATE_Y| STATUS_ROTATE_Z, FALSE);

    alignment = llGetPos();
    llSetStatus(STATUS_PHYSICS, FALSE);
    llStopSound();
    lastCommand = llGetTimeOfDay();
    llListenRemove(numListen);
    numListen = llListen( 0, "", NULL_KEY, "");
}
default
{
    state_entry()
    {
        reset();
    }
    on_rez(integer start_param)
    {
        reset();
        if (start_param > 0)
        {
            commChannel = start_param;
            llListenRemove(numListenPrivate);
            numListenPrivate = llListen(commChannel, "", NULL_KEY, "");
        }
    }
    listen(integer a, string n, key id, string m)
    {
        vector  pos;
        integer Floor;
        float   tempFloat;
        list    tempList;
        float   timeStamp;
        integer index;
        string  command;
        string  data;
        float   timediff;

        timediff = (llGetTimeOfDay() - lastCommand);
        if ((a == commChannel)&&(timediff > TTL))
        {
            lastCommand = llGetTimeOfDay();
            //Separate out incoming data
            tempList  = llCSV2List(m);
            timeStamp = llList2Float(tempList, 0);
            index     = llList2Integer(tempList, 1);
            command   = llList2String(tempList, 2);
            data      = llList2String(tempList, 3);

            //If public command then extract message
            if ((index == -2) && (command == "pub"))
            {
                m = data;
            }
        }

        if (llSubStringIndex(m, "goto floor") == 0)
        {
            Floor = (integer)llGetSubString(m, 10, llStringLength(m));
            GotoFloor(Floor, NULL_KEY);
        }
        if (llSubStringIndex(m, "speed") == 0)
        {
            tempFloat = (float)llGetSubString(m, 5, llStringLength(m));
            if ((tempFloat > 0.001) && (tempFloat <= 1.0))
            {
                speed = tempFloat;
            }
        }
        if ((m=="elevator reset") && (id==llGetOwner()))
        {
            reset();
        }
    }

    timer()
    {
        vector CurrentPos;
        float tempfloat;

        CurrentPos = llGetPos();
        tempfloat = (CurrentPos.z - targetVector.z);

        if (llFabs(tempfloat) < 2)
        {
            if (llFabs(tempfloat) < 0.05)
            {
                //Arrived at Floor
                llWhisper(0, "Arrived at floor #" + (string)targetFloor);
                llSetTimerEvent(0);
                llSetStatus(STATUS_PHYSICS, FALSE);
                llStopSound();
            }
            else
            {
                llMoveToTarget(targetVector,1.0);
            }
        }
        else
        {
            if (fixedFloorHeight > 0)
            {
                targetVector = alignment;
                targetVector.z = alignment.z + (fixedFloorHeight * targetFloor);
            }
            else
            {
                targetVector = alignment;
                targetVector.z = llList2Float(floorHeights, targetFloor);
            }
            elevate(targetVector);
        }
    }
}
```