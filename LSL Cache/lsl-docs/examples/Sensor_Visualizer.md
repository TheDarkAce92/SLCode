---
name: "Sensor Visualizer"
category: "example"
type: "example"
language: "LSL"
description: "This script can show you how the llSensor radius and range parameters work."
wiki_url: "https://wiki.secondlife.com/wiki/Sensor_Visualizer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script can show you how the llSensor radius and range parameters work.

Drop the script in a prim. The prim will turn into a sphere 10 meters across so leave plenty of space. Touch the prim to start. You will see a list of commands you can use. An information display will hover over the prim.

When the prim is grey it is not sensing, remember to touch it and say "start" in chat to begin. When it is red it is active but the sensor does not see any avatars. Walk into the prim, it will turn green when the sensor detects you.

llSensor can have a range up to 96 meters and an arc down to zero. This demonstration uses a smaller range because prims are less flexible.

```lsl
// llSensor visualizer.
//
// This will make a prim be the same size and shape as
// its sensor range.
//
// There are some limits!
//
// - Sensors can cover a 0 to 96 meters radius but
//   a prim sphere can only show 0.05 to 5, so the sensor range is
//   restricted to match the prim limits.
//
// - Sensors can cover a 0 to pi arc but prim sphere dimples
//   can only show .063 to PI, so the sensor arc is restricted
//   to match the prim limits.
//
// Cerise Sorbet wrote this, use and change it as you wish.

float gSensorRange = 5.0;
float gSensorArc = PI;
float gTimerInterval = 0.0;

integer gListening;
integer gListenChannel = 0;
integer gListener;
float gListenTimeout = 30.0;

string gListenAvatar;
key gListenWho;
integer gAvatarCount;

float gMinRange = 0.005; // prims only shrink to 0.01 meter
float gMaxRange = 5.0; // prims only grow to 10 meters
float gMinArc; // set in state_entry, PI * 0.02, end dimple limit
float gSensorTime = 1.0;

SetTimer(float seconds)
{
    gTimerInterval = seconds;
    llSetTimerEvent(seconds);
}

UpdateText()
{
    string status = "idle";
    vector rot = llRot2Euler(llGetRot());
    if (gListening)
    {
        llSetColor(<0.5, 0.5, 0.5>, ALL_SIDES);
        llSetText(gListenAvatar + ",\ntype a command in chat, or help", <0.25, 1.0, 0.25>, 1.0);
    }
    else
    {
        if (gTimerInterval)
        {
            status = "sensing";
            if (gAvatarCount)
            {
                llSetColor(<0.5, 1.0, 0.5>, ALL_SIDES); // green, someone in range
            }
            else
            {
                llSetColor(<1.0, 0.5, 0.5>, ALL_SIDES); // red, none in range
            }
        }
        else
        {
                llSetColor(<0.5, 0.5, 0.5>, ALL_SIDES); // grey, inactive
        }
        llSetText("llSensor visualizer (" + status + ")\nTouch me for commands\n \nrange = " +
        (string)gSensorRange + "\t\tarc = " + (string)gSensorArc + "\nEuler rot = " +
        (string)rot + "\ndegrees rot = " + (string)(rot * RAD_TO_DEG) +
        "\navatars in range = " + (string)gAvatarCount,
        <1.0, 1.0, 1.0>, 1.0);
    }
}

SetShape(float radius, float arc)
{

    float diameter = 2 * radius;

    if (arc < gMinArc)
    {
        arc = gMinArc;
    }
    else if (arc > PI)
    {
        arc = PI;
    }

    if (radius < gMinRange)
    {
        radius = gMinRange;
    }
    else if (radius > gMaxRange)
    {
        radius = gMaxRange;
    }

    llSetPrimitiveParams
    ([
        PRIM_TYPE,
            PRIM_TYPE_SPHERE,
                PRIM_HOLE_DEFAULT, // hole shape
                <0.0, 1.0, 0.0>, // cut
                0.0, // hollow
                ZERO_VECTOR, // twist
                <0.0, arc / PI, 0.0>, // dimple
        PRIM_SIZE,
            ,
        PRIM_PHANTOM,
            TRUE
    ]);
}

PrintHelp() {
    llSay
    (0,
        "Sensing paused. Say a command in chat:\n" +
        "\t\tarc " + (string)gSensorArc + "  - angle out from front to look, values 0.0 - 3.1416 (pi)\n" +
        "\t\trange " + (string)gSensorRange + " - distance from center to look, values 0.0 - 5.0\n" +
        "\t\tstart - begin sensing"
    );
}

default
{
    state_entry()
    {
        gMinArc = PI * 0.02;
        llSetTexture(TEXTURE_BLANK, ALL_SIDES);
        llSetAlpha(0.7, ALL_SIDES);
        UpdateText();
        SetShape(gSensorRange, PI);
        llSetObjectName("Sensor visualizer");
        llSetObjectDesc("Touch me to begin");
    }

    touch_start(integer total_number)
    {
        gListening = TRUE;
        gListenAvatar = llDetectedName(0);
        gListener = llListen(gListenChannel, "", llDetectedKey(0), "");
        UpdateText();
        gAvatarCount = 0;
        SetTimer(gListenTimeout);
        PrintHelp();
    }

    timer()
    {
        if (gListening)
        {
            SetTimer(0.0);
            gListening = FALSE;
            llListenRemove(gListener);
            UpdateText();
        }
        else
        {
            llSensor("", "", AGENT, gSensorRange, gSensorArc);
        }
    }

    sensor(integer detected)
    {
        if (gAvatarCount != detected)
        {
            gAvatarCount = detected;
            UpdateText();
        }
    }

    no_sensor()
    {
        if (gAvatarCount)
        {
            gAvatarCount = 0;
            UpdateText();
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        SetTimer(gListenTimeout); // restart the clock

        list argv = llParseString2List(llToLower(message), [" "], []);
        integer argc = llGetListLength(argv);
        if (argc == 0) return;

        string command = llList2String(argv, 0);
        if (command == "help")
        {
            PrintHelp();
        }
        else if (command == "start")
        {
            gListening = FALSE;
            llListenRemove(gListener);
            llSay(0, "Sensing...");
            SetTimer(gSensorTime);
        }
        else if (command == "arc")
        {
            if (argc < 2)
            {
                llSay(0, "must supply an arc value, 0.0 to pi");
                return;
            }
            gSensorArc = llList2Float(argv, 1);
            if (gSensorArc > PI)
            {
                llSay(0, (string)gSensorArc + " is more than pi, using pi");
                gSensorArc = PI;
            }
            if (gSensorArc < gMinArc)
            {
                llSay(0, (string)gSensorArc + "radians is less than I can show, using " + (string)gMinArc);
                gSensorArc = gMinArc;
            }
            SetShape(gSensorRange, gSensorArc);
        }
        else if (command == "range")
        {
            if (argc < 2)
            {
                llSay(0, "must supply a radius value, 0.0 to 5.0");
                return;
            }
            gSensorRange = llList2Float(argv, 1);
            if (gSensorRange > gMaxRange)
            {
                llSay(0, (string) gSensorRange + "meters is more than I can show, using " + (string)gMaxRange);
                gSensorRange = gMaxRange;
            }
            if (gSensorRange < gMinRange)
            {
                llSay(0, (string) gSensorRange + "meters is smaller than I can show, using " + (string)gMinRange);
                gSensorRange = gMinRange;
            }
            SetShape(gSensorRange, gSensorArc);
        }
        UpdateText();
    }
}
```