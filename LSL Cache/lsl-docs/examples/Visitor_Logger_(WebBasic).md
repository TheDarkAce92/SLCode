---
name: "Visitor Logger (Web/Basic)"
category: "example"
type: "example"
language: "LSL"
description: "I was asked to log visitors for a two-day event a while ago, and then asked if the scripts I used could be given to original users. Being very simple scripts, I didn't want to charge for these, and so I've decided to make them public."
wiki_url: "https://wiki.secondlife.com/wiki/Visitor_Logger_(Web/Basic)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

### Notes

I was asked to log visitors for a two-day event a while ago, and then asked if the scripts I used could be given to original users. Being very simple scripts, I didn't want to charge for these, and so I've decided to make them public.

**Licence info**

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can obtain a copy of the GNU General Public License
from here: [[1]](http://www.gnu.org/licenses/).

The software is copyright (c) Daniel Livingstone 2008 ### Use: Upload the server side script to your web server, and place the LSL script a phantom prim in SL - the script will turn the prim invisible if it is not already. Ideal placement may be a small prim at waist height at a telehub, or at floor level covering a large area where users might walk through. You will need to edit the LSL script with the appropriate URL for your server. Serverside script:

```lsl

   Simple Visitor Logger

<?php

$name = htmlspecialchars($_GET['name']);
$object = htmlspecialchars($_GET['object']);
$key = htmlspecialchars($_GET['key']);
$ip = $_SERVER['REMOTE_ADDR'];
$ref = $_SERVER['HTTP_REFERER'];
$dtime = date('r');
if($ref == ""){
   $ref = "None";
}
if($name == ""){
   $name = "anon";
}
?>
Hello <?php echo  $name ?>.
thank you for visiting.
<?php
$entry_line = "$dtime - IP: $ip | name: $name | key: $key | object: $object\n";
$fp = fopen("visitors.txt", "a");
fputs($fp, $entry_line);
fclose($fp);
?>

```

The text file, "visitors.txt" must have write permissions.

**LSL script:**

```lsl
// Copyright (c) Daniel Livingstone 2008
// Released under GNU Public License GPL 3.0
string lastVisitor;

default
{
    state_entry()
    {
        llSetAlpha((float)FALSE, ALL_SIDES);
        llVolumeDetect(TRUE);
    }

    collision_start(integer num_detected)
    {
        integer i;
        do
        {
            key id = llDetectedKey(i);
            string name = llDetectedName(i);

            if (name != lastVisitor)
            {
                string url = "http://www.YOURSITE.URL/get_data.php?"
                    + "name=" + llEscapeURL(name)
                    + "&key=" + llEscapeURL((string)id)
                    + "&object=" + llEscapeURL(llGetObjectName());

                llHTTPRequest(url, [], "");
                lastVisitor = name;
            }
        }
        while (++i < num_detected);
    }

    http_response(key request_id, integer status, list data, string body)
    {
        //llOwnerSay(body);
        //llOwnerSay("here!");
    }
}
```