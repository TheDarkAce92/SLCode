---
name: "Serverless Key Exchange"
category: "example"
type: "example"
language: "LSL"
description: "This is a script to address a common issue I had for a long time in SL: how do you maintain a network of objects across multiple sims, given that the key of each object might change at any time?"
wiki_url: "https://wiki.secondlife.com/wiki/Serverless_Key_Exchange"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Description
- 2 Directions and Explanation
- 3 Exchange
- 4 The Helper Script
- 5 Changes Needed

## Description

This is a script to address a common issue I had for a long time in SL: how do you maintain a network of objects across multiple sims, given that the key of each object might change at any time?

## Directions and Explanation

Create two objects. Take the key of one object and put it into the *description* of the other object. Now put the scripts in, and after a few minutes (depending on email exchange speed), they will be linked. When creating additional nodes on the network, simply make sure to put the key of another node into the description of your object.

The way this works is it stores its "neighbors'" keys in its description. Then it shares information with its neighbors, chattering back and forth about who is on the 'network'. Ultimately the result is a fault-tolerant network of client/servers, sort of like a P2P system. I suggest you just read the script, if it makes sense to you then maybe you can use it... if it doesn't, then likely you have no use for it.

## Exchange

```lsl
list keylist;
integer rotn;
integer rotm;

loadKeylist()
{
    if( llStringLength(llGetObjectDesc()) < 8 ) return;
    keylist = llParseString2List(llGetObjectDesc(),[","],[]);
}
saveKeylist()
{
    if( llGetListLength(keylist) > 3 ) {
        integer st = (integer)llFrand( llGetListLength(keylist)-3 );
        llSetObjectDesc( llDumpList2String( llList2List( keylist, st, st+2 ), "," ) );
    } else
        llSetObjectDesc(llDumpList2String(keylist,","));
}
addKeys( string mesg )
{
    list newkeys = llParseString2List(mesg,[","],[]);
    integer i;
    integer len = llGetListLength(newkeys);

    for( i = 0; i < len; i++ ) {
        if( llGetKey() != llList2Key(newkeys,i) && llListFindList(keylist,[llList2String(newkeys,i)]) < 0 ) {
            keylist=(keylist=[])+keylist+[llList2String(newkeys,i)];
        }
    }
}
checkKeylist()
{
    integer i;
    integer j;
    integer len = llGetListLength(keylist);

    for( i = 0; i < len; i++ ) {
        if( llList2Key(keylist,i) == llGetKey() || llStringLength(llList2Key(keylist,i)) < 36 ) {
            keylist=llDeleteSubList(keylist,i,i);
            len = len-1;
            i = i-1;
        } else {
            for( j = i+1; j < len; j++ ) {
                if( llList2String(keylist,i) == llList2String(keylist,j) ) {
                    keylist=llDeleteSubList(keylist,j,j);
                    len = len-1;
                    j = j-1;
                }
            }
        }
    }
}

validateKeylist()
{
//    llOwnerSay("Validating keylist");
    broadcastEmail("validate", (string)llGetKey());
    keylist=[];
}
broadcastEmail( string subj, string mesg )
{
    integer i;
    integer len = llGetListLength(keylist);

    for( i=0; i 0 )
                    broadcastEmail( "keys", "~" + (string)llGetKey() + "," + llDumpList2String(keylist, ",") );
                else
                    broadcastEmail( "keys", "~" + (string)llGetKey() );
            }
        }
    }

    email(string time, string addr, string subj, string mesg, integer nl)
    {
        list msgdet = llParseString2List(mesg,["~"],[]);
        string realmesg = llList2String(msgdet,1);
 //       llOwnerSay("Got " + subj + ": " + realmesg);

        if( subj == "validate" ) {
            if( llListFindList( keylist, [realmesg] ) < 0 ) keylist = (keylist=[]) + keylist + [realmesg];
            llEmail(addr, "valid", "~" + (string)llGetKey() );
        } else if( subj == "valid" && ( llListFindList( keylist, [realmesg] ) < 0 ) ) {
            keylist = (keylist=[]) + keylist + [realmesg];
        } else if( subj == "keys" ) {
            addKeys( realmesg );
//        } else if( subj == "echo" ) {
//            llSay(0, (string)llGetKey() + " recv'd: " + realmesg);
        }

        if( nl > 0 ) llGetNextEmail("","");
    }
}
```

## The Helper Script

```lsl
integer touched_already=0;

default
{
    on_rez(integer sp)
    {
        llResetScript();
    }
    state_entry()
    {
        integer i = 1+(integer)llFrand(5.0);
        llListen(i,"","","");
        llSay(0,"On channel " + (string)i);
    }

    touch_start( integer nd )
    {
        if( touched_already==0 ) {
            llOwnerSay("key: " + (string)llGetKey());
            llOwnerSay("Touch within 2 seconds to get detailed info");
            llSetTimerEvent(2.0);
            touched_already=1;
        } else {
            touched_already=0;
            llMessageLinked( LINK_SET, 42, "", "" );
        }
    }
    timer()
    {
        touched_already=0;
        llSetTimerEvent(0.0);
    }

    listen( integer ch, string nam, key id, string msg )
    {
        llMessageLinked( LINK_SET, 32, msg, "" );
    }
}
```

## Changes Needed

Currently all this sucker does is maintain a list and coincidentally distribute chat. It doesn't do anything with the keys. If you happen to modify it to do something more interesting, please let Sendao Goodman know, and/or update this page.