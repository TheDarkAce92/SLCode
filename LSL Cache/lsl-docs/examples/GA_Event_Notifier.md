---
name: "GA Event Notifier"
category: "example"
type: "example"
language: "LSL"
description: "This calendar consists of an lsl script and a php script."
wiki_url: "https://wiki.secondlife.com/wiki/GA_Event_Notifier"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This calendar consists of an lsl script and a php script.

The lsl script is listed first, and the php script is listed below it.

Please be careful not to overlap when copying the scripts.

```lsl
FUNCTION:
Gather seven days event data from a Google calendar and display it through a simple interface.
The lsl script can access several calendars at once through seperate php files. One file per calendar.
```



```lsl
/////////////////////////////////////////////////////////////////////
// GA Event Notifier 1.0 by Jason Dahlen (aka Victor Hua)
// SpotOn3D
// https://spoton3d.com/
// (c) 2010 - Jason Dahlen
//
// Distributed as GPL, donated to wiki.secondlife.com on 13 July 2010
//
// SCRIPT:  GA Event Notifier.lsl 1.0    :: Use on your web server
//          gaenot_1.0.php           :: Use inworld
//
// FUNCTION:
// Gather seven days event data from a Google calendar and display it through a simple interface.
//The lsl script can access several calendars at once through seperate php files. One file per calendar.
//
// USAGE:
// 1. Place gaenot_1.0.php in your web directory. Anywhere you can view the php file in a web browser.
//      You will need a seperate gaenot_1.0.php file for each calendar you want to display. You can rename the files.
// 2. At the top of your gaenot_1.0.php file you will find two variables.
//      $email            Enter your gmail address
//      $Calendar_xml_URL     A URL that points to your Live Bookmarks feed for Google Calendars.
//                               You can find this under My Calendar in the settings toward the bottom.
//                             Choose the 'xml' button selection from the following:
//                              -Calendar Address - This address works if you have a publically viewable calendar
//                              (ie viewable publically in a web browser)
//                            -Private Address - Use this address if you want to display information from an
//                                   otherwise private calendar. This calendar would then only be viewable by
//                                      yourself and those using the in world lsl tool.
// 3. Drop the GA Event Notifier.lsl in your object.
// 4. Add the locations of the php files in the url list. You can have one or several.
// 5. Set the  gmtOffset to your time or the time of the calendar you are accessing.
//
/////////////////////////////////////////////////////////////////////

//Add URLs to the list pointing to the location of your gaenot.php script.
//list urls = [
//                "https://yourdomain.com/gaenot_1.0.php",
//                "https://yourdomain.com/gaenot_1.0-2.php"
//            ];
list urls = [
                "https://yourdomain.com/gaenot_1.0.php"
            ];

//Set the GMT offset to your timezone or to the timezone of the google calendar.
integer gmtOffset = -5;

//######################################### Edit below this line at your own risk ##########################

list days; //Day value reference
list dates; //List of event dates
list titles; //Event titles
list place; //Event locations if given
list details; //Event details if given
integer calendars; //Number of calendars traced by this tool.
integer thisCalendar; //Used when retrieving calendar data.

//Used to parse incoming event data
list weekdays = ["Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed"];

//Used for generating button list.
list week = ["Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"];
list buttonList;

//Channels
integer CHANNEL;
integer HANDLE;

//Initialize script variables
constructor()
{
    days = [];
    dates = [];
    titles = [];
    place = [];
    details = [];
    calendars = llGetListLength(urls);
    thisCalendar = 0;
    llSetTimerEvent(3600);
    makeButtonList();
    //llHTTPRequest(url, [], "");
    requestData();
    llOwnerSay("Events List Refreshed");
    llOwnerSay("");
    llListenControl(HANDLE, FALSE);
}

requestData()
{
    if(thisCalendar < calendars)
    {
        llHTTPRequest(llList2String(urls,thisCalendar), [], "");
        thisCalendar += 1;
    }
}

// Generate dialog button list
makeButtonList()
{
    buttonList = [];
    list tempList = [];
    integer day = getDay(gmtOffset);
    integer i;
    for (i=0; i<7; i++)
    {
        tempList += llList2String(week,day);
        day++;
        if (day > 6)
        {
            day = 0;
        }
    }

    buttonList =    [llList2String(tempList,6),"Today", "Refresh",
                    llList2String(tempList,3), llList2String(tempList,4), llList2String(tempList,5),
                    llList2String(tempList,0), llList2String(tempList,1), llList2String(tempList,2)];
}

//Creates dialog channel based on the object UUID. Reduces the chance of cross messaging.
integer hex2int(string hex)
{
    if(llGetSubString(hex,0,1) == "0x")
        return (integer)hex;
    if(llGetSubString(hex,0,0) == "x")
        return (integer)("0"+hex);
    return(integer)("0x"+hex);
}

//Parse incoming data from the php file into seperate lists.
parceString(string body)
{
    list tempList = llParseString2List(body, ["||"], []);

    integer listLength = llGetListLength(tempList);
    integer i;

    for (i = 0; i < listLength; i++)
    {
        list data = llParseString2List(llList2String(tempList, i), [":"], []);
        string flag = llStringTrim(llList2String(data,0), STRING_TRIM);
        string val = llStringTrim(llList2String(data,1), STRING_TRIM);

        if (flag == "Date")
        {
            string day = llList2String(llParseString2List(val, [" "], []), 0);
            integer dayNum = llListFindList(weekdays, [day]);
            days += dayNum;
            dates+=val;
        }
        else
        if (flag == "Title")
        {
            titles+=val;
        }
        else
        if (flag == "Event Description")
        {
            //Google uses a colon for its data tags.
            //Unfortionatly this means that if you used a colon in your description such as a URL, it would be cut off prematurly.
            //I put a check here so at least two URLs or SLURLS such as secondlife://lambda/175/30/26 could be included.
            if (llStringTrim(llList2String(data,3), STRING_TRIM) != "")
            {
                place += (val + ":" + llStringTrim(llList2String(data,2), STRING_TRIM)+ ":" + llStringTrim(llList2String(data,3), STRING_TRIM));
            }
            else
            if (llStringTrim(llList2String(data,2), STRING_TRIM) != "")
            {
                place += (val + ":" + llStringTrim(llList2String(data,2), STRING_TRIM));
            }
            else
            {
                place+=val;
            }
        }
        else
        if (flag == "Where" || flag == "Event Status")
        {
            details+=val;
        }
    }
}

//Display day event.
displayEvent(integer day)
{
    llListenControl(HANDLE, FALSE);
    integer i;
    if(llListFindList(days, [day]) != -1)
    {
        for (i=0; i "Thu", 1 =>"Fri", 2=>"Sat", 3=>"Sun", 4=>"Mon", 5=>"Tue", 6=>"Wed"];
        if(message == "Today")
        {
            displayEvent(getDay(gmtOffset));
        }
        else
        if(message == "Sunday")
        {
            displayEvent(3);
        }
        else
        if(message == "Monday")
        {
            displayEvent(4);
        }
        else
        if(message == "Tuesday")
        {
            displayEvent(5);
        }
        else
        if(message == "Wednesday")
        {
            displayEvent(6);
        }
        else
        if(message == "Thursday")
        {
            displayEvent(0);
        }
        else
        if(message == "Friday")
        {
            displayEvent(1);
        }
        else
        if(message == "Saturday")
        {
            displayEvent(2);
        }
        else
        if(message == "Refresh")
        {
            constructor();
        }
    }
    timer()
    {
        llSetTimerEvent(3600);
        constructor();
    }
}
```





