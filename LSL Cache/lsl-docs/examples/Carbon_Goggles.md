---
name: "Carbon Goggles"
category: "example"
type: "example"
language: "LSL"
description: "float gSelectionTimeout = 120.0; float gScanDelay = 5.0; float gRateDelay = 0.0;"
wiki_url: "https://wiki.secondlife.com/wiki/Carbon_Goggles"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Carbon Goggles 0.7
//
// An Augmented Virtual Reality HUD for Second Life
// by Babbage Linden
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

float gSelectionTimeout = 120.0;
float gScanDelay = 5.0;
float gRateDelay = 0.0;

integer gAnnotateDialogChannel = 8888;
integer gAnnotateDialogChannelHandle = 0;

integer gCommandChannel = 5;
integer gCommandChannelHandle = 0;

integer gConfigDialogChannel = 9999;
integer gConfigDialogChannelHandle = 0;

float gSensorRange = 10.0;
integer gMaxOverlays = 8;
float gRefreshPeriod = 4.0;
float gFOV;
list gSkipNames = ["Object", "Tree", ""];

list gDetectedNames;
list gDetectedKeys;
list gDetectedPositions;
list gDetectedEmissions;

integer gAnnotate = FALSE;
string gAnnotationType;
string gAnnotationUrl = "http://wiki.amee.com/andrew/secondlife/get.php?path=/data";
string gAnnotationPath;
string gAnnotationParams;
key gAnnotationRequest;

key gEmissionsRequest;
integer gEmissionsRequestIndex;

// Emission parameters
integer gDistanceKmPerMonth = 1207; // cars, motorcycles
integer gJourneysPerYear = 2; // flights
integer gHoursPerMonth = 90; // tv
integer gCyclesPerMonth = 12; // washing machine, dryer, dishwasher
integer gNumberOwned = 1; // entertainment devices, e.g. computers, dvd, freeview box, game console etc.

key gUpdateId;
string gRegionName;
vector gCameraPos;
rotation gCameraRot;
integer gHidingOverlays;
integer gSelectedIndex;

key gNotecardId;
integer gNotecardLine;

string gURL = "http://carbongoggles.org/";

float gLastRateTime;
float gLastScanTime;
float gLastSelectedTime;

integer DISPLAY_STRING = 204000;
integer SET_COLOR = 204007;
integer SET_POSITION = 204008;
integer SET_SCALE = 204009;
integer SET_TEXT_COLOUR = 204010;
integer SET_ALPHA = 204011;
integer OVERLAY_LINK_OFFSET = 2;
integer OVERLAY_COUNT = 8;

key httpRequest(string url, list parameters, string body)
{
    //llOwnerSay("llHTTPRequest " + url + " " + body);
    return llHTTPRequest(url, parameters, body);
}

requestEmissions()
{
    if(gEmissionsRequestIndex < llGetListLength(gDetectedEmissions) && llList2Float(gDetectedEmissions, gEmissionsRequestIndex) < 0.0f)
    {
        string url = gURL + "object/" + (string)llList2Key(gDetectedKeys, gEmissionsRequestIndex) + "/emissions?";
        url += "distanceKmPerMonth=" + (string) gDistanceKmPerMonth;
        url += "%26journeysPerYear=" + (string) gJourneysPerYear;
        url += "%26hoursPerMonth=" + (string) gHoursPerMonth;
        url += "%26cyclesPerMonth=" + (string) gCyclesPerMonth;
        url += "%26numberOwned=" + (string) gNumberOwned;
        //llOwnerSay(url);
        gEmissionsRequest = httpRequest(url, [HTTP_METHOD, "GET"], "");
    }
}

rescan()
{
    float time = llGetTime();
    if(time > gLastScanTime + gScanDelay && gSelectedIndex == -1)
    {
        llSensor("", NULL_KEY, ACTIVE | PASSIVE, gSensorRange, PI / 2.0);
        gLastScanTime = time;
    }
}

