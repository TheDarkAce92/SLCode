---
name: "Object to Data v1.4"
category: "example"
type: "example"
language: "LSL"
description: "(http://www.gnu.org/copyleft/fdl.html) in the spirit of which this script is GPL'd. Copyright (C) 2011 Xaviar Czervik"
wiki_url: "https://wiki.secondlife.com/wiki/Object_to_Data_v1.4"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Introduction
- 2 Revision History
- 3 Instructions
- 4 Data To Object (Script)
- 5 Object To Data (Script)
- 6 Holo Box (Script)

## Introduction

([http://www.gnu.org/copyleft/fdl.html](http://www.gnu.org/copyleft/fdl.html)) in the spirit of which this script is GPL'd. Copyright (C) 2011 Xaviar Czervik

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

This is one of the projects that I've spent a significant amount of time on, and that I've uploaded to the wiki.
It's purpose is simple: it allows anyone to transfer objects through text. This may seem trivial, but it has several advantages to it.
Below are a few ways in which this script can be used:

1. The Internet. There is no way (yet) to go on to the Internet and request an object be sent to your SL character. This solves this issue. One could post the data on to the Internet, and allow people to copy the text down to SL, run this script, and obtain an object from it.
1. Management Scripts. There is no way to have an object create a totally new object. And objects can only call llGiveInventory on other objects when in the same sim. This solves the issue by allowing objects to use email to send data, which can then be turned into an object.





## Revision History

Version 1.4:

1. Doesn't require rerezing.
1. Simpler to turn object to data.
1. Backwards compatible with 1.3.
1. Bug fix from KimAnn Galaxy.

Version 1.3:

1. 100% success rate.
1. Added PRIM_GLOW
1. Added functionality for multiple notecards (for really big objects).
1. Improved efficiency; removed the delink/relink sections.

Version 1.2:

1. Around 95% success rate.
1. Changed to almost all llGetPrimitiveParams calls.
1. Added more than just ten different descriptors of an object.
1. Removed freakish menu-controlled system.
1. Script need only be dropped in root object, not every prim.

Version 1.1:

1. Made process simpler: removed replicate from listen.
1. Changed to work (slightly) better.

Version 1.0:

1. First release.



## Instructions

Thanks to DMC Zsigmond for the original documentation shown below, modified for Version 1.4 by Xaviar.

Check List (Parts Required):

1. 1 x Script, named: "Object to Data"
1. 1 x Script, named: "Holo Script"
1. 1 x Object, named: "HoloBox"
1. 1 x Notecard, named: "Data_Default"

Plus,

1. 1 x Any Object you wish to use these scripts with to turn into data, or re-rez it back again.

Part 1/3 - Creating Scripts and Assembling Objects

1. Open your "Inventory", and create a new folder, called: "Object to Data v1.4".
1. Under the new "Object to Data v1.4" folder, right-click and create a new script, named "Data To Object". Then copy and paste the "Data To Object" LSL code on this wiki page into the "Data To Object" script you just created under your "Object to Data v1.4" folder. Click on "Save" to compile the "Data to Object" script,  and then after that "Data to Object" script has successfully compiled, close the script.
1. Repeat Step 2, for the "Holo Script" and "Object to Data" scripts.
1. Create a new Object on the ground, and then right-click on it, and select "Edit".
1. Under the "General" tab, name the Object you just created as, "HoloBox". This object must be inserted into your "Data to Object" object in future to supply the prim that will be converted back into the original Object you once sort to have turned into text/notecard data.
1. Go the the "Content" tab of the "HoloBox" prim, to view its contents.
1. Drag'n'drop the "Holo Script" script under the "Object to Data v1.4" folder in your Inventory, to the "Contents" folder of the "HoloBox" object you have selected.
1. Right-click the "HoloBox" object, and select "Take", to take the object back into your inventory.
1. Create a new Object on the ground, right-click it, and select "Edit".
1. Under the "General" tab, name the Object you just created as, "Data to Object". (not necessary)
1. Go the the "Content" tab of the "Data to Object" prim, to view its contents.
1. Drag'n'drop the "Data To Object" script under the "Object to Data v1.4" folder in your Inventory, to the "Contents" folder of the "Data to Object" object you have selected.
1. Drag'n'drop the "HoloBox" object you have either in your "Objects" folder in your Inventory or under the "Object to Data v1.4" folder in your Inventory, to the "Contents" folder of the "Data to Object" object you have selected.

You should now have two things:

1. An object named "Data to Object" which contains (1) a script named "Data to Object" (found below) and (2) an object named HoloBox. Holobox should contain a script named "Holo Script" (found below).
1. A script named "Object to Data".



Part 2/3 - Convert an Object to Data

1. Select an Object you wish to turn into data (NB. perhaps start with a single object which is relatively simple).
1. Rez the Object you wish to turn into data on the ground.
1. Right-click the Object you wish to turn into data, and select edit. Then click on the "Content" tab to view its contents.
1. Now drag'n'drop the "Object to Data" script you created in your Inventory, from your "Object to Data v1.4" folder into the "Contents" folder of the Object you wish to turn into data.
1. Wait a few moments (or possibly a minute or two) until your Local Chat Window outputs the Object's data.
1. Copy the text data from your Local Chat Window (including the time code) from the very beginning to the very end.
1. Return to your Inventory folder named, "Object to Data v1.4", and then right-click and create a new note (i.e. notecard) called, "Data_Default".
1. Paste the Object code data copied from your Local Chat Window to the "Data_Default" notecard, and then "Save" it. This notecard now holds the data information for your Object.
1. If the information does not fit in to one notecard, the first object stays named "Data_Default", however name the second notecard "Data_Default 1", the third "Data_Default 2", etc.

The entire object has now been turned into data. It can now be transferred through many means not usually possible, including a text file on the Internet.



Part 3/3 Instructions to convert Data to Object

1. Rez the "Data to Object" object from the "Object to Data v1.4" folder. (Move the object some meters above the ground, since it will silently fail and hang if later if it attempts to rez objects slightly below ground level!)
1. Right-click the Object you wish to turn into data, and select edit. Go to the "Contents" tab of the "Data to Object" object.
1. Drag'n'drop the "Data_Default" notecard(s) to the object.
1. Now touch the object, "Data to Object" to begin rebuilding the original Object that you had turned into data.
1. View your Local Chat window for confirm of the build "Start", and notification when the build is "Done".

The original Object you sort to have turned into data will now rez as a new object above the "Data to Object" prim.

This object will be empty, ready for use as intended.





## Data To Object (Script)

```lsl
string name = "Data_Default";

integer numberOfNotes;
key     qid;
integer line = 0;
integer lineTotal = 0;
integer prims;
list    totalLines;
integer totalLinesTotal;

string hexDigits = "0123456789ABCDEF";

integer rand;

integer whichNote;

vector start;

get() {
    if (whichNote == 0) {
        qid = llGetNotecardLine(name, line);
    } else {
        qid = llGetNotecardLine(name + " " + (string)whichNote, line);
    }

}

rezObj(vector pos, string num) {
    while (llVecDist(llGetPos(), start-pos) > .001) llSetPos(start-pos);
    llRezObject("HoloBox", llGetPos(), <0,0,0>, <0,0,0,0>, hex2int(num) + rand);
}

integer hex2int(string hex) {
    integer p1 = llSubStringIndex(hexDigits, llGetSubString(hex, 0, 0));
    integer p2 = llSubStringIndex(hexDigits, llGetSubString(hex, 1, 1));
    integer data = p2 + (p1 << 4);
    return data;
}

default {
    touch_start(integer i) {
        llSetText("Starting Up... (1/4)", <1,1,1>, 1);
        numberOfNotes = llGetInventoryNumber(INVENTORY_NOTECARD);

        qid = llGetNumberOfNotecardLines(name);
    }
    dataserver(key queryId, string data) {
        if (queryId == qid)  {
            totalLines += data;
            totalLinesTotal += (integer)data;
            ++whichNote;
            if (whichNote < numberOfNotes) {
                llOwnerSay(name + " " + (string)whichNote);
                qid = llGetNumberOfNotecardLines(name + " " + (string)whichNote);
            } else {
                state rez;
            }
        }
    }
}

state rez {
    state_entry() {
        start = llGetPos();
        rand = (integer)llFrand(0x6FFFFFFF) + 0x10000000;
        llOwnerSay("Start");
        line = 0;
        qid = llGetNotecardLine(name, line);
        whichNote = 0;
    }
    dataserver(key queryId, string data) {
        if (queryId == qid)  {
            if (data != EOF) {
                data = llList2String(llParseString2List(data, ["-----: "], []), 1);
                if (llGetSubString(data, 0, 3) == "#NEW") {
                    string num = llGetSubString(data, 5, 6);
                    vector pos = (vector)llGetSubString(data, 8, -1);
                    rezObj(pos, num);
                }
                llSetText("Rezing Prims: " + (string)((integer)(100*lineTotal/totalLinesTotal)) + "% (2/4)", <1,1,1>, 1);
                line += 1;
                lineTotal += 1;
                get();
            } else {
                whichNote++;
                if (whichNote < numberOfNotes) {
                    line = 0;
                    get();
                } else {
                    state run;
                }
            }
        }
    }
}

state run {
    state_entry() {
        line = 0;
        lineTotal = 0;
        qid = llGetNotecardLine(name, line);
        whichNote = 0;
    }
    dataserver(key queryId, string data) {
        if (queryId == qid)  {
            if (data != EOF) {
                data = llList2String(llParseString2List(data, ["-----: "], []), 1);
                if (llGetSubString(data, 0, 3) != "#NEW") {
                    list parts = llParseString2List(data, [":::"], []);
                    integer prim = hex2int(llList2String(parts, 0));
                    llRegionSay(rand + prim, llList2String(parts, 1));
                }
                llSetText("Sending Data: " + (string)((integer)(100*lineTotal/totalLinesTotal)) + "% (3/4)", <1,1,1>, 1);
                line += 1;
                lineTotal += 1;
                get();
            } else {
                whichNote++;
                if (whichNote < numberOfNotes) {
                    line = 0;
                    get();
                } else {
                    llSetText("Cleaning Up... (4/4)", <1,1,1>, 1);
                    integer i = 0;
                    while (i < 256) {
                        llRegionSay(rand + i, "Finish");
                        ++i;
                    }
                    llSetTimerEvent(3);
                }
            }
        }
    }
    timer() {
        llSetText("Finished.", <1,1,1>, 1);
        llOwnerSay("Done");
        llSetTimerEvent(0);
        llResetScript();
    }
}
```



## Object To Data (Script)

```lsl
string hexc="0123456789ABCDEF";//faster

string Float2Hex(float input)
{// Copyright Strife Onizuka, 2006-2007, LGPL, http://www.gnu.org/copyleft/lesser.html
    if((integer)input != input)//LL screwed up hex integers support in rotation & vector string typecasting
    {//this also keeps zero from hanging the zero stripper.
        float unsigned = llFabs(input);//logs don't work on negatives.
        integer exponent = llFloor(llLog(unsigned) / 0.69314718055994530941723212145818);//floor(log2(b)) + rounding error
        integer mantissa = (integer)((unsigned / (float)("0x1p"+(string)(exponent -= (exponent == 128)))) * 0x1000000);//shift up into integer range
        integer index = (integer)(llLog(mantissa & -mantissa) / 0.69314718055994530941723212145818);//index of first 'on' bit
        string str = "p" + (string)((exponent += index) - 24);
        mantissa = mantissa >> index;
        do
            str = llGetSubString(hexc,15&mantissa,15&mantissa) + str;
        while(mantissa = mantissa >> 4);
        if(input < 0)
            return "-0x" + str;
        return "0x" + str;
    }//integers pack well so anything that qualifies as an integer we dump as such, supports netative zero
    return llDeleteSubString((string)input,-7,-1);//trim off the float portion, return an integer
}

string safeVector(vector v) {
    return "<"+safeFloat(v.x)+","+safeFloat(v.y)+","+safeFloat(v.z)+">";
}

string safeRotation(rotation v) {
    return "<"+safeFloat(v.x)+","+safeFloat(v.y)+","+safeFloat(v.z)+","+safeFloat(v.s)+">";
}

string safeFloat(float f) {
    return Float2Hex(f);
}

string list2string(list l) {
    string ret;
    integer len = llGetListLength(l);
    integer i;

    while (i < len) {
        integer type = llGetListEntryType(l, i);
        if (type == 1) {
            ret += "#I"+(string)llList2Integer(l, i);
        } else if (type == 2) {
            ret += "#F"+safeFloat(llList2Float(l, i));
        } else if (type == 3) {
            ret += "#S"+llList2String(l, i);
        } else if (type == 4) {
            ret += "#K"+(string)llList2Key(l, i);
        } else if (type == 5) {
            ret += "#V"+safeVector(llList2Vector(l, i));
        } else if (type == 6) {
            ret += "#R"+safeRotation(llList2Rot(l, i));
        }
        ret += "-=-";
        i++;
    }
    return ret;
}

integer LINK_NUM = 0;

string getTexture() {
    string ret;

    integer sides = llGetLinkNumberOfSides(LINK_NUM);

    integer same = 1;
    list texture;
    list repeat;
    list offset;
    list rot;

    integer i = 0;
    while (i < sides) {
        list side  = llGetLinkPrimitiveParams(LINK_NUM, [PRIM_TEXTURE, i]);
        texture += llList2String(side, 0);
        repeat  += llList2Vector(side, 1);
        offset  += llList2Vector(side, 2);
        rot     += llList2Float(side, 3);

        if (!(llList2String(texture, i) == llList2String(texture, i-1) && llList2Vector(repeat, i) == llList2Vector(repeat, i-1) &&
            llList2Vector(offset, i) == llList2Vector(offset, i-1) && llList2Float(rot, i) == llList2Float(rot, i-1))) {
                same = 0;
        }
        i++;
    }

    if (same) {
        ret += list2string([PRIM_TEXTURE, ALL_SIDES, llList2String(texture, 0), llList2Vector(repeat, 0), llList2Vector(offset, 0), llList2Float(rot, 0)]);
    } else {
        integer j = 0;
        while (j < llGetListLength(texture)) {
            ret += list2string([PRIM_TEXTURE, j, llList2String(texture, j), llList2Vector(repeat, j), llList2Vector(offset, j), llList2Float(rot, j)]);
            j++;
        }
    }

    return ret;
}

string getColor() {
    string ret;

    integer sides = llGetLinkNumberOfSides(LINK_NUM);

    integer same = 1;
    list color;
    list alpha;

    integer i = 0;
    while (i < sides) {
        list side  = llGetLinkPrimitiveParams(LINK_NUM, [PRIM_COLOR, i]);
        alpha += llList2Float(side, 1);
        color  += llList2Vector(side, 0);

        if (!(llList2String(color, i) == llList2String(color, i-1) && llList2Vector(alpha, i) == llList2Vector(alpha, i-1))) {
                same = 0;
        }
        i++;
    }

    if (same) {
        ret += list2string([PRIM_COLOR, ALL_SIDES, llList2Vector(color, 0), llList2Float(alpha, 0)]);
    } else {
        integer j = 0;
        while (j < llGetListLength(color)) {
            ret += list2string([PRIM_COLOR, j, llList2Vector(color, j), llList2Float(alpha, j)]);
            j++;
        }
    }

    return ret;
}

string getShiny() {
    string ret;

    integer sides = llGetLinkNumberOfSides(LINK_NUM);

    integer same = 1;
    list shiny;
    list bump;

    integer i = 0;
    while (i < sides) {
        list side  = llGetLinkPrimitiveParams(LINK_NUM, [PRIM_BUMP_SHINY, i]);
        shiny += llList2Integer(side, 0);
        bump += llList2Integer(side, 1);

        if (!(llList2Integer(shiny, i) == llList2Integer(shiny, i-1) && llList2Integer(bump, i) == llList2Integer(bump, i-1))) {
                same = 0;
        }
        i++;
    }

    if (same) {
        ret += list2string([PRIM_BUMP_SHINY, ALL_SIDES, llList2Integer(shiny, 0), llList2Integer(bump, 0)]);
    } else {
        integer j = 0;
        while (j < llGetListLength(shiny)) {
            ret += list2string([PRIM_BUMP_SHINY, j, llList2Integer(shiny, j), llList2Integer(bump, j)]);
            j++;
        }
    }

    return ret;
}

string getBright() {
    string ret;

    integer sides = llGetLinkNumberOfSides(LINK_NUM);

    integer same = 1;
    list fullbright;

    integer i = 0;
    while (i < sides) {
        list side  = llGetLinkPrimitiveParams(LINK_NUM, [PRIM_FULLBRIGHT, i]);
        fullbright += llList2Integer(side, 0);

        if (!(llList2Integer(fullbright, i) == llList2Integer(fullbright, i-1))) {
                same = 0;
        }
        i++;
    }

    if (same) {
        ret += list2string([PRIM_FULLBRIGHT, ALL_SIDES, llList2Integer(fullbright, 0)]);
    } else {
        integer j = 0;
        while (j < llGetListLength(fullbright)) {
            ret += list2string([PRIM_FULLBRIGHT, j, llList2Integer(fullbright, j)]);
            j++;
        }
    }

    return ret;
}
string getGlow() {
    string ret;

    integer sides = llGetLinkNumberOfSides(LINK_NUM);

    integer same = 1;
    list glow;

    integer i = 0;
    while (i < sides) {
        list side  = llGetLinkPrimitiveParams(LINK_NUM, [PRIM_GLOW, i]);
        glow += llList2Integer(side, 0);

        if (!(llList2Integer(glow, i) == llList2Integer(glow, i-1))) {
                same = 0;
        }
        i++;
    }

    if (same) {
        ret += list2string([PRIM_GLOW, ALL_SIDES, llList2Integer(glow, 0)]);
    } else {
        integer j = 0;
        while (j < llGetListLength(glow)) {
            ret += list2string([PRIM_GLOW, j, llList2Integer(glow, j)]);
            j++;
        }
    }

    return ret;
}

vector getPos() {
    vector pos = llGetPos();
    pos -= llList2Vector(llGetLinkPrimitiveParams(LINK_NUM, [PRIM_POSITION]), 0);

    if (LINK_NUM == 1) {
        pos = <0,0,0>;
    }
    return pos;
}

string getType() {
    list type = [PRIM_TYPE] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_TYPE]);
    type += [PRIM_PHYSICS] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_PHYSICS]);
    type += [PRIM_MATERIAL] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_MATERIAL]);
    type += [PRIM_TEMP_ON_REZ] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_TEMP_ON_REZ]);
    type += [PRIM_PHANTOM] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_PHANTOM]);
    type += [PRIM_ROTATION] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_ROTATION]);
    type += [PRIM_SIZE] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_SIZE]);
    type += [PRIM_FLEXIBLE] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_FLEXIBLE]);
    type += [PRIM_POINT_LIGHT] + llGetLinkPrimitiveParams(LINK_NUM, [PRIM_POINT_LIGHT]);
    return list2string(type);
}

string getPrimitiveParams() {
    string ret;
    ret += getType();
    ret += getTexture();
    ret += getShiny();
    ret += getColor();
    ret += getBright();
    ret += getGlow();
    return ret;
}

string getMeta() {
    return llDumpList2String([llGetLinkName(LINK_NUM), llList2String(llGetLinkPrimitiveParams(LINK_NUM, [PRIM_DESC]), 0)], "-=-");
}

string int2hex(integer num) {
    integer p1 = num & 0xF;
    integer p2 = (num >> 4) & 0xF;
    string data = llGetSubString(hexc, p2, p2) + llGetSubString(hexc, p1, p1);
    return data;
}

default {
    state_entry() {
        string name = llGetObjectName();
        llSetObjectName("-----");
        LINK_NUM = 1;
        while (LINK_NUM <= llGetNumberOfPrims()) {
            llOwnerSay("#NEW " + int2hex(LINK_NUM) + " " + safeVector(getPos()));
            LINK_NUM++;
        }
        LINK_NUM = 1;
        llSetObjectName(name);
        while (LINK_NUM <= llGetNumberOfPrims()) {
            string meta = getMeta();
            string data = getPrimitiveParams();
            llSetObjectName("-----");
            llOwnerSay(int2hex(llGetLinkNumber()) + ":::0"+meta);
            integer i = 0;
            integer num = 1;
            while (i < llStringLength(data)) {
                llOwnerSay(int2hex(LINK_NUM) + ":::" + (string)num + "" + (string)llGetSubString(data, i, i+199));
                i += 200;
                llSleep(.1);
                num++;
            }
            LINK_NUM++;
        }
    }
}
```



## Holo Box (Script)

```lsl
string meta;
list data = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""];

setLink() {
    list m = llParseString2List(meta, ["-=-"], []);
    llSetObjectName(llList2String(m, 0));
    llSetObjectDesc(llList2String(m, 1));

    list l = llParseString2List((string)data, ["-=-"], []);
    list real;
    integer i = 0;
    while (i < llGetListLength(l)) {
        string this = llList2String(l, i);
        string thisPart = llGetSubString(this, 0, 1);
        if (thisPart == "#S") {
            real += (string)llGetSubString(this, 2, -1);
        } else if (thisPart == "#K") {
            real += (key)llGetSubString(this, 2, -1);
        } else if (thisPart == "#I") {
            real += (integer)llGetSubString(this, 2, -1);
        } else if (thisPart == "#F") {
            real += (float)llGetSubString(this, 2, -1);
        } else if (thisPart == "#V") {
            real += (vector)llGetSubString(this, 2, -1);
        } else if (thisPart == "#R") {
            real += (rotation)llGetSubString(this, 2, -1);
        }
        i++;
    }
    llSetPrimitiveParams(real);
}

default {
    on_rez(integer i) {
        llListen(i, "", "", "");
    }
    listen(integer i, string n, key id, string m) {
        if (m == "Finish") {
            setLink();
            llSleep(.5);
            llRemoveInventory(llGetScriptName());
        }
        integer num = (integer)llGetSubString(m, 0, 0);
        if (num == 0) {
            meta = llGetSubString(m, 1, -1);
        } else {
            num--;
            data = llListReplaceList(data, [llGetSubString(m, 1, -1)], num, num);
        }
    }
}
```