Start of the gaenot_1.0.php script.



<source lang="php">

<?php
/*
/////////////////////////////////////////////////////////////////////
// GA Event Notifier 1.0 by Jason Dahlen (aka Victor Hua)
// SpotOn3D
// [https://spoton3d.com/](https://spoton3d.com/)
// (c) 2010 - Jason Dahlen
//
// Distributed as GPL, donated to wiki.secondlife.com on 13 July 2010
//
// SCRIPT:  GA Event Notifier.lsl 1.0    :: Use on your web server
//          gaenot_1.0.php           :: Use inworld
//
// FUNCTION:
// Gather seven days event data from a Google calendar and display it through a simple interface.
//The lsl script can access several calendars at once through seperate php files. One file per calendar.
//
// USAGE:
// 1. Place gaenot_1.0.php in your web directory. Anywhere you can view the php file in a web browser.
//      You will need a seperate gaenot_1.0.php file for each calendar you want to display. You can rename the files.
// 2. At the top of your gaenot_1.0.php file you will find two variables.
//      $email            Enter your gmail address
//      $Calendar_xml_URL     A URL that points to your Live Bookmarks feed for Google Calendars.
//                               You can find this under My Calendar in the settings toward the bottom.
//                             Choose the 'xml' button selection from the following:
//                              -Calendar Address - This address works if you have a publically viewable calendar
//                              (ie viewable publically in a web browser)
//                            -Private Address - Use this address if you want to display information from an
//                                   otherwise private calendar. This calendar would then only be viewable by
//                                      yourself and those using the in world lsl tool.
// 3. Drop the GA Event Notifier.lsl in your object.
// 4. Add the locations of the php files in the url list. You can have one or several.
// 5. Set the  gmtOffset to your time or the time of the calendar you are accessing.
//
/////////////////////////////////////////////////////////////////////

- /

$email = 'myname@gmail.com';
$Calendar_xml_URL = "[http://www.google.com/calendar/feeds/myfeed](http://www.google.com/calendar/feeds/myfeed)";



//######################################### Edit below this line at your own risk ##########################





/*Debug
ini_set('display_errors',1);
error_reporting(E_ALL|E_STRICT);

- /

```lsl
   $userid = $email;
   $magicCookie = 'cookie';
   date_default_timezone_set('America/Chicago');

   // build feed URL
   $feedURL = $Calendar_xml_URL;
```

```lsl
   //Return string date as a timestamp.
   function _dateConv($str)
   {
       $dateStr = substr_replace($str[3], , -1, 1).' '.$str[2];

       if (isset($str['4']))
       {
           $dateStr = $dateStr.' '.$str[4];
       }
```

```lsl
       if (isset($str['5']))
       {
           $dateStr = $dateStr.' '.$str[5];
       }

       if (isset($str[7]))
       {
           $dateStr = $dateStr.' '.substr($str[7], -3, 3);
       }
       return $dateStr;
   }
```

```lsl
   //Print Array
   function printArrayElements($array)
   {
       foreach($array as $key => $value)
       {
           echo "$value"."||";
       }
   }
```

```lsl
   // read feed into SimpleXML object
   $sxml = simplexml_load_file($feedURL);

   // get number of events
   $total = count($sxml);
```

```lsl
   //Populate data arrays
   foreach ($sxml->entry as $entry)
   {
       $content = stripslashes($entry->content);
```

```lsl
       $data = explode('', $content);
```

```lsl
       $dateArr = explode(" ",$data[0]);
```

```lsl
       $dateString =  _dateConv($dateArr);
       $date = strtotime(_dateConv($dateArr));
```

```lsl
       $pastDue = strtotime("12:00 am -11 hours");
       $endDate = strtotime("+6 day");
```

```lsl
       if ($date > $pastDue && $date < $endDate)
       {
           $t = "test string";
           $timeList[] = 'Date: '.$dateArr[1].' '.trim($dateString);
           $titleList[] = 'Title: '.trim(stripslashes($entry->title));
           $placeList[] = trim($data[2]);
```



```lsl
           if (isset($data[4]))
           {
               $descList[] = trim($data[4]);
           }
           else
           {
               $descList[] = "Event Description:";
           }
       }
   }
```

```lsl
   //print arrays

   printArrayElements($timeList);
```

```lsl
   printArrayElements($titleList);
```

```lsl
   printArrayElements($placeList);
```

```lsl
   printArrayElements($descList);
```



```lsl
   ?>
```



</php>