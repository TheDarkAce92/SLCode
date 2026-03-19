---
name: "Pathfinder"
category: "example"
type: "example"
language: "LSL"
description: "integer gPotentialFieldChannel = 1; integer gDigitsPerElement = 2; integer gMinValue = 0; integer gMaxValue = 255; integer gWidth = 0; integer gHeight = 0; integer gMaxUpdates = 10;"
wiki_url: "https://wiki.secondlife.com/wiki/Pathfinder"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 The Base Script
- 2 The Rezzer Script
- 3 The Agent Script
- 4 The Square Script

## The Base Script

```lsl
// Pathfinder PotentialField by Babbage Linden
//
// Part of the Pathfinder Open Source Pathfinding Demo
//
// The potential field maintains a representation of the navigation space
// as a string containing the number of steps to the exit for each square.
// The potential field lists for various commands: SETSIZE sets the size
// of the navigation space, the exit and intializes the potential field;
// ADDOBSTACLE and ADDOBSTACLEINDEX sets one point in the navigation space
// to an obstacle that must be navigated around and updates the potential
// field; NEXTPOS queries the potential field to find the next point to
// for an agent at a given point to move to. When the potential field is
// updated, care is taken to only update parts of the field affected by
// the change and to spread the update across a number of timer events to
// avoid blocking and so becoming unresponsive to NEXTPOS queries.
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

integer gPotentialFieldChannel = 1;
integer gDigitsPerElement = 2;
integer gMinValue = 0;
integer gMaxValue = 255;
integer gWidth = 0;
integer gHeight = 0;
integer gMaxUpdates = 10;

integer gCurrentUpdateMinX;
integer gCurrentUpdateMinY;
integer gCurrentUpdateMaxX;
integer gCurrentUpdateMaxY;
integer gNextUpdateMinX;
integer gNextUpdateMinY;
integer gNextUpdateMaxX;
integer gNextUpdateMaxY;

string gPotentialField;

integer min(integer a, integer b)
{
    if(a < b)
    {
        return a;
    }
    return b;
}

integer max(integer a, integer b)
{
    if(a > b)
    {
        return a;
    }
    return b;
}

string replace(string s, integer index, string newString)
{
    integer newStringLength = llStringLength(newString);
    if(newStringLength)
        return  llInsertString(
                    llDeleteSubString(
                        s,
                        index,
                        index + newStringLength - 1),
                    index,
                    newString
                );
    return s;
}

string hexc="0123456789ABCDEF";

string int2hex(integer x)
{
    integer x0 = x & 0xF;
    string res = llGetSubString(hexc, x0, x0);
    if(( x = ((x >> 4) & 0x0FFFFFFF) ))
    {
        do{
            res = llGetSubString(hexc, x0 = (x & 0xF), x0) + res;
        }while(x = x >> 4);
    }
    return res;
}

integer hex2int(string hex)
{
    return (integer)("0x" + hex);
}

string setElement(string elements, integer index, integer value)
{
    string stringValue = int2hex(value);
    integer len = llStringLength(stringValue);
    while(gDigitsPerElement >= ++len)
    {
        stringValue = "0" + stringValue;
    }
    //llSay(PUBLIC_CHANNEL, "setElement " + elements + " " + (string)index + " " + stringValue);
    elements = replace(elements, index * gDigitsPerElement, stringValue);
    return elements;
}

string getElementString(string elements, integer index)
{
    if(index < 0)
    {
        return int2hex(gMaxValue);
    }
    return llGetSubString(elements, index * gDigitsPerElement, index * gDigitsPerElement + gDigitsPerElement - 1);
}

integer getElement(string elements, integer index)
{
    return hex2int(getElementString(elements, index));
}

sayPotentialField(string elements)
{
    string s = "\n";
    integer y = gHeight;
    while(0 <= --y)
    {
        integer x = ERR_GENERIC;
        while( gWidth > ++x )
        {
            s += getElementString(elements, squareToIndex(x, y)) + " ";
        }
        s += "\n";
    }
    llSay(PUBLIC_CHANNEL,s);
}

integer squareToIndex(integer x, integer y)
{
    if(x < 0 || x >= gWidth || y < 0 || y >= gHeight)
    {
        return ERR_GENERIC;
    }

    return x + y * gWidth;
}

string addObstacle(string elements, integer x, integer y)
{
    elements = setElement(elements, squareToIndex(x, y), gMaxValue);
    expandUpdateRegion(x, y);
    return updatePotentialField(elements);
}

expandUpdateRegion(integer x, integer y)
{
    gNextUpdateMinX = min(gNextUpdateMinX, x - 1);
    gNextUpdateMinX = max(gNextUpdateMinX, 0);
    gNextUpdateMinY = min(gNextUpdateMinY, y - 1);
    gNextUpdateMinY = max(gNextUpdateMinY, 0);
    gNextUpdateMaxX = max(gNextUpdateMaxX, x + 1);
    gNextUpdateMaxX = min(gNextUpdateMaxX, gWidth - 1);
    gNextUpdateMaxY = max(gNextUpdateMaxY, y + 1);
    gNextUpdateMaxY = min(gNextUpdateMaxY, gHeight - 1);
}

resetNextUpdateRegion()
{
    gNextUpdateMinX = gWidth - 1;
    gNextUpdateMinY = gHeight - 1;
    gNextUpdateMaxX = 0;
    gNextUpdateMaxY = 0;
}

string updatePotentialField(string elements)
{
    // If current update region finished, switch to next region.
    if(gCurrentUpdateMinY > gCurrentUpdateMaxY)
    {
        gCurrentUpdateMinX = gNextUpdateMinX;
        gCurrentUpdateMinY = gNextUpdateMinY;
        gCurrentUpdateMaxX = gNextUpdateMaxX;
        gCurrentUpdateMaxY = gNextUpdateMaxY;
        resetNextUpdateRegion();

        // If next region empty, stop updating.
        if(gCurrentUpdateMinY > gCurrentUpdateMaxY)
        {
            llSay(PUBLIC_CHANNEL, "updatePotentialField:DONE");
            llSetTimerEvent(0.0);
            return elements;
        }

        llSay(PUBLIC_CHANNEL, "updatePotentialField:(" + (string)gCurrentUpdateMinX + "," + (string)gCurrentUpdateMinY + ")
           (" + (string)gCurrentUpdateMaxX + "," + (string)gCurrentUpdateMaxY + ")");
    }

    // Recalculate potentials.
    llResetTime();
    integer updates = 0;
    if(gCurrentUpdateMinX <= gCurrentUpdateMaxX)
    {
        while((updates < gMaxUpdates) && (gCurrentUpdateMinY <= gCurrentUpdateMaxY))
        {
            //llSay(PUBLIC_CHANNEL, "updatePotentialField:" + (string)gCurrentUpdateMinY);
            integer x = gCurrentUpdateMinX;
            do{
                elements = calculatePotentialField(elements, x, gCurrentUpdateMinY);
            }while(gCurrentUpdateMaxX >= ++x);
            //x = gCurrentUpdateMaxX + 1; this saves us from doing "++updates;" in the loop
            updates += x - gCurrentUpdateMinX;
            ++gCurrentUpdateMinY;
        }
    }

    llSetTimerEvent((llGetTime() * 2.0) + 0.1);
    return elements;
}

string calculatePotentialField(string elements, integer x, integer y)
{
    integer currentValue = getElement(elements, squareToIndex(x, y));

    // Don't update obstacles or exits.
    if(currentValue == gMaxValue || currentValue == gMinValue)
    {
        return elements;
    }

    integer minValue = gMaxValue;
    minValue = min(minValue, getElement(elements, squareToIndex(x - 1, y)));
    minValue = min(minValue, getElement(elements, squareToIndex(x + 1, y)));
    minValue = min(minValue, getElement(elements, squareToIndex(x, y - 1)));
    minValue = min(minValue, getElement(elements, squareToIndex(x, y + 1)));
    minValue = min(minValue + 1, gMaxValue - 1);
    if(minValue != currentValue)
    {
        //llSay(PUBLIC_CHANNEL, "calculatePotentialField:" + (string)x + "," + (string)y + " currentValue " + (string)currentValue + " newValue " + (string)minValue);
        elements = setElement(elements, squareToIndex(x, y), minValue);
        expandUpdateRegion(x, y);
    }
    return elements;
}

string nextStep(string elements, integer x, integer y)
{
    integer nextX;
    integer nextY;
    integer minValue = gMaxValue;
    integer currentX = x - 1;
    integer currentY = y;
    integer currentValue = getElement(elements, squareToIndex(currentX, currentY));
    if(currentValue < minValue)
    {
        minValue = currentValue;
        nextX = currentX;
        nextY = currentY;
    }
    currentX = x + 1;
    currentValue = getElement(elements, squareToIndex(currentX, currentY));
    if(currentValue < minValue)
    {
        minValue = currentValue;
        nextX = currentX;
        nextY = currentY;
    }
    currentX = x;
    currentY = y - 1;
    currentValue = getElement(elements, squareToIndex(currentX, currentY));
    if(currentValue < minValue)
    {
        minValue = currentValue;
        nextX = currentX;
        nextY = currentY;
    }
    currentY = y + 1;
    currentValue = getElement(elements, squareToIndex(currentX, currentY));
    if(currentValue < minValue)
    {
        minValue = currentValue;
        nextX = currentX;
        nextY = currentY;
    }
    if(minValue == gMaxValue)
    {
        return "";
    }
    return (string)nextX + "," + (string)nextY;
}

setSize(integer width, integer height, integer exitX, integer exitY)
{
    gWidth = width;
    gHeight = height;

    gPotentialField = "";

    integer y = ERR_GENERIC;
    while(height > ++y)
    {
        integer x = ERR_GENERIC;
        while(width > ++x)
        {
            gPotentialField = setElement(gPotentialField, squareToIndex(x, y), llAbs(exitX - x) + llAbs(exitY - y));
        }
    }
    resetNextUpdateRegion();
    sayPotentialField(gPotentialField);
}

init()
{
    llListen(PUBLIC_CHANNEL, "", NULL_KEY, "");
    llListen(gPotentialFieldChannel, "", NULL_KEY, "");
}

default
{
    state_entry()
    {
        init();
    }

    on_rez(integer param)
    {
        init();
    }

    timer()
    {
        gPotentialField = updatePotentialField(gPotentialField);
    }

    listen(integer channel, string name, key id, string s)
    {
        list message = llCSV2List(s);
        string command = llList2String(message, 0);
        integer x = llList2Integer(message, 1);
        integer y = llList2Integer(message, 2);
        if(command == "ADDOBSTACLE")
        {
            gPotentialField = addObstacle(gPotentialField, x, y);
        }
        else if(command == "ADDOBSTACLEINDEX")
        {
            y = x / gWidth;
            x %= gWidth;
            gPotentialField = addObstacle(gPotentialField, x, y);
        }
        else if(command == "SETSIZE")
        {
            integer width = x;
            integer height = y;
            x = llList2Integer(message, 3);
            y = llList2Integer(message, 4);
            setSize(width, height, x, y);
        }
        else if(command == "NEXTPOS")
        {
            integer channel = llList2Integer(message, 3);
            if(getElement(gPotentialField, squareToIndex(x, y)) == 0)
            {
                llSay(channel, "RESET");
            }
            string nextStepString = nextStep(gPotentialField, x, y);
            if(llStringLength(nextStepString) > 0)
            {
                list nextStepList = llCSV2List(nextStepString);
                x = llList2Integer(nextStepList, 0);
                y = llList2Integer(nextStepList, 1);
                llSay(channel, "NEXTPOS," + (string)x + "," + (string)y);
            }
        }
        //sayPotentialField(gPotentialField);
    }
}
```

