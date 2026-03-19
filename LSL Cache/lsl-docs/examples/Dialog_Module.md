---
name: "Dialog module"
category: "example"
type: "example"
language: "LSL"
description: "This script is a standalone module for the handling of dialog boxes."
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/Dialog_module/Dialog_module/Object/Dialog_module_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / Dialog_module"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "Dialog_module/Dialog_module/Object/Dialog_module_1.lsl"
source_project: "Dialog_module"
source_part_total: "3"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-dialog-module-2026-03-19"
---

```lsl
// === Part 1/3 ===
// :CATEGORY:Dialog
// :NAME:Dialog_module
// :AUTHOR:Strife Onizuka
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2014-01-17 11:07:14
// :ID:233
// :NUM:319
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// This script is a standalone module for the handling of dialog boxes.
// :CODE:
// The dialog boxes each use a random unique negative channel, for each dialog box.
// Channel numbers range from -2147483648 to -255 with the possibility of the lower 8 bits being zero.
// The listens are bound to the user's key. This means that no script or other user can activate the interface.
// By using a negative number there is no way for the user to type in a command and have it mistaken as a response.
// Only responses that are valid buttons from the requested user (and in the mask) will result in a return; no 3rd party tampering is possible.
// It would be very difficult for anyone to predict the channel number to listen on (2 billion is a big range).
// 
// The Request:
// The link message string format is a list. The first element of this list is the integer that will be used as the second integer in the return the link message. The rest of this list is string that will be returned (in list form with the same separating character).
// 
// The link message key format is a list. The first element is the key of the user, if this is left blank (or NULL_KEY) the owner is assumed. The second element is the message, this can be any valid string. The third element is a float, which is the dialog box time to live. The forth element is an integer it is used as a mask for when a button is pressed if it will trigger a response. The rest of the list is for the buttons; an empty list can be used, but it will default to ["OK"] (there is no way around this, just cope).
// 
// The Response:
// The link message string format is a list. It is whatever was passed as the second string minus the first entry of that list.
// The link message key format is a list. The first element of this list is the number of the button pressed (or error code). The second entry is the text of the button pressed. The third entry is the key it used for creating the dialog box. The forth entry is the user name. The fifth entry is how much time was left in the time to live of the dialog box (not very useful but maybe it is).
// The response always goes back to only the prim that requested the dialog box.
// 
// (string)dump(llList2List(parse(paramString),1,-1)),
// (key)dump([integer buttonNum, string buttonText, key user, string userName, float aproxTimeLeft],"")
// 
// 
// There is no way to create a dialog box that won't timeout. The value must be between 5.0 and 7200.0; or it will be replaced by the default timeout. The timeout won't make a box disapeer off the users screen, but the script will stop listening for results.
// 
// Notes:
// Know your data; if your strings contain "|" then don't use "|" as the separator. If the script acts weirdly this is probably why. The separator can only be one character. The two different strings being passed in the linked message can use different separating characters.
// 
// Misc:
// The ButtonMask has a few extra tricks.
// The first 12 bits corespond to the 12 buttons (bits 0 -> 11)
// Bits 16 through 22 are special bits for error handling and setup.
// All other bits are ignored, do with them as you please but be warned they may be used in the future.
// Bit 	Hex Value 	Event 	Return Button
// 0 	0x000001 	Button 0 Pressed 	0
// 1 	0x000002 	Button 1 Pressed 	1
// 2 	0x000004 	Button 2 Pressed 	2
// 3 	0x000008 	Button 3 Pressed 	3
// 4 	0x000010 	Button 4 Pressed 	4
// 5 	0x000020 	Button 5 Pressed 	5
// 6 	0x000040 	Button 6 Pressed 	6
// 7 	0x000080 	Button 7 Pressed 	7
// 8 	0x000100 	Button 8 Pressed 	8
// 9 	0x000200 	Button 9 Pressed 	9
// 10 	0x000400 	Button 10 Pressed 	10
// 11 	0x000800 	Button 11 Pressed 	11
// 16 	0x010000 	Dialog box times out 	-1
// 17 	0x020000 	Queue being cleared 	-2
// 18 	0x040000 	Target agent not found 	-3
// 19 	0x080000 	No buttons to listen for, bad mask or bad return channel 	-4
// 20 	0x100000 	Clears the queue then creates the dialog box 	-2 via Bit 17
// 21 	0x200000 	Same as bit 20 but only for boxes for the current user 	-2 via Bit 17
// 22 	0x400000 	Target agent has left the sim 	-5
// 
// The queue is cleared in two ways: on_rez or when creating a dialog box requests it. When the script is rez'ed, the old dialog box requests become meaningless (because the script cannot receive the response). By having bit 17 on, it allows for this event to be returned to the script requesting the box. By having bit 20 turned on also causes the queue to be reset (exactly like an on_rez). Using bit 20 may have undesired effects if you are using this module with multiple scripts. Using bit 21 causes a partial clear. It clears out all boxes for the requested user; it is advisable to use this option instead of bit 20.
// 
// Todo:
// When bits 20 and 21 are true have the inverse result happen. All boxes not of the current user would be cleared from the queue.
// 
// Tricks:
// Pass a list of useful values as the return list. Have them correspond to the button list. Then use the code below to get that value from the return (remember if you have any of bits 16 -> 19 enabled you will get negative index values on errors).
// 
// llList2String(parse(c),(integer)llList2String(parse(d),0));

string sepchar = "|";

integer answer = 546;

integer DialogComm = 12;



dialog(key user, string message, float timeout, list buttons, integer buttonmask, integer retchan, list ret)

{

    llMessageLinked(llGetLinkNumber(), DialogComm, dump([retchan] + ret, sepchar),

        dump([user, message, timeout, buttonmask] + buttons, sepchar));

}



string dump(list a, string b)

{

    string c = (string)a;

    if(1+llSubStringIndex(c,b) || llStringLength(b)!=1)

    {

        b += "|\\/?!@#$%^&*()_=:;~{}[],\n qQxXzZ";

        integer d = -llStringLength(b);

        while(1+llSubStringIndex(c,llGetSubString(b,d,d)) && d)

            d++;

        b = llGetSubString(b,d,d);

    }

    return b + llDumpList2String(a, b);

}



list parse(string a) {

    string b = llGetSubString(a,0,0);//save memory

    return llParseStringKeepNulls(llDeleteSubString(a,0,0), [b],[]);

}



default

{

    state_entry()

    {

        integer rint = 6;

        string question = "Would you like a drink?";

        list Answers = ["Yes", "No", "Strongest"];

        integer AnswerMask = 0x005;

        list ExtraPassback = ["extra info to pass back"];

        dialog(llGetOwner(), question, 30,Answers, AnswerMask , answer, ExtraPassback);

    }

    touch_start(integer a)

    {

        dialog(llDetectedKey(0), "Hello\nDo you like me?", 30, ["Yes", "No"], 0xf0fff, answer, ["I think they like us"]);

    }

    link_message(integer a, integer b, string c, key d)

    {

        if(b==answer)

        {

            llWhisper(0,(string)b);

            llWhisper(0,llList2CSV(parse(c)));

            llWhisper(0,llList2CSV(parse(d)));

            //c is the return list

            //d is a list [button number pressed, user, time left, user name, button text]

        }

    }

}

// === Part 2/3 ===
// :CATEGORY:Dialog
// :NAME:Dialog_module
// :AUTHOR:Strife Onizuka
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:51
// :ID:233
// :NUM:320
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// 
// Dialog Module:
// :CODE:
//////////////////////////////////////////////////////////////////////////////////////

//

//    Dialog Module

//    Version 9.3 Release

//    Copyright (C) 2004-2006, Strife Onizuka

//    http://home.comcast.net/~mailerdaemon/

//    http://secondlife.com/badgeo/wakka.php?wakka=LibraryDialogModule

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

//////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////////////

//Don't change anything else unless you *really* need to.



list handles;

list time;

list chans;

string users;//save memory

list answer;

list button;

list prim;

list mask;

list intchan;



integer ticks;



remove(integer a)

{

    llListenRemove(llList2Integer(handles,a));

    handles = llDeleteSubList(handles,a,a);

    time    = llDeleteSubList(time,   a,a);

    chans   = llDeleteSubList(chans,  a,a);

    answer  = llDeleteSubList(answer, a,a);

    button  = llDeleteSubList(button, a,a);

    prim    = llDeleteSubList(prim,   a,a);

    mask    = llDeleteSubList(mask,   a,a);

    intchan = llDeleteSubList(intchan,a,a);

    users   = llDeleteSubString(users,a*=36,a+35);

}



list TightListParse(string a) {

    string b = llGetSubString(a,0,0);//save memory

    return llParseStringKeepNulls(llDeleteSubString(a,0,0), [a=b],[]);

}



clear()

{

    integer a = llGetListLength(handles);

    while(a)

    {

        llListenRemove(llList2Integer(handles,--a));

        if(llList2Integer(mask,a)&0x20000)

            llMessageLinked(llList2Integer(prim,a), llList2Integer(intchan,a),

                    llList2String(answer,a), "|-2||"+llGetSubString(users,a * 36,(a * 36) + 35)+"||-1");

    }

    llSetTimerEvent(ticks = 0);

}



default

{

    state_entry()

    {



            llOwnerSay("Dialog Module, Version 9.2, Released Under the GNU Lesser General Public License");

            llOwnerSay("Copyright (C) 2004-2006, Strife Onizuka, http://secondlife.com/badgeo/wakka.php?wakka=LibraryDialogModule");





    }

    on_rez(integer a)

    {

        clear();

    }

    link_message(integer a, integer b, string c, key d)

    {

        if(b == 12)

        {

            b = llSubStringIndex(llDeleteSubString(c,0,0), llGetSubString(c,0,0));

            list    e = TightListParse(d);

            integer buttonmask =  (integer)llList2String(e,3);

            string  user       =  llList2String(e,0);

            list    buttons    =  llDeleteSubList(e,0,3);

            float   timeout    =  (float)llList2String(e,2);

            integer cat        =  (integer)llFrand(-2147483392.0) - 255;

            integer chan       =  (integer)llDeleteSubString(c, b + 1, 0);

            string  ans        =  llDeleteSubString(c,0,b);



            if(buttonmask & 0x100000)

                clear();

            else if(buttonmask & 0x200000)

            {//clean out other box's that went to this user.

                while(1 + (b = llSubStringIndex(users, user)))

                {

                    if(llList2Integer(mask,b/=36)&0x20000)

                        llMessageLinked(llList2Integer(prim,b), llList2Integer(intchan,b),

                                        llList2String(answer,b), "|-2||"+llGetSubString(users,b * 36,(b * 36) + 35)+"||-1");

                    remove(b);

                }

                if(time == [])

                    llSetTimerEvent(ticks = 0);

            }



            if(user == "" || user == NULL_KEY) //lazy check

                user = llGetOwner();

            if(!llGetAgentInfo(user)) 

            {// target not in the sim

                if(buttonmask & 0x40000)

                    llMessageLinked(a, chan, ans, "|-3||"+user+"||0");

                jump end1;//instead of a return, too many local variables to clear off the stack.

            }

            while(1+llListFindList(chans,[cat]))

                --cat;



            b = llListen(cat,"",user,"");

            llDialog(user, llList2String(e,1), buttons, cat);

            if(chan != 12)

            {//loopback catch

                if(buttons == []) // so we can match the ok button

                    buttons = ["OK"];

                if(buttonmask & ((1<<llGetListLength(buttons)) - 1))

                { //we checked the mask to see if we should expect any values back

                    chans   +=  cat;

                    handles +=  b;

                    if(timeout < 5.0 || timeout > 7200)

                        timeout = 5.0;

                    time    +=  (ticks + (timeout / 5.0));

                    users   +=  user;

                    answer  +=  ans;

                    button  +=  (llGetSubString(d,0,0) + llDumpList2String(buttons, llGetSubString(d,0,0)));

                    prim    +=  a;

                    mask    +=  buttonmask;

                    intchan +=  chan;

                    llSetTimerEvent(5.0);

                    jump end2;//instead of a return, too many local variables to clear off the stack.

                }

            }

            llListenRemove(b);

            if(buttonmask & 0x80000)

                llMessageLinked(a, chan, ans, "|-4||"+(string)user+"||0");

        }

        @end1;@end2;

    }

    listen(integer a, string b, key c, string d)

    {

        if(a+1 && llGetSubString(users,36 * a=llListFindList(chans,[a]),(a * 36) + 35) == c)

        {//it's one of our listens

            integer f = llListFindList(TightListParse(llList2String(button,a)),[d]);

            if(f+1)

            {//we matched a button

                if(llList2Integer(mask,a)&(1<<f))

                {

                    list ret = [f, d, c, b,(llList2Float(time,a) - ticks) * 5.0];

                    if(llSubStringIndex(d = (string)ret,b = "|") + 1)

                    {

                        f = -37;

                        b = "|\\/?!@#$%^&*()_=:;~{}[]<>`',\n\" qQxXzZ";

                        do;while(1+llSubStringIndex(d,llGetSubString(b,f,f)) && ++f);

                        b = llGetSubString(b,f,f);

                    }

                    d = "";

                    llMessageLinked(llList2Integer(prim,a), llList2Integer(intchan,a), 

                                    llList2String(answer,a), (b + llDumpList2String(ret, b)));

                }

                remove(a);

                if(time == [])

                    llSetTimerEvent(ticks = 0);

            }

        }

    }

    timer()

    {

        ++ticks;

        integer a = llGetListLength(time);

        float c;

        key d;

        while(a)

        {

            if(((c = llList2Float(time,a)) <= ticks) || !llGetAgentInfo(d = llGetSubString(users,--a * 36,(a * 36) + 35)))

            {

                if(llList2Integer(mask,a)&0x10000)

                    llMessageLinked(llList2Integer(prim,a), llList2Integer(intchan,a),

                            llList2String(answer,a), "|-1||"+(string)d+"||"+(string)((ticks - c) * 5.0));



                remove(a);

            }

        }

        if(time == [])

            llSetTimerEvent(ticks = 0);

    }

}

