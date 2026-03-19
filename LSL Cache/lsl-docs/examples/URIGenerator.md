---
name: "URIGenerator"
category: "example"
type: "example"
language: "LSL"
description: "It is tough getting a hold of people when you need to give them updated information about something and they aren't in your friends list or not showing up in search. This is a handy URI generator I wrote to bypass that using the Name2Key service by w-hat. You just click on a prim and enter their full name into the textbox and it will generate a URI to their profile privately in local using OwnerSay if they exist in the database."
wiki_url: "https://wiki.secondlife.com/wiki/URIGenerator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Introduction

It is tough getting a hold of people when you need to give them updated information about something and they aren't in your friends list or not showing up in search. This is a handy URI generator I wrote to bypass that using the Name2Key service by w-hat. You just click on a prim and enter their full name into the textbox and it will generate a URI to their profile privately in local using OwnerSay if they exist in the database.

Usage

To use this script, stick it into the root prim of pretty much any object, and wear that object somewhere on your person. When you click on it it will generate a textbox dialog to enter their whole name this includes Resident as a last.

The Code

You may do anything you like with this code, without limitation. I am not liable for any griefing done with this script it is for utility and administrative purposes only.

```lsl
//written by To-mos Codewarrior (tomos.halsey)
//URI Generator to do whatever you want with

key SYSTEM_user;
//name2key
string URL   = "http://w-hat.com/name2key"; // name2key url
string registered_id;
key    reqid;                               // http request id
llName2Key(string str)
{
    while(~llSubStringIndex(str,"\n"))
    str=llDeleteSubString(str,llSubStringIndex(str,"\n"),llSubStringIndex(str,"\n")+1);

    llOwnerSay("Generating URI for "+str+"...");
    reqid = llHTTPRequest( URL + "?terse=1&name=" +
    llEscapeURL(str), [], "" );
}
default
{
    state_entry()
    {llListen(1561456,"",NULL_KEY,"");}
    touch_start(integer total_number)
    {
        SYSTEM_user=llDetectedKey(0);
        llTextBox(SYSTEM_user,"Enter The Resident's name",1561456);
    }
    listen(integer channel,string name,key id,string message)
    {if(id==SYSTEM_user)llName2Key(message);}
    http_response(key req,integer stat, list met, string body)
    {
        if(req != reqid)
            return;
        if(stat == 499)
            llOwnerSay("name2key request timed out");
        else if(stat != 200)
            llOwnerSay("the internet exploded!! (responce:200)");
        else if((key)body == NULL_KEY)
            llOwnerSay("Key not found.");
        else
            llOwnerSay("secondlife:///app/agent/"+body+"/about");
    }
}
```