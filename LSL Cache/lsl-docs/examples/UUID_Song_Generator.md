---
name: "UUID Song Generator"
category: "example"
type: "example"
language: "LSL"
description: "integer max_note=7; // change this to the # of notes available! float speed=2.0; // change this to the length to wait before playing the next note"
wiki_url: "https://wiki.secondlife.com/wiki/UUID_Song_Generator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Sendao Goodman wrote this

integer max_note=7; // change this to the # of notes available!
float speed=2.0; // change this to the length to wait before playing the next note

//Don't change anything else yo
list playback;
integer spot;
list notes;

loadNotes()
{
    integer i;
    integer ln;

    notes=[];

    for( i = llGetNumberOfPrims(); i > 0; i-- )
    {
        notes=(notes=[])+notes+[(integer)llGetLinkName(i)];
    }

// we tell the players how long each sound is
    llMessageLinked(LINK_SET, 3, (string)speed, "");
}

list transformKey(key uuid_k, integer max_note)
{ // convert a key into a string of numbers
    string uuid = (string)uuid_k;
    list uuid_untrans = llParseString2List(uuid, ["", "-"], []);
    list uuid_new;
    string mark;
    integer val;
    float conval;

    integer len = llStringLength(uuid);
    uuid_new=[];
    while( len > 0 ) {
        len--;
        mark = llGetSubString(uuid,len,len);
        val = (integer)mark;
        if( val == 0 ) {
            if( mark == "a" )
                val = 10;
            else if( mark == "b" )
                val = 11;
            else if( mark == "c" )
                val = 12;
            else if( mark == "d" )
                val = 13;
            else if( mark == "e" )
                val = 14;
            else if( mark == "f" )
                val = 15;
        }
        conval = (float)val / 16.0;
        if( mark != "-" )
            uuid_new=(uuid_new=[]) + uuid_new + [(integer)(conval*(float)max_note)];
    }
    return uuid_new;
}

playNote( integer notenum ) // send the message to trigger the note
{
    llMessageLinked( llList2Integer(notes,notenum), 1, "", "" );
}
default
{
    on_rez(integer sp)
    {
        llResetScript();
    }

    state_entry()
    {
        loadNotes();
    }

    touch_start(integer total_number) // scan avatar key and start playback
    {
        playback = transformKey(llDetectedKey(0), max_note);
        spot = 0;
//        llSay(0, "Your adjusted key is " + llDumpList2String(playback, ","));
        llSetTimerEvent(speed);
    }

    timer() // timer is used to play each sound
    {
        spot++;
        if( spot >= llGetListLength(playback) ) {
            llSetTimerEvent(0.0);
            llSay(0, "Song complete.");
            return;
        }
        playNote( llList2Integer(playback,spot) );
//      llSay(0, "Play note " + (string)llList2Integer(playback,spot) + " link " + (string)(llList2Integer(notes,llList2Integer(playback,spot))));
    }
}
```