---
name: "Sim Restart Logger"
category: "example"
type: "example"
language: "LSL"
description: "Counts region restarts and displays log of last 5 restarts together with region FPS and dilation."
wiki_url: "https://wiki.secondlife.com/wiki/Sim_Restart_Logger"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Counts region restarts and displays log of last 5 restarts together with region FPS and dilation.

Updated version: Achieves accurate information about Sim restarts by checking the newly
introduced CHANGED_REGION_START flag in 'changed' event to log data instead of previous
version's method of approximating restarts by checking for poor script performance.

**Requirements:**

- Place this script into a single prim and decorate to taste.

**Operation:**

- No special instructions. It operates stand alone once installed.

```lsl
//********************************************************
// This Script was pulled out for you by YadNi Monde from the SL FORUMS at
// http://forums.secondlife.com/forumdisplay.php?f=15, it is intended to stay FREE by it's author(s)
// and all the comments here in ORANGE must NOT be deleted. They include notes on how to use it
// and no help will be provided either by YadNi Monde or it's Author(s).
// IF YOU DO NOT AGREE WITH THIS JUST DONT USE!!!
//********************************************************

/////////////////////////////////////////
// SIM CRASH/REBOOT LOGGER
// by: Kyrah Abattoir
// Updated by: Huney Jewell
// January 2010:
// Fixed:      Log display truncated if more than 5 entries due to llSetText length restriction
// Added:      Log start date
// Added:      Code to easily specify appearance of hovertext
// July 2009:
// Changed:    Achieving more accurate information about SIM restarts to log data by checking the newly introduced
//             CHANGED_REGION_START flag in 'changed' event instead of approximation by checking for poor script performance
// Added:      Last FPS and dilation values to hover text
/////////////////////////////////////////

// GLOBALS
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// User adjustable settings

float   timering    = 120; // Sets the polling rate. Put the speed you wish, in seconds
vector  blue        = <0,0,1>;
vector  orange      = <1,0.5,0>;
vector  cyan        = <0,1,1>;
vector  pink        = <1,0.5,0.76>;
vector  green       = <0,1,0>;
vector  red         = <1,0,0>;
vector  white       = <1,1,1>;
vector  yellow      = <1,1,0.1>;
vector  purple      = <1,0,1>;
vector  black       = <0,0,0>;

vector  hoverColor  = white; // Sets the color the text will show. Use predefined colors or any RGB color vector in float form
float   hoverAlpha  = 1.0; // Sets the text's transparency, 1.0 being SOLID, while 0 would be clear

// System settings - Do Not Change Anything Below!

string  _buffer   = "";
list    log       = [];
string  region_name;
integer span;
float   fps_avg;
float   dilation_avg;
integer restarts  = 0;
string  startDate;
string  date      = "";
//2004-08-27T00:56:21.785886Z

// FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

string FormatDecimal(float number, integer precision)
{
    float roundingValue = llPow(10, -precision)*0.5;
    float rounded;
    if (number < 0) rounded = number - roundingValue;
    else            rounded = number + roundingValue;

    if (precision < 1) // Rounding integer value
    {
        integer intRounding = (integer)llPow(10, -precision);
        rounded = (integer)rounded/intRounding*intRounding;
        precision = -1; // Don't truncate integer value
    }

    string strNumber = (string)rounded;
    return llGetSubString(strNumber, 0, llSubStringIndex(strNumber, ".") + precision);
}

hoverText()
{
    string _date = llGetDate();
    if(date == _date)
        span++;
    else // daily reset of the average FPS and dilation
    {
        span = 1;
        date = _date;
        fps_avg = 0;
        dilation_avg = 0;
    }

    float fps = llGetRegionFPS();
    fps_avg += fps;
    float dilation = llGetRegionTimeDilation();
    dilation_avg += dilation;
    string buffer = "";
    buffer += region_name + "\nFPS avg: " + FormatDecimal(fps_avg/span, 0)
        + ", last: " + FormatDecimal(fps, 0);
    buffer += "\nDilation avg: " + FormatDecimal(dilation_avg/span, 2)
        + ", last: " + FormatDecimal(dilation, 2);
    buffer += "\nSim restarts (since " + startDate + "): " + (string)restarts
        + "\nLast restarts (UTC): \n" + llDumpList2String(log,"\n");
    if(_buffer != buffer)
    { // display changed hovertext
        llSetText(buffer, hoverColor, hoverAlpha);
        _buffer = buffer;
    }
}

// CODE ENTRY
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

default
{
    state_entry()
    {
        region_name = llGetRegionName();
        startDate = llGetDate();
        hoverText(); // display hover text
        llSetTimerEvent(timering); // starting our timer
    }

    on_rez(integer num)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & CHANGED_REGION_START)
        { // log region restart
            restarts++;
            string timestamp = llGetTimestamp();
            list temp = llParseString2List(timestamp,["T",":","."],[]);
            log += llList2String(temp,0) + " - " + llList2String(temp,1) + ":"
                + llList2String(temp,2) + ":" + llList2String(temp,3);
            if(llGetListLength(log) > 5) // limit log entries to avoid hovertext truncation
                log = llDeleteSubList(log,0,0);
        }
    }

    timer()
    {
        hoverText(); // display hover text
    }
}
```

--Huney Jewell 12:46, 22 July 2009 (UTC)