## The Rezzer Script

```lsl
// Pathfinder Rezzer by Babbage Linden
//
// Part of the Pathfinder Open Source Pathfinding Demo
//
// The rezzer listens for SETSIZE commands, which causes it to rez
// a grid of Square objects of the appropriate size and set the
// entry and exit points as exits. Touching the rezzer
// causes it to rez and agent above the entry point at the origin.
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

float gSquareWidth = 1.0;
float gPeriod = 5.0;
vector gOrigin;
vector gEntrance;
integer gEntranceX;
integer gEntranceY;
integer gPopulation = 0;
integer gMaxPopulation = 10;
integer gPotentialFieldChannel = 1;
integer gSquareChannel = 2;
integer gAgentChannel = 3;

init()
{
    llListen(PUBLIC_CHANNEL, "", NULL_KEY, "");
}

default
{
    state_entry()
    {
        init();
    }

    on_rez(integer param)
    {
        init();
    }

    listen(integer channel, string name, key id, string s)
    {
        list message = llCSV2List(s);
        string command = llList2String(message, 0);
        integer x = llList2Integer(message, 1);
        integer y = llList2Integer(message, 2);
        if(command == "SETSIZE")
        {
            integer width = x;
            integer height = y;
            integer exitX = llList2Integer(message, 3);
            integer exitY = llList2Integer(message, 4);
            gEntranceX = llList2Integer(message, 5);
            gEntranceY = llList2Integer(message, 6);
            gOrigin = llGetPos();
            gOrigin.x -= ((width - 1) * gSquareWidth) / 2.0;
            gOrigin.y -= ((height - 1) * gSquareWidth) / 2.0;
            gEntrance = gOrigin;
            gEntrance.x += gEntranceX * gSquareWidth;
            gEntrance.y += gEntranceY * gSquareWidth;
            gEntrance.z += 1.0;
            for(y = 0; y < height; ++y)
            {
                for(x = 0; x < width; ++x)
                {
                    vector pos = gOrigin;
                    pos.x += x * gSquareWidth;
                    pos.y += y * gSquareWidth;
                    pos.z += 0.5;
                    integer channel = (x + y * width);
                    llRezObject("Square", pos, <0,0,0>, <0,0,0,0>, channel);
                }
            }
            llSay(gSquareChannel, "EXIT," + (string)(gEntranceX + gEntranceY * width));
            llSay(gSquareChannel, "EXIT," + (string)(exitX + exitY * width));
            gAgentChannel = 3;
            gMaxPopulation = 10;
            llSetTimerEvent(gPeriod);
        }
        else if(command == "RESET")
        {
            gPopulation = 0;
            llSay(gSquareChannel, "RESET");
            integer channel;
            for(channel = 2; channel <= gAgentChannel; ++channel)
            {
                llSay(channel, "RESET");
            }
            llSetTimerEvent(0);
            gMaxPopulation = 0;
        }
        else if(command == "FINISHED")
        {
            --gPopulation;
            if(gPopulation < 0) {gPopulation = 0;}
            llSetTimerEvent(gPeriod);
            //llSay(PUBLIC_CHANNEL,"Population:" + (string)gPopulation);
        }
    }

    timer()
    {
        if(gPopulation >= gMaxPopulation)
        {
            llSetTimerEvent(0);
            return;
        }
        integer channel = gAgentChannel++;
        llRezObject("Agent", gEntrance, <0,0,0>, <0,0,0,0>, channel);
        llSay(channel, "POS," + (string)gEntranceX + "," + (string)gEntranceY);
        ++gPopulation;
        //llSay(PUBLIC_CHANNEL,"Population:" + (string)gPopulation);
    }
}
```

