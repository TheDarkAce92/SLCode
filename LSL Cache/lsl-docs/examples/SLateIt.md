---
name: "SLateIt"
category: "example"
type: "example"
language: "LSL"
description: "float gNextObjectTimeout = 3.0; float gSensorTimeout = 30.0; float gSensorRange = 30.0; integer gChannel = 9999;"
wiki_url: "https://wiki.secondlife.com/wiki/SLateIt"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## HUD script

```lsl
// SLateIt HUD by Babbage Linden
//
// An Open Source Augmented Virtual Reality HUD for Second Life
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

float gNextObjectTimeout = 3.0;
float gSensorTimeout = 30.0;
float gSensorRange = 30.0;
integer gChannel = 9999;

list gDetectedNames;
list gDetectedKeys;
list gDetectedPositions;
list gDetectedRatings;

integer gDetectedIndex = 0;

string gURL = "http://w-hat.com/httpdb/slateit/";
key gRequestId;
integer gRequestIndex;

string gRegionName;
vector gCameraPos;

string ERROR_NOT_HUD = "Error: This object needs to be attached to HUD to function properly.";

requestRating()
{
    if(gRequestIndex < llGetListLength(gDetectedKeys))
    {
        gRequestId = llHTTPRequest(gURL + (string)llList2Key(gDetectedKeys, gRequestIndex), [HTTP_METHOD, "GET"], "");
    }
}

rescan()
{
    if(llGetTime() > gSensorTimeout)
    {
        llSensor("", NULL_KEY, ACTIVE | PASSIVE | AGENT, 20.0, PI / 2.0);
        llResetTime();
    }
}

default
{
    state_entry()
    {
        if(llGetAttached() > 29)
            llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
    }

    on_rez(integer i)
    {
        if(llGetAttached() < 30)
        {
            llSetTimerEvent(0);
            llSay(0, ERROR_NOT_HUD);
        }
    }

    attach(key avatar)
    {
        if(avatar == NULL_KEY)
        {
            llSetTimerEvent(0);
        }
        else
        {
            if(llGetAttached() < 30)
            {
                llSetTimerEvent(0);
                llSay(0, ERROR_NOT_HUD);
            }
            else
            {
                llRequestPermissions(llGetOwner(), PERMISSION_TRACK_CAMERA);
            }
        }
    }

    run_time_permissions(integer perm)
    {
        llResetTime();
        llSetTimerEvent(gNextObjectTimeout);
        llSensor("", NULL_KEY, ACTIVE | PASSIVE | AGENT, 20.0, PI / 2.0);
    }

    timer()
    {
        vector cameraPos = llGetCameraPos();
        rotation cameraRot = llGetCameraRot();
        string regionName = llGetRegionName();
        if(llVecDist(cameraPos, gCameraPos) > 30.0 || regionName != gRegionName)
        {
            // Too far from last scan point, hide HUD and rescan.
            llSetPos(<0, 0, -1.1>);
            rescan();
            return;
        }

        integer skipped = 0;
        while(gDetectedIndex < llGetListLength(gDetectedNames))
        {
            integer pendingRatings = 0;
            string ratingString = llList2String(gDetectedRatings, gDetectedIndex);
            if(ratingString != "...")
            {
                vector objectPos = llList2Vector(gDetectedPositions, gDetectedIndex);

                // Translate object in to camera space.
                objectPos = objectPos - cameraPos;

                // Rotate object in camera space.
                rotation invCameraRot = <0.0,0.0,0.0,1.0> / cameraRot;
                objectPos = objectPos * invCameraRot;

                // Switch axes from Z = up to RHS (X = left, Y = up, Z = forward)
                objectPos = <-objectPos.y, objectPos.z, objectPos.x>;

                // Apply perspective distortion.
                float FOV = 60.0 * DEG_TO_RAD;
                float xHUD = (objectPos.x * (1.0 / llTan(FOV / 2.0))) / objectPos.z;
                float yHUD = (objectPos.y * (1.0 / llTan(FOV / 2.0))) / objectPos.z;

                // Set front clipping plane to 1m and back clipping plane to infinity.
                float zHUD = (objectPos.z - 2) / objectPos.z;

                // Clip object to HUD.
                if( xHUD > -1.0 && xHUD < 1.0 &&
                    yHUD > -1.0 && yHUD < 1.0 &&
                    zHUD > -1.0 && zHUD < 1.0)
                {
                    llSay(gChannel, ratingString + ":" + llList2String(gDetectedKeys, gDetectedIndex));
                    integer DISPLAY_STRING = 204000;
                    llMessageLinked(LINK_SET, DISPLAY_STRING, ratingString, "");
                    llSetPos(<0, -xHUD / 2, yHUD / 2>);
                    if((integer) ratingString < 0)
                    {
                        llSetTexture("51c399a0-abf6-f7bc-b382-816da1da1ed5", ALL_SIDES);
                    }
                    else
                    {
                        llSetTexture("e433cbeb-1920-9f3d-0a29-449d6db7f1c6", ALL_SIDES);
                    }
                    ++gDetectedIndex;
                    return;
                }
            }
            ++gDetectedIndex;
            ++skipped;
        }
        gDetectedIndex = 0;

        if(skipped == llGetListLength(gDetectedNames))
        {
            // No objects visible, hide HUD.
            llSetPos(<0, 0, -1.1>);
        }
        rescan();
    }

    sensor(integer num)
    {
        gDetectedNames = [];
        gDetectedKeys = [];
        gDetectedPositions = [];
        gDetectedRatings = [];
        integer i;
        for(i = 0; i < num; ++i)
        {
            string name = llDetectedName(i);
            gDetectedNames += llDetectedName(i);
            gDetectedKeys += llDetectedKey(i);
            gDetectedPositions += llDetectedPos(i);
            gDetectedRatings += "...";
        }
        gRegionName = llGetRegionName();
        gCameraPos = llGetCameraPos();
        gRequestId = NULL_KEY;
        gRequestIndex = 0;
        requestRating();
    }

    http_response( key id, integer status, list meta, string body)
    {
        if(id == gRequestId)
        {
            if(status == 404)
            {
                gDetectedRatings = llListReplaceList(gDetectedRatings, ["0"], gRequestIndex, gRequestIndex);
            }
            else if(status == 200)
            {
                gDetectedRatings = llListReplaceList(gDetectedRatings, [body], gRequestIndex, gRequestIndex);
            }
            else
            {
                llOwnerSay("http_response " + (string)status + " " + body);
            }
        }
        gRequestId = NULL_KEY;
        ++gRequestIndex;
        requestRating();
    }
}
```

## HUD button script

```lsl
// SLateIt HUD Button by Babbage Linden
//
// An Open Source Augmented Virtual Reality HUD for Second Life
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

integer gListenChannel = 9999;
integer gListenHandle;

string gName;
integer gRating;

string gURL = "http://w-hat.com/httpdb/slateit/";

default
{
    state_entry()
    {
        gListenHandle = llListen(gListenChannel, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string message)
    {
        gRating = (integer) message;
        gName = llGetSubString(message, llSubStringIndex(message, ":") + 1, -1);
    }

    touch_start(integer total_number)
    {
        llHTTPRequest(gURL + gName, [HTTP_METHOD, "PUT"], (string)(++gRating));
    }

    http_response( key reqid, integer status, list meta, string body )
    {
        if(status != 200 && status != 201)
        {
            llOwnerSay("http_response " + (string)status);
        }
    }
}
```