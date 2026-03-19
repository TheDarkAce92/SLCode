---
name: "Read Note Card Configuration"
category: "example"
type: "example"
language: "LSL"
description: "Learn how to read configuration files with Linden Scripting Language (LSL) in Second Life (SL). After viewing this tutorial, you will be able to:"
wiki_url: "https://wiki.secondlife.com/wiki/Read_Note_Card_Configuration"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Learn how to read configuration files with Linden Scripting Language (LSL) in Second Life (SL). After viewing this tutorial, you will be able to:

- Create a script
- Read each line of a note card
- Skip over comments
- Skip blank lines
- Notify the owner of the lines with unknown settings

  - Unknown setting name
  - Missing delimiter (equal sign)
- Notify the owner of missing configuration note card
- Detect when the notecard has been changed
- Offer case-insensitive settings
- Trim white-space from name/value settings
- Initialize with default values
- Detect that the name of the configuration file is a notecard
- Detect that  you have reached the end of the file



1. **DOWNLOAD**  [How to read configuration information from a notecard](http://dedricmauriac.wordpress.com/2008/05/03/configuration-reading-tutorial/)

```lsl
# this is a file to configure your application
# blank lines are ignored as well as lines
# proceeded with a "#" sign.
Name = Dedric Mauriac
Favorite Color = Blue
```

```lsl
string configurationNotecardName = "Application.Config";
key notecardQueryId;
integer line;

string AvatarName;
string FavoriteColor;

init()
{
//  reset configuration values to default
    AvatarName = "Unknown";
    FavoriteColor = "None";

//  make sure the file exists and is a notecard
    if(llGetInventoryType(configurationNotecardName) != INVENTORY_NOTECARD)
    {
    //  notify owner of missing file
        llOwnerSay("Missing inventory notecard: " + configurationNotecardName);
    //  don't do anything else
        return;
    }

//  initialize to start reading from first line (which is 0)
    line = 0;
    notecardQueryId = llGetNotecardLine(configurationNotecardName, line);
}

processConfiguration(string data)
{
//  if we are at the end of the file
    if(data == EOF)
    {
    //  notify the owner
        llOwnerSay("We are done reading the configuration");

    //  notify what was read
        llOwnerSay("The avatar name is: " + AvatarName);
        llOwnerSay("The favorite color is: " + FavoriteColor);

    //  do not do anything else
        return;
    }

//  if we are not working with a blank line
    if(data != "")
    {
    //  if the line does not begin with a comment
        if(llSubStringIndex(data, "#") != 0)
        {
        //  find first equal sign
            integer i = llSubStringIndex(data, "=");

        //  if line contains equal sign
            if(i != -1)
            {
            //  get name of name/value pair
                string name = llGetSubString(data, 0, i - 1);

            //  get value of name/value pair
                string value = llGetSubString(data, i + 1, -1);

            //  trim name
                list temp = llParseString2List(name, [" "], []);
                name = llDumpList2String(temp, " ");

            //  make name lowercase (case insensitive)
                name = llToLower(name);

            //  trim value
                temp = llParseString2List(value, [" "], []);
                value = llDumpList2String(temp, " ");

            //  name
                if(name == "name")
                    AvatarName = value;

            //  color
                else if(name == "favorite color")
                    FavoriteColor = value;

            //  unknown name
                else
                    llOwnerSay("Unknown configuration value: " + name + " on line " + (string)line);

            }
        //  line does not contain equal sign
            else
            {
                llOwnerSay("Configuration could not be read on line " + (string)line);
            }
        }
    }

//  read the next line
    notecardQueryId = llGetNotecardLine(configurationNotecardName, ++line);
}

default
{
    on_rez(integer start_param)
    {
        init();
    }

    changed(integer change)
    {
        if(change & (CHANGED_OWNER | CHANGED_INVENTORY))
            init();
    }

    state_entry()
    {
        init();
    }

    dataserver(key request_id, string data)
    {
        if(request_id == notecardQueryId)
            processConfiguration(data);
    }
}
```