## The Agent Script

```lsl
// Pathfinder Agent by Babbage Linden
//
// Part of the Pathfinder Open Source Pathfinding Demo
//
// The agent periodically makes NEXTPOS queries to the PotentialField
// script to find the next point to move to and can have its current
// position set with the POS command.
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

float gSquareWidth = 1.0;
float gStartPeriod = 2.0;
float gPeriod = 2.0;
integer gChannel;
integer gX;
integer gY;
integer gSquareChannel = 2;
integer gPotentialFieldChannel = 1;

default
{
    on_rez(integer param)
    {
        gChannel = param;
        llListen(gChannel, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string s)
    {
        list message = llCSV2List(s);
        string command = llList2String(message, 0);
        integer x = llList2Integer(message, 1);
        integer y = llList2Integer(message, 2);
        if(command == "POS")
        {
            gX = x;
            gY = y;
            llSetTimerEvent(gPeriod);
        }
        else if(command == "NEXTPOS")
        {
            integer dX = x - gX;
            integer dY = y - gY;
            vector pos = llGetPos();
            pos.x += dX * gSquareWidth;
            pos.y += dY * gSquareWidth;
            llSetPos(pos);
            gX = x;
            gY = y;
            gPeriod = gStartPeriod;
            llSetTimerEvent(gPeriod);
        }
        else if(command == "RESET")
        {
            llSay(PUBLIC_CHANNEL,"FINISHED");
            llDie();
        }
    }

    timer()
    {
        llSay(gPotentialFieldChannel, "NEXTPOS," + (string)gX + "," + (string)gY + "," + (string)gChannel);
        gPeriod *= 2.0;
        llSetTimerEvent(gPeriod);
    }
}
```