hideOverlay(integer index)
{
    float offset = 0.5 + ((2 / 16.0) * (float)index);
    //string s = (string)index;
    //float offset = 1.1;
    string s = "";
    llMessageLinked(index + OVERLAY_LINK_OFFSET, SET_ALPHA, (string)0.0f, NULL_KEY);
    llMessageLinked(index + OVERLAY_LINK_OFFSET, DISPLAY_STRING, s, NULL_KEY);
    llMessageLinked(index + OVERLAY_LINK_OFFSET, SET_SCALE, (string)<0.1,0.1,0.1>, NULL_KEY);
    llMessageLinked(index + OVERLAY_LINK_OFFSET, SET_POSITION, (string)<0,0,offset>, NULL_KEY);
}

hideOverlays()
{
    integer i = 0;
    while(i < OVERLAY_COUNT)
    {
        hideOverlay(i);
        ++i;
    }
    gHidingOverlays = TRUE;
}

setOverlayColour(vector colour)
{
    integer i;
    for(i = 0; i < OVERLAY_COUNT; ++i)
    {
        llMessageLinked(i + OVERLAY_LINK_OFFSET, SET_COLOR, (string)<0.8,0.8,0.8>, NULL_KEY);
    }
}

init(key id)
{
    gFOV = 60.0 * DEG_TO_RAD;
    gLastRateTime = 0.0;
    gLastScanTime = 0.0;
    llResetTime();
    llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
    gCommandChannelHandle = llListen(gCommandChannel, "", id, "");
    gAnnotateDialogChannelHandle = llListen(gAnnotateDialogChannel, "", id, "");
    gConfigDialogChannelHandle = llListen(gConfigDialogChannel, "", id, "");
    llOwnerSay("Loading settings");
    gNotecardLine = 0;
    gNotecardId = llGetNotecardLine("Settings", gNotecardLine);
    hideOverlays();
    gSelectedIndex = -1;
    setOverlayColour(<0,1,0>);
}

integer overlay(integer index)
{
    vector cameraPos = llGetCameraPos();
    rotation cameraRot = llGetCameraRot();
    integer overlayLinkNum = index + OVERLAY_LINK_OFFSET;
    float emissions = llList2Float(gDetectedEmissions, index);
    vector objectPos = llList2Vector(gDetectedPositions, index);

    if(emissions >= 0.0f || gAnnotate)
    {
        // Translate object in to camera space.
        objectPos = objectPos - cameraPos;

        // Rotate object in camera space.
        rotation invCameraRot = <0.0,0.0,0.0,1.0> / cameraRot;
        objectPos = objectPos * invCameraRot;

        // Switch axes from Z = up to RHS (X = left, Y = up, Z = forward)
        objectPos = <-objectPos.y, objectPos.z, objectPos.x>;

        // Apply perspective distortion.
        float xHUD = (objectPos.x * (1.0 / llTan(gFOV / 2.0))) / objectPos.z;
        float yHUD = (objectPos.y * (1.0 / llTan(gFOV / 2.0))) / objectPos.z;

        // Set front clipping plane to 1m and back clipping plane to infinity.
        float zHUD = (objectPos.z - 2) / objectPos.z;

        // Clip object to HUD.
        if( xHUD > -1.0 && xHUD < 1.0 &&
            yHUD > -1.0 && yHUD < 1.0 &&
            zHUD > -1.0 && zHUD < 1.0)
        {
            string label = "Click to annotate";
            if(llList2Float(gDetectedEmissions, index) >= 0.0f)
            {
                label = (string)llList2String(gDetectedNames, index) + "\n";
                label += (string)llList2Float(gDetectedEmissions, index) + " kg co2/month";
            }
            else
            {
                emissions = 1.0f;
            }

            vector posHUD = <0, -xHUD / 2, yHUD / 2> - llGetLocalPos();
            llMessageLinked(overlayLinkNum, SET_POSITION, (string)posHUD, NULL_KEY);
            float radius = llPow((3.0f * emissions) / (4.0f * PI), (1.0 / 3.0));
            float scale = (float)radius / 10.0f;
            if(scale > 1.0)
            {
                scale /= 10.0;
                llMessageLinked(overlayLinkNum, SET_COLOR, (string)<0.5,0.05,0.05>, NULL_KEY);
            }
            else
            {
                llMessageLinked(overlayLinkNum, SET_COLOR, (string)<0.8,0.8,0.8>, NULL_KEY);
            }
            llMessageLinked(overlayLinkNum, SET_SCALE, (string), NULL_KEY);
            llMessageLinked(overlayLinkNum, DISPLAY_STRING, label, NULL_KEY);
            llMessageLinked(overlayLinkNum, SET_ALPHA, (string)1.0f, NULL_KEY);
            return TRUE;
        }
    }
    hideOverlay(index);
    return FALSE;
}

