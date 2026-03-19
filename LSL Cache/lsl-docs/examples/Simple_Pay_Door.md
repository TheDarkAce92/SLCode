---
name: "Simple Pay Door"
category: "example"
type: "example"
language: "LSL"
description: "This is a very simple pay door. With this, you have to pay a door to get access into something. You can set the amount of money, how long it takes to close after payment. Override coming soon."
wiki_url: "https://wiki.secondlife.com/wiki/Simple_Pay_Door"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a very simple pay door. With this, you have to pay a door to get access into something. You can set the amount of money, how long it takes to close after payment. Override coming soon.

```lsl
// Pay Door that rules
// Made by: Giygas Static
// 2011/01/30

/// START USER SETTINGS

integer time = 1; // How much time until the door closes again
integer price = 20; // Price of Admission in L
integer DEBUG = 0; // 0 for RETAIL, 1 for TESTING

/// END USER SETTINGS

integer door1chan = 696736; //channel used to communicate to the door to override and open as such
string name = "NULL"; //Name of Person who eventually gives
string own = "NULL"; //Name of Owner that is defined later
integer difference = 0; //Temp spot for difference if someone over pays.
vector      mypos;      // door position (objects move a tiny amount
integer     DOOR_OPEN   = 1;
integer     DOOR_CLOSE  = 2;
integer     DIRECTION   = -1;       // direction door opens in. Either 1 (outwards) or -1

door(integer what) {
    rotation    rot;
    rotation    delta;

    llSetTimerEvent(0); // kill any running timers

    if ( what == DOOR_OPEN ) {
        //llTriggerSound("Door open", 0.8);

        rot = llGetRot();
        delta = llEuler2Rot(<0, 0, -DIRECTION * PI_BY_TWO>);
        rot = delta * rot;                  // rotate by -45 degree
        llSetRot(rot);

    } else if ( what == DOOR_CLOSE) {
        rot = llGetRot();
        delta = llEuler2Rot(<0, 0, DIRECTION * PI_BY_TWO>);    // rotate by 45 degree
        rot = delta * rot;
        llSetRot(rot);

        //llTriggerSound("Door close", 0.8);
    }
}

default
{
    state_entry()
    {
    llSetTimerEvent(5);
    }

    timer()
    {
    llRequestPermissions(llGetOwner(), PERMISSION_DEBIT);
    }

    run_time_permissions(integer permissions)
    {
        //Only wait for payment if the owner agreed to pay out money
        if (permissions & PERMISSION_DEBIT)
        {
            state ready;
        }
    }

    on_rez(integer start_par)
    {
    llResetScript();
    }
}

state ready
{
    state_entry()
    {
        if (DEBUG == 1)
        {
        llOwnerSay("WARNING! Debug is on, you will not recieve money if someone clicks your door without paying!");
        }
        llOwnerSay("Ready.");
        own = llKey2Name(llGetOwner());
    }

    touch_start(integer total_num){
        name = llKey2Name(llDetectedKey(0));
        llSay(0, "Hello " + name + " to access " + own + "'s House you need to pay " + (string)price + "L. Thank you.");
        if (DEBUG == 1)
        {
            door(DOOR_OPEN);
            state on;
        }
    }

    on_rez(integer start_par)
    {
    llResetScript();
    }

    money(key giver, integer amt)
    {
        name = llKey2Name(giver);
        if( amt == price ) {
            llSay(0, "Paid, Access Granted for " + (string)time + " Seconds: " + name);
            door(DOOR_OPEN);
            state on;
        }
        if( amt < price ) {
            llSay(0, "ACCESS DENIED: you need to pay " + (string)price + "L.\n You Tried to pay " + (string)amt + "L.");
            llGiveMoney(giver, amt);
        }
        if( amt > price ) {
            difference = amt - price;
            llSay(0, "Access granted, You paid too much, here's the difference from" + (string)price + "L, which is " + (string)difference + "L." );
            llGiveMoney(giver, difference);
            door(DOOR_OPEN);
            state on;
        }
    }
}

state on
{
    state_entry()
    {
    llSetTimerEvent(time);
    }

    timer()
    {
    door(DOOR_CLOSE);

    llSetPos(mypos);        // workaround for tiny movements during rotation
     state ready;
    }

    on_rez(integer start_par)
    {
    llResetScript();
    }
}
```