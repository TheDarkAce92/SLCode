---
name: "Timer Module"
category: "example"
type: "example"
language: "LSL"
description: "(Please bear with me as I'm recreating what I had on my old user page."
wiki_url: "https://wiki.secondlife.com/wiki/Timer_Module"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

(Please bear with me as I'm recreating what I had on my old user page. **Timer Module** - based in part on the Dialog Module of [BlindWanderer](http://www.avisynth.org/BlindWanderer), known in SL as Strife Onizuka (I saw it. It worked. Why reinvent the wheel?)
(Hopefully this will be added to the Script Library someday.)

The current llSetTimerEvent is currently limited to one timer per script. While creative programming can overcome many obsticles, at times, this limitation can interfere with what the programmer wishes to accomplish. This library will allow for dynamic creation of timers whenever called upon. This library will make use of lists to keep track of the timers assigned to it, thus limiting it to how ever many timers it can stuff into the memory of the script. The individual timers can be ADDed, REMoved, PAUsed, and RESumed. The library can be set into motion simply by calling a llMessageLinked command to the scirpt. When there are no timers left, the library turns off it's internal timer to help reduce lag. This library, while still functional, will most likely become obsolete when Mono is finally released.

This timer uses 'ticks' and 'cycles'. The ticks are just the library's internal timer going off. The tick duration (in seconds) can be set to any positive float. Cycles are how many times a timer will be repeated before it is removed from the list. Using -1 for the cycle number will cause the timer to repeat indefinitely. Setting the ticks in the library to 2, the time in the ADD command to 20, and the cycles in the ADD command to 5, would cause the library to respond for that timer once every 40 seconds a total of 5 times.

**Command Format****Commands are CSV values sent in the following format: COMMAND, Timername, Ticks, Cycles where: COMMAND can be ADD, REM, PAU, RES (not case sensitive). Timername can be any string. The library will truncate this value to 10 characters. Ticks and Cycles can be any positive integer. Example**

```lsl
llMessageLinked(LINK_SET, 1234, "ADD,myTimer,20,5", "");
```

1. 'LINK_SET' ( integer linknum ) - If you happen to know the prim number that the library will be in, use that instead of LINK_SET.
1. '1234' ( integer num ) - You can use this field as a channel number. It will be returned in the message back from the library.
1. "ADD,myTimer,0," ( string str ) - In this example, we are adding a timer named 'myTimer' that will go off every 20 ticks a total of 5 cycles before it is removed from the lists.
1. ("") ( key id ) - Currently not used, hence the "".

When the timer goes off, the library will send a linked message back to the prim the timer was added from to trigger the link_message event. The message will be in the format of: "TIMER,myTimer,20,4,xxx,yyy".1. 'TIMER' - Indentifies the type of message. (really only of importance if you have several linked messages going back and forth between prims) 1. 'myTimer' - Name of the timer that went off. 1. '20' - Number of ticks before the timer goes off. 1. '4' - Number of cycles remaining before the timer is removed. This number will decay to 0, then the timer is removed. 1. 'xxx' - This is the current number of timers being tracked. 1. 'yyy' - This is the estimated number of timers that can still be added to the module. 1. '1234' ( not shown, but will be returned via link_message ) - This is the 'integer num' that we used above when creating the timer. It is simply echoed back. Sending "REM,myTimer,0,0" will remove 'myTimer' from the lists. Sending "PAU,myTimer,0,0" will pause 'myTimer' indefinately. Sending "RES,myTimer,0,0" will resume 'myTimer'. None of these commands will generate a message from the library, even if the timer does not exist, you are trying the pause an already paused timer, or trying to resume an already running timer. The library will send a messages only when a timer goes off. it is running out of memory, or you passed an invalid tick or cycle value. ADDing a timer when one of the same name with a matching 'channel' that already exists will simply cause the timer to be replaced without causing it to go off first. Additional commands and responses: In the event that you are trying to add more timers than the script can currently support you will received a response stating that the script is out of memory. If you try to use non-positive values for either ticks or cycles when adding a timer, you will receive a response stating so. You can send 'TIMER_STATUS_CHECK' to the script and you will receive a response giving you a plethora of information regarding to current status of the script. ConcernsScript Delays Since this library concerns time, delays could cause issues. While there is no true built-in script delay for neither the function llMessageLinked nor the link_message event, the link_message event can only queue up to 64 messages. So you may want to make sure the library isn't sending too many timer responses at once. You may also want to keep the tick duration above 0.1 to help prevent the sim CPU from becoming overburdened and causing lag. Additionally, the more timers you have, the slower the library will run. Security While there are no chat channels that can be eavesdropped on, foreign scripts will still have their link_message events triggered and therefore can listen in and even manipulate the timers. Whether your work around is a simple cypher substitution or a Elliptic curve cryptosystem initiated by a Diffie-Hellman key agreement or variant thereof is totally up to you (and whether or not the SL server can handle it in a timely manner). Memory Usage The number of timers that the library can keep track of is completely dependent upon the available memory. During initial testing, each timer consumed about 130 bytes of memory and loading the script with timers allowed for just over 120 timers. The library keeps track of free memory and will attempt to leave a 500 byte buffer. If an attempt is made to add a timer and it is determined that there is not enough free memory, the library will return an error message and not add the timer. Performance Issues While performing the initial tests, I discovered that any amount of timers over 20 seemed to really slow down the script. While the script still functioned, it would take an increasing amount of time to process the lists as more timers were added. If any of the optimizing geniuses what to take a look sat this, feel free. /me nudges Strife. Example usage

```lsl
integer timerchannellisten = 1234; //Incoming messages.
integer timerchannelspeak  = 1235; // Outgoing messages.
string  timername    = "boom"; // This is case sensitive, i.e. mytimer != MYTIMER != myTimer != MyTiMeR ... etc.

default {
    state_entry() {
        timername = llGetSubString(timername, 0, 9); // Truncates the timer name to 10 characters
    }
     touch_start(integer num_detected) {
        if (llDetectedKey(0) == llGetOwner()) {
             llOwnerSay("This object will self destruct in 5 seconds");
            // If using encryption, insert the function call around the string in the next line
            llMessageLinked(LINK_SET, timerchannelspeak, "ADD," + timername + ",5,1", NULL_KEY); // Sends "ADD,boom,5,1" to the library
        }
    }
    link_message(integer sender_num, integer num, string str, key id) { // In this example str should equal "TIMER,boom,5,0"
         if(num == timerchannellisten) { //Checks to make sure we are listening to the correct 'channel'
             // If you use any form of encryption, decrypt it at this point
            list parsedstr = llCSV2List(str); // Convert str into a list. We will use the first and second values.
                                               // The rest are only given for informational purposes and can be ignored.
            if(llList2String(parsedstr, 0) == "TIMER") {
                if(llList2String(parsedstr, 1) == "ERROR") { // Checks for a returned error
                    llOwnerSay(str);
                } else if(llList2String(parsedstr, 1) == timername) { //Checks to make sure this is the timer we are looking for
                     if((integer)llList2String(parsedstr, 3) > 0) { // Check to see if this is the last cycle.
                         llOwnerSay("How did you end up here?"); // Since in this example the cycles sent were 1, this line should never run.
                    } else {
                         llOwnerSay("I'm melting! Oh, what a world! What a world...");
                        llDie();
                    }
                }
            } else if (llList2String(parsedstr, 0) == "TIMER_STATUS") {
                llOwnerSay("TIMER STATUS - Master Timer Interval: " + (llList2String(parsedstr, 2)));
                llOwnerSay("TIMER STATUS - Current Tick Count: " + (llList2String(parsedstr, 1)));
                llOwnerSay("TIMER STATUS - Timers: " + (llList2String(parsedstr, 3)));
                llOwnerSay("TIMER STATUS - Free Memory: " + (llList2String(parsedstr, 4)));
                llOwnerSay("TIMER STATUS - Estimated Free Timers: " + (llList2String(parsedstr, 5)));
                llOwnerSay("TIMER STATUS - Input Link Channel: " + (llList2String(parsedstr, 7)));
                llOwnerSay("TIMER STATUS - Output Link Channel: " + (llList2String(parsedstr, 6)));
            }
        }
    }
}
```

During my initial testing in the example above, I had the 'TIMER STATUS' portion piped to llSetText instead of the llOwnerSay.

**Timer Module**

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//    Timer Module
//    Version 1.0 Release
//    Copyright (C) 2007, Isabelle Aquitaine
//    http://wiki.secondlife.com/wiki/LSL_Library_Timer_Module
//    http://wiki.secondlife.com/wiki/User:Isabelle_Aquitaine
//
//    This library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU Lesser General Public License
//    as published by the Free Software Foundation; either
//    version 2.1 of the License, or (at your option) any later version.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Lesser General Public License for more details.
//
//    You should have received a copy of the GNU Lesser General Public License
//    along with this library; if not, write to the Free Software
//    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
//    Based mostly in part on:
//
//    Dialog Module
//    Version 9.3 Release
//    Copyright (C) 2004-2006, Strife Onizuka
//    http://home.comcast.net/~mailerdaemon/
//    http://wiki.secondlife.com/wiki/Dialog_Module
//
//    References:
//
//    Timer Enhancer by ChristopherOmega
//    http://lslwiki.net/lslwiki/wakka.php?wakka=LibraryTimerEnhancer
//
//////////////////////////////////////////////////////////////////////////////////////
// Modifiable variables:
integer timerchannelspeak = 1234;// Any valid integer can be used. Just make sure that it matches the control message.
integer timerchannellisten = 1235;

float   timeint = 1;      // Time interval. 1 = 1 second, 60 = 60 seconds, .5 = half of a second, etc. Adjust this
                            //   as needed. Remember to adjust the number of ticks that is passed to this module via
                            //   other scripts. I.E. if this value is set at .1 and you need the event to be reported
                            //   every second, then the value sent should be 10.

//////////////////////////////////////////////////////////////////////////////////////
//Don't change anything else unless you *really* need to.

//////////////////////////////////////////////////////////////////////////////////////
//Declarations
integer ticks;               // master timer counter

list    timername;           // Name of the timer
list    timerticks;          // Duration of the timer
list    timercycles;         // How many times the timer will be cycled before it is removed
list    timerprim;           // Prim the timer was added from
list    timerticksremaining; // How many ticks remain before the event is reported

string  timerstate;        // Running state of the timer. 0 = Stopped; 1 = Running. While this will be only ones
                             //   and zeros, it should not be converted to an integer with bitwise testing against
                             //   it due to the dynamic state of the lists and since the lists could grow beyond
                             //   the limits of a 32-bit integer. Originally wrote script with this as a list.
                             //   Converted it to a string to save memory.

//////////////////////////////////////////////////////////////////////////////////////
// User Defined Functions
add(string a, integer b, integer c, integer d, integer e, integer f){ //adds a timer to the lists
    integer g = llGetListLength(timername);
    timername           = llListInsertList(timername,           [a], g);
    timerticks          = llListInsertList(timerticks,          [b], g);
    timercycles         = llListInsertList(timercycles,         [c], g);
    timerprim           = llListInsertList(timerprim,           [d], g);
    timerticksremaining = llListInsertList(timerticksremaining, [e], g);
    timerstate          = llInsertString  (timerstate,           g,  (string)f);
}

remove(integer a){ //removes a timer from the lists
    timername           = llDeleteSubList(timername,            a,a);
    timerticks          = llDeleteSubList(timerticks,           a,a);
    timercycles         = llDeleteSubList(timercycles,          a,a);
    timerprim           = llDeleteSubList(timerprim,            a,a);
    timerticksremaining = llDeleteSubList(timerticksremaining,  a,a);
    timerstate          = llDeleteSubString(timerstate,         a,a);
}

clear(){ // Clears all timers and stops the master timer
    timername           = [];
    timerticks          = [];
    timercycles         = [];
    timerprim           = [];
    timerticksremaining = [];
    timerstate          = "";
    llSetTimerEvent(ticks = 0);
}

//////////////////////////////////////////////////////////////////////////////////////
// Main Script
default
{
    state_entry(){
        llSetTimerEvent(0); //Start master timer in an idle state
    }
    on_rez(integer a){
        clear(); // Reset the lists
    }
    link_message(integer a, integer b, string c, key d){
        if(b == timerchannellisten){ // Check to make sure message is from the correct channel
            if(c == "TIMER_STATUS_CHECK") { // send status report if proper command is received
                    llMessageLinked(a, timerchannelspeak,"TIMER_STATUS," +
						(string)ticks + "," + (string)timeint + "," +
						(string)llGetListLength(timername) + "," +
						(string)llGetFreeMemory() + "," +
						(string)(llFloor((llGetFreeMemory() - 500)/130)) +
						"," + (string)timerchannelspeak + "," +
						(string)timerchannellisten, NULL_KEY);
            } else if (c == "TIMER_RESET") { //Reset timer module lists if proper command is received
                clear();
            } else {
                list e = llCSV2List(c);
                if(llGetListLength(e) >= 3){ // makes sure the list length is at minimum a valid command length
                    string  f = llToLower(llList2String(e, 0));  // Gets the command then converts to lowercase to make the commands case insensitive
                    string  g = (string)a + llGetSubString(llList2String(e, 1), 0, 9);
                                                                    // Gets timer name from the command string and prepends the prim number to it to
                                                                    // guarantee uniqueness from prim to prim within the same object. Also truncates the
                                                                    // the timer name to 10 characters to allow for reliable memory usage estimations.
                    integer h = (integer)llList2String(e, 2);    // Gets the timer's interval from the command string
                    integer i = (integer)llList2String(e, 3);    // Gets the timer's cycle from the command string
                    integer j = llListFindList(timername, [g]);  // Index of the called timer
                    if(f == "add"){
                        if(h < 1 || i < 1) { // Checks to make sure both the ticks and the cycles are positive
                            llMessageLinked(llList2Integer(timerprim, i), timerchannelspeak,"TIMER,ERROR,Non positive Tick or Cycle value.", NULL_KEY);
                            jump end;
                        }
                        if(llFloor((llGetFreeMemory() - 500)/130) == 0) { // Checks available memory, attempts to leave at least 500 bytes available.
                            llMessageLinked(llList2Integer(timerprim, i), timerchannelspeak,"TIMER,ERROR,Out of memory", NULL_KEY);
                        } else {
                            if(timername == [])
                                llSetTimerEvent(timeint); // If the master timer is not started, then start it.
                            if(j != -1) // Check to see if the timer already exists
                                remove(j);// if it does, remove it
                            add(g, h, i, a, h, 1); // Add timer
                            if(ticks == 0)
                                llSetTimerEvent(timeint); // If the master timer is not started, then start it.
                        }
                    } else if(f == "rem") {
                        remove(j); // Remove timer
                        if(timername == [])
                            llSetTimerEvent(ticks = 0);
                    } else if(f == "pau") {
                        if(j != -1){ // Make sure the timer already exists. If not, do nothing.
                            timerstate = llDeleteSubString(timerstate, j, j); // Change timer
                            timerstate = llInsertString(timerstate, j, "0");  //              state to paused
                        }
                    } else if(f == "res") {
                        if(j != -1){ // Make sure the timer already exists. If not, do nothing.
                            timerstate = llDeleteSubString(timerstate, j, j); // Change timer
                            timerstate = llInsertString(timerstate, j, "1");  //              state to run
                        }
                    }
                    @end;
                    // If the message made it this far without doing anything, then the command must not be a timer command
                } else {
                    llMessageLinked(a, timerchannelspeak,"TIMER_STATUS," + //This part was added solely for debugging purposes and can be removed.
                                                        (string)ticks + "," +
                                                        (string)timeint + "," +
                                                        (string)llGetListLength(timername) + "," +
                                                        (string)llGetFreeMemory() + "," +
                                                        (string)(llFloor((llGetFreeMemory() - 500)/130)) + "," +
                                                        (string)timerchannelspeak + "," +
                                                        (string)timerchannellisten,
                                                    NULL_KEY);
                }
            }
        }
    }

    timer(){ // master timer
        ++ticks;
        integer a = llGetListLength(timername); // Determines how many timers to update
        integer i;
        list timerstoremove = [];
        for (i = 0; i < a; ++i) { // Goes through the entire timer list
            if(llGetSubString(timerstate, i, i) == "1"){ // Check timer run state. If 0, then step to next timer.
                timerticksremaining = llListReplaceList(timerticksremaining, [llList2Integer(timerticksremaining, i) - 1], i, i); // Subtracts 1 from ticksremaining
                if(llList2Integer(timerticksremaining, i) == 0) { // Checks to see if the timer has elapsed
                    if(llList2Integer(timercycles, i) != -1) // Checks to see if timer is indefinite
                        timercycles = llListReplaceList(timercycles, [llList2Integer(timercycles, i) - 1], i, i); // Subtracts 1 from cycles
                    timerticksremaining = llListReplaceList(timerticksremaining, [llList2Integer(timerticks, i)], i, i); // Resets ticksremaining
                    // Send linked message reporting timer event
                    llMessageLinked(llList2Integer(timerprim, i), timerchannelspeak,"TIMER," +
                                    llDeleteSubString(llList2String(timername, i), 0, llStringLength((string)llList2Integer(timerprim, i)) - 1) +
                                    "," + (string)llList2Integer(timerticks, i) + "," + (string)llList2Integer(timercycles, i) + "," + (string)a + "," +
                                    (string)(llFloor((llGetFreeMemory() - 500)/130)), NULL_KEY);
                    if(llList2Integer(timercycles, i) == 0) {// Checks to see if tiemr has expired
                        timerstoremove = (timerstoremove=[]) + timerstoremove + [i]; // Assemble list of timers to remove
                    }
                }
            }
        }
        a = llGetListLength(timerstoremove); // Determines how many timers to remove
        for (i = a; i > 0; --i) {
            remove(i - 1); // Removes timer
            if(timername == [])
                llSetTimerEvent(ticks = 0);
        }
    }
}
```