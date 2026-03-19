---
name: "Library Chat Relay"
category: "example"
type: "example"
language: "LSL"
description: "This is a script to easily distribute a conversation in a large area, or keep people in contact while off in different parts of the sim. I have it set up to relay objects that the avatar might be wearing (such as OOC chatters), and so that anyone can set up a relay and join in the conversation."
wiki_url: "https://wiki.secondlife.com/wiki/Library_Chat_Relay"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a script to easily distribute a conversation in a large area, or keep people in contact while off in different parts of the sim.
I have it set up to relay objects that the avatar might be wearing (such as OOC chatters), and so that anyone can set up a relay and join in the conversation.

This script, however, was designed to be polite. It asks you if you want to join the chat relay system, and you can click on the relay prim at any time to opt-out.

```lsl
string original_name = "Chat Relay v1.0";

integer CHANNEL = -3735928559;

list acl;
list blk;

// CONSTANTS
string STR_ASK = "Would you like to be included in the chat-relay system?";
list   LST_OPT = ["ALLOW","DENY"];

// Vars for speed
integer int;
key tempkey;
string str;

hovertext(){
    llSetText(original_name + "\nCLICK TO CHANGE ALLOW/DENY SETTINGS\nAllow list: " + (string)llGetListLength(acl) +
              "\nDeny list: " + (string)llGetListLength(blk)+
              "\nMemory Left: " + (string)llGetFreeMemory(),
              <1.0,0.0,1.0>,1.0);
}

default{
    on_rez(integer i){llResetScript();}
    changed(integer i){if(i & CHANGED_OWNER){llResetScript();}}
    state_entry() {
        llSetObjectName(original_name);
        llListen(0,"",NULL_KEY,"");
        llListen(CHANNEL,"",NULL_KEY,"");
        hovertext();
    }
    listen(integer chan,string name,key k,string message){
        if(chan == 0){
            //Get the name of the avatar/owner of object
            str = name;
            tempkey = llGetOwnerKey(k);
            if(tempkey != k){
                str = llKey2Name(tempkey);
                if(str == ""){return;}
            }
            //Be nice to nearby vendors and such
            if(name == ""){ return; }

            //Ignore anyone on the blocklist
            if(~llListFindList(blk,(list)str)){ return; }
            //Check if not on ACL
            if(!~llListFindList(acl,(list)str)){
                llDialog(tempkey,STR_ASK,LST_OPT,CHANNEL);
                return;
            }
            llSetObjectName(name);
            llRegionSay(CHANNEL,message);
            llSetObjectName(original_name);
            return;
        }
        if(chan == CHANNEL){
            if(message == "ALLOW"){
                if(1 + llListFindList(acl,(list)name)){ return; }
                int = llListFindList(blk,(list)name);
                if(~int){ blk = llDeleteSubList(blk,int,int); }
                acl = (acl = []) + acl + name;
                hovertext();
                return;
            }
            if(message == "DENY") {
                if(1 + llListFindList(blk,(list)name)){ return; }
                int = llListFindList(acl,(list)name);
                if(~int){ acl = llDeleteSubList(acl,int,int); }
                blk = (blk = []) + blk + name;
                hovertext();
                return;
            }
            llSetObjectName(name);
            llSay(0,message);
            llSetObjectName(original_name);
            return;
        }
    }
    touch_start(integer i){ llDialog(llDetectedKey(0),STR_ASK,LST_OPT,CHANNEL); }
}
```