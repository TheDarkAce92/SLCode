---
name: "Sim Performance Collector (Web-based"
category: "example"
type: "example"
language: "LSL"
description: "created by DeniseHoorn Slade"
wiki_url: "https://wiki.secondlife.com/wiki/Sim_Performance_Collector_(Web-based"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

created by DeniseHoorn Slade

Want to present your Sim on a website with a graph for DIL, FPS and PING? Or do you have some troubles with your sim and problems with LL-support, because they are in opinion, that your sim is running fine? So with these graphs you can show the LL-support the DIL, FPS and PING-times during the last 24 hours!

See examples at the professional service of [SL-Simperformance.de](http://www.sl-simperformance.de)

I am sure if other scripter will realize other ideas, we will have at least a very good overview on our sims - PLEEEEASE inform me, if you pimp up this script!

#### Important

This scripts are under the licence of GPL. You are not allowed to sell any objects using this script.

#### What you need:

A server elsewhere in the WWW with an installed Apache or IIS. PHP, and rrdtools installed. You need some basic knowledge on PHP-scripting and LSL-scripting. I try to describe the installation as easy as possible.

#### Introduction

This is the lsl-script. Rezz a box, texture it like a server and place it elsewhere on the sim. No need to be a simowner, no need to deed this prim.
This script collects the internal grabable informations: FPS, DIL, servername and simname and sends it via HTTP to a PHP-Script on your website. The PHP-script is below. Attention! Watch, that the path to your php-script is correct!

```lsl
float   currentTimeDilation;

integer currentFPS;
integer totalFPS;
float   averageFPS;

integer numberOfUpdates;

string  regionName;
string  server;

string  simstatus;

key     simStatusReqId;
key     postReqId;

string  website;

init()
{
    website = "http://www.yourdomainhere.com/php/write_rrd.php";

    update_data();

//  every minute
    llSetTimerEvent(60.0);
}

update_data()
{
//  increment counter...
    ++numberOfUpdates;

    regionName          = llGetRegionName();
    currentTimeDilation = llGetRegionTimeDilation();
    server              = llGetSimulatorHostname();

    currentFPS          = llFloor(llGetRegionFPS());
    totalFPS            += currentFPS;

    averageFPS          = totalFPS / numberOfUpdates;

    vector color_red = <1.0, 0.0, 0.0>;
    llSetText("Region Performance\n"
              + server + "\n"
              + regionName + "\n"
              + (string)currentFPS + "fps",
              color_red, 1.0);

    simStatusReqId      = llRequestSimulatorData(regionName, DATA_SIM_STATUS);
}

send_data(float dil, integer fps)
{
    postReqId = llHTTPRequest(website, [
                                    HTTP_METHOD, "POST",
                                    HTTP_MIMETYPE, "application/x-www-form-urlencoded"],
                                "dil=" + (string)dil
                                + "&fps=" + (string)fps
                                + "&region=" + regionName
                                + "&server=" + server
                                + "&method=set");
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & CHANGED_REGION)
            llResetScript();
    }

    state_entry()
    {
        init();
    }

    timer()
    {
        update_data();
        send_data(currentTimeDilation, currentFPS);
        //simstatus == "up"/"down"/"starting"/"stopping"/"crashed"/"unknown"
    }

    http_response(key id, integer status, list meta, string body)
    {
    //  llSay(0, body);
        if (id != postReqId)
            return;

        integer stringpartposition = llSubStringIndex(body, "result = ");
        if (stringpartposition == 0)
            return;

        string result = llGetSubString(body, stringpartposition + 9, -1);
        llStringTrim(result, STRING_TRIM);

        if (result != "ERROR occured")
            return;

        key owner = llGetOwner();
        llInstantMessage(owner,
            "An error has occured with the Simperformance-Grapher for sim '"
            + regionName + "'. Check the rrd and the PHP-Script!");
    }

    dataserver(key query_id, string data)
    {
        if (query_id != simStatusReqId)
            return;

        simStatusReqId = "";
        simstatus = (data);
    }
}
```

On your server lets create the rrd's (Round Robin Databases) --> [http://www.mrtg.org/rrdtool/](http://www.mrtg.org/rrdtool/)
Here are the commands to create a rrd. Let me first say, that I have very less knowledge on rrd's what I have created is an overview for a day. if somebody is able to make it much much better, PLEASE let me know!
IMPORTANT: The synonym "nameofyoursim" has to be replaced exactly with the simname! The php-script get's the simname and adds only a "_dilfps.rrd" so watch

`/usr/bin/rrdtool create nameofyoursim_dilfps.rrd --step 600 DS:dil:GAUGE:600:0:1 DS:fps:GAUGE:600:0:50 RRA:AVERAGE:0.5:1:5040 RRA:AVERAGE:0.5:12:9600`

The ping-database will be created with:

`/usr/bin/rrdtool create NDL_FeEseGrimLa_ping.rrd --step 300 DS:ping:GAUGE:300:0:1 RRA:AVERAGE:0.5:1:5040 RRA:AVERAGE:0.5:12:9600`

This is the PHP-script which is called by the lsl-script. It takes the data, pings the server and put all data into the rrd's

```lsl
<?php

$method = $_POST['method'];
$dil = $_POST['dil'];
$fps = $_POST['fps'];
$region = $_POST['region'];
$server = $_POST['server'];
$path = "/home/n/ndlsim.de/php/cms/php/";

if ($method=="")
{
    die("result = No Method provided!");
}

if ($region=="")
{
    die("result = No region provided!");
    //alerts script in SL not to send any data any more and to inform the owner about this damn error... :)
} else {
    $region = str_replace(" ","_",$region);
    $RRDFILE = $path.$region."_dilfps.rrd";
    $RRDFILE_ping = $path.$region."_ping.rrd";
}

echo ("result = $server");
$resultping = shell_exec("/bin/ping $server -c 1");
$var1 = strpos($resultping, "time=");
$ping = trim((substr($resultping,$var1+5,3)));

if ($method=="set")
{

    //write data into rrd's

    $ret = exec("/usr/bin/rrdtool update $RRDFILE -t dil:fps N:$dil:$fps");
        if( $ret1 != 0 )
        {
            die ("result = ERROR occurred");
        }
//    echo "result = /usr/bin/rrdtool update $RRDFILE -t dil:fps N:$dil:$fps";

    $ret = exec("/usr/bin/rrdtool update $RRDFILE_ping -t ping N:$ping");
        if( $ret2 != 0 )
        {
            die ("result = ERROR occurred");
        }
//    echo ("result = /usr/bin/rrdtool update $RRDFILE_ping -t ping N:$ping");
//echo ("result = $ping");

}
?>
```

And last but not least, we have to build the graph from the data. it's a bash-script (Linux) which create the graphs.

```lsl
#!/bin/bash
#
RRDFILE=/home/n/ndlsim.de/php/cms/php/yoursimnamehere_dilfps.rrd
RRDPING=/home/n/ndlsim.de/php/cms/php/yoursimnamehere_ping.rrd

GRAPHFILE1=/home/n/ndlsim.de/php/cms/bilder/yoursimname_DIL.png
GRAPHFILE2=/home/n/ndlsim.de/php/cms/bilder/yoursimname_FPS.png
GRAPHFILE3=/home/n/ndlsim.de/php/cms/bilder/yoursimname_ping.png

rrdtool graph $GRAPHFILE1 -v "Dilation" \
  -u 1.1 -l 0 \
  -t "Dilation Time for yoursim" \
  DEF:dil=$RRDFILE:dil:AVERAGE LINE2:dil#309030:"Dilation Time" \
  HRULE:1.0#AAAA00:"Performace best / Performance sehr gut" \
  HRULE:0.8#0000FF:"Performace ok / Performance gut" \
  HRULE:0.5#FF0000:"Lagging expected / Lag zu erwarten" \
  COMMENT:"\\n" \
  COMMENT:"(Last updated\: $(/bin/date "+%d.%m.%Y %H\:%M\:%S"))\r" \
  -w 600 -h 200 -a PNG

rrdtool graph $GRAPHFILE2 -v "FPS" \
  -u 50.0 -l 0 \
  -t "Frames Per Second for yoursim" \
  DEF:fps=$RRDFILE:fps:AVERAGE LINE2:fps#309030:"Frames Per Second" \
  HRULE:44#AAAA00:"Performace best / Performance sehr gut" \
  HRULE:35#0000FF:"Performance ok /Performance gut" \
  HRULE:20#FF0000:"Lagging / Lag" \
  HRULE:10#FF0000:"Terrible / Katastrophal" \
  COMMENT:"\\n" \
  COMMENT:"(Last updated\: $(/bin/date "+%d.%m.%Y %H\:%M\:%S"))\r" \
  -w 600 -h 200 -a PNG

rrdtool graph $GRAPHFILE3 -v "PING-Time" \
  -u 200.0 -l 60 \
  -t "PING-Time for yoursim" \
  DEF:ping=$RRDPING:ping:AVERAGE LINE2:ping#309030:"PING in ms" \
  HRULE:90#AAAA00:"Performace best / Performance sehr gut" \
  HRULE:140#0000FF:"Performance ok /Performance gut" \
  HRULE:190#FF0000:"Lagging / Lag" \
  COMMENT:"\\n" \
  COMMENT:"(Last updated\: $(/bin/date "+%d.%m.%Y %H\:%M\:%S"))\r" \
  -w 600 -h 200 -a PNG
```

Hope you will find it useful. If so, drop me a note inworld...