// === Part 3/3 ===
// :CATEGORY:Dialog
// :NAME:Dialog_module
// :AUTHOR:Strife Onizuka
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:51
// :ID:233
// :NUM:321
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// ESL Version:
// :CODE:
//////////////////////////////////////////////////////////////////////////////////////

//

//    Dialog Module

//    Version 9.3 Release

//    Copyright (C) 2004-2006, Strife Onizuka

//    http://home.comcast.net/~mailerdaemon/

//    http://secondlife.com/badgeo/wakka.php?wakka=LibraryDialogModule

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

//////////////////////////////////////////////////////////////////////////////////////



#ifndef DIALOGCOMM

    #define DIALOGCOMM    12

#endif

#ifdef USESCRIPTNAME

integer DialogComm = DIALOGCOMM;

#elif !defined DialogComm

#define DialogComm DIALOGCOMM

#endif



#ifndef TICKSIZE

    #define TICKSIZE 5.0

#endif

#ifndef DEFAULTTIMEOUT

    #define DEFAULTTIMEOUT TICKSIZE

#endif

//////////////////////////////////////////////////////////////////////////////////////

//Don't change anything else unless you *really* need to.

#define ZERO_INTEGER 0

list handles;

list time;

list chans;

string users;//save memory

list answer;

list button;