integer setOption(string option)
{
    list pair = llParseString2List(option, [":", " "], []);
    string name = llList2String(pair, 0);
    name = llToLower(name);
    if(name == "sensorrange")
    {
        gSensorRange = llList2Float(pair, 1);
    }
    else if(name == "refreshperiod")
    {
        gRefreshPeriod = llList2Float(pair, 1);
        llSetTimerEvent(gRefreshPeriod);
    }
    else if(name == "selectiontimeout")
    {
        gSelectionTimeout = llList2Float(pair, 1);
    }
    else if(name == "annotate")
    {
        gAnnotate = llList2Integer(pair, 1);
    }
    else if(name == "fieldofview")
    {
        gFOV = llList2Float(pair, 1) * DEG_TO_RAD;
    }
    else if(name == "skipnames")
    {
        gSkipNames = llCSV2List(llList2String(pair, 1));
    }
    else if(name == "overlayrgb")
    {
        vector colour;
        list rgb = llCSV2List(llList2String(pair, 1));
        colour.x = llList2Float(rgb, 0);
        colour.y = llList2Float(rgb, 1);
        colour.z = llList2Float(rgb, 2);
        setOverlayColour(colour);
    }
    else if(name == "distancekmpermonth")
    {
        gDistanceKmPerMonth = llList2Integer(pair, 1);
    }
    else if(name == "journeysperyear")
    {
        gJourneysPerYear = llList2Integer(pair, 1);
    }
    else if(name == "hourspermonth")
    {
        gHoursPerMonth = llList2Integer(pair, 1);
    }
    else if(name == "cyclespermonth")
    {
        gCyclesPerMonth = llList2Integer(pair, 1);
    }
    else if(name == "numberowned")
    {
        gNumberOwned = llList2Integer(pair, 1);
    }
    else
    {
        return FALSE;
    }
    //llOwnerSay(llList2String(pair, 0) + ":" + llList2String(pair, 1));
    return TRUE;
}

annotateObject(integer index, string ameeurl)
{
    key id = llList2Key(gDetectedKeys, index);
    vector position = llList2Vector(gDetectedPositions, index);
    string body = (string)((integer)position.x);
    body += "," + (string)((integer)position.y);
    body += "," + (string)((integer)position.z);
    body += "," + llEscapeURL(ameeurl);
    body += "," + llList2String(gDetectedNames, index);
    string url = gURL + "object/" + (string)id;
    gUpdateId = httpRequest(url, [HTTP_METHOD, "POST"], body);
    llOwnerSay("Annotated " + llList2String(gDetectedNames, gSelectedIndex));
    gSelectedIndex = -1;
}

saySettings()
{
    llOwnerSay("To change settings, chat \"/5 Setting:Value\" or change values in Settings notecard then re-attach HUD\nSensorRange:N (scan objects up to N meters away)\nRefreshTime:N (update overlay positions every N seconds)\nShowUnknown:N (augment objects with unknown emissions if N is 1)\nFieldOfView:N (field of view in degrees, must match viewer)\nSkipNames:X,Y,...,Z (ignore objects with names in list X,Y,...,Z)\nOverlayRGB:R,G,B (set overlay colour to )\nSelectionTimeout:N (time out object selection after N seconds)\n");
}

