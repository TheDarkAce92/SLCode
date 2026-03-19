---
name: "llAddToLandBanList"
category: "function"
type: "function"
language: "LSL"
description: "Add avatar to the land ban list for hours, or indefinitely if hours is zero."
signature: "void llAddToLandBanList(key avatar, float hours)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAddToLandBanList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lladdtolandbanlist"]
---

Add avatar to the land ban list for hours, or indefinitely if hours is zero.


## Signature

```lsl
void llAddToLandBanList(key avatar, float hours);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID |
| `float` | `hours` |  |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAddToLandBanList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAddToLandBanList) — scraped 2026-03-18_

Add avatar to the parcel ban list for the specified number of hours.

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- Must be owned by the land owner.
- When values below 1 are used, it seems the function bans in approximately 30 second increments. (Probably 36 second increments, as 0.01 of an hour is 36 seconds)

## Examples

```lsl
// This is not a complete solution, requires full avatar names to work - even for unbanning someone!
// This is meant only as an example of the land ban and pass management functions.
// free to copy, use, modify, distribute - just don't ask me to debug your modified code. ;-)
//
// Commands are:
//   /5 ban:full_avatar_name
//   /5 tempban:full_avatar_name
//   /5 unban:full_avatar_name
//   /5 pass:full_avatar_name
//   /5 unpass:full_avatar_name
//   /5 clearban
//   /5 clearpass

string command;

default
{
    state_entry()
    {
        llListen(5, "", llGetOwner(), "");
    }

    on_rez(integer param)
    {
        llResetScript();
    }

    listen(integer chan, string name, key id, string message)
    {
        if (command != "")
        {
            llOwnerSay("Sorry, still processing last command, try again in a second.");
        }

        list args = llParseString2List(message,[":"],[]);
        command = llToLower(llList2String(args,0));

        if (command == "clearbans")
        {
            llResetLandBanList();
        }
        if (command == "clearpass")
        {
            llResetLandPassList();
        }
        else
        {
            llSensor(llList2String(args,1),NULL_KEY,AGENT,96,PI);
        }
    }

    no_sensor()
    {
        command = "";
    }

    sensor(integer num)
    {
        integer i = 0;
        for (; i < num; ++i)
        {
            if (command == "ban")
            {
                // Ban indefinetely
                llAddToLandBanList(llDetectedKey(i),0.0);
            }
            if (command == "tempban")
            {
                // Ban for 1 hour.
                llAddToLandBanList(llDetectedKey(i),1.0);
            }
            if (command == "unban")
            {
                llRemoveFromLandBanList(llDetectedKey(i));
            }
            if (command == "pass")
            {
                // Add to land pass list for 1 hour
                llAddToLandPassList(llDetectedKey(i),1.0);
            }
            if (command == "unpass")
            {
                llRemoveFromLandPassList(llDetectedKey(i));
            }
        }
        command = "";
    }
}
```

## See Also

### Functions

- llAddToLandPassList
- llRemoveFromLandBanList
- llRemoveFromLandPassList
- llResetLandBanList
- llResetLandPassList

<!-- /wiki-source -->