list prim;

list mask;

list intchan;



integer ticks;



remove(integer a)

{

    llListenRemove(llList2Integer(handles,a));

    handles = llDeleteSubList(handles,a,a);

    time    = llDeleteSubList(time,   a,a);

    chans   = llDeleteSubList(chans,  a,a);

    answer  = llDeleteSubList(answer, a,a);

    button  = llDeleteSubList(button, a,a);

    prim    = llDeleteSubList(prim,   a,a);

    mask    = llDeleteSubList(mask,   a,a);

    intchan = llDeleteSubList(intchan,a,a);

    users   = llDeleteSubString(users,a*=36,a+35);

}



#define wipe() llSetTimerEvent(ticks = ZERO_INTEGER)

#define quickdump(a, b)  (b + llDumpList2String(a, b)) 

#ifndef quickdump

string quickdump(list a, string b){  return b + llDumpList2String(a, b); }

#endif



list TightListParse(string a) {

    string b = llGetSubString(a,ZERO_INTEGER,ZERO_INTEGER);//save memory

    return llParseStringKeepNulls(llDeleteSubString(a,ZERO_INTEGER,ZERO_INTEGER), [a=b],[]);

}



clear()

{

    integer a = llGetListLength(handles);

    while(a)

    {

        llListenRemove(llList2Integer(handles,--a));

        if(llList2Integer(mask,a)&0x20000)

            llMessageLinked(llList2Integer(prim,a), llList2Integer(intchan,a),

                    llList2String(answer,a), "|-2||"+llGetSubString(users,a * 36,(a * 36) + 35)+"||-1");

    }

    wipe();

}