## The Square Script

```lsl
// Pathfinder Square by Babbage Linden
//
// Part of the Pathfinder Open Source Pathfinding Demo for Second Life
//
// The square listens for various commands: RESET causes it to kill itself;
// EXIT causes it to turn black and set itself as an exit. Touching the
// causes it to grow and to send the ADDOBSTACLEINDEX command to the
// PotentialField script.
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

integer gSquareChannel = 2;
integer gPotentialFieldChannel = 1;
integer gIndex;
integer STATE_DEFAULT = 0;
integer STATE_OBSTACLE = 1;
integer STATE_EXIT = 2;
integer gState = STATE_DEFAULT;

default
{
    on_rez(integer param)
    {
        gIndex = param;
        llListen(gSquareChannel, "", NULL_KEY, "");
    }

    touch_start(integer num)
    {
        if(gState == STATE_DEFAULT)
        {
            llSay(gPotentialFieldChannel, "ADDOBSTACLEINDEX," + (string)gIndex);
            llSetScale(<1,1,1>);
            llSetPos(llGetPos() + <0,0,0.5>);
            gState = STATE_OBSTACLE;
        }
    }

    listen(integer channel, string name, key id, string s)
    {
        list message = llCSV2List(s);
        string command = llList2String(message, 0);
        if(command == "RESET")
        {
            llDie();
        }
        else if(command == "EXIT")
        {
            integer index = llList2Integer(message, 1);
            if(index == gIndex)
            {
                llSetColor(<0,0,0>, ALL_SIDES);
                gState = STATE_EXIT;
            }
        }
        else if(command == "ENTRANCE")
        {
            integer index = llList2Integer(message, 1);
            if(index == gIndex)
            {
                llSetTexture("5748decc-f629-461c-9a36-a35a221fe21f", ALL_SIDES);
                gState = STATE_EXIT;
            }
        }
    }
}
```