default
{
    state_entry()
    {
        init(llGetOwner());
    }

    attach(key id)
    {
        if(id != NULL_KEY)
        {
            init(id);
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        if(channel == gCommandChannel)
        {
            list pair = llParseString2List(message, ["", " "], []);
            string command = llList2String(pair, 0);
            command = llToLower(command);
            if(setOption(message) == TRUE)
            {
                return;
            }
            else if(command == "annotate")
            {
                annotateObject(gSelectedIndex, llList2String(pair, 1));
            }
            else
            {
                llOwnerSay("ERROR: Unrecognised command \"" + message + "\" chat \"/5 Help\" for help");
            }
        }
        else if(channel == gAnnotateDialogChannel)
        {
            if(gAnnotationType == "path")
            {
                gAnnotationPath += "/" + llEscapeURL(message);
            }
            else
            {
                if(gAnnotationParams == "")
                {
                    gAnnotationParams = "/drill%3f";
                }
                else
                {
                    gAnnotationParams += "%26";
                }
                gAnnotationParams += gAnnotationType;
                gAnnotationParams += "=";
                gAnnotationParams += llEscapeURL(message);
            }
            string url = gAnnotationUrl + gAnnotationPath + gAnnotationParams;
            gAnnotationRequest = httpRequest(url, [], "");
            //llOwnerSay(url);
        }
        else if(channel == gConfigDialogChannel)
        {
            if(message == "Visualise")
            {
                llOwnerSay("Hiding annotation interface...");
                gAnnotate = FALSE;
            }
            else if(message == "Annotate")
            {
                llOwnerSay("Showing annotation interface...");
                gAnnotate = TRUE;
            }
            else if(message == "Web")
            {
                llOwnerSay("Loading web interface...");
                llLoadURL(llGetOwner(), "", gURL);
            }
            else if(message == "Settings")
            {
                saySettings();
            }
            else if(message == "Off")
            {
                llOwnerSay("Turning off...");
                state off;
            }
        }
    }

    timer()
    {
        if((gSelectedIndex != -1) && (gLastSelectedTime + gSelectionTimeout < llGetTime()))
        {
            gSelectedIndex = -1;
            llOwnerSay("Selection timeout");
        }

        vector cameraPos = llGetCameraPos();
        rotation cameraRot = llGetCameraRot();
        string regionName = llGetRegionName();
        integer hide = (regionName != gRegionName)
                        || (llVecDist(cameraPos, gCameraPos) / gRefreshPeriod > 0.1)
                        || (llAngleBetween(cameraRot, gCameraRot) * RAD_TO_DEG > 10);
        gRegionName = regionName;
        gCameraPos = cameraPos;
        gCameraRot = cameraRot;
        if(hide == TRUE)
        {
            hideOverlays();
            return;
        }
        gHidingOverlays = FALSE;

        integer count = llGetListLength(gDetectedNames);
        integer i = 0;
        while(i < count)
        {
            overlay(i);
            ++i;
        }
        while(i < OVERLAY_COUNT)
        {
            hideOverlay(i);
            ++i;
        }
        rescan();
    }

    sensor(integer num)
    {
        //llOwnerSay("sensor");
        list oldKeys = gDetectedKeys;
        list oldEmissions = gDetectedEmissions;
        gDetectedNames = [];
        gDetectedKeys = [];
        gDetectedPositions = [];
        gDetectedEmissions = [];
        integer i;
        for(i = 0; i < num && i < gMaxOverlays; ++i)
        {
            string name = llDetectedName(i);
            //llOwnerSay("scanned " + name);
            integer skip = FALSE;
            integer skipCount = llGetListLength(gSkipNames);
            integer skipIndex;
            for(skipIndex = 0; (skipIndex < skipCount) && (skip == FALSE); ++skipIndex)
            {
                if(name == llList2String(gSkipNames, skipIndex))
                {
                    skip = TRUE;
                }
            }

            if(skip == FALSE)
            {
                key newKey = llDetectedKey(i);
                integer oldCount = llGetListLength(oldKeys);
                integer oldIndex;
                integer found = FALSE;
                for(oldIndex = 0; (oldIndex < oldCount) && (found == FALSE); ++oldIndex)
                {
                    key oldKey = llList2Key(oldKeys, oldIndex);
                    if(oldKey == newKey)
                    {
                        gDetectedEmissions += llList2Float(oldEmissions, oldIndex);
                        found = TRUE;
                    }
                }
                if(found == FALSE)
                {
                    gDetectedEmissions += -1.0f;
                }
                gDetectedNames += name;
                gDetectedKeys += newKey;
                gDetectedPositions += llDetectedPos(i);
            }
        }
        gRegionName = llGetRegionName();
        gCameraPos = llGetCameraPos();
        gEmissionsRequest = NULL_KEY;
        gEmissionsRequestIndex = 0;
        gSelectedIndex = -1;
        requestEmissions();
    }

    http_response(key id, integer status, list meta, string body)
    {
        if(id == gEmissionsRequest)
        {
            //llOwnerSay("request http_response " + (string)status + " length " + (string)llStringLength(body) + " " + body);
            if(status == 200)
            {
                list result = llParseString2List(body, [","], []);
                //llOwnerSay(llList2CSV(result));
                float emissions = llList2Float(result, 1);
                //llOwnerSay((string) emissions + " " + (string) gEmissionsRequestIndex + " " + llList2CSV(gDetectedEmissions));
                gDetectedEmissions = llListReplaceList(gDetectedEmissions, [emissions], gEmissionsRequestIndex, gEmissionsRequestIndex);
            }
            overlay(gEmissionsRequestIndex);
            gEmissionsRequest = NULL_KEY;
            ++gEmissionsRequestIndex;
            requestEmissions();
        }
        else if(id == gAnnotationRequest)
        {
            //llOwnerSay((string)status);
            //llOwnerSay(body);
            //list result = llParseString2List(body, [" ",",","\n"], []);
            //llOwnerSay(llList2CSV(result));
            //string type = llList2String(result, 0);
            string type = llGetSubString(body, 0, llSubStringIndex(body, ",") - 1);
            list result = llParseString2List(body, [type + ",","\n"], []);
            //llOwnerSay(body);
            //llOwnerSay(llList2CSV(result));
            if(type == "uid")
            {
                // AMEE data item UID found, build and store AMEE URL.
                string uid = llList2String(result, 0);
                string url = gAnnotationUrl + gAnnotationPath + "/" + uid;
                annotateObject(gSelectedIndex, url);
                llOwnerSay("(To annotate another object with the same data, select it, then say \"/5 annotate " + url + "\"");
            }
            else
            {
                gAnnotationType = type;
                list options = [];
                integer length = llGetListLength(result);
                integer i;
                for(i = 0; i < length; i += 1)
                {
                    options += llList2String(result, i);
                }
                if(type == "path")
                {
                    type = "catagory";
                }
                options = llList2List(options, 0, 11); // TODO: Paginate instead of truncating options.
                //llOwnerSay(llList2CSV(options));
                llDialog(llGetOwner(), "Select " + type, options, gAnnotateDialogChannel);
            }
        }
        if(status != 200 && status != 404)
        {
            llOwnerSay("ERROR:" + (string)status + ":" + body);
        }
        //llOwnerSay("http_response " + (string)status + " length " + (string)llStringLength(body) + " " + body);
    }

    dataserver(key id, string data)
    {
        if(id == gNotecardId)
        {
            if(data != EOF)
            {
                if(setOption(data) == FALSE)
                {
                    llOwnerSay("ERROR: Unknown setting " + data);
                }
                ++gNotecardLine;
                gNotecardId = llGetNotecardLine("Settings", gNotecardLine);
            }
            else
            {
                llOwnerSay("Settings loaded\nEmissions data will be overlayed on objects when avatar is stationary\nClick logo for settings");
                llSetTimerEvent(gRefreshPeriod);
                llSensor("", NULL_KEY,  ACTIVE | PASSIVE, gSensorRange, PI / 2.0);
            }
        }
    }

    touch_start(integer num)
    {
        integer linkNum = llDetectedLinkNumber(0);
        //llOwnerSay((string)linkNum);
        linkNum -= OVERLAY_LINK_OFFSET;
        if(linkNum >= 0)
        {
            gSelectedIndex = linkNum;
            gLastSelectedTime = llGetTime();
            llOwnerSay("Selected " + llList2String(gDetectedNames, gSelectedIndex) + "(" + llList2String(gDetectedKeys, gSelectedIndex) + ")");
            gAnnotationPath = "";
            gAnnotationParams = "";
            gAnnotationRequest = httpRequest(gAnnotationUrl, [], "");
        }
        else
        {
            llDialog(llGetOwner(), "Select Interface", ["Web", "Settings", "Off", "Visualise", "Annotate"], gConfigDialogChannel);
        }
    }
}

state off
{
    state_entry()
    {
        hideOverlays();
        llSetTimerEvent(0);
    }

    touch_start(integer num)
    {
        llOwnerSay("Turning on...");
        state default;
    }
}
```