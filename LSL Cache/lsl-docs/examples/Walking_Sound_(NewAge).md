---
name: "Walking Sound (NewAge)"
category: "example"
type: "example"
language: "LSL"
description: "NewAge Walking Sound Version 1 Copy and Paste Script into your object/shoes that will play the walking sounds and edit the configuration section '// Configure;'"
wiki_url: "https://wiki.secondlife.com/wiki/Walking_Sound_(NewAge)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**NewAge Walking Sound**
Version 1
Copy and Paste Script into your object/shoes that will play the walking sounds and edit the configuration section '// Configure;'



```lsl
/////////////////////////////////
// NewAge Walking Sound Script
// By Asia Snowfall
// Version 1.0
/////////////////////////////////

// Configure;

string Default_Start_Walking_Sound = ""; // Paste in the UUID for the sound that will play when avatar starts to walk

string Default_Walking_Sound = ""; // Paste in the UUID for the sound that will play during walking

string Default_Stop_Walking_Sound = ""; // Paste in the UUID for the sound that will play when avatar stops walking

float Walking_Sound_Speed = 0.2; // This feature is added so that creators can match the sound speed to walking motion

float Volume_For_Sounds = 1.0; // This is for the volume of the sounds played, 1.0 = Max, 0.0 = Mute

// API Sound Feature
// Allows customers to add their own sounds to the script by placing sounds into object inventory

string API_Start_Walking_Sound_Name = "start"; // If there is a sound name in inventory with this name somewhere in the sound name, it will load as an API Sound to start walking

string API_Walking_Sound_Name = "loop"; // If there is a sound name in inventory with this name somewhere in the sound name, it will load as an API Sound to play during walking

string API_Stop_Walking_Sound_Name = "stop"; // If there is a sound name in inventory with this name somewhere in the sound name, it will load as an API Sound to play when avatar stops walking

// Varibles;

string API_Start_Sound;
string API_Walking_Sound;
string API_Stop_Sound;

// Integer Varibles

integer walking = FALSE;

// Float Varibles

float seconds_to_check_when_avatar_walks = 0.01;

// Pre-made functions

key llGetObjectOwner()
{
    list details = llGetObjectDetails(llGetKey(), [OBJECT_OWNER]);
    return (key)llList2CSV(details);
}

asLoadSounds()
{
    API_Start_Sound = "";
    API_Walking_Sound = "";
    API_Stop_Sound = "";
    integer i = 0;
    integer a = llGetInventoryNumber(INVENTORY_SOUND)-1;
    string name;
    do
    {
        name = llGetInventoryName(INVENTORY_SOUND, i);
        if(llStringLength(name) > 0)
        {
            if(llSubStringIndex(name, API_Start_Walking_Sound_Name) != -1)
            {
                API_Start_Sound = name;
            }
            else if(llSubStringIndex(name, API_Walking_Sound_Name) != -1)
            {
                API_Walking_Sound = name;
            }
            else if(llSubStringIndex(name, API_Stop_Walking_Sound_Name) != -1)
            {
                API_Stop_Sound = name;
            }
        }
    }while(i++ 40000)
    {
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}

default
{
    state_entry()
    {
        if(CheckMono() == FALSE)
        {
            llInstantMessage(llGetObjectOwner(), "This script will run better in Mono");
        }
        if(llGetAttached() != 0)
        {
            llSetTimerEvent(seconds_to_check_when_avatar_walks);
            asLoadSounds();
        }
        else
        {
            llSetTimerEvent(0);
            llInstantMessage(llGetObjectOwner(), "Sounds disabled, Please attach object to your avatar");
        }
    }
    attach(key id)
    {
        llResetScript();
    }
    changed(integer p)
    {
        if(llGetInventoryNumber(INVENTORY_SOUND) > 0)
        {
            asLoadSounds();
        }
    }
    timer()
    {
        if(llGetAgentInfo(llGetObjectOwner()) & AGENT_WALKING)
        {
            llSetTimerEvent(Walking_Sound_Speed);
            if(walking == FALSE)
            {
                if(llStringLength(API_Start_Sound) > 0)
                {
                    llTriggerSound(API_Start_Sound, Volume_For_Sounds);
                }
                else if(llStringLength(Default_Start_Walking_Sound) > 0)
                {
                    llTriggerSound(Default_Start_Walking_Sound, Volume_For_Sounds);
                }
                walking = TRUE;
                llSetTimerEvent(Walking_Sound_Speed);
            }
            else if(walking == TRUE)
            {
                if(llStringLength(API_Walking_Sound) > 0)
                {
                    llTriggerSound(API_Walking_Sound, Volume_For_Sounds);
                }
                else if(llStringLength(Default_Walking_Sound) > 0)
                {
                    llTriggerSound(Default_Walking_Sound, Volume_For_Sounds);
                }
            }
        }
        else
        {
            if(walking == TRUE)
            {
                walking = FALSE;
                if(llStringLength(API_Stop_Sound) > 0)
                {
                    llTriggerSound(API_Stop_Sound, Volume_For_Sounds);
                }
                else if(llStringLength(Default_Stop_Walking_Sound) > 0)
                {
                    llTriggerSound(Default_Stop_Walking_Sound, Volume_For_Sounds);
                }
                llSetTimerEvent(seconds_to_check_when_avatar_walks);
            }
        }
    }
}
```