default

{

    state_entry()

    {

        #ifdef USESCRIPTNAME

        if((DialogComm += (integer)llList2String(llParseString2List(llGetScriptName(), [" "],[]), -1)) == DialogComm)

        {

        #endif

            llOwnerSay("Dialog Module, Version 9.2, Released Under the GNU Lesser General Public License");

            llOwnerSay("Copyright (C) 2004-2006, Strife Onizuka, http://secondlife.com/badgeo/wakka.php?wakka=LibraryDialogModule");

        #ifdef USESCRIPTNAME

        }

        #endif

    }

    on_rez(integer a)

    {

        clear();

    }

    link_message(integer a, integer b, string c, key d)

    {

        if(b == DialogComm)

        {

            b = llSubStringIndex(llDeleteSubString(c,ZERO_INTEGER,ZERO_INTEGER), llGetSubString(c,ZERO_INTEGER,ZERO_INTEGER));

            list    e = TightListParse(d);

            integer buttonmask =  (integer)llList2String(e,3);

            string  user       =  llList2String(e,ZERO_INTEGER);

            list    buttons    =  llDeleteSubList(e,ZERO_INTEGER,3);

            float   timeout    =  (float)llList2String(e,2);

            integer cat        =  (integer)llFrand(-2147483392.0) - 255;

            integer chan       =  (integer)llDeleteSubString(c, b + 1, ZERO_INTEGER);

            string  ans        =  llDeleteSubString(c,ZERO_INTEGER,b);

            

            if(buttonmask & 0x100000)

                clear();

            else if(buttonmask & 0x200000)

            {//clean out other box's that went to this user.

                while(1 + (b = llSubStringIndex(users, user)))

                {

                    if(llList2Integer(mask,b/=36)&0x20000)

                        llMessageLinked(llList2Integer(prim,b), llList2Integer(intchan,b),

                                        llList2String(answer,b), "|-2||"+llGetSubString(users,b * 36,(b * 36) + 35)+"||-1");

                    remove(b);

                }

                if(time == [])

                    wipe();

            }

            

            if(user == "" || user == NULL_KEY) //lazy check

                user = llGetOwner();

            if(!llGetAgentInfo(user)) 

            {// target not in the sim

                if(buttonmask & 0x40000)

                    llMessageLinked(a, chan, ans, "|-3||"+user+"||0");

                jump end1;//instead of a return, too many local variables to clear off the stack.

            }

            while(1+llListFindList(chans,[cat]))

                --cat;

            

            b = llListen(cat,"",user,"");

            llDialog(user, llList2String(e,1), buttons, cat);

            if(chan != DialogComm)

            {//loopback catch

                if(buttons == []) // so we can match the ok button

                    buttons = ["OK"];

                if(buttonmask & ((1<<llGetListLength(buttons)) - 1))

                { //we checked the mask to see if we should expect any values back

                    chans   +=  cat;

                    handles +=  b;

                    if(timeout < 5.0 || timeout > 7200)

                        timeout = DEFAULTTIMEOUT;

                    time    +=  (ticks + (timeout / TICKSIZE));

                    users   +=  user;

                    answer  +=  ans;

                    button  +=  quickdump(buttons,llGetSubString(d,ZERO_INTEGER,ZERO_INTEGER));

                    prim    +=  a;

                    mask    +=  buttonmask;

                    intchan +=  chan;

                    llSetTimerEvent(TICKSIZE);

                    jump end2;//instead of a return, too many local variables to clear off the stack.

                }

            }

            llListenRemove(b);

            if(buttonmask & 0x80000)

                llMessageLinked(a, chan, ans, "|-4||"+(string)user+"||0");

        }

        @end1;@end2;

    }

    listen(integer a, string b, key c, string d)

    {

        if(a+1 && llGetSubString(users,36 * a=llListFindList(chans,[a]),(a * 36) + 35) == c)

        {//it's one of our listens

            integer f = llListFindList(TightListParse(llList2String(button,a)),[d]);

            if(f+1)

            {//we matched a button

                if(llList2Integer(mask,a)&(1<<f))

                {

                    list ret = [f, d, c, b,(llList2Float(time,a) - ticks) * TICKSIZE];

                    if(llSubStringIndex(d = (string)ret,b = "|") + 1)

                    {

                        f = -37;

                        b = "|\\/?!@#$%^&*()_=:;~{}[]<>`',\n\" qQxXzZ";

                        do;while(1+llSubStringIndex(d,llGetSubString(b,f,f)) && ++f);

                        b = llGetSubString(b,f,f);

                    }

                    d = "";

                    llMessageLinked(llList2Integer(prim,a), llList2Integer(intchan,a), 

                                    llList2String(answer,a), quickdump(ret, b));

                }

                remove(a);

                if(time == [])

                    wipe();

            }

        }

    }

    timer()

    {

        ++ticks;

        integer a = llGetListLength(time);

        float c;

        key d;

        while(a)

        {

            if(((c = llList2Float(time,a)) <= ticks) || !llGetAgentInfo(d = llGetSubString(users,--a * 36,(a * 36) + 35)))

            {

                if(llList2Integer(mask,a)&0x10000)

                    llMessageLinked(llList2Integer(prim,a), llList2Integer(intchan,a),

                            llList2String(answer,a), "|-1||"+(string)d+"||"+(string)((ticks - c) * TICKSIZE));



                remove(a);

            }

        }

        if(time == [])

            wipe();

    